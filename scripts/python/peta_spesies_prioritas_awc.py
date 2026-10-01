"""Peta sebaran per spesies untuk spesies prioritas konservasi (status
IUCN Endangered) dari data AWC Indonesia 2026 -- small multiples, satu
panel per spesies, beda dengan peta grid agregat
(peta_grid_resmi_awc.py) yang menggabungkan semua spesies jadi satu sel.

Jumlah individu per lokasi dihitung dari NILAI MAKSIMUM baris per
(spesies, lokasi) -- bukan jumlah semua baris -- untuk menghindari hitung
ganda antar-sesi pengamatan, mengikuti konvensi di sheet "Rekap Spesies
Final" pada file sumber.

Workflow: data/raw/awc_indonesia_2026/awc_indonesia_2026_anonim.xlsx
          + data/raw/boundaries/indonesia_nasional.geojson
-> this script -> outputs/figures/peta_spesies_prioritas_awc.png
"""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT_AWC = ROOT / "data" / "raw" / "awc_indonesia_2026" / "awc_indonesia_2026_anonim.xlsx"
INPUT_BOUNDARY = ROOT / "data" / "raw" / "boundaries" / "indonesia_nasional.geojson"
FIG_PATH = ROOT / "outputs" / "figures" / "peta_spesies_prioritas_awc.png"

DECISION_VALID = {"OK", "1"}
CRS_INDONESIA_EQUAL_AREA = (
    "+proj=aea +lat_1=-8 +lat_2=6 +lat_0=-2 +lon_0=118 "
    "+x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
)

# Spesies berstatus IUCN "Endangered" yang tercatat di AWC 2026 (tidak
# ada spesies "Critically Endangered" di dataset ini).
SPESIES_PRIORITAS = [
    "Calidris tenuirostris",
    "Anarhynchus mongolus",
    "Mycteria cinerea",
    "Numenius madagascariensis",
    "Tringa guttifer",
    "Zosterops flavus",
]


def load_verified() -> pd.DataFrame:
    df = pd.read_excel(INPUT_AWC, sheet_name="COUNT")
    df = df[df["Decision (OK/1/Parkir)"].isin(DECISION_VALID)].copy()
    df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce").fillna(0)
    return df


def titik_per_spesies(df: pd.DataFrame, nama_ilmiah: str) -> gpd.GeoDataFrame:
    subset = df[df["Nama Ilmiah"] == nama_ilmiah]
    per_lokasi = (
        subset.groupby(["ID Lokasi", "Latitude (DD)", "Longitude (DD)"])["Jumlah"]
        .max()
        .reset_index()
    )
    gdf = gpd.GeoDataFrame(
        per_lokasi,
        geometry=gpd.points_from_xy(per_lokasi["Longitude (DD)"], per_lokasi["Latitude (DD)"]),
        crs="EPSG:4326",
    )
    return gdf.to_crs(CRS_INDONESIA_EQUAL_AREA)


def plot_spesies(ax, boundary: gpd.GeoDataFrame, titik: gpd.GeoDataFrame, nama_indonesia: str, nama_ilmiah: str) -> None:
    boundary.plot(ax=ax, color="#e8e4d8", edgecolor="#999999", linewidth=0.3)

    if len(titik) > 0:
        sizes = 30 + (titik["Jumlah"] / titik["Jumlah"].max()) * 250
        ax.scatter(
            titik.geometry.x, titik.geometry.y,
            s=sizes, color="#c62828", edgecolor="#5c0000", linewidth=0.5, alpha=0.8, zorder=3,
        )

    total_individu = int(titik["Jumlah"].sum())
    jumlah_lokasi = len(titik)
    ax.set_title(f"{nama_indonesia}\n({nama_ilmiah})\n{jumlah_lokasi} lokasi, {total_individu} individu", fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def main() -> None:
    df = load_verified()
    boundary = gpd.read_file(INPUT_BOUNDARY).to_crs(CRS_INDONESIA_EQUAL_AREA)

    nama_indonesia_map = df.drop_duplicates("Nama Ilmiah").set_index("Nama Ilmiah")["Nama Indonesia"]

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    fig.suptitle(
        "Sebaran Spesies Prioritas Konservasi (Status IUCN: Endangered) -- AWC Indonesia 2026\n"
        "Ukuran titik proporsional terhadap jumlah individu per lokasi (nilai maksimum antar-sesi)",
        fontsize=12,
    )

    for ax, nama_ilmiah in zip(axes.flat, SPESIES_PRIORITAS):
        titik = titik_per_spesies(df, nama_ilmiah)
        nama_indonesia = nama_indonesia_map.get(nama_ilmiah, nama_ilmiah)
        plot_spesies(ax, boundary, titik, nama_indonesia, nama_ilmiah)

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    FIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_PATH, dpi=160)
    plt.close(fig)

    print(f"Peta 6 spesies prioritas -> {FIG_PATH}")
    for nama_ilmiah in SPESIES_PRIORITAS:
        titik = titik_per_spesies(df, nama_ilmiah)
        print(f"  {nama_indonesia_map.get(nama_ilmiah, nama_ilmiah)}: {len(titik)} lokasi, {int(titik['Jumlah'].sum())} individu")


if __name__ == "__main__":
    main()
