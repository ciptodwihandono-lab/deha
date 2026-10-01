"""Analisis kesenjangan status perlindungan: spesies terancam (IUCN) vs
status perlindungan nasional (StaNas) dari data AWC Indonesia 2026.

Silang kolom `IUCN_RedList` (status global) dengan `StaNas` (status
perlindungan hukum Indonesia) untuk menemukan spesies yang sudah
berstatus terancam (EN/VU/CR) secara global tapi BELUM dilindungi
secara hukum nasional -- gap kebijakan yang relevan untuk advokasi
konservasi.

Workflow: data/raw/awc_indonesia_2026/awc_indonesia_2026_anonim.xlsx
-> this script -> data/processed/awc_gap_status_perlindungan.csv
                  outputs/figures/awc_gap_status_perlindungan.png
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "raw" / "awc_indonesia_2026" / "awc_indonesia_2026_anonim.xlsx"
OUT_TABLE = ROOT / "data" / "processed" / "awc_gap_status_perlindungan.csv"
FIG_PATH = ROOT / "outputs" / "figures" / "awc_gap_status_perlindungan.png"

DECISION_VALID = {"OK", "1"}
IUCN_TERANCAM = {"CR", "EN", "VU"}

WARNA_STANAS = {"Protected": "#2e7d32", "Non-protected": "#c62828", "Uniden": "#9e9e9e"}


def load_verified() -> pd.DataFrame:
    df = pd.read_excel(INPUT_PATH, sheet_name="COUNT")
    df = df[df["Decision (OK/1/Parkir)"].isin(DECISION_VALID)].copy()
    df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce").fillna(0)
    return df


def rekap_spesies_terancam(df: pd.DataFrame) -> pd.DataFrame:
    spesies = (
        df.groupby("Nama Ilmiah")
        .agg(
            nama_indonesia=("Nama Indonesia", "first"),
            iucn=("IUCN_RedList", "first"),
            status_perlindungan_nasional=("StaNas", "first"),
            total_individu=("Jumlah", "sum"),
            jumlah_lokasi=("ID Lokasi", "nunique"),
        )
        .reset_index()
        .rename(columns={"Nama Ilmiah": "nama_ilmiah"})
    )
    terancam = spesies[spesies["iucn"].isin(IUCN_TERANCAM)].copy()
    terancam["total_individu"] = terancam["total_individu"].astype(int)
    terancam["gap_perlindungan"] = terancam["status_perlindungan_nasional"] == "Non-protected"
    return terancam.sort_values("total_individu", ascending=False).reset_index(drop=True)


def plot_gap(terancam: pd.DataFrame) -> None:
    df_plot = terancam.sort_values("total_individu").copy()
    colors = df_plot["status_perlindungan_nasional"].map(WARNA_STANAS)

    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.barh(df_plot["nama_indonesia"], df_plot["total_individu"], color=colors)

    for bar, iucn in zip(bars, df_plot["iucn"]):
        ax.text(bar.get_width() * 1.02, bar.get_y() + bar.get_height() / 2, iucn,
                va="center", fontsize=8, fontweight="bold")

    ax.set_xlabel("Total individu (baris terverifikasi, AWC 2026)")
    ax.set_title(
        "Status Perlindungan Nasional vs Status IUCN\n"
        "Spesies Terancam (EN/VU/CR) -- AWC Indonesia 2026",
        fontsize=12,
    )

    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in WARNA_STANAS.values()]
    ax.legend(handles, WARNA_STANAS.keys(), loc="lower right", fontsize=8,
              title="Status perlindungan nasional")

    fig.tight_layout()
    FIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_PATH, dpi=160)
    plt.close(fig)


def main() -> None:
    df = load_verified()
    terancam = rekap_spesies_terancam(df)

    OUT_TABLE.parent.mkdir(parents=True, exist_ok=True)
    terancam.to_csv(OUT_TABLE, index=False)
    plot_gap(terancam)

    gap = terancam[terancam["gap_perlindungan"]]
    print(f"{len(terancam)} spesies berstatus IUCN terancam (EN/VU/CR) -> {OUT_TABLE}")
    print(f"Grafik -> {FIG_PATH}")
    print(f"\n{len(gap)} dari {len(terancam)} spesies terancam BELUM dilindungi secara nasional:")
    print(gap[["nama_indonesia", "nama_ilmiah", "iucn", "total_individu", "jumlah_lokasi"]].to_string(index=False))


if __name__ == "__main__":
    main()
