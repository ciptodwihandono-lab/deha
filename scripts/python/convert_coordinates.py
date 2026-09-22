"""Convert field-note DMS coordinates to decimal degrees and build a point layer.

Isi kolom `koordinat_dms` di data/raw/observations/vegetasi_kukang_jawa.csv
dari catatan lapangan (format bebas, mis. `6 12 57.2 S 106 49 12.4 E` atau
`6°12'57.2"S 106°49'12.4"E`), lalu jalankan script ini untuk mengisi kolom
`lat`/`lon` (decimal degrees) dan membuat titik GeoJSON untuk QGIS/R.

Workflow: data/raw/observations/vegetasi_kukang_jawa.csv (koordinat_dms)
-> this script -> data/processed/vegetasi_kukang_jawa.geojson
"""

import re
from pathlib import Path

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "raw" / "observations" / "vegetasi_kukang_jawa.csv"
OUTPUT_CSV = INPUT_PATH
OUTPUT_GEOJSON = ROOT / "data" / "processed" / "vegetasi_kukang_jawa.geojson"

# Menerima derajat-menit-detik dengan pemisah bebas (spasi, °, ', ", o).
DMS_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\D+(\d+(?:\.\d+)?)\D+(\d+(?:\.\d+)?)\D*([NSEW])", re.IGNORECASE
)


def dms_to_decimal(degrees: float, minutes: float, seconds: float, direction: str) -> float:
    decimal = degrees + minutes / 60 + seconds / 3600
    return -decimal if direction.upper() in ("S", "W") else decimal


def parse_koordinat_dms(text: str) -> tuple[float, float]:
    """Parse dua koordinat DMS (lat lalu lon) dari satu string."""
    matches = DMS_PATTERN.findall(text)
    if len(matches) != 2:
        raise ValueError(f"Tidak bisa parse koordinat: {text!r}")
    (lat_d, lat_m, lat_s, lat_dir), (lon_d, lon_m, lon_s, lon_dir) = matches
    lat = dms_to_decimal(float(lat_d), float(lat_m), float(lat_s), lat_dir)
    lon = dms_to_decimal(float(lon_d), float(lon_m), float(lon_s), lon_dir)
    return lat, lon


def build(input_path: Path = INPUT_PATH) -> gpd.GeoDataFrame:
    df = pd.read_csv(input_path)

    needs_conversion = df["lat"].isna() & df["koordinat_dms"].notna()
    for idx in df[needs_conversion].index:
        lat, lon = parse_koordinat_dms(str(df.at[idx, "koordinat_dms"]))
        df.at[idx, "lat"] = lat
        df.at[idx, "lon"] = lon

    df.to_csv(OUTPUT_CSV, index=False)

    with_coords = df.dropna(subset=["lat", "lon"])
    gdf = gpd.GeoDataFrame(
        with_coords,
        geometry=[Point(xy) for xy in zip(with_coords["lon"], with_coords["lat"])],
        crs="EPSG:4326",
    )

    OUTPUT_GEOJSON.parent.mkdir(parents=True, exist_ok=True)
    if len(gdf) > 0:
        gdf.to_file(OUTPUT_GEOJSON, driver="GeoJSON")

    return gdf


if __name__ == "__main__":
    result = build()
    print(f"{len(result)} titik dengan koordinat valid -> {OUTPUT_GEOJSON}")
    skipped = pd.read_csv(INPUT_PATH)
    skipped = skipped[skipped["lat"].isna()]
    if len(skipped) > 0:
        print(f"{len(skipped)} baris belum punya koordinat (isi kolom koordinat_dms atau lat/lon).")
