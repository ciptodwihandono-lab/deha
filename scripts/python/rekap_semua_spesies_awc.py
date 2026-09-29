"""Rekap SEMUA jenis (spesies) dari data AWC Indonesia 2026 -- bukan cuma
3 spesies prioritas seperti di analisis_tren_iwc.py.

Hanya baris berkeputusan verifikasi "OK"/"1" yang dipakai (PARKIR
dikeluarkan), sama seperti analisis_diversitas_awc.py.

Workflow: data/raw/awc_indonesia_2026/awc_indonesia_2026_anonim.xlsx
-> this script -> data/processed/awc_rekap_semua_spesies.csv (tabel lengkap semua jenis)
                  outputs/figures/awc_top40_spesies_individu.png
                  outputs/figures/awc_sebaran_jumlah_individu_semua_spesies.png
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "raw" / "awc_indonesia_2026" / "awc_indonesia_2026_anonim.xlsx"
OUT_TABLE = ROOT / "data" / "processed" / "awc_rekap_semua_spesies.csv"
FIG_TOP40 = ROOT / "outputs" / "figures" / "awc_top40_spesies_individu.png"
FIG_HIST = ROOT / "outputs" / "figures" / "awc_sebaran_jumlah_individu_semua_spesies.png"

DECISION_VALID = {"OK", "1"}

WARNA_IUCN = {
    "CR": "#7b0000",
    "EN": "#d32f2f",
    "VU": "#f57c00",
    "NT": "#fbc02d",
    "LC": "#2e7d32",
    "NE": "#9e9e9e",
    "DD": "#9e9e9e",
}


def load_verified(path: Path = INPUT_PATH) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="COUNT")
    df = df[df["Decision (OK/1/Parkir)"].isin(DECISION_VALID)].copy()
    df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce").fillna(0)
    return df


def rekap_semua_spesies(df: pd.DataFrame) -> pd.DataFrame:
    rekap = (
        df.groupby("Nama Ilmiah")
        .agg(
            nama_indonesia=("Nama Indonesia", "first"),
            nama_inggris=("English_Name_AviList", "first"),
            famili=("Family", "first"),
            kelompok=("Kelompok", "first"),
            iucn=("IUCN_RedList", "first"),
            status_nasional=("StaNas", "first"),
            total_individu=("Jumlah", "sum"),
            jumlah_lokasi=("ID Lokasi", "nunique"),
        )
        .reset_index()
        .rename(columns={"Nama Ilmiah": "nama_ilmiah"})
    )
    rekap["total_individu"] = rekap["total_individu"].astype(int)
    return rekap.sort_values("total_individu", ascending=False).reset_index(drop=True)


def plot_top40(rekap: pd.DataFrame) -> None:
    top40 = rekap.nlargest(40, "total_individu").iloc[::-1]
    colors = [WARNA_IUCN.get(iucn, "#9e9e9e") for iucn in top40["iucn"]]

    fig, ax = plt.subplots(figsize=(10, 12))
    ax.barh(top40["nama_indonesia"], top40["total_individu"], color=colors)
    ax.set_xlabel("Total individu (baris terverifikasi OK/1)")
    ax.set_title("40 Spesies dengan Total Individu Tertinggi\nAWC Indonesia 2026", fontsize=12)

    handles = [
        plt.Rectangle((0, 0), 1, 1, color=c)
        for c in ["#d32f2f", "#f57c00", "#fbc02d", "#2e7d32", "#9e9e9e"]
    ]
    ax.legend(handles, ["Endangered/CR", "Vulnerable", "Near Threatened", "Least Concern", "NE/DD"],
              loc="lower right", fontsize=8, title="Status IUCN")

    fig.tight_layout()
    FIG_TOP40.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_TOP40, dpi=150)
    plt.close(fig)


def plot_histogram(rekap: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(rekap["total_individu"], bins=40, color="#1565c0", edgecolor="white")
    ax.set_yscale("log")
    ax.set_xlabel("Total individu per spesies")
    ax.set_ylabel("Jumlah spesies (skala log)")
    ax.set_title(f"Sebaran Total Individu di Semua {len(rekap)} Spesies -- AWC Indonesia 2026")
    fig.tight_layout()
    fig.savefig(FIG_HIST, dpi=150)
    plt.close(fig)


def main() -> None:
    df = load_verified()
    rekap = rekap_semua_spesies(df)

    OUT_TABLE.parent.mkdir(parents=True, exist_ok=True)
    rekap.to_csv(OUT_TABLE, index=False)
    plot_top40(rekap)
    plot_histogram(rekap)

    print(f"{len(rekap)} spesies direkap -> {OUT_TABLE}")
    print(f"Grafik top 40 -> {FIG_TOP40}")
    print(f"Grafik sebaran semua spesies -> {FIG_HIST}")
    print("\nSpesies terancam punah (EN/CR) yang tercatat:")
    print(rekap[rekap["iucn"].isin(["EN", "CR"])][["nama_indonesia", "nama_ilmiah", "iucn", "total_individu", "jumlah_lokasi"]].to_string(index=False))


if __name__ == "__main__":
    main()
