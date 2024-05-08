"""
This tool can be used to automate the process of creating a latex report
"""

import argparse
import codecs
import datetime
import colorama
from colorama import Fore, Back, Style
from colorama.ansi import AnsiBack, AnsiFore
import glob
import logging
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import path
import yaml

from latexmlsuite import __version__

MODES = ("all", "html", "latex", "clean", "xml", "none", "docx")
DEFAULT_MAIN = "main"
DEFAULT_MODE = "all"

FOREGROUND_COLOR_OPTIONS = set([c for c in dir(AnsiFore) if "__" not in c])
BACKGROUND_COLOR_OPTIONS = set([c for c in dir(AnsiBack) if "__" not in c])
# dit is nodig om kleuren in een powershell te kunnen gebruiken
colorama.init(True)

__author__ = "Eelco van Vliet"
__copyright__ = "Eelco van Vliet"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from latexmlsuite.main_suite import main`,
# when using this Python module as a library.


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def check_make_was_clean(make_result):
    make_was_clean = True
    try:
        first_line = make_result[0]
    except IndexError:
        pass
    else:
        if not (
            "Nothing to be done" in first_line or "Er is niets te doen" in first_line
        ):
            make_was_clean = False
    return make_was_clean


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Compile your latex project")
    parser.add_argument(
        "--version",
        action="version",
        version="latexmlsuite {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
        default=logging.WARNING,
    )
    parser.add_argument(
        "-vv",
        "--debug",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "--settings_filename",
        help="Extra input yaml file to pass extra parameters",
        default="rapport_settings.yml",
    )
    parser.add_argument(
        "--make_exe",
        help="executable naam om Makefile te runnen. Default 'make'",
        default="make",
    )
    parser.add_argument(
        "--no_make",
        help="Sla het runnen van de makefiles over",
        action="store_false",
        default=True,
        dest="do_make",
    )
    parser.add_argument(
        "--no_scripts",
        help="Sla het runnen van de alle scripts over",
        action="store_false",
        default=True,
        dest="do_scripts",
    )
    parser.add_argument(
        "--no_post_scripts",
        help="Sla het runnen van de postscripts over",
        action="store_false",
        default=True,
        dest="do_postscripts",
    )
    parser.add_argument(
        "--no_pre_scripts",
        help="Sla het runnen van de prescripts over",
        action="store_false",
        default=True,
        dest="do_prescripts",
    )
    parser.add_argument(
        "--no_latexml",
        help="Sla het runnen van alle latexml scripts over",
        action="store_false",
        default=True,
        dest="do_latexml",
    )
    parser.add_argument(
        "--no_colors",
        help="Geef geen kleur aan de commando's die naar terminal geschreven worden",
        action="store_false",
        default=True,
        dest="use_terminal_colors",
    )
    parser.add_argument(
        "--foreground_color",
        help="Voorgrondkleur van commando's",
        choices=FOREGROUND_COLOR_OPTIONS,
        default="GREEN",
    )
    parser.add_argument(
        "--background_color",
        help="Achtergrondkleur van commando's",
        choices=BACKGROUND_COLOR_OPTIONS,
        default=None,
    )
    parser.add_argument(
        "--test",
        help="Doe een droge run, dus laat alleen commando's zien",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--include_graphs",
        help="Plot ook de tabellen en grafieken in de html output",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--include_hyperref",
        help="Genereer CCN html met hyperrefs",
        action="store_true",
        default=True,
    )
    parser.add_argument(
        "--include_nohyperref",
        help="Genereer CCN html zonder hyperrefs",
        action="store_false",
        default=True,
        dest="include_hyperref",
    )
    parser.add_argument(
        "--include_json",
        help="Naast de highcharts html files worden ook de json files gesynchroniseerd in het "
        "geval je die ook naar CCN wilt meeleveren",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--force_html",
        help="Forceer het compileren van de html files met latexml, ook al is er"
        "geen update geweest",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--mode",
        help="Welke type document wil je maken?",
        choices=MODES,
        default=DEFAULT_MODE,
    )
    parser.add_argument(
        "--no_overwrite",
        help="Schrijf de schoongemaakte html's naar een nieuwe file",
        action="store_false",
        default=True,
        dest="overwrite",
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "%(levelname)-8s [%(filename)s:%(lineno)4d] %(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def update_target_compared_to_source(source_file: Path, target_file: Path):
    """
    Script to check if we need to update the file

    Update if target does not exist yet, or if the target is older than the source

    Args:
        source_file: Path of str
            Name of the source file
        target_file: Path of str
            Name of the target file

    Returns: bool
        Flag indicating that the target must be updated
    """
    source_file = Path(source_file)
    target_file = Path(target_file)
    time0 = datetime.datetime.fromtimestamp(
        source_file.stat().st_mtime, tz=datetime.timezone.utc
    )
    update_target = True
    if target_file.exists():
        time1 = datetime.datetime.fromtimestamp(
            target_file.stat().st_mtime, tz=datetime.timezone.utc
        )
        update_target = time1 < time0
    return update_target


def copy_main_for_latexml(
    tex_input_file: Path,
    tex_output_file: Path,
    include_graphics: bool = False,
    include_hyperref: bool = False,
):
    # lees de inhoud van main en pas de opties aan om grafieken en tabellen weg te laten
    _logger.debug(f"Reading {tex_input_file}")
    with open(tex_input_file, "r") as in_stream:
        tex_content = in_stream.read()

    _logger.debug(f"Writing {tex_output_file}")

    options = ""
    if not include_graphics:
        options += ",nographs,notables"
    if not include_hyperref:
        options += ",nohyperrefs"
    cbsdocs = "]{cbsdocs}"

    tex_content_new = re.sub(cbsdocs, options + cbsdocs, tex_content)
    with open(tex_output_file, "w") as out_stream:
        out_stream.write(tex_content_new)


class TerminalColors:
    def __init__(
        self, foreground_color=None, background_color=None, use_terminal_colors=False
    ):
        self.use_terminal_colors = use_terminal_colors
        self.foreground_color = self.set_color(
            color_name=foreground_color, foreground=True
        )
        self.background_color = self.set_color(
            color_name=background_color, foreground=False
        )
        if use_terminal_colors:
            self.reset_colors = Style.RESET_ALL
        else:
            self.reset_colors = ""

    def set_color(self, color_name, foreground=True):
        if color_name is not None and self.use_terminal_colors:
            if foreground:
                color = getattr(Fore, color_name)
            else:
                color = getattr(Back, color_name)
        else:
            color = ""

        return color


class LaTeXMLSuite:
    def __init__(
        self,
        main_file_name="main",
        make_exe="make",
        do_make=True,
        do_postscripts=True,
        do_prescripts=True,
        do_latexml=True,
        overwrite=True,
        bibtex_file=None,
        output_directory=None,
        output_directory_html=None,
        output_directory_highcharts=None,
        output_directory_tabellen=None,
        output_filename=None,
        ccn_output_directory=None,
        makefile_directories=None,
        pre_scripts=None,
        post_scripts=None,
        mode=None,
        test=False,
        merge_chapters=False,
        include_graphs=False,
        include_hyperref=False,
        platform_is_windows=False,
        foreground_color=None,
        background_color=None,
        use_terminal_colors=False,
        force_html=False,
        include_json=False,
    ):

        self.terminal_colors = TerminalColors(
            foreground_color=foreground_color,
            background_color=background_color,
            use_terminal_colors=use_terminal_colors,
        )
        self.force_html = force_html
        self.output_filename = output_filename
        if ccn_output_directory is not None:
            self.ccn_output_directory = Path(ccn_output_directory)
        else:
            self.ccn_output_directory = Path("ccn")
        self.ccn_html_dir = self.ccn_output_directory / Path("html")
        self.ccn_docx_dir = self.ccn_output_directory / Path("docx")
        self.overwrite = overwrite
        self.makefile_directories = makefile_directories
        self.pre_scripts = pre_scripts
        self.post_scripts = post_scripts
        self.platform_is_windows = platform_is_windows
        self.make_exe = make_exe
        self.include_graphs = include_graphs
        self.include_hyperref = include_hyperref
        self.test = test
        self.do_make = do_make
        self.do_prescripts = do_prescripts
        self.do_postscripts = do_postscripts
        self.do_latexml = do_latexml
        self.include_json = include_json
        if main_file_name is None:
            self.main_file_name = Path("main.tex")
        else:
            self.main_file_name = Path(main_file_name)

        self.bibtex_file = bibtex_file

        if output_directory is None:
            self.output_directory = Path("out")
        else:
            self.output_directory = Path(output_directory)

        if output_directory_html is None:
            self.output_directory_html = Path("out_html")
        else:
            self.output_directory_html = Path(output_directory_html)

        if output_directory_highcharts is None:
            self.ccn_highcharts_dir = self.ccn_output_directory / Path("highcharts")
        else:
            self.ccn_highcharts_dir = self.ccn_output_directory / Path(
                output_directory_highcharts
            )

        if output_directory_tabellen is None:
            self.ccn_tables_dir = self.ccn_output_directory / Path("tabellen")
        else:
            self.ccn_tables_dir = self.ccn_output_directory / Path(
                output_directory_tabellen
            )

        self.xml_refs = None
        self.updated_references = False
        self.merge_chapters = merge_chapters

        if mode is None:
            self.mode = "all"
        else:
            self.mode = mode

        # zorg dat de ccn directory wel aan het begin bestaat
        if self.mode != "clean":
            _logger.info(f"Maak output directory {self.ccn_highcharts_dir}")
            self.ccn_highcharts_dir.mkdir(exist_ok=True, parents=True)
            self.ccn_tables_dir.mkdir(exist_ok=True, parents=True)

        # deze directories proberen we te synchroniseren
        self.synchronise_directories = [self.ccn_highcharts_dir, self.ccn_tables_dir]

    def run(self):

        if self.makefile_directories is not None and self.do_make:
            self.launch_makefiles()

        if self.pre_scripts is not None and self.do_prescripts and self.mode != "clean":
            self.launch_scripts(self.pre_scripts)

        if self.mode == "none":
            # met none maken we de documenten niet, alleen de make files worden gerund
            return

        if self.mode in ("clean", "latex", "all", "docx"):
            self.launch_latexmk()
            if self.mode == "clean":
                self.clean_log()
        if self.mode in ("xml", "all", "docx"):
            self.launch_latexmk_for_html()
            self.copy_pdf()
            if self.do_latexml:
                if self.bibtex_file is not None:
                    self.launch_latexml_bibtex()
                self.launch_latexml()
        if self.mode in ("html", "all", "docx"):
            if self.do_latexml:
                # This only works if you have installed latexml
                self.launch_latexml_post()
                self.rename_and_clean_html()
                self.clean_ccs()
            if self.post_scripts is not None and self.do_postscripts:
                self.launch_scripts(self.post_scripts)
            if self.mode == "docx":
                self.launch_html_to_docx()

    def clean_ccs(self):

        pattern = f"{self.ccn_html_dir.as_posix()}/*.css"
        css_files = glob.glob(pattern)
        if len(css_files) == 0:
            _logger.debug("No css files found.")
            return

        rm = []
        if self.test:
            rm.append("echo")
        if self.platform_is_windows:
            rm.append("powershell.exe")
            rm.append("Remove-Item")
            rm.append("-recurse")
            rm.append("-force")
            rm.append(pattern)
        else:
            rm.append("rm")
            rm.append("-v")
            for file in css_files:
                rm.append(file)
        run_command(rm, terminal_colors=self.terminal_colors)

    def clean_log(self):
        pattern = f"*.css"
        log_files = glob.glob(pattern)
        if len(log_files) == 0:
            _logger.debug("No log files found.")
            return

        rm = []
        if self.test:
            rm.append("echo")
        if self.platform_is_windows:
            rm.append("powershell.exe")
            rm.append("Remove-Item")
            rm.append("-recurse")
            rm.append("-force")
            rm.append(pattern)
        else:
            rm.append("rm")
            rm.append("-v")
            for file in log_files:
                rm.append(file)

        run_command(rm, terminal_colors=self.terminal_colors)

    def rename_and_clean_html(self):
        """
        Hernoem alle html files met een prefix
        """
        html_files = glob.glob(f"{self.ccn_html_dir.as_posix()}/*.html")
        fc = self.terminal_colors.foreground_color
        bc = self.terminal_colors.background_color
        rs = self.terminal_colors.reset_colors

        for html_file in html_files:
            html = Path(html_file)

            if html.stem.startswith(self.main_file_name.stem):
                continue

            prefix = self.main_file_name.stem
            new_base = "_".join([prefix, html.stem + html.suffix])
            new_html = html.parent / Path(new_base)

            print(f"{fc}{bc}mv {html} {new_html}{rs}")
            if not self.test:
                shutil.move(html.as_posix(), new_html.as_posix())

            cleaner = []
            if self.test:
                cleaner.append("echo")

            cleaner.append("htmlcleaner")
            cleaner.append(new_html.as_posix())

            if self.overwrite:
                cleaner.append("--overwrite")

            run_command(command=cleaner, terminal_colors=self.terminal_colors)

    def launch_scripts(self, scripts):
        """
        Loop over alle directories die een Makefile bevatten en lanceer het make commando
        """
        fc = self.terminal_colors.foreground_color
        bc = self.terminal_colors.background_color
        rs = self.terminal_colors.reset_colors
        for script_filename in scripts:
            cmd = []
            script = Path(script_filename)
            if self.test:
                cmd.append("echo")
            if self.platform_is_windows:
                script = script.with_suffix(".ps1")
                cmd.append("powershell.exe")
            else:
                script = script.with_suffix(".sh")
                cmd.append("sh")

            print(f"{fc}{bc}cd {script.parent}{rs}", end="; ")
            with path.Path(script.parent):
                script_base = Path(script.stem + script.suffix)
                if not Path(script_base).exists():
                    _logger.warning(f"{script_base} does not exist")
                script_full = script_base.absolute()
                cmd.append(script_full.as_posix())

                run_command(command=cmd, terminal_colors=self.terminal_colors)

    def launch_makefiles(self):
        """
        Loop over alle directories die een Makefile bevatten en lanceer het make commando
        """
        fc = self.terminal_colors.foreground_color
        bc = self.terminal_colors.background_color
        rs = self.terminal_colors.reset_colors

        # voor we beginnen, checken we eerst of de ccn directory wel bestaat
        self.ccn_output_directory.mkdir(exist_ok=True)

        for makefile_dir in self.makefile_directories:
            cmd = []
            if self.test:
                cmd.append("echo")
            cmd.append(self.make_exe)
            if self.mode == "clean":
                cmd.append("clean")
            print(f"{fc}{bc}cd {makefile_dir}{rs}", end="; ")
            with path.Path(makefile_dir) as pp:
                make_result = run_command(
                    command=cmd, terminal_colors=self.terminal_colors
                )
                if (
                    not check_make_was_clean(make_result=make_result)
                    and self.mode != "clean"
                ):
                    for sync_dir in self.synchronise_directories:
                        sync_dir_base = Path(sync_dir.stem)
                        # als we de make file inderdaad gedraaid hebben en we hebben een sync
                        # directory, sync deze dan met de ccn output directory
                        if sync_dir_base.exists():
                            sync_cmd = self.make_sync_command(
                                parent_path=pp, synchronize_directory=sync_dir_base
                            )
                            run_command(
                                command=sync_cmd, terminal_colors=self.terminal_colors
                            )

    def make_sync_command(self, parent_path, synchronize_directory):
        """
        Maak een commando om een highcharts directory te synchroniseren met de ccn output

        Args:
            parent_path: Path
                Het pad van de makefile, hebben we nodig om te kijken hoeveel niveau we omhoog
                moeten
            synchronize_directory: Path
                Directory we want to synchronise

        """
        sync_cmd = []
        this_parent = Path(parent_path)
        n_up_dir = Path(".")
        while this_parent != Path(""):
            n_up_dir = Path("..") / n_up_dir
            this_parent = this_parent.parent

        ccn_sync_dir = self.ccn_output_directory / synchronize_directory

        if self.test:
            sync_cmd.append("echo")

        # gebruik robocopy op windows, rsync op linux
        if self.platform_is_windows:
            sync_cmd.append("Robocopy.exe")
        else:
            sync_cmd.append("rsync")
            sync_cmd.append("-arv")

        # paden toevoegen
        sync_cmd.append(synchronize_directory.as_posix() + "/")
        sync_cmd.append((n_up_dir / ccn_sync_dir).as_posix())

        # Either Robocopy switches or rsync switches to exclude json
        if self.platform_is_windows:
            sync_cmd.append("/E")
            sync_cmd.append("/NDL")

        if not self.include_json:
            # robocopy switches of rsync switches om json te excluden
            if self.platform_is_windows:
                sync_cmd.append("/XF")
            else:
                sync_cmd.append("--exclude")

            sync_cmd.append("*.json")

        return sync_cmd

    def launch_latexmk_for_html(self):
        """
        Run latexmk voor de tex file in de html output directory
        """
        cmd = []

        if self.test:
            cmd.append("echo")

        out_dir = Path(self.output_directory_html)
        out_dir.mkdir(exist_ok=True)
        main_file = out_dir / Path(self.main_file_name)
        cmd.append("latexmk")
        cmd.append(f"{main_file}")
        cmd.append("-xelatex")
        cmd.append("-shell-escape")
        cmd.append(f"-output-directory={out_dir}")

        # lees de inhoud van main en pas de opties aan om grafieken en tabellen weg te laten
        if update_target_compared_to_source(self.main_file_name, main_file):
            copy_main_for_latexml(
                tex_input_file=self.main_file_name,
                tex_output_file=main_file,
                include_graphics=self.include_graphs,
                include_hyperref=self.include_hyperref,
            )
        else:
            _logger.debug(
                f"No update need for {self.main_file_name} compared to {main_file}"
            )

        run_command(command=cmd, terminal_colors=self.terminal_colors)

    def launch_html_to_docx(self):

        html_files = glob.glob(f"{self.ccn_html_dir.as_posix()}/*.html")
        self.ccn_docx_dir.mkdir(exist_ok=True, parents=True)

        for html_file_str in html_files:
            html_file = Path(html_file_str)
            cmd = []
            if self.test:
                cmd.append("echo")
            docx_file = self.ccn_docx_dir / Path(html_file.stem + ".docx")

            if update_target_compared_to_source(self.main_file_name, docx_file):
                cmd.append("pandoc")
                cmd.append(html_file.as_posix())
                cmd.append("-o")
                cmd.append(docx_file.as_posix())
                run_command(command=cmd, terminal_colors=self.terminal_colors)
            else:
                _logger.info(f"docx file {docx_file} already up to date ")

    def copy_pdf(self):
        """
        Kopieer de volledige pdf voor ccn (dus met de plaatjes)
        """
        out_dir = Path(self.output_directory)
        main_file = out_dir / Path(self.main_file_name)

        pdf_file = main_file.with_suffix(".pdf")
        if not pdf_file.exists():
            self.launch_latexmk()
        ccn_pdf = self.ccn_output_directory / Path(self.output_filename)

        update_pdf = update_target_compared_to_source(pdf_file, ccn_pdf)

        if update_pdf:
            print(f"mkdir {ccn_pdf.parent}; cp {pdf_file} {ccn_pdf}")
            if not self.test:
                ccn_pdf.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(pdf_file.as_posix(), ccn_pdf.as_posix())
        else:
            _logger.debug(f"No update need for {ccn_pdf} compared to {pdf_file}")

    def launch_latexml_bibtex(self):
        cmd = []

        if self.test:
            cmd.append("echo")

        references = self.bibtex_file
        self.xml_refs = self.output_directory_html / Path(references + ".xml")

        if update_target_compared_to_source(references, self.xml_refs):
            cmd.append("latexml")
            if self.platform_is_windows:
                cmd[-1] += ".bat"
            cmd.append(f"--dest={self.xml_refs.as_posix()}")
            cmd.append(f"--preload=hyperref.sty")
            cmd.append(f"{references}")

            run_command(command=cmd, terminal_colors=self.terminal_colors)
            self.updated_references = True
        else:
            _logger.debug(
                f"No update need for {self.xml_refs} compared to {references}"
            )
            self.updated_references = False

    def launch_latexml(self):
        cmd = []

        if self.test:
            cmd.append("echo")

        cmd.append("latexml")
        if self.platform_is_windows:
            cmd[-1] += ".bat"

        out_dir = Path(self.output_directory_html)
        main_file = out_dir / Path(self.main_file_name)
        xml_file = main_file.with_suffix(".xml")

        cmd.append(f"--dest={xml_file.as_posix()}")
        cmd.append(f"{main_file.as_posix()}")

        if (
            update_target_compared_to_source(main_file, xml_file)
            or self.updated_references
            or self.force_html
        ):
            run_command(command=cmd, terminal_colors=self.terminal_colors)
        else:
            _logger.info(f"No update need for {xml_file} compared to {main_file}")

    def launch_latexml_post(self):
        cmd = []

        if self.test:
            cmd.append("echo")

        cmd.append("latexmlpost")
        if self.platform_is_windows:
            cmd[-1] += ".bat"

        out_dir = self.output_directory_html
        main_file = out_dir / Path(self.main_file_name)
        html_file = self.ccn_html_dir / Path(main_file.stem).with_suffix(".html")
        self.ccn_html_dir.mkdir(exist_ok=True, parents=True)
        xml_file = main_file.with_suffix("")

        cmd.append(f"--dest={html_file.as_posix()}")
        cmd.append(f"{xml_file}")

        if self.xml_refs is not None:
            cmd.append(f"--bibliography={self.xml_refs.as_posix()}")

        if not self.merge_chapters:
            cmd.append("--split")
            cmd.append("--splitat")
            cmd.append("chapter")

        run_command(command=cmd, terminal_colors=self.terminal_colors)

    def launch_latexmk(self):

        cmd = []

        main_base = self.main_file_name.stem
        if self.test:
            cmd.append("echo")

        cmd.append("latexmk")
        cmd.append(f"-output-directory={self.output_directory.as_posix()}")

        if self.mode in ("latex", "all", "docx"):
            cmd.append(f"{main_base}.tex")
            cmd.append("-xelatex")
            cmd.append("-shell-escape")

        elif self.mode == "clean":
            cmd.append("-c")
        else:
            raise AssertionError("Alleen aanroepen voor all en clean")

        run_command(command=cmd, terminal_colors=self.terminal_colors)


def run_command(command, shell=False, terminal_colors=None):
    if terminal_colors is not None:
        fc = terminal_colors.foreground_color
        bc = terminal_colors.background_color
        rs = terminal_colors.reset_colors
    else:
        fc = ""
        bc = ""
        rs = ""
    all_output_lines = list()
    if command[0] != "echo":
        print(f"{fc}{bc}" + " ".join(command) + f"{rs}")
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=os.environ,
            shell=shell,
        )

    except FileNotFoundError as err:
        _logger.warning(f"Failed for '{command}' with error:\n{err}")
    else:
        for line in iter(process.stdout.readline, b""):
            try:
                clean_line = line.decode("utf-8").strip()
            except UnicodeDecodeError as err:
                _logger.warning(err)
                _logger.warning(line)
            else:
                print(clean_line)
                all_output_lines.append(clean_line)

    return all_output_lines


class Settings:
    def __init__(self, settings_filename=None):
        self.main_name = "main"
        self.bibtex_file = None
        self.mode = "all"
        self.output_filename = None
        self.ccn_output_directory = None
        self.makefile_directories = None
        self.post_scripts = None
        self.pre_scripts = None
        self.output_directory = None
        self.output_directory_html = None

        if settings_filename is not None:
            self.read_settings_file(settings_filename)

    def read_settings_file(self, settings_filename):
        _logger.debug("Reading settings file {}".format(settings_filename))
        with codecs.open(settings_filename, "r", encoding="UTF-8") as stream:
            settings = yaml.load(stream=stream, Loader=yaml.Loader)
        general_settings = settings["general"]
        cache_settings = settings["cache"]
        self.main_name = general_settings.get("latex_main", self.main_name)
        self.bibtex_file = general_settings.get("bibtex_file", self.main_name)
        self.ccn_output_directory = general_settings.get("ccn_output_directory", "ccn")
        self.makefile_directories = settings.get("makefiles")
        self.post_scripts = settings.get("postscripts")
        self.pre_scripts = settings.get("prescripts")
        out_def = Path(self.main_name).with_suffix(".pdf")
        self.output_filename = general_settings.get("output_filename", out_def)
        if cache_settings is not None:
            self.output_directory = cache_settings.get("output_directory", "out")
            self.output_directory_html = cache_settings.get(
                "output_directory_html", "out_html"
            )
        else:
            self.output_directory = "out"
            self.output_directory_html = "out_html"

    def report_settings(self):
        message = "{:40s} : {}"
        _logger.debug(message.format("main_file_name", self.main_name))
        _logger.debug(message.format("output_file_name", self.output_filename))
        _logger.debug(message.format("ccn_output_directory", self.ccn_output_directory))
        _logger.debug(message.format("makefile_directories", self.makefile_directories))
        _logger.debug(message.format("prescripts", self.pre_scripts))
        _logger.debug(message.format("postscripts", self.post_scripts))


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    settings = Settings(settings_filename=args.settings_filename)
    _logger.debug("Start here")
    settings.report_settings()

    if "win" in sys.platform:
        platform_is_windows = True
    else:
        platform_is_windows = False

    if not args.do_scripts:
        args.do_prescripts = False
        args.do_postscripts = False

    suite = LaTeXMLSuite(
        mode=args.mode,
        test=args.test,
        make_exe=args.make_exe,
        do_make=args.do_make,
        do_postscripts=args.do_postscripts,
        do_prescripts=args.do_prescripts,
        do_latexml=args.do_latexml,
        overwrite=args.overwrite,
        main_file_name=settings.main_name,
        bibtex_file=settings.bibtex_file,
        output_directory=settings.output_directory,
        output_directory_html=settings.output_directory_html,
        output_filename=settings.output_filename,
        ccn_output_directory=settings.ccn_output_directory,
        makefile_directories=settings.makefile_directories,
        pre_scripts=settings.pre_scripts,
        post_scripts=settings.post_scripts,
        include_graphs=args.include_graphs,
        include_hyperref=args.include_hyperref,
        platform_is_windows=platform_is_windows,
        foreground_color=args.foreground_color,
        background_color=args.background_color,
        use_terminal_colors=args.use_terminal_colors,
        force_html=args.force_html,
        include_json=args.include_json,
    )

    suite.run()

    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m latexmlsuite.skeleton 42
    #
    run()
