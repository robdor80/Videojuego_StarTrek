"""Illustrative ASTER QA projection of public F06 sensor coordinates.

The sensor +Y axis is drawn toward the Enterprise-D bow and +X to
starboard. F06 does not expose the ship's real attitude; this alignment is
only a fixed display convention. Distances never set marker radius.
"""
from __future__ import annotations

from math import atan2, cos, degrees, hypot, radians, sin


def angles(x: int, y: int, z: int) -> tuple[float | None, float] | None:
    """Return sensor bearing clockwise from +Y and elevation in degrees.

    A zero vector has no resolved direction. Pure vertical readings have
    a resolved elevation but no horizontal bearing.
    """
    if x == y == z == 0:
        return None
    horizontal = hypot(x, y)
    bearing = (degrees(atan2(x, y)) + 360.0) % 360.0 if horizontal else None
    return bearing, degrees(atan2(z, horizontal))


def project(x: int, y: int, z: int, radius: float,
            center_x: float, center_y: float, elevation_span: float
            ) -> tuple[tuple[float, float], tuple[float, float], float | None, float] | None:
    """Return top and profile points for one observed vector.

    Top: bow up, starboard right. Profile: bow right, positive elevation up.
    The fixed radius conveys direction only, independent of milli-AU scale.
    """
    result = angles(x, y, z)
    if result is None:
        return None
    bearing, elevation = result
    angle = radians(bearing or 0.0)
    horizontal_radius = radius if x or y else 0.0
    top = (center_x + horizontal_radius * sin(angle),
           center_y - horizontal_radius * cos(angle))
    profile = (center_x + horizontal_radius * cos(angle),
               center_y - elevation_span * elevation / 90.0)
    return top, profile, bearing, elevation
