import sqlite3
from osgeo import gdal
import os

DB_NAME = "db.sqlite3"


def init_db():
    with sqlite3.connect(DB_NAME) as db:
        with db as cur:
            query = """CREATE TABLE IF NOT EXISTS reference (
                id INTEGER PRIMARY KEY,
                ulx INTEGER,
                uly INTEGER,
                lrx INTEGER,
                lry INTEGER
            )"""
            cur.execute(query)


def create_references():
    with sqlite3.connect(DB_NAME) as db:
        for root, dirs, files in os.walk("./static/dsm/"):
            for file in files:
                if file.endswith(".tif"):
                    path = os.path.join(root, file)
                    src = gdal.Open(path)
                    ulx, xres, xskew, uly, yskew, yres = src.GetGeoTransform()
                    lrx = ulx + (src.RasterXSize * xres)
                    lry = uly + (src.RasterYSize * yres)
                    with db as cur:
                        query = """INSERT INTO reference (ulx, uly, lrx, lry)
                        VALUES(?, ?, ?, ?)
                        """
                        cur.execute(query, (ulx, uly, lrx, lry))
                        print(f"Added {path} reference to database")


if __name__ == "__main__":
    create_references()
