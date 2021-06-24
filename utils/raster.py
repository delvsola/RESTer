from osgeo import gdal
from shapely.geometry import Point
import numpy


def slice_tif(fp: str, ul: Point, lr: Point) -> numpy.ndarray:
    gdal_options = {
        "destName": "",
        "format": "MEM",
        "projWin": [ul.x, ul.x, lr.x, lr.y]

    }
    ds = gdal.Translate(
        srcDS=fp,
        **gdal_options
    )
    band = ds.GetRasterBand(1)
    return band.ReadAsArray()
