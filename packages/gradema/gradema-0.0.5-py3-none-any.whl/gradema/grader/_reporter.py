import abc

from gradema.section import Section
from gradema.test import TestReporter, TestResult


class GraderReporter(abc.ABC):
    """
    A GraderReporter provides functionality to report on things occurring during the grading process.
    """

    @property
    @abc.abstractmethod
    def test_reporter(self) -> TestReporter:
        pass

    @abc.abstractmethod
    def report_start(self, max_points: int) -> None:
        pass

    @abc.abstractmethod
    def report_test_result(self, result: TestResult, points: int, max_points: int) -> None:
        pass

    @abc.abstractmethod
    def subsection(self, section: Section) -> "GraderReporter":
        """
        Creates a similar GraderReporter containing the passed subsection and updated attributes to correctly report on a subsection.

        :param section: A subsection of the current section being reported on.
        :return: The modified GraderReporter
        """
        pass
