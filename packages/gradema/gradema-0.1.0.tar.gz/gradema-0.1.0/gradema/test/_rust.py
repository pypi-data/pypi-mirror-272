from os import PathLike
from pathlib import Path
from typing import Sequence, Optional

from gradema.test import Test
from gradema.test._command import CommandTest
from gradema.test._stdio import StdioTest
from gradema.test.argument import Argument


# noinspection PyMethodMayBeStatic
class RustProgram:
    def __init__(self, main_location: str | PathLike[str] | Path, binary_location: str | PathLike[str] | Path):
        self.main_location = main_location if isinstance(main_location, Path) else Path(main_location)
        self.binary_location = binary_location if isinstance(binary_location, Path) else Path(binary_location)

    def create_compile_step(self) -> Test:
        return CommandTest(["cargo", "build"])

    def create_stdio_test(self, test_identifier: str, args: Sequence[Argument], input_file: Optional[Path], goal_file: Path, stdout_as_output: bool) -> Test:
        command: list[Argument] = [str(self.binary_location)]
        command.extend(args)
        return StdioTest(command, test_identifier, input_file, goal_file, stdout_as_output)

    def create_traditional_stdio_test(self, test_identifier: str, input_file: Path, goal_file: Path) -> Test:
        return self.create_stdio_test(test_identifier, [], input_file, goal_file, stdout_as_output=True)

    def create_traditional_arg_test(self, test_identifier: str, args: Sequence[Argument], goal_file: Path) -> Test:
        return self.create_stdio_test(test_identifier, args, None, goal_file, stdout_as_output=False)

    def create_format_check(self) -> Test:
        """
        Creates a rustfmt check.

        Note that the resulting command will be something like ``rustfmt --check src/main.rs``.
        Even though this only includes the main file, all files referenced by main will also be format checked -- it's not necessary to list all the files here!
        https://github.com/rust-lang/rustfmt/issues/2426

        :return: A test that completes successfully when there are no formatting errors
        """
        return CommandTest(["rustfmt", "--check", str(self.main_location)])

    def create_cargo_command(self, arguments: list[str]) -> Test:
        return CommandTest(["cargo"] + arguments)
