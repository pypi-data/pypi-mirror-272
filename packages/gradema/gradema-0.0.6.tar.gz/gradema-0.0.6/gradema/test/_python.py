import importlib.util
from pathlib import Path
from typing import Sequence, Optional

import editorconfig  # type: ignore

from . import Test
from ._command import CommandTest
from ._stdio import StdioTest
from .argument import Argument


def create_python_test(module_name: str) -> Test:
    """
    Creates a python test that runs the given module and is successful depending on the successful exit code of running the given module.

    Please note that this kind of test is susceptible to "early exit attacks".
    Details here: https://gradema.readthedocs.io/en/latest/develop/assignment/security.html#early-exit-attacks

    :param module_name: The name of the module to run
    :return: A test whose success is based on the exit code of running the specified module
    """
    if importlib.util.find_spec(module_name) is None:
        raise ValueError(f"Module {module_name} not found")

    return CommandTest(["python", "-m", module_name], ["pudb", "-m", module_name])


def create_python_pytest(file_argument: str) -> Test:
    """
    Creates a pytest test.

    Currently, does not have a debugging option. See source code if this function for detailed comment.

    :param file_argument: The argument to pass to pytest that is the file and optionally has a ``::test_function_name`` tacked on at the end
    :return: A pytest test
    """
    # TODO add a debug command to pytest
    """
    So... I (Lavender Shannon) spent a couple of hours trying to figure out how to use pudb and pytest together.

    If you do something like ``pudb -m pytest example/binaryconvert/autograder/test/unit/test_convert_1.py::test_convert_1`` it drops you into pytest's main.
    You can eventually get dropped into debugging the function you actually care about, but it's not intuitive.

    You can try something like ``pytest --pdb --pdbcls=pudb.debugger:Debugger example/binaryconvert/autograder/test/unit/test_convert_5.py::test_convert_5``,
    and that works reasonably well only if you want to view the stacktrace within pudb. You don't actually get to debug the function.

    The only thing that works reasonably well is using https://github.com/wronglink/pytest-pudb and set pudb.set_trace() calls at the beginning of your test function.
    Problem with this is that it seems glitchy after you are done debugging the function you care about. Like it's running it multiple times? I'm not sure why...
    """

    # return CommandTest(["pytest", "-q", "--no-summary", "--no-header", file_argument])
    return CommandTest(["pytest", "-q", "--no-header", file_argument])


def create_python_stdio_test(module_name: str, test_identifier: str, args: Sequence[Argument], input_file: Optional[Path], goal_file: Path, stdout_as_output: bool) -> Test:
    command: list[Argument] = ["python", "-m", module_name]
    command.extend(args)
    return StdioTest(command, test_identifier, input_file, goal_file, stdout_as_output)


def create_python_traditional_stdio_test(module_name: str, test_identifier: str, input_file: Path, goal_file: Path) -> Test:
    """
    Creates a traditional stdio test

    :param module_name:
    :param test_identifier:
    :param input_file:
    :param goal_file:
    :return:
    """
    return create_python_stdio_test(module_name, test_identifier, [], input_file, goal_file, stdout_as_output=True)


def create_python_traditional_arg_test(module_name: str, test_identifier: str, args: Sequence[Argument], goal_file: Path) -> Test:
    return create_python_stdio_test(module_name, test_identifier, args, None, goal_file, stdout_as_output=False)


def create_python_format_check_from_path(path: str) -> Test:
    line_length = editorconfig.get_properties(str((Path(path) / "some_random_file.py").absolute())).get("max_line_length")
    command = ["black", "--check"]
    if line_length is not None:
        command.append(f"--line-length={line_length}")
    command.append(path)
    return CommandTest(command)


def create_python_format_check() -> Test:
    return create_python_format_check_from_path(".")


def create_python_type_check() -> Test:
    return CommandTest(["mypy", "--strict", "--disallow-any-explicit", "."])
