import dataclasses
from typing import Optional

from gradema.test import Test


SectionNode = list["Section"] | Test
"""Either a list of Sections, or a Test"""


@dataclasses.dataclass
class Section:
    """
    A section contains information about how many points it is worth.
    A section where points and weight are both none indicate an evenly weighted section.
    A section with points = 0 indicates an ungraded section.
    A section where points is non-zero indicates a pointed section.
    A section where weight is not None indicates a weighted section.
    """

    points: Optional[int]
    weight: Optional[float]
    name: str
    node: SectionNode

    @property
    def is_pointed(self) -> bool:
        return self.points is not None and self.points > 0

    @property
    def is_ungraded(self) -> bool:
        return self.points == 0

    @property
    def is_weighted(self) -> bool:
        return self.weight is not None

    @property
    def is_evenly_weighted(self) -> bool:
        return self.points is None and self.weight is None

    @classmethod
    def pointed(cls, points: int, name: str, node: SectionNode) -> "Section":
        if points <= 0:
            raise ValueError(f"points must be > 0. points: {points}")
        return Section(points, None, name, node)

    @classmethod
    def ungraded(cls, name: str, node: SectionNode) -> "Section":
        return Section(0, None, name, node)

    @classmethod
    def weighted(cls, weight: float, name: str, node: SectionNode) -> "Section":
        if weight <= 0:
            raise ValueError(f"weight must be > 0. weight: {weight}")
        return Section(None, weight, name, node)

    @classmethod
    def evenly_weighted(cls, name: str, node: SectionNode) -> "Section":
        return Section(None, None, name, node)
