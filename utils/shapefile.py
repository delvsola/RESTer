import geopandas as gpd
from shapely.geometry import Point
from typing import Tuple


def get_bbox(pt: Point) -> [Tuple, None]:
    """
    Get the bounding box of a building on a Point
    :param pt: Shapely point with the coordinates of the building
    :return: A tuple with Upper-Left and Lower-Right coordinates of the box or
    None if no building found
    """
    shape = gpd.read_file('./shapefile/belgium//Bpn_ReBu.shp',
                          mask=pt)
    if len(shape) == 0:
        return None
    bounds = shape.bounds
    return bounds.minx, bounds.maxy, bounds.maxx, bounds.miny
