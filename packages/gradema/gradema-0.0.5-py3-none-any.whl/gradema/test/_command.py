import subprocess

from gradema.test._reporter import TestReporter
from gradema.test._test import Test, TestResult, FractionalTestResult


class CommandTest(Test):
    def __init__(self, command: list[str], debug_command: list[str] | None = None):
        self.command = command
        self.debug_command = debug_command

    def run(self, reporter: TestReporter) -> TestResult:
        data = reporter.report_command(self.command)

        completed = subprocess.run(
            self.command,
            stdin=subprocess.DEVNULL,
            stdout=data.stdout,
            stderr=data.stderr,
        )
        # TODO prevent students from doing sys.exit(0)
        if completed.returncode == 0:
            return FractionalTestResult(1, 1)
        if self.debug_command is not None:
            reporter.maybe_launch_debugger(self.debug_command)
        return FractionalTestResult(0, 1)
