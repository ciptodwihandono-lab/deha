"""Analisis keanekaragaman hayati burung air dari data AWC Indonesia 2026.

AWC 2026 adalah snapshot satu tahun (bukan deret waktu), jadi pendekatan
yang cocok adalah analisis komunitas: kekayaan spesies, indeks
keanekaragaman Shannon-Wiener, dan kemerataan (evenness) per lokasi --
bukan analisis tren (itu perlu data multi-tahun, lihat
analisis_tren_iwc.py).

Hanya baris berkeputusan verifikasi "OK" atau "1" yang dipakai (PARKIR
dikeluarkan), konsisten dengan metodologi "Rekap Spesies Final" di
workbook aslinya.

Workflow: data/raw/awc_indonesia_2026/awc_indonesia_2026_anonim.xlsx
-> this script -> data/processed/awc_diversitas_per_lokasi.csv
                  data/processed/awc_diversitas_per_provinsi.csv
                  outputs/figures/awc_top_lokasi_kekayaan_spesies.png
                  outputs/figures/awc_sebaran_shannon.png
"""

import math
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "raw" / "awc_indonesia_2026" / "awc_indonesia_2026_anonim.xlsx"
OUT_LOKASI = ROOT / "data" / "processed" / "awc_diversitas_per_lokasi.csv"
OUT_PROVINSI = ROOT / "data" / "processed" / "awc_diversitas_per_provinsi.csv"
FIG_TOP_LOKASI = ROOT / "outputs" / "figures" / "awc_top_lokasi_kekayaan_spesies.png"
FIG_SHANNON = ROOT / "outputs" / "figures" / "awc_sebaran_shannon.png"

DECISION_VALID = {"OK", "1"}


def shannon_wiener(counts: pd.Series) -> float:
    total = counts.sum()
    if total == 0:
        return 0.0
    proportions = counts[counts > 0] / total
    return float(-(proportions * proportions.apply(math.log)).sum())


def load_verified_counts(path: Path = INPUT_PATH) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="COUNT")
    df = df[df["Decision (OK/1/Parkir)"].isin(DECISION_VALID)].copy()
    df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce").fillna(0)
    return df


def diversity_per_site(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for id_lokasi, group in df.groupby("ID Lokasi"):
        species_counts = group.groupby("Nama Ilmiah")["Jumlah"].sum()
        species_counts = species_counts[species_counts > 0]
        richness = len(species_counts)
        total_individu = species_counts.sum()
        h = shannon_wiener(species_counts)
        evenness = h / math.log(richness) if richness > 1 else float("nan")
        n_threatened = group.loc[
            group["IUCN_RedList"].isin(["EN", "CR", "VU"]), "Nama Ilmiah"
        ].nunique()
        rows.append(
            {
                "id_lokasi": id_lokasi,
                "nama_lokasi": group["Nama Lokasi"].iloc[0],
                "provinsi": group["Provinsi"].iloc[0],
                "lat": group["Latitude (DD)"].iloc[0],
                "lon": group["Longitude (DD)"].iloc[0],
                "kekayaan_spesies": richness,
                "total_individu": total_individu,
                "shannon_h": round(h, 3),
                "evenness_j": round(evenness, 3) if richness > 1 else None,
                "jumlah_spesies_terancam": n_threatened,
            }
        )
    return pd.DataFrame(rows).sort_values("kekayaan_spesies", ascending=False)


def diversity_per_province(per_site: pd.DataFrame) -> pd.DataFrame:
    return (
        per_site.groupby("provinsi")
        .agg(
            jumlah_lokasi=("id_lokasi", "count"),
            rata2_kekayaan_spesies=("kekayaan_spesies", "mean"),
            rata2_shannon=("shannon_h", "mean"),
            total_individu=("total_individu", "sum"),
        )
        .round(2)
        .sort_values("total_individu", ascending=False)
    )


def make_plots(per_site: pd.DataFrame) -> None:
    FIG_TOP_LOKASI.parent.mkdir(parents=True, exist_ok=True)

    top15 = per_site.nlargest(15, "kekayaan_spesies").iloc[::-1]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top15["nama_lokasi"], top15["kekayaan_spesies"], color="#2e7d32")
    ax.set_xlabel("Jumlah spesies (kekayaan spesies)")
    ax.set_title("15 Lokasi Kekayaan Spesies Tertinggi\nAWC Indonesia 2026")
    fig.tight_layout()
    fig.savefig(FIG_TOP_LOKASI, dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.hist(per_site["shannon_h"], bins=20, color="#1565c0", edgecolor="white")
    ax.set_xlabel("Indeks Shannon-Wiener (H')")
    ax.set_ylabel("Jumlah lokasi")
    ax.set_title("Sebaran Indeks Keanekaragaman Shannon-Wiener per Lokasi")
    fig.tight_layout()
    fig.savefig(FIG_SHANNON, dpi=150)
    plt.close(fig)


def main() -> None:
    df = load_verified_counts()
    per_site = diversity_per_site(df)
    per_province = diversity_per_province(per_site)

    OUT_LOKASI.parent.mkdir(parents=True, exist_ok=True)
    per_site.to_csv(OUT_LOKASI, index=False)
    per_province.to_csv(OUT_PROVINSI)
    make_plots(per_site)

    print(f"{len(per_site)} lokasi dianalisis -> {OUT_LOKASI}")
    print(f"Rekap per provinsi -> {OUT_PROVINSI}")
    print(f"Grafik -> {FIG_TOP_LOKASI}, {FIG_SHANNON}")
    print("\nTop 5 lokasi paling beragam:")
    print(per_site[["nama_lokasi", "provinsi", "kekayaan_spesies", "shannon_h"]].head(5).to_string(index=False))


if __name__ == "__main__":
    main()
