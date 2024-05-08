from . import GraderReporter
from gradema.section import Section
from gradema.test import Test, FractionalTestResult, PercentTestResult


def point_sections(max_points: int, sections: list[Section]) -> list[int]:
    point_values_sum = 0
    point_values: list[int] = [0 for _ in range(len(sections))]
    weight_total = 0.0
    evenly_weighted_count = 0
    for i, section in enumerate(sections):
        if section.is_pointed or section.is_ungraded:
            assert section.points is not None
            point_values[i] = section.points
            point_values_sum += section.points
        elif section.is_weighted:
            assert section.weight is not None
            weight_total += section.weight
        else:
            assert section.is_evenly_weighted
            evenly_weighted_count += 1
    if evenly_weighted_count > 0:
        evenly_weighted_weight = (1 - weight_total) / evenly_weighted_count
        if evenly_weighted_weight <= 0:
            raise ValueError(
                f"weight_total: {weight_total} which is invalid when you have evenly weighted section. "
                f"Make sure it is less than 1 so the weight can be distributed evenly among those sections."
            )
        weight_divisor = 1.0
    else:
        evenly_weighted_weight = 0.0
        weight_divisor = weight_total

    remaining_points = max_points - point_values_sum
    if remaining_points < 0:
        raise ValueError(f"The sum of all the pointed sections are higher than max points. max_points: {max_points} sum: {sum(point_values)}")

    points_assigned = 0  # the sum of the points assigned to weighted or evenly weighted sections
    running_weight_sum = 0.0
    for i, section in enumerate(sections):
        if section.is_weighted or section.is_evenly_weighted:
            if section.is_weighted:
                assert section.weight is not None
                weight = section.weight / weight_divisor
            else:
                weight = evenly_weighted_weight
            running_weight_sum += weight
            target_points_assigned = remaining_points * running_weight_sum
            points = int(target_points_assigned - points_assigned)
            point_values[i] = points
            points_assigned += points

    assert points_assigned == remaining_points
    return point_values


def grade_test(reporter: GraderReporter, max_points: int, test: Test) -> int:
    reporter.report_start(max_points)
    result = test.run(reporter.test_reporter)
    if isinstance(result, FractionalTestResult):
        points = max_points * result.success_count // result.total_count
    else:
        assert isinstance(result, PercentTestResult)
        points = int(result.percent * max_points)

    reporter.report_test_result(result, points, max_points)
    return points


def grade_section(reporter: GraderReporter, max_points: int, section: Section) -> int:
    if isinstance(section.node, Test):
        return grade_test(reporter, max_points, section.node)
    assert isinstance(section.node, list)
    sections: list[Section] = section.node
    assert len(sections) > 0
    assert isinstance(sections[0], Section)
    point_values = point_sections(max_points, sections)

    reporter.report_start(max_points)
    total_points_earned = 0
    for i, section in enumerate(sections):
        points = point_values[i]
        subsection_reporter = reporter.subsection(section)
        points_received = grade_section(subsection_reporter, points, section)
        total_points_earned += points_received
    return total_points_earned
