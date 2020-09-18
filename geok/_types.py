import geok
import arcgis
from pydantic import BaseModel, ValidationError

# TODO: long-term need to own the typing and internal validation components of the geometry types


class PolygonType(list):
    """
    Polyon geometry validation.
    """

    @classmethod
    def validate(cls, p):
        """
        Validates the geometry of a polygon
        """

        def check_polygon(part):
            import numpy as np
            import pandas as pd

            return {
                "length": len(part) >= 4,
                "valid": _is_line(part),
                "is_ring": part[0] == part[-1],
                "type": isinstance(
                    part[0],
                    (
                        np.int32,
                        int,
                        np.int16,
                        np.int8,
                        float,
                        np.float64,
                        np.float32,
                        np.int,
                        np.int64,
                    ),
                ),
            }

        return all(list(map(lambda x: check_polygon(x), p)))


def is_line(line):
    if isinstance(line, (arcgis.geometry.Polyline, geok.core.PolylineModel)):
        return True
    if isinstance(line, (list, tuple, set)) and len(line) > 0:
        return all(is_point(pt) for pt in line)


def is_point(pt):
    num = (int, float)
    if isinstance(pt, (geok.core.PointModel, arcgis.geometry.Point)):
        return True
    if isinstance(pt, dict):
        if ("x" in pt and "y" in pt) and (
            isinstance(pt["y"], num) and isinstance(pt["y"], num)
        ):
            return True

    if isinstance(pt, (list, tuple)):
        pass
