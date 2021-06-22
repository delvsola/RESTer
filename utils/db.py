import sqlite3
from osgeo import gdal
import os
from shapely.geometry import Point

DB_NAME = "db.sqlite3"


def init_db():
    with sqlite3.connect(DB_NAME) as db:
        with db as cur:
            query = """CREATE TABLE IF NOT EXISTS reference (
                id INTEGER PRIMARY KEY,
                ulx REAL,
                uly REAL,
                lrx REAL,
                lry REAL
            )"""
            cur.execute(query)


def create_references():
    with sqlite3.connect(DB_NAME) as db:
        for root, dirs, files in os.walk("./static/dsm/"):
            for file in sorted(files):
                if file.endswith(".tif"):
                    path = os.path.join(root, file)
                    options = {
                        "format": "json"
                    }
                    infos = gdal.Info(path, **options)
                    ulx, uly = infos["cornerCoordinates"]["upperLeft"]
                    lrx, lry = infos["cornerCoordinates"]["lowerRight"]
                    with db as cur:
                        query = """INSERT INTO reference (ulx, uly, lrx, lry)
                        VALUES(?, ?, ?, ?)
                        """
                        cur.execute(query, (ulx, uly, lrx, lry))
                        print(f"Added {path} reference to database")


if __name__ == "__main__":
    init_db()
    create_references()
