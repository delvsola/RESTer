import requests
from zipfile import ZipFile
from threading import Thread


def extract_raster(zp: str, fp: str, filename: str, is_dsm: bool = True):
    with ZipFile(zp) as z:
        with open(f"./static/{'dsm' if is_dsm else 'dtm'}/{filename}",
                  "wb") as f:
            f.write(z.read(fp))


def download_raster(rnge, is_dsm=True):
    for i in rnge:
        if is_dsm:
            url = f"https://downloadagiv.blob.core.windows.net/dhm-vlaanderen-ii-dsm-raster-1m/DHMVIIDSMRAS1m_k{i:02d}.zip"
            path = f"./static/dsm/DHMVIIDSMRAS1m_k{i:02d}.zip"
        else:
            url = f"https://downloadagiv.blob.core.windows.net/dhm-vlaanderen-ii-dtm-raster-1m/DHMVIIDTMRAS1m_k{i:02d}.zip"
            path = f"./static/dtm/DHMVIIDTMRAS1m_k{i:02d}.zip"
        print(f"Downloading {path}")
        r = requests.get(url, stream=True)
        if r.status_code != 200:
            print(url)
            raise Exception(f"Status code is {r.status_code}")
        with open(path, "wb") as f:
            f.write(r.content)
        extract_raster(
            zp=path,
            fp=f"GeoTIFF/DHMVII{'DSM' if is_dsm else 'DTM'}RAS1m_k{i:02d}.tif",
            filename=f"DHMVII{'DSM' if is_dsm else 'DTM'}RAS1m_k{i:02d}.tif",
            is_dsm=is_dsm
        )


class RasterDownload(Thread):
    def __init__(self, rng, is_dsm=True):
        super().__init__()
        self.rng = rng
        self.is_dsm = is_dsm

    def run(self) -> None:
        download_raster(self.rng, self.is_dsm)
        

if __name__ == "__main__":
    rgs = [
        range(1,22),
        range(22, 44)
    ]

    threads = []

    for rng in rgs:
        t_dsm = RasterDownload(rng)
        t_dst = RasterDownload(rng, is_dsm=False)
        t_dsm.start()
        t_dst.start()
        threads.extend([t_dsm, t_dst])

    for thread in threads:
        thread.join()

    print("Done!")
