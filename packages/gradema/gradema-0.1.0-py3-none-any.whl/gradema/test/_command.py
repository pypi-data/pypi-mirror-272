import subprocess

from gradema.test._reporter import TestReporter
from gradema.test._test import Test, TestResult, FractionalTestResult


class CommandTest(Test):
    def __init__(self, command: list[str], debug_command: list[str] | None = None):
        self.command = command
        self.debug_command = debug_command

    def run(self, reporter: TestReporter) -> TestResult:
        data = reporter.report_command(self.command)

        try:
            completed = subprocess.run(
                self.command,
                stdin=subprocess.DEVNULL,
                stdout=data.stdout,
                stderr=data.stderr,
            )
        except FileNotFoundError as e:
            reporter.log_unexpected_exception(e)
            reporter.log(f"Your environment may not be configured correctly. Could not find binary for {self.command[0]}")
            return FractionalTestResult(0, 1)

        # Note that these kinds of tests are susceptible to early-exit-attacks
        #   It is up to the user of this test to make sure that it cannot be exploited.
        if completed.returncode == 0:
            return FractionalTestResult(1, 1)
        if self.debug_command is not None:
            reporter.maybe_launch_debugger(self.debug_command)
        return FractionalTestResult(0, 1)
