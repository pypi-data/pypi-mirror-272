import abc
import dataclasses
from pathlib import Path
from typing import TextIO, Optional, Sequence, Mapping

from gradema.test.argument import Argument, ResolvedArgumentInfo

"""
It's worth noting that whenever you see TextIO in this file, it likely doesn't really mean TextIO.
Since both sys.stdout and sys.stderr are TextIO, it makes sense to describe its type as such.
However, most implementations that reference fields from this file are actually using the subprocess module under the hood.
If you change the implementation here, you need to take special care to make sure the object you supply to callers works with the subprocess module.

https://docs.python.org/3/library/subprocess.html#popen-constructor
"""


@dataclasses.dataclass
class CommandData:
    stdout: TextIO
    """The stdout to pass to subprocess.run"""
    stderr: TextIO
    """The stderr to pass to subprocess.run"""


@dataclasses.dataclass
class StdioCommandData:
    """
    Represents what stdout and stderr should be set to on a command.
    stdout is represented by a file path because it is expected that the caller wants to be able to know how to read from that file after the command is executed.
    """

    stdout_file: Optional[Path]
    """The file that stdout should be directed to"""
    stdout: TextIO
    """The stdout to pass to subprocess.run assuming that stdout_file is None"""
    stderr: TextIO
    """The stderr to pass to subprocess.run"""


class TestReporter(abc.ABC):
    """
    A TestReporter is passed to all tests. This exposes a public API for tests to use and report what they are doing.
    A TestReporter's implementation may log what the test is doing to the console, or even perform an action depending on how the TestReporter is configured.
    """

    @abc.abstractmethod
    def log(self, message: str) -> None:
        """
        Log an informative message to the user.

        :param message: The message to log. No formatting is support
        """
        pass

    @abc.abstractmethod
    def log_unexpected_exception(self, exception: BaseException) -> None:
        """
        Log an unexpected exception

        :param exception: The exception to log
        """
        pass

    @abc.abstractmethod
    def resolve_command(self, command: Sequence[Argument], test_identifier: str) -> tuple[Sequence[str], Mapping[tuple[int, Argument], ResolvedArgumentInfo]]:
        """
        Resolves a list of Arguments by returning a list of strings.

        The returned value contains the resolved command and an argument info dictionary.
        The key of the argument info dictionary is a tuple of (index, Argument) where index is the index of the Argument in the command parameter.

        If you are wondering why ``command``'s type is  ``Sequence[Argument]`` rather than a ``list[Argument]``, it is because the Sequence type is covariant.
        That means that you can assign a ``Sequence[str]`` to a ``Sequence[Argument]``, which is necessary to make sure mypy type checking is happy,
        and correctly documents how the ``command`` argument is used: it is not modified. More information here: https://mypy.readthedocs.io/en/stable/common_issues.html#variance

        :param test_identifier: The identifier of the test being run
        :param command: The command to resolve
        :return: A tuple of (resolved command, argument info dictionary)
        :raises ValueError: A ValueError may be risen if the parameters supplied to this function do not give enough information to resolve a particular Argument.
                            This exception is currently not risen in any known implementation, but it's possible that optional parameters will be added in the future
                            that aid in resolving an Argument that is not created as of writing this docstring
        """
        pass

    @abc.abstractmethod
    def report_command(self, command: Sequence[str]) -> CommandData:
        """
        Reports that the given command WILL be run

        :param command: The command that will be run
        :return: A CommandData object containing parameters that determine where the stdout and stdin of the command should go.
        """
        pass

    @abc.abstractmethod
    def report_stdio_command(self, command: Sequence[str], test_identifier: str, input_file: Optional[Path], stdout_as_output: bool) -> StdioCommandData:
        """
        Reports that a stdio test command WILL be run.

        This is similar to report_command, but it is expected that the caller will run the command and direct its output to that specified by the returned object.

        :param command: The base command that is being run (not including any I/O redirection)
        :param test_identifier: An identifier for the test. This is not recommended to contain spaces or upper case characters
        :param input_file: The input file that will be directed into the command's stdin, or None if no specific input file is being used.
        :param stdout_as_output: True to use the command's stdout as an output, False to not
        :return: A StdioCommandData that contains the file to direct stdout to and the TextIO to direct stderr to.
        """
        pass

    @abc.abstractmethod
    def maybe_launch_debugger(self, command: Sequence[str]) -> None:
        """
        Calling this function will launch the debugger by running the given command only if we are in debugging mode.
        The implementation will likely prompt the user to make sure they want to launch the debugger

        :param command: The command to launch the debugger
        """
        pass

    @abc.abstractmethod
    def report_diff_result(self, test_identifier: str, goal_file: Path, output_file: Path, similarity: float, fuzzy: bool) -> None:
        """
        Reports the result of a diff and possibly opens a diff viewer depending on the configuration of this reporter.

        :param test_identifier: The identifier for the test
        :param goal_file: The goal file
        :param output_file: The output file that is supposed to contain the same contents of the goal file
        :param similarity: A number from 0 to 1 representing the similarity (1 is exactly the same). Non-fuzzy diffs should only pass 0 or 1.
        :param fuzzy: True if fuzzy, false otherwise
        """
        pass

    @abc.abstractmethod
    def report_file_exists_test(self, file: Path, expected: str) -> None:
        """
        Reports that a file existence test WILL BE performed.

        :param file:
        :param expected:
        :return:
        """
        pass

    @abc.abstractmethod
    def report_file_exists_test_result(self, file: Path, expected: str, is_correct: bool, actual: Optional[str]) -> None:
        """
        Reports that a file existence test has been performed and that the result is this.

        :param file: The file being tested for its existence
        :param expected: The expected type of the file (basically the output of `file <file>`
        :param is_correct: True if the actual matches the expected
        :param actual: The actual type of the file, or None if the file does not exist
        :return:
        """
        pass
