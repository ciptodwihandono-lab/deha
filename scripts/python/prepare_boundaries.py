"""Prepare kecamatan boundary data joined with attribute data for mapping.

Contoh skala kecil (kecamatan di Kota Yogyakarta) sebagai bukti alur kerja.
Untuk skala nasional (seluruh kecamatan/desa Indonesia), ganti input di
data/raw/boundaries/ dengan data resmi BIG/GADM (lihat
data/raw/boundaries/README.md) -- struktur dan script ini tetap sama.

Workflow: data/raw/boundaries/*.geojson -> this script
-> data/processed/*.geojson (+ .csv) -> scripts/r/map_indonesia.R -> outputs/
"""

import random
from pathlib import Path

import geopandas as gpd

ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "raw" / "boundaries" / "yogyakarta_kecamatan.geojson"
OUTPUT_GEOJSON = ROOT / "data" / "processed" / "kecamatan_yogyakarta.geojson"
OUTPUT_CSV = ROOT / "data" / "processed" / "kecamatan_yogyakarta_attributes.csv"

random.seed(42)


def add_dummy_attributes(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Simulate a statistic per kecamatan (mis. kepadatan penduduk).

    Ganti bagian ini dengan data asli (mis. dari BPS) saat sudah tersedia.
    """
    gdf["kepadatan_penduduk"] = [random.randint(8000, 20000) for _ in range(len(gdf))]
    return gdf


def prepare(input_path: Path = INPUT_PATH) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(input_path)
    gdf = gdf.rename(columns={"name": "kecamatan"})
    gdf = add_dummy_attributes(gdf)

    OUTPUT_GEOJSON.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(OUTPUT_GEOJSON, driver="GeoJSON")
    gdf.drop(columns="geometry").to_csv(OUTPUT_CSV, index=False)
    return gdf


if __name__ == "__main__":
    result = prepare()
    print(f"Prepared {len(result)} kecamatan -> {OUTPUT_GEOJSON}")
    print(f"Attribute table -> {OUTPUT_CSV}")
