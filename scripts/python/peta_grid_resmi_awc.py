"""Peta sebaran burung air AWC Indonesia 2026 -- versi GRID "resmi".

Beda dengan peta_grid_sebaran_awc.py (grid kotak derajat lintang/bujur,
eksploratif), script ini pakai:

1. **Proyeksi equal-area** (Albers Equal Area Conic, dikustomisasi untuk
   Indonesia: lat_1=-8, lat_2=6, lat_0=-2, lon_0=118) -- supaya luas tiap
   sel grid konsisten dalam km^2 di seluruh Indonesia, tidak terdistorsi
   seperti kotak derajat.
2. **Grid dalam satuan jarak nyata** (default 100 km x 100 km), bukan
   derajat -- konvensi standar atlas biogeografi/burung (mis. grid UTM
   10x10 km yang dipakai banyak atlas burung Eropa).
3. **Garis batas negara Indonesia** (`data/raw/boundaries/indonesia_nasional.geojson`)
   sebagai konteks peta, bukan cuma titik-titik lokasi survei.

Workflow: data/raw/awc_indonesia_2026/awc_indonesia_2026_anonim.xlsx
          + data/raw/boundaries/indonesia_nasional.geojson
-> this script -> data/processed/awc_grid_resmi_100km.geojson
                  outputs/figures/peta_grid_resmi_awc.png
"""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely.geometry import Point, box

ROOT = Path(__file__).resolve().parents[2]
INPUT_AWC = ROOT / "data" / "raw" / "awc_indonesia_2026" / "awc_indonesia_2026_anonim.xlsx"
INPUT_BOUNDARY = ROOT / "data" / "raw" / "boundaries" / "indonesia_nasional.geojson"
OUT_GRID = ROOT / "data" / "processed" / "awc_grid_resmi_100km.geojson"
FIG_PATH = ROOT / "outputs" / "figures" / "peta_grid_resmi_awc.png"

DECISION_VALID = {"OK", "1"}
UKURAN_SEL_M = 100_000  # 100 km

# Albers Equal Area Conic dikustomisasi untuk cakupan Indonesia.
CRS_INDONESIA_EQUAL_AREA = (
    "+proj=aea +lat_1=-8 +lat_2=6 +lat_0=-2 +lon_0=118 "
    "+x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
)


def load_verified_points() -> gpd.GeoDataFrame:
    df = pd.read_excel(INPUT_AWC, sheet_name="COUNT")
    df = df[df["Decision (OK/1/Parkir)"].isin(DECISION_VALID)].copy()
    df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce").fillna(0)
    geometry = [Point(xy) for xy in zip(df["Longitude (DD)"], df["Latitude (DD)"])]
    return gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")


def build_grid(boundary: gpd.GeoDataFrame, cell_size: float = UKURAN_SEL_M) -> gpd.GeoDataFrame:
    minx, miny, maxx, maxy = boundary.total_bounds
    xs = np.arange(minx, maxx + cell_size, cell_size)
    ys = np.arange(miny, maxy + cell_size, cell_size)
    cells = [box(x, y, x + cell_size, y + cell_size) for x in xs[:-1] for y in ys[:-1]]
    grid = gpd.GeoDataFrame({"geometry": cells}, crs=boundary.crs)
    # cuma sel yang beririsan dengan daratan/perairan Indonesia (bounding area)
    grid = grid[grid.intersects(boundary.union_all())].reset_index(drop=True)
    grid["cell_id"] = grid.index
    return grid


def aggregate_to_grid(points: gpd.GeoDataFrame, grid: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    joined = gpd.sjoin(points, grid[["cell_id", "geometry"]], how="inner", predicate="within")
    agg = (
        joined.groupby("cell_id")
        .agg(
            kekayaan_spesies=("Nama Ilmiah", "nunique"),
            total_individu=("Jumlah", "sum"),
            jumlah_lokasi=("ID Lokasi", "nunique"),
        )
        .reset_index()
    )
    return grid.merge(agg, on="cell_id", how="left")


def plot_official_map(boundary: gpd.GeoDataFrame, grid: gpd.GeoDataFrame, points: gpd.GeoDataFrame) -> None:
    fig, ax = plt.subplots(figsize=(11, 9))

    boundary.plot(ax=ax, color="#e8e4d8", edgecolor="#666666", linewidth=0.5, zorder=1)

    occupied = grid[grid["kekayaan_spesies"].notna()]
    empty = grid[grid["kekayaan_spesies"].isna()]
    empty.boundary.plot(ax=ax, color="#cccccc", linewidth=0.3, zorder=2)
    occupied.plot(
        ax=ax,
        column="kekayaan_spesies",
        cmap="YlGnBu",
        edgecolor="#333333",
        linewidth=0.4,
        legend=True,
        legend_kwds={"label": "Kekayaan spesies per sel (100km x 100km)", "shrink": 0.6},
        zorder=3,
    )

    points.plot(ax=ax, color="black", markersize=6, alpha=0.6, zorder=4, label="Lokasi survei AWC 2026")

    # Skala batang sederhana (100 km), digambar di pojok kiri bawah.
    minx, miny, maxx, maxy = boundary.total_bounds
    bar_x0 = minx + (maxx - minx) * 0.03
    bar_y0 = miny + (maxy - miny) * 0.03
    ax.plot([bar_x0, bar_x0 + 100_000], [bar_y0, bar_y0], color="black", linewidth=3, zorder=5)
    ax.text(bar_x0 + 50_000, bar_y0 + (maxy - miny) * 0.015, "100 km", ha="center", fontsize=8, zorder=5)

    # Panah utara sederhana.
    arrow_x = maxx - (maxx - minx) * 0.04
    arrow_y0 = miny + (maxy - miny) * 0.05
    ax.annotate(
        "U", xy=(arrow_x, arrow_y0 + 150_000), xytext=(arrow_x, arrow_y0),
        arrowprops=dict(facecolor="black", width=2, headwidth=8, headlength=8),
        ha="center", fontsize=10, fontweight="bold", zorder=5,
    )

    ax.set_title(
        "Peta Sebaran Burung Air -- Grid Resmi 100 km x 100 km\n"
        "Proyeksi Albers Equal-Area (kustom Indonesia) -- AWC Indonesia 2026",
        fontsize=12,
    )
    ax.set_axis_off()
    ax.legend(loc="lower left", fontsize=8, bbox_to_anchor=(0.0, -0.02))

    fig.tight_layout()
    FIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_PATH, dpi=200)
    plt.close(fig)


def main() -> None:
    boundary = gpd.read_file(INPUT_BOUNDARY).to_crs(CRS_INDONESIA_EQUAL_AREA)
    points = load_verified_points().to_crs(CRS_INDONESIA_EQUAL_AREA)

    grid = build_grid(boundary)
    grid = aggregate_to_grid(points, grid)

    OUT_GRID.parent.mkdir(parents=True, exist_ok=True)
    grid.to_crs("EPSG:4326").to_file(OUT_GRID, driver="GeoJSON")

    plot_official_map(boundary, grid, points)

    n_occupied = grid["kekayaan_spesies"].notna().sum()
    print(f"{len(grid)} sel grid dibuat ({UKURAN_SEL_M/1000:.0f}km x {UKURAN_SEL_M/1000:.0f}km), {n_occupied} terisi data")
    print(f"Grid (GeoJSON, EPSG:4326) -> {OUT_GRID}")
    print(f"Peta -> {FIG_PATH}")
    top5 = grid.dropna(subset=["kekayaan_spesies"]).nlargest(5, "kekayaan_spesies")
    print("\n5 sel dengan kekayaan spesies tertinggi:")
    print(top5[["cell_id", "kekayaan_spesies", "total_individu", "jumlah_lokasi"]].to_string(index=False))


if __name__ == "__main__":
    main()
