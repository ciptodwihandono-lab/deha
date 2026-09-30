"""Peta intensitas pengamatan burung air AWC Indonesia 2026 -- versi GRID "resmi".

Warna tiap sel = jumlah lokasi survei di sel itu (proxy intensitas
pengamatan/banyaknya "pengamat" di sana) -- bukan lagi kekayaan spesies.
Data jumlah pengamat individu sudah dihapus dari sumbernya demi privasi
(lihat data/raw/awc_indonesia_2026/README.md), jadi jumlah lokasi survei
dipakai sebagai proxy terdekat yang masih tersedia. Kolom
`kekayaan_spesies` dan `total_individu` tetap disimpan di
awc_grid_resmi_100km.geojson untuk dipakai analisis lain.

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
4. **Label nama provinsi** dari `data/raw/boundaries/indonesia_provinsi.geojson`
   -- CATATAN: dataset ini lama (32 provinsi, masih pakai nama "Irian Jaya",
   belum ada pemekaran Papua 2022 atau Kalimantan Utara) -- dipakai murni
   untuk label orientasi visual, BUKAN batas administratif yang presisi.

Output berupa PDF 2 halaman: halaman 1 peta grid provinsi (di atas),
halaman 2 rekap kabupaten/kota (grafik batang -- belum ada poligon batas
kabupaten/kota di repo ini, lihat data/raw/boundaries/README.md untuk
sumber resmi kalau nanti mau dibuat versi peta).

Workflow: data/raw/awc_indonesia_2026/awc_indonesia_2026_anonim.xlsx
          + data/raw/boundaries/indonesia_nasional.geojson
          + data/raw/boundaries/indonesia_provinsi.geojson
-> this script -> data/processed/awc_grid_resmi_100km.geojson
                  data/processed/awc_rekap_kabupaten_kota.csv
                  outputs/figures/peta_grid_resmi_awc.png (halaman provinsi saja)
                  outputs/figures/peta_grid_resmi_awc.pdf (2 halaman)
"""

import re
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from adjustText import adjust_text
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
from shapely.geometry import Point, box

# Provinsi yang terlalu kecil/rapat untuk dilabeli langsung di peta utama
# skala nasional -- dipindah ke panel inset zoom terpisah.
PROVINSI_INSET = {
    "Dki Jakarta",
    "Probanten",
    "Jawa Barat",
    "Jawa Tengah",
    "Daerah Istimewa Yogyakarta",
    "Jawa Timur",
    "Bali",
}

ROOT = Path(__file__).resolve().parents[2]
INPUT_AWC = ROOT / "data" / "raw" / "awc_indonesia_2026" / "awc_indonesia_2026_anonim.xlsx"
INPUT_BOUNDARY = ROOT / "data" / "raw" / "boundaries" / "indonesia_nasional.geojson"
INPUT_PROVINCES = ROOT / "data" / "raw" / "boundaries" / "indonesia_provinsi.geojson"
OUT_GRID = ROOT / "data" / "processed" / "awc_grid_resmi_100km.geojson"
OUT_KABKOTA_TABLE = ROOT / "data" / "processed" / "awc_rekap_kabupaten_kota.csv"
FIG_PATH = ROOT / "outputs" / "figures" / "peta_grid_resmi_awc.png"
PDF_PATH = ROOT / "outputs" / "figures" / "peta_grid_resmi_awc.pdf"

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


def load_province_labels() -> gpd.GeoDataFrame:
    provinces = gpd.read_file(INPUT_PROVINCES).to_crs(CRS_INDONESIA_EQUAL_AREA)
    provinces["label"] = provinces["Propinsi"].str.title()
    provinces["label_point"] = provinces.geometry.representative_point()
    return provinces


def draw_layer(ax, boundary, grid, vmax) -> None:
    """Gambar satu lapisan peta (boundary + grid) -- dipakai ulang untuk
    peta utama maupun panel inset. Warna sel = jumlah lokasi survei
    (proxy intensitas pengamatan; data pengamat individu sudah dihapus
    demi privasi, lihat awc_indonesia_2026_anonim.xlsx)."""
    boundary.plot(ax=ax, color="#e8e4d8", edgecolor="#666666", linewidth=0.5, zorder=1)

    occupied = grid[grid["jumlah_lokasi"].notna()]
    empty = grid[grid["jumlah_lokasi"].isna()]
    empty.boundary.plot(ax=ax, color="#cccccc", linewidth=0.3, zorder=2)
    occupied.plot(
        ax=ax,
        column="jumlah_lokasi",
        cmap="YlOrRd",
        vmin=0,
        vmax=vmax,
        edgecolor="#333333",
        linewidth=0.4,
        zorder=3,
    )


def add_labels(ax, provinces: gpd.GeoDataFrame, fontsize: float) -> list:
    texts = []
    for _, prov in provinces.iterrows():
        texts.append(
            ax.text(
                prov["label_point"].x,
                prov["label_point"].y,
                prov["label"],
                fontsize=fontsize,
                ha="center",
                va="center",
                color="#333333",
                zorder=6,
                path_effects=[pe.withStroke(linewidth=2, foreground="white")],
            )
        )
    return texts


def plot_official_map(
    boundary: gpd.GeoDataFrame,
    grid: gpd.GeoDataFrame,
    provinces: gpd.GeoDataFrame,
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(11, 9))
    vmax = grid["jumlah_lokasi"].max()

    draw_layer(ax, boundary, grid, vmax)

    sm = plt.cm.ScalarMappable(cmap="YlOrRd", norm=plt.Normalize(vmin=0, vmax=vmax))
    cbar = fig.colorbar(sm, ax=ax, shrink=0.6, pad=0.03)
    cbar.ax.set_title("Jumlah\nlokasi\nsurvei\nper sel", fontsize=9, pad=10)

    provinces_utama = provinces[~provinces["label"].isin(PROVINSI_INSET)]
    provinces_inset = provinces[provinces["label"].isin(PROVINSI_INSET)]

    texts_utama = add_labels(ax, provinces_utama, fontsize=6)
    adjust_text(texts_utama, ax=ax, expand=(1.3, 1.5), force_text=(0.4, 0.6))

    # Kotak penanda area yang di-zoom di panel inset.
    inset_bounds = provinces_inset.total_bounds
    margin = 40_000
    inset_minx, inset_miny, inset_maxx, inset_maxy = (
        inset_bounds[0] - margin, inset_bounds[1] - margin,
        inset_bounds[2] + margin, inset_bounds[3] + margin,
    )
    ax.add_patch(
        Rectangle(
            (inset_minx, inset_miny),
            inset_maxx - inset_minx,
            inset_maxy - inset_miny,
            fill=False,
            edgecolor="#c62828",
            linewidth=1.2,
            zorder=7,
        )
    )

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
        "Peta Intensitas Pengamatan Burung Air (Proxy: Jumlah Lokasi Survei)\n"
        "Grid Resmi 100 km x 100 km, Proyeksi Albers Equal-Area -- AWC Indonesia 2026",
        fontsize=12,
    )
    ax.set_axis_off()

    # Panel inset: zoom ke Jawa-Bali (provinsi terlalu rapat untuk peta utama).
    # Ditaruh di area kosong kanan-bawah supaya tidak menimpa judul/peta utama.
    inset_ax = fig.add_axes([0.56, 0.08, 0.38, 0.36])
    draw_layer(inset_ax, boundary, grid, vmax)
    texts_inset = add_labels(inset_ax, provinces_inset, fontsize=7)
    inset_ax.set_xlim(inset_minx, inset_maxx)
    inset_ax.set_ylim(inset_miny, inset_maxy)
    adjust_text(texts_inset, ax=inset_ax, expand=(1.4, 1.8), force_text=(0.5, 0.8))
    for spine in inset_ax.spines.values():
        spine.set_edgecolor("#c62828")
        spine.set_linewidth(1.2)
    inset_ax.set_xticks([])
    inset_ax.set_yticks([])
    inset_ax.set_title("Detail: Jawa & Bali", fontsize=9)

    FIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_PATH, dpi=200, bbox_inches="tight", pad_inches=0.4)
    return fig


def clean_kabkota_name(raw: str) -> str:
    """Hapus prefiks nomor urut (mis. '7. Kabupaten Cilacap' -> 'Kabupaten Cilacap')."""
    return re.sub(r"^\d+\.\s*", "", str(raw)).strip()


def summarize_by_kabkota(points: gpd.GeoDataFrame) -> pd.DataFrame:
    df = points.copy()
    df["kabupaten_kota"] = df["Kabupaten/Kota"].apply(clean_kabkota_name)
    summary = (
        df.groupby("kabupaten_kota")
        .agg(
            jumlah_lokasi=("ID Lokasi", "nunique"),
            kekayaan_spesies=("Nama Ilmiah", "nunique"),
            total_individu=("Jumlah", "sum"),
        )
        .reset_index()
        .sort_values("jumlah_lokasi", ascending=False)
        .reset_index(drop=True)
    )
    return summary


def plot_kabkota_page(summary: pd.DataFrame) -> plt.Figure:
    """Halaman ke-2: rekap per kabupaten/kota. Belum ada data poligon batas
    kabupaten/kota di repo ini, jadi disajikan sebagai tabel/grafik batang,
    bukan peta -- lihat data/raw/boundaries/README.md untuk sumber resmi
    (BIG/GADM) kalau nanti mau dibuat versi peta."""
    fig, ax = plt.subplots(figsize=(9, max(8, len(summary) * 0.22)))

    ordered = summary.iloc[::-1]
    vmax = summary["jumlah_lokasi"].max()
    colors = plt.colormaps["YlOrRd"](ordered["jumlah_lokasi"] / vmax)
    ax.barh(ordered["kabupaten_kota"], ordered["jumlah_lokasi"], color=colors, edgecolor="#333333", linewidth=0.3)

    ax.set_xlabel("Jumlah lokasi survei")
    ax.set_title(
        f"Rekap {len(summary)} Kabupaten/Kota -- AWC Indonesia 2026\n"
        "(belum ada peta poligon batas kabupaten/kota di repo ini)",
        fontsize=11,
    )
    ax.tick_params(axis="y", labelsize=7)
    fig.tight_layout()
    return fig


def main() -> None:
    boundary = gpd.read_file(INPUT_BOUNDARY).to_crs(CRS_INDONESIA_EQUAL_AREA)
    points = load_verified_points().to_crs(CRS_INDONESIA_EQUAL_AREA)
    provinces = load_province_labels()

    grid = build_grid(boundary)
    grid = aggregate_to_grid(points, grid)

    OUT_GRID.parent.mkdir(parents=True, exist_ok=True)
    grid.to_crs("EPSG:4326").to_file(OUT_GRID, driver="GeoJSON")

    kabkota_summary = summarize_by_kabkota(points)
    OUT_KABKOTA_TABLE.parent.mkdir(parents=True, exist_ok=True)
    kabkota_summary.to_csv(OUT_KABKOTA_TABLE, index=False)

    fig_provinsi = plot_official_map(boundary, grid, provinces)
    fig_kabkota = plot_kabkota_page(kabkota_summary)

    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(PDF_PATH) as pdf:
        pdf.savefig(fig_provinsi, bbox_inches="tight", pad_inches=0.4)
        pdf.savefig(fig_kabkota, bbox_inches="tight")
    plt.close(fig_provinsi)
    plt.close(fig_kabkota)

    n_occupied = grid["jumlah_lokasi"].notna().sum()
    print(f"{len(grid)} sel grid dibuat ({UKURAN_SEL_M/1000:.0f}km x {UKURAN_SEL_M/1000:.0f}km), {n_occupied} terisi data")
    print(f"Grid (GeoJSON, EPSG:4326) -> {OUT_GRID}")
    print(f"Rekap kabupaten/kota ({len(kabkota_summary)} unit) -> {OUT_KABKOTA_TABLE}")
    print(f"Peta (PNG, halaman provinsi saja) -> {FIG_PATH}")
    print(f"PDF 2 halaman (provinsi + kabupaten/kota) -> {PDF_PATH}")
    top5 = grid.dropna(subset=["jumlah_lokasi"]).nlargest(5, "jumlah_lokasi")
    print("\n5 sel dengan jumlah lokasi survei (proxy intensitas pengamatan) tertinggi:")
    print(top5[["cell_id", "jumlah_lokasi", "kekayaan_spesies", "total_individu"]].to_string(index=False))


if __name__ == "__main__":
    main()
