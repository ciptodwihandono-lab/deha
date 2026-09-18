"""Process point data exported from QGIS and hand it off to R for analysis.

Workflow: QGIS (digitize/edit) -> data/raw/*.geojson -> this script
-> data/processed/*.csv -> scripts/r/analyze_data.R -> outputs/
"""

from pathlib import Path

import geopandas as gpd

ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "raw" / "sample_points.geojson"
OUTPUT_PATH = ROOT / "data" / "processed" / "sample_processed.csv"

# Jakarta as reference point (EPSG:4326 -> EPSG:3857 for metric distance).
REFERENCE_POINT = gpd.GeoSeries(
    gpd.points_from_xy([106.8456], [-6.2088]), crs="EPSG:4326"
).to_crs(epsg=3857).iloc[0]


def process(input_path: Path = INPUT_PATH, output_path: Path = OUTPUT_PATH) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(input_path)
    projected = gdf.to_crs(epsg=3857)
    gdf["distance_from_jakarta_km"] = projected.geometry.distance(REFERENCE_POINT) / 1000

    output_path.parent.mkdir(parents=True, exist_ok=True)
    columns = ["id", "name", "population", "distance_from_jakarta_km"]
    gdf[columns].to_csv(output_path, index=False)
    return gdf


if __name__ == "__main__":
    result = process()
    print(f"Processed {len(result)} features -> {OUTPUT_PATH}")
