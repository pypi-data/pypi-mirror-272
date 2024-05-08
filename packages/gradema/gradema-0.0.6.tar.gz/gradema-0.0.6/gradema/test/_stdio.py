import filecmp
import subprocess
from pathlib import Path
from typing import Optional, TextIO, Sequence

from gradema.test.argument import Argument, OUTPUT_FILE
from ._reporter import TestReporter
from ._test import Test, TestResult, FractionalTestResult


class StdioTest(Test):
    """
    A Standard Input/Output Test

    Traditionally, a stdio test would have no arguments passed to the command, it would have an input file, and a goal file.
    Output is piped to some output file that is not committed to version control.

    This new stdio test is very similar, but it can also do what a traditional arg test could do:
    take no input, and have custom arguments passed to the command.
    If you don't want anything directed into the command's stdin, then just assign None to input_file.
    If you want custom arguments passed to the command, give those custom arguments to the command argument (you may have to do that manually).
    """

    def __init__(self, command: Sequence[Argument], test_identifier: str, input_file: Optional[Path], goal_file: Path, stdout_as_output: bool):
        self.command = command
        self.test_identifier = test_identifier
        self.input_file = input_file
        self.goal_file = goal_file
        self.stdout_as_output = stdout_as_output

    def run(self, reporter: TestReporter) -> TestResult:
        command, argument_info_dictionary = reporter.resolve_command(self.command, self.test_identifier)
        data = reporter.report_stdio_command(command, self.test_identifier, self.input_file, self.stdout_as_output)
        output_file = data.stdout_file
        if output_file is None:  # output file will be None when stdout_as_output is False
            # By calling index() we are requiring that the command has an OUTPUT_FILE argument.
            #   If this is not the case, calling index() will raise a ValueError
            output_file_argument_index = self.command.index(OUTPUT_FILE)
            output_file_info = argument_info_dictionary[(output_file_argument_index, OUTPUT_FILE)]
            assert isinstance(output_file_info, Path), f"We expect OUTPUT_FILE's resolved argument info to be a Path! Instead it is {output_file_info}"
            output_file = output_file_info

        stdin: Optional[TextIO] = None
        try:
            if self.input_file is not None:
                stdin = self.input_file.open("r")
            stdout: Optional[TextIO] = None
            try:
                if data.stdout_file is not None:
                    stdout = data.stdout_file.open("w")
                try:
                    completed = subprocess.run(
                        command,
                        stdin=stdin if stdin is not None else subprocess.DEVNULL,
                        stdout=stdout if stdout is not None else data.stdout,
                        stderr=data.stderr,
                    )
                except FileNotFoundError as e:
                    reporter.log_unexpected_exception(e)
                    reporter.log(f"Your environment may not be configured correctly. Could not find binary for {command[0]}")
                    return FractionalTestResult(0, 1)
            finally:
                if stdout is not None:
                    stdout.close()
        finally:
            if stdin is not None:
                stdin.close()
        if completed.returncode != 0:
            reporter.log(f"Process had non-zero exit code: {completed.returncode}. Not going to execute a diff until the program can complete successfully.")
            return FractionalTestResult(0, 1)

        exactly_the_same = filecmp.cmp(self.goal_file, output_file)
        # TODO fuzzy diff stuff here
        reporter.report_diff_result(self.test_identifier, self.goal_file, output_file, 1.0 if exactly_the_same else 0.0, fuzzy=False)
        if exactly_the_same:
            return FractionalTestResult(1, 1)

        return FractionalTestResult(0, 1)
