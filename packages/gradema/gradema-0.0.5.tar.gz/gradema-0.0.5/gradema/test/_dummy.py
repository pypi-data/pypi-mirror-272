from . import TestReporter, Test, TestResult, FractionalTestResult


class DummyTest(Test):

    @property
    def name(self) -> str:
        return "Dummy Test"

    def run(self, reporter: TestReporter) -> TestResult:
        return FractionalTestResult(1, 1)


DUMMY_TEST = DummyTest()


def dummy_test() -> Test:
    return DUMMY_TEST
