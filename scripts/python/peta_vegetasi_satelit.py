"""Buat peta titik vegetasi kukang jawa di atas citra satelit.

Workflow: data/raw/observations/vegetasi_kukang_jawa.csv
-> this script -> outputs/figures/peta_vegetasi_kukang_satelit.png

Butuh package tambahan: pip install contextily adjustText
"""

from pathlib import Path

import contextily as cx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from adjustText import adjust_text
from shapely.geometry import Point

ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "raw" / "observations" / "vegetasi_kukang_jawa.csv"
OUTPUT_PATH = ROOT / "outputs" / "figures" / "peta_vegetasi_kukang_satelit.png"

WARNA_KATEGORI = {
    "pohon_pakan": "#2e7d32",
    "pohon_tidur": "#8d6e63",
    "belum_teridentifikasi": "#9e9e9e",
    "lainnya": "#1565c0",
}

LABEL_KATEGORI = {
    "pohon_pakan": "Pohon pakan",
    "pohon_tidur": "Pohon tidur (bambu)",
    "belum_teridentifikasi": "Belum teridentifikasi",
    "lainnya": "Lainnya",
}


def build_map(input_path: Path = INPUT_PATH, output_path: Path = OUTPUT_PATH) -> None:
    df = pd.read_csv(input_path)
    df = df.dropna(subset=["lat", "lon"])

    gdf = gpd.GeoDataFrame(
        df, geometry=[Point(xy) for xy in zip(df["lon"], df["lat"])], crs="EPSG:4326"
    ).to_crs(epsg=3857)

    fig, ax = plt.subplots(figsize=(10, 10))

    for kategori, warna in WARNA_KATEGORI.items():
        subset = gdf[gdf["kategori"] == kategori]
        if len(subset) == 0:
            continue
        subset.plot(
            ax=ax,
            color=warna,
            markersize=180,
            edgecolor="white",
            linewidth=1.5,
            label=LABEL_KATEGORI[kategori],
            zorder=3,
        )

    # Beri margin tetap (dalam meter) di sekitar titik, bukan persentase dari
    # rentang data -- supaya titik yang jauh sendiri (mis. Vegetasi 5) tidak
    # membuat area kosong yang berlebihan. Diset sebelum adjust_text supaya
    # label ditempatkan sesuai batas kanvas yang sebenarnya.
    bounds = gdf.total_bounds
    padding_m = 35
    ax.set_xlim(bounds[0] - padding_m, bounds[2] + padding_m)
    ax.set_ylim(bounds[1] - padding_m, bounds[3] + padding_m)

    xs = gdf.geometry.x.values
    ys = gdf.geometry.y.values

    texts = []
    for _, row in gdf.iterrows():
        nama_singkat = str(row["nama_ilmiah_tentatif"]).split(" --")[0].strip()
        label = f"{row['titik']}\n{nama_singkat}"
        texts.append(
            ax.annotate(
                label,
                xy=(row.geometry.x, row.geometry.y),
                fontsize=8,
                ha="center",
                zorder=5,
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#666666", lw=0.5, alpha=1.0),
            )
        )

    adjust_text(
        texts,
        x=xs,
        y=ys,
        ax=ax,
        force_text=(0.6, 0.9),
        force_points=(0.5, 0.8),
        expand=(1.3, 1.5),
        arrowprops=dict(arrowstyle="-", color="#333333", lw=0.7),
    )

    try:
        cx.add_basemap(ax, source=cx.providers.Esri.WorldImagery, crs=gdf.crs)
    except Exception as exc:  # jaringan mungkin memblokir server tile satelit
        print(f"Basemap satelit gagal dimuat ({exc}); pakai background polos.")
        ax.set_facecolor("#eef2f0")

    ax.set_axis_off()
    ax.set_title(
        "Vegetasi Terkait Perjumpaan Kukang Jawa\nTaman Kehati Kiarapayung -- identifikasi jenis masih tentatif dari foto",
        fontsize=12,
    )
    ax.legend(loc="lower right", frameon=True, fontsize=9, title="Kategori")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    print(f"Peta tersimpan di {output_path}")


if __name__ == "__main__":
    build_map()
