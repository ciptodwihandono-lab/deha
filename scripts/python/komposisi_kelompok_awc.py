"""Komposisi kelompok (taksonomi) burung air per provinsi dari data AWC
Indonesia 2026 -- proporsi total individu per kelompok (mis. "Burung
Pantai (Cerek)", "Kuntul & Cangak", dll) untuk melihat karakter habitat
tiap provinsi.

Kelompok dengan proporsi nasional kecil (<2% total individu) digabung
jadi "Lainnya" supaya grafik tetap terbaca.

Workflow: data/raw/awc_indonesia_2026/awc_indonesia_2026_anonim.xlsx
-> this script -> data/processed/awc_komposisi_kelompok_provinsi.csv
                  outputs/figures/awc_komposisi_kelompok_provinsi.png
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "raw" / "awc_indonesia_2026" / "awc_indonesia_2026_anonim.xlsx"
OUT_TABLE = ROOT / "data" / "processed" / "awc_komposisi_kelompok_provinsi.csv"
FIG_PATH = ROOT / "outputs" / "figures" / "awc_komposisi_kelompok_provinsi.png"

DECISION_VALID = {"OK", "1"}
AMBANG_LAINNYA = 0.02  # kelompok di bawah 2% total individu nasional digabung jadi "Lainnya"

NORMALISASI_PROVINSI = {
    "DKI_Jakarta": "DKI Jakarta", "DKI Jakarta": "DKI Jakarta",
    "DI_Yogyakarta": "DI Yogyakarta",
    "Jawa_Barat": "Jawa Barat", "Jawa_Tengah": "Jawa Tengah", "Jawa_Timur": "Jawa Timur",
    "Kalimantan_Barat": "Kalimantan Barat", "Kalimantan_Tengah": "Kalimantan Tengah",
    "Kalimantan_Timur": "Kalimantan Timur", "Kalimantan_Utara": "Kalimantan Utara",
    "Kepulauan_Riau": "Kepulauan Riau", "Maluku_Utara": "Maluku Utara",
    "Nusa_Tenggara_Barat": "Nusa Tenggara Barat", "Nusa_Tenggara_Timur": "Nusa Tenggara Timur",
    "Papua_Selatan": "Papua Selatan", "Sulawesi_Barat": "Sulawesi Barat",
    "Sulawesi_Selatan": "Sulawesi Selatan", "Sulawesi_Tengah": "Sulawesi Tengah",
    "Sumatra_Barat": "Sumatera Barat", "Sumatra_Selatan": "Sumatera Selatan",
    "Sumatra_Utara": "Sumatera Utara",
}


def load_verified() -> pd.DataFrame:
    df = pd.read_excel(INPUT_PATH, sheet_name="COUNT")
    df = df[df["Decision (OK/1/Parkir)"].isin(DECISION_VALID)].copy()
    df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce").fillna(0)
    df["provinsi"] = df["Provinsi"].map(NORMALISASI_PROVINSI).fillna(df["Provinsi"])
    return df


def gabung_kelompok_kecil(df: pd.DataFrame) -> pd.DataFrame:
    total_per_kelompok = df.groupby("Kelompok")["Jumlah"].sum()
    proporsi_nasional = total_per_kelompok / total_per_kelompok.sum()
    kelompok_kecil = proporsi_nasional[proporsi_nasional < AMBANG_LAINNYA].index

    df = df.copy()
    df["kelompok_tampil"] = df["Kelompok"].where(~df["Kelompok"].isin(kelompok_kecil), "Lainnya")
    return df


def build_komposisi(df: pd.DataFrame) -> pd.DataFrame:
    pivot = df.pivot_table(
        index="provinsi", columns="kelompok_tampil", values="Jumlah", aggfunc="sum", fill_value=0
    )
    proporsi = pivot.div(pivot.sum(axis=1), axis=0)
    # Urutkan provinsi berdasarkan total individu (terbanyak di atas)
    urutan = pivot.sum(axis=1).sort_values(ascending=False).index
    return proporsi.loc[urutan]


def plot_komposisi(proporsi: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(11, 10))
    cmap = plt.colormaps["tab20"]
    colors = [cmap(i / len(proporsi.columns)) for i in range(len(proporsi.columns))]

    proporsi.iloc[::-1].plot(kind="barh", stacked=True, ax=ax, color=colors, width=0.8)

    ax.set_xlabel("Proporsi total individu")
    ax.set_xlim(0, 1)
    ax.set_title(
        "Komposisi Kelompok Burung Air per Provinsi -- AWC Indonesia 2026\n"
        "(diurutkan dari provinsi dengan total individu terbanyak)",
        fontsize=12,
    )
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.06), ncol=3, fontsize=7.5, title="Kelompok")

    fig.tight_layout()
    FIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_PATH, dpi=160, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    df = load_verified()
    df = gabung_kelompok_kecil(df)
    proporsi = build_komposisi(df)

    OUT_TABLE.parent.mkdir(parents=True, exist_ok=True)
    proporsi.to_csv(OUT_TABLE)
    plot_komposisi(proporsi)

    print(f"Komposisi {len(proporsi.columns)} kelompok x {len(proporsi)} provinsi -> {OUT_TABLE}")
    print(f"Grafik -> {FIG_PATH}")
    print("\nKelompok dominan secara nasional (rata-rata proporsi lintas provinsi):")
    print(proporsi.mean().sort_values(ascending=False).round(3).to_string())


if __name__ == "__main__":
    main()
