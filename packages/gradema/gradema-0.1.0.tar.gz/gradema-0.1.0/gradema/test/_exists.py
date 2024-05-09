from os import PathLike
from pathlib import Path

from . import TestReporter, Test, TestResult, FractionalTestResult


def create_file_exists_test(files: list[tuple[str | Path | PathLike[str], str]], mime: bool = False) -> Test:
    return FileExistsTest(files, mime)


class FileExistsTest(Test):

    def __init__(self, files: list[tuple[str | Path | PathLike[str], str]], mime: bool):
        self.files: list[tuple[str | Path | PathLike[str], str]] = files
        self.mime = mime

    def run(self, reporter: TestReporter) -> TestResult:
        success_count = 0
        total_count = 0
        for path_like, expected in self.files:
            path = path_like if isinstance(path_like, Path) else Path(path_like)
            reporter.report_file_exists_test(path, expected)
            total_count += 1
            output = None
            try:
                # noinspection PyUnresolvedReferences
                import magic

                # NOTE: magic.from_file(path) works when path is a pathlib.Path on Linux, but does not work on Windows.
                #   We must convert to string first!
                output = magic.from_file(str(path))
            except FileNotFoundError:
                pass
            except OSError as e:
                reporter.log_unexpected_exception(e)
            except ImportError as e:
                reporter.log_unexpected_exception(e)
                reporter.log("Unexpected import error")
            except AttributeError:
                # An AttributeError occurs on Windows when python-magic-bin is not installed
                #   `AttributeError: module 'magic' has no attribute 'from_file'
                # https://github.com/ahupp/python-magic?tab=readme-ov-file#installation
                reporter.log("libmagic is not installed. This test will fail. Make sure that python-magic-bin is installed if you are on Windows.")
            is_correct = output is not None and expected in output  # expected and output don't have to match, expected just has to be contained in the actual output
            if is_correct:
                success_count += 1
            reporter.report_file_exists_test_result(path, expected, is_correct, output)

        return FractionalTestResult(success_count, total_count)
