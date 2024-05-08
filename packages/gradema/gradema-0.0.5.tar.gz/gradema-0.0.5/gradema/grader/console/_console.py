import copy
import dataclasses
import difflib
import io
import shlex
import shutil
import subprocess
import traceback
from pathlib import Path
from typing import TextIO, Optional, Sequence, Mapping

from rich import markup
from rich.console import Console
from rich.prompt import Prompt

from gradema.grader import GraderReporter
from gradema.grader.console._util import indentation, arrow, header, indent_text
from gradema.section import Section
from gradema.test import (
    TestReporter,
    CommandData,
    Test,
    TestResult,
    FractionalTestResult,
    PercentTestResult,
    StdioCommandData,
)
from gradema.test.argument import Argument, ResolvedArgumentInfo, OutputFile

TEST_DIRECTORY = Path("build/test")


def has_vim_installed() -> bool:
    return shutil.which("vim") is not None


def vim_diff(goal_file: Path, output_file: Path, html_output: Path) -> None:
    """
    Creates a diff using vim.
    Note that calling this function takes a while to complete.

    :param goal_file:
    :param output_file:
    :param html_output:
    """
    subprocess.run(
        [
            "vim",
            "-d",
            str(goal_file),
            str(output_file),
            "-c",
            "highlight DiffAdd ctermbg=Grey ctermfg=White",
            "-c",
            "highlight DiffDelete ctermbg=Grey ctermfg=Black",
            "-c",
            "highlight DiffChange ctermbg=Grey ctermfg=Black",
            "-c",
            "highlight DiffText ctermbg=DarkGrey ctermfg=White",
            "-c",
            "TOhtml",
            "-c",
            f"w! {str(html_output)}",
            "-c",
            "qa!",
        ],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def html_diff(goal_path: Path, actual_output_path: Path, html_output_path: Path) -> None:
    # TODO remember that file.readlines() LOADS THE ENTIRE FILE INTO MEMORY
    #   We might not care about that right now, but this could be a problem later with huge files
    with goal_path.open("r") as left, actual_output_path.open("r") as right:
        diff = difflib.HtmlDiff().make_file(
            left.readlines(),
            right.readlines(),
            f"Goal: {goal_path}",
            f"Your output: {actual_output_path}",
        )
        with html_output_path.open("w") as f_out:
            f_out.write(diff)


@dataclasses.dataclass
class ConsoleTestReporter(TestReporter):
    reporter: "ConsoleGraderReporter"

    def log(self, message: str) -> None:
        self.reporter.console.print(markup.escape(message))

    def log_unexpected_exception(self, exception: BaseException) -> None:
        indent = indentation(self.reporter.depth)
        buffer = io.StringIO()
        traceback.print_exception(exception, file=buffer)
        indented_text = indent_text(self.reporter.depth, buffer.getvalue())
        # make end="" because the exception text should have a trailing newline
        self.reporter.console.print(f"{indent}Unexpected exception:\n{indented_text}", highlight=False, end="")

    def __get_output_file(self, test_identifier: str) -> Path:
        directory = TEST_DIRECTORY / "stdio/outputs"
        directory.mkdir(parents=True, exist_ok=True)
        return directory / f"{test_identifier}.txt"

    def resolve_command(self, command: Sequence[Argument], test_identifier: str) -> tuple[Sequence[str], Mapping[tuple[int, Argument], ResolvedArgumentInfo]]:
        resolved_command = []
        argument_info_dictionary: dict[tuple[int, Argument], ResolvedArgumentInfo] = dict()
        # NOTE: We have to specify the type of argument_info_dictionary because the key is not covariant: https://github.com/python/typing/pull/273
        for i, argument in enumerate(command):
            if isinstance(argument, OutputFile):
                output_file = self.__get_output_file(test_identifier)
                resolved_command.append(str(output_file))
                argument_info_dictionary[(i, argument)] = output_file
            else:  # argument should be a str. If you get errors here, someone messed with the definition of Argument and you need to implement more cases
                resolved_command.append(argument)

        return resolved_command, argument_info_dictionary

    def report_command(self, command: Sequence[str]) -> CommandData:
        indent = indentation(self.reporter.depth)
        self.reporter.console.print(f"{indent}Running command: [magenta]{markup.escape(shlex.join(command))}[/magenta]")
        return CommandData(self.reporter.stdout, self.reporter.stderr)

    def report_stdio_command(self, command: Sequence[str], test_identifier: str, input_file: Optional[Path], stdout_as_output: bool) -> StdioCommandData:
        indent = indentation(self.reporter.depth)
        indent_plus = indentation(self.reporter.depth + 1)
        output_file = self.__get_output_file(test_identifier)
        self.reporter.console.print(f"{indent}Command to be run: [magenta]{markup.escape(shlex.join(command))}[/magenta]")
        if input_file is not None or stdout_as_output:
            self.reporter.console.print(f"{indent}Command to be run including I/O redirection:")
            self.reporter.console.print(
                f"{indent}[magenta]{markup.escape(shlex.join(command))}[/magenta]"
                + (f" \\\n{indent_plus}[magenta]< {markup.escape(shlex.quote(str(input_file)))}[/magenta]" if input_file is not None else "")
                + (f" \\\n{indent_plus}[magenta]> {markup.escape(shlex.quote(str(output_file)))}[/magenta]" if stdout_as_output else "")
            )

        return StdioCommandData(output_file, self.reporter.stdout, self.reporter.stderr)

    def maybe_launch_debugger(self, command: Sequence[str]) -> None:
        indent = indentation(self.reporter.depth)
        if self.reporter.debug_mode:
            self.reporter.console.print(f"{indent}This test did not complete successfully. We are going to launch the debugger now.")
            self.reporter.console.print(f"{indent}Debug command: [magenta]{markup.escape(shlex.join(command))}[/magenta]")
            launch_debugger = True
            while True:
                response = Prompt.ask(
                    prompt=f"{indent}Press [cyan]Enter[/cyan] to launch the debugger, or type 's' and then [cyan]Enter[/cyan] to skip",
                    console=self.reporter.console,
                )
                if response == "":
                    break
                if response[0].lower() == "s":
                    launch_debugger = False
                    break
            if launch_debugger:
                subprocess.run(command)

    def report_diff_result(self, test_identifier: str, goal_file: Path, output_file: Path, similarity: float, fuzzy: bool) -> None:
        indent = indentation(self.reporter.depth)
        self.reporter.console.print(f"{indent}Diff between [yellow]{markup.escape(str(goal_file))}[/yellow] and [yellow]{markup.escape(str(output_file))}[/yellow]")
        # TODO Customize stdio directory here
        directory = TEST_DIRECTORY / "stdio/diffs"
        directory.mkdir(parents=True, exist_ok=True)
        html_output = directory / f"{test_identifier}.html"
        html_diff(goal_file, output_file, html_output)
        self.reporter.console.print(f"{indent}Diff available to view at file://{html_output.resolve().absolute()}")

    def report_file_exists_test(self, file: Path, expected: str) -> None:
        indent = indentation(self.reporter.depth)
        self.reporter.console.print(f"{indent}Checking for the existence of '{file}' and its containing type of data: {expected}")

    def report_file_exists_test_result(self, file: Path, expected: str, is_correct: bool, actual: Optional[str]) -> None:
        indent_plus = indentation(self.reporter.depth + 1)
        if is_correct:
            self.reporter.console.print(f"{indent_plus}[green]Actual type matches expected type![/green] Actual: {actual}")
        elif actual is not None:
            self.reporter.console.print(f"{indent_plus}[red]Actual type DOES NOT match expected type![/red] Actual: {actual}")
        else:
            self.reporter.console.print(f"{indent_plus}[red]File does not exist![/red]")


@dataclasses.dataclass
class ConsoleGraderReporter(GraderReporter):
    section: Section
    console: Console
    stdout: TextIO
    stderr: TextIO
    interactive: bool
    debug_mode: bool
    depth: int

    @property
    def test_reporter(self) -> TestReporter:
        return ConsoleTestReporter(self)

    def __report_test(self, max_points: int) -> None:
        test = self.section.node
        assert isinstance(test, Test)
        indent = indentation(self.depth)
        self.console.line()
        if self.depth == 0:
            self.console.print(
                (indent + header(self.depth, self.console.width))[: self.console.width],
                style="blue",
            )
        if max_points == 0:
            self.console.print(f"{arrow(self.depth)}[yellow]{markup.escape(self.section.name)}[/yellow] (ungraded)")
        else:
            self.console.print(f"{arrow(self.depth)}[yellow]{markup.escape(self.section.name)}[/yellow] is worth {max_points} points")
        self.console.print(
            (indent + header(self.depth, self.console.width))[: self.console.width],
            style="blue",
        )

    def __report_section(self, max_points: int) -> None:
        assert isinstance(self.section.node, list)
        sections: list[Section] = self.section.node
        assert len(sections) > 0
        assert isinstance(sections[0], Section)

        indent = indentation(self.depth)
        self.console.line()
        if self.depth == 0:
            self.console.print(
                (indent + header(self.depth, self.console.width))[: self.console.width],
                style="blue",
            )
        self.console.print(f"{arrow(self.depth)}[orange_red1]{self.section.name}[/orange_red1] is worth {max_points} points and has {len(sections)} parts")
        self.console.print(
            (indent + header(self.depth, self.console.width))[: self.console.width],
            style="blue",
        )

    def report_start(self, max_points: int) -> None:
        if isinstance(self.section.node, Test):
            self.__report_test(max_points)
        else:
            self.__report_section(max_points)

    def report_test_result(self, result: TestResult, points: int, max_points: int) -> None:
        indent = indentation(self.depth)
        if max_points == 0:
            self.console.print(f"{indent}Ungraded step completed successfully.")
        elif isinstance(result, FractionalTestResult):
            if result.total_count == 1:
                if result.success_count == 0:
                    self.console.print(
                        f"{indent}FAIL gives you {points} / {max_points} points",
                        style="red",
                    )
                else:
                    self.console.print(
                        f"{indent}SUCCESS gives you {points} / {max_points} points",
                        style="green",
                    )
            else:
                self.console.print(
                    f"{indent}Result is {result.success_count} / {result.total_count} which gives you {points} / {max_points} points",
                    style="green" if points > max_points // 2 else "red",
                )
        else:
            assert isinstance(result, PercentTestResult)
            self.console.print(f"Result is {result.percent:.2%} which gives you {points}")

    def subsection(self, section: Section) -> "GraderReporter":
        r = copy.copy(self)
        r.section = section
        r.depth += 1
        return r
