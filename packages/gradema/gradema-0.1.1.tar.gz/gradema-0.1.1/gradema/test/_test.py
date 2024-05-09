import abc
import dataclasses
from typing import Union

from gradema.test import TestReporter


@dataclasses.dataclass
class FractionalTestResult:
    success_count: int
    total_count: int


@dataclasses.dataclass
class PercentTestResult:
    percent: float


TestResult = Union[FractionalTestResult, PercentTestResult]


class Test(abc.ABC):
    """
    This is the abstract class inherited by all tests.
    """

    @abc.abstractmethod
    def run(self, reporter: TestReporter) -> TestResult:
        pass
