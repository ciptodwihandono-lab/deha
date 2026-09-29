"""Peta sebaran burung air AWC Indonesia 2026 dengan metode GRID.

Metode grid: wilayah dibagi jadi sel-sel berukuran tetap (default 1x1
derajat), lalu tiap sel diwarnai berdasarkan kekayaan spesies (jumlah
spesies unik) dari semua lokasi survei yang jatuh di sel itu. Ini metode
umum di atlas burung/biogeografi untuk memvisualisasikan pola sebaran
tanpa perlu basemap citra satelit.

Catatan: grid di sini murni berdasar kotak lat/lon (bukan proyeksi peta
resmi seperti grid UTM/MGRS yang dipakai atlas burung formal), cukup
untuk visualisasi eksploratif. Untuk peta grid resmi, sebaiknya pakai
sistem grid baku (mis. grid QGIS "Create Grid" dengan CRS proyeksi yang
sesuai).

Workflow: data/raw/awc_indonesia_2026/awc_indonesia_2026_anonim.xlsx
-> this script -> data/processed/awc_grid_1deg.csv
                  outputs/figures/peta_grid_sebaran_awc.png
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "raw" / "awc_indonesia_2026" / "awc_indonesia_2026_anonim.xlsx"
OUT_TABLE = ROOT / "data" / "processed" / "awc_grid_1deg.csv"
FIG_PATH = ROOT / "outputs" / "figures" / "peta_grid_sebaran_awc.png"

DECISION_VALID = {"OK", "1"}
UKURAN_GRID_DERAJAT = 1.0


def load_verified(path: Path = INPUT_PATH) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="COUNT")
    df = df[df["Decision (OK/1/Parkir)"].isin(DECISION_VALID)].copy()
    df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce").fillna(0)
    return df


def buat_grid(df: pd.DataFrame, ukuran: float = UKURAN_GRID_DERAJAT) -> pd.DataFrame:
    df = df.copy()
    df["grid_x"] = np.floor(df["Longitude (DD)"] / ukuran) * ukuran
    df["grid_y"] = np.floor(df["Latitude (DD)"] / ukuran) * ukuran

    rows = []
    for (gx, gy), group in df.groupby(["grid_x", "grid_y"]):
        n_threatened = group.loc[group["IUCN_RedList"].isin(["EN", "CR", "VU"]), "Nama Ilmiah"].nunique()
        rows.append(
            {
                "grid_x": gx,
                "grid_y": gy,
                "kekayaan_spesies": group["Nama Ilmiah"].nunique(),
                "total_individu": int(group["Jumlah"].sum()),
                "jumlah_lokasi": group["ID Lokasi"].nunique(),
                "jumlah_spesies_terancam": n_threatened,
            }
        )
    return pd.DataFrame(rows).sort_values("kekayaan_spesies", ascending=False)


def plot_grid(grid: pd.DataFrame, df_points: pd.DataFrame, ukuran: float = UKURAN_GRID_DERAJAT) -> None:
    fig, ax = plt.subplots(figsize=(11, 8))

    vmax = grid["kekayaan_spesies"].max()
    cmap = plt.colormaps["YlGnBu"]

    for _, row in grid.iterrows():
        color = cmap(row["kekayaan_spesies"] / vmax)
        ax.add_patch(
            Rectangle(
                (row["grid_x"], row["grid_y"]),
                ukuran,
                ukuran,
                facecolor=color,
                edgecolor="white",
                linewidth=0.5,
            )
        )

    ax.scatter(
        df_points["Longitude (DD)"],
        df_points["Latitude (DD)"],
        s=8,
        color="black",
        alpha=0.5,
        label="Lokasi survei AWC 2026",
    )

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=vmax))
    cbar = fig.colorbar(sm, ax=ax, shrink=0.7)
    cbar.set_label("Kekayaan spesies per sel grid")

    ax.set_xlim(94, 142)
    ax.set_ylim(-12, 7)
    ax.set_xlabel("Bujur (\N{DEGREE SIGN}BT)")
    ax.set_ylabel("Lintang (\N{DEGREE SIGN}, negatif = LS)")
    ax.set_title(
        f"Peta Sebaran Burung Air -- Metode Grid {ukuran:g}\N{DEGREE SIGN} x {ukuran:g}\N{DEGREE SIGN}\n"
        f"Kekayaan Spesies per Sel, AWC Indonesia 2026 (baris terverifikasi)",
        fontsize=11,
    )
    ax.set_aspect("equal")
    ax.legend(loc="lower left", fontsize=8)
    ax.grid(False)

    fig.tight_layout()
    FIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_PATH, dpi=180)
    plt.close(fig)


def main() -> None:
    df = load_verified()
    grid = buat_grid(df)

    OUT_TABLE.parent.mkdir(parents=True, exist_ok=True)
    grid.to_csv(OUT_TABLE, index=False)

    points = df[["ID Lokasi", "Latitude (DD)", "Longitude (DD)"]].drop_duplicates()
    plot_grid(grid, points)

    print(f"{len(grid)} sel grid terisi dari {points.shape[0]} lokasi -> {OUT_TABLE}")
    print(f"Peta -> {FIG_PATH}")
    print("\n5 sel grid dengan kekayaan spesies tertinggi:")
    print(grid.head(5).to_string(index=False))


if __name__ == "__main__":
    main()
