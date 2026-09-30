"""Analisis kesenjangan (gap) cakupan survei AWC Indonesia 2026 per provinsi.

Tindak lanjut rekomendasi #3 di docs/laporan_sintesis_burung_pantai_awc.md
("Perluas cakupan survei ke provinsi dengan data minim"). Script ini
membandingkan provinsi yang punya lokasi survei AWC 2026 terverifikasi
dengan daftar 38 provinsi resmi Indonesia (pasca pemekaran Papua 2022),
lalu memberi prioritas berdasarkan ada/tidaknya situs penting yang sudah
terdokumentasi di docs/referensi_burung_pantai_dan_kehati_indonesia.md
(situs Ramsar, EAAFP Flyway Network Site, IBA).

Workflow: data/raw/awc_indonesia_2026/awc_indonesia_2026_anonim.xlsx
-> this script -> data/processed/awc_gap_survei_provinsi.csv
                  outputs/figures/awc_gap_survei_provinsi.png
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "raw" / "awc_indonesia_2026" / "awc_indonesia_2026_anonim.xlsx"
OUT_TABLE = ROOT / "data" / "processed" / "awc_gap_survei_provinsi.csv"
FIG_PATH = ROOT / "outputs" / "figures" / "awc_gap_survei_provinsi.png"

DECISION_VALID = {"OK", "1"}

# 38 provinsi resmi Indonesia (pasca pemekaran Papua 2022 & pembentukan
# Kalimantan Utara 2012), dikelompokkan per pulau untuk keterbacaan.
PROVINSI_RESMI = {
    "Aceh": "Sumatera", "Sumatera Utara": "Sumatera", "Sumatera Barat": "Sumatera",
    "Riau": "Sumatera", "Kepulauan Riau": "Sumatera", "Jambi": "Sumatera",
    "Sumatera Selatan": "Sumatera", "Kepulauan Bangka Belitung": "Sumatera",
    "Bengkulu": "Sumatera", "Lampung": "Sumatera",
    "DKI Jakarta": "Jawa-Bali", "Jawa Barat": "Jawa-Bali", "Jawa Tengah": "Jawa-Bali",
    "DI Yogyakarta": "Jawa-Bali", "Jawa Timur": "Jawa-Bali", "Banten": "Jawa-Bali",
    "Bali": "Jawa-Bali",
    "Nusa Tenggara Barat": "Nusa Tenggara", "Nusa Tenggara Timur": "Nusa Tenggara",
    "Kalimantan Barat": "Kalimantan", "Kalimantan Tengah": "Kalimantan",
    "Kalimantan Selatan": "Kalimantan", "Kalimantan Timur": "Kalimantan",
    "Kalimantan Utara": "Kalimantan",
    "Sulawesi Utara": "Sulawesi", "Sulawesi Tengah": "Sulawesi",
    "Sulawesi Selatan": "Sulawesi", "Sulawesi Tenggara": "Sulawesi",
    "Gorontalo": "Sulawesi", "Sulawesi Barat": "Sulawesi",
    "Maluku": "Maluku-Papua", "Maluku Utara": "Maluku-Papua",
    "Papua": "Maluku-Papua", "Papua Barat": "Maluku-Papua",
    "Papua Selatan": "Maluku-Papua", "Papua Tengah": "Maluku-Papua",
    "Papua Pegunungan": "Maluku-Papua", "Papua Barat Daya": "Maluku-Papua",
}

# Nama provinsi di kolom "Provinsi" data AWC (underscore/spasi tidak
# konsisten) -> nama resmi di PROVINSI_RESMI.
NORMALISASI_NAMA = {
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

# Situs penting yang SUDAH terdokumentasi dengan sumber di
# docs/referensi_burung_pantai_dan_kehati_indonesia.md, dipetakan ke
# provinsi resmi tempatnya berada. Dipakai untuk menandai gap yang
# paling mendesak (provinsi tanpa data AWC tapi punya situs penting).
SITUS_PENTING = {
    "Sulawesi Tenggara": "TN Rawa Aopa Watumohai (situs Ramsar)",
    "Jambi": "TN Berbak-Sembilang & Pantai Cemara (EAAFP Flyway Network Site / KEE)",
    "Sumatera Selatan": "TN Berbak-Sembilang & Semenanjung Banyuasin (EAAFP Flyway Network Site)",
    "Papua Selatan": "TN Wasur (EAAFP Flyway Network Site, situs Ramsar)",
    "Kalimantan Barat": "Danau Sentarum (situs Ramsar)",
    "Kalimantan Tengah": "Tanjung Puting (situs Ramsar)",
    "DKI Jakarta": "Suaka Margasatwa Pulau Rambut (situs Ramsar)",
    "Aceh": "Pesisir timur Aceh Besar & Banda Aceh (IBA sejak 2001)",
    "Sumatera Utara": "Pesisir timur Sumatera Utara (IBA sejak 2001)",
}


def load_jumlah_lokasi_per_provinsi() -> dict:
    df = pd.read_excel(INPUT_PATH, sheet_name="COUNT")
    df = df[df["Decision (OK/1/Parkir)"].isin(DECISION_VALID)].copy()
    df["provinsi_resmi"] = df["Provinsi"].map(NORMALISASI_NAMA).fillna(df["Provinsi"])
    return df.groupby("provinsi_resmi")["ID Lokasi"].nunique().to_dict()


def klasifikasi_prioritas(jumlah_lokasi: int, punya_situs_penting: bool) -> str:
    if jumlah_lokasi == 0:
        return "Tinggi (situs penting, 0 data)" if punya_situs_penting else "Sedang (0 data)"
    if jumlah_lokasi <= 2:
        return "Sedang (data minim)"
    return "Rendah (cakupan cukup)"


def build_gap_table() -> pd.DataFrame:
    jumlah_per_provinsi = load_jumlah_lokasi_per_provinsi()

    rows = []
    for provinsi, pulau in PROVINSI_RESMI.items():
        jumlah_lokasi = jumlah_per_provinsi.get(provinsi, 0)
        situs = SITUS_PENTING.get(provinsi, "")
        rows.append(
            {
                "provinsi": provinsi,
                "wilayah": pulau,
                "jumlah_lokasi_awc_2026": jumlah_lokasi,
                "situs_penting_terdokumentasi": situs,
                "prioritas_survei_lanjutan": klasifikasi_prioritas(jumlah_lokasi, bool(situs)),
            }
        )

    urutan_prioritas = {
        "Tinggi (situs penting, 0 data)": 0,
        "Sedang (0 data)": 1,
        "Sedang (data minim)": 1,
        "Rendah (cakupan cukup)": 2,
    }
    df = pd.DataFrame(rows)
    df["_urutan"] = df["prioritas_survei_lanjutan"].map(urutan_prioritas)
    df = df.sort_values(["_urutan", "jumlah_lokasi_awc_2026"]).drop(columns="_urutan")
    return df.reset_index(drop=True)


def plot_gap(df: pd.DataFrame) -> None:
    warna = {
        "Tinggi (situs penting, 0 data)": "#b71c1c",
        "Sedang (0 data)": "#f57c00",
        "Sedang (data minim)": "#fbc02d",
        "Rendah (cakupan cukup)": "#2e7d32",
    }
    colors = df["prioritas_survei_lanjutan"].map(warna)

    fig, ax = plt.subplots(figsize=(9, 11))
    ax.barh(df["provinsi"], df["jumlah_lokasi_awc_2026"], color=colors)
    ax.set_xlabel("Jumlah lokasi survei AWC 2026 (baris terverifikasi)")
    ax.set_title(
        "Kesenjangan Cakupan Survei AWC 2026 per Provinsi\n"
        "(38 provinsi resmi Indonesia)",
        fontsize=12,
    )

    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in warna.values()]
    ax.legend(handles, warna.keys(), loc="lower right", fontsize=8, title="Prioritas survei lanjutan")

    fig.tight_layout()
    FIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_PATH, dpi=160)
    plt.close(fig)


def main() -> None:
    df = build_gap_table()

    OUT_TABLE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_TABLE, index=False)
    plot_gap(df)

    n_zero = (df["jumlah_lokasi_awc_2026"] == 0).sum()
    n_tinggi = (df["prioritas_survei_lanjutan"] == "Tinggi (situs penting, 0 data)").sum()

    print(f"{len(df)} provinsi dianalisis -> {OUT_TABLE}")
    print(f"Grafik -> {FIG_PATH}")
    print(f"\n{n_zero} dari 38 provinsi TIDAK punya data lokasi AWC 2026 sama sekali.")
    print(f"{n_tinggi} provinsi berprioritas TINGGI (0 data + situs penting terdokumentasi):")
    print(
        df[df["prioritas_survei_lanjutan"] == "Tinggi (situs penting, 0 data)"][
            ["provinsi", "situs_penting_terdokumentasi"]
        ].to_string(index=False)
    )
    print("\nProvinsi tanpa data sama sekali (prioritas sedang, belum ada situs terdokumentasi di proyek ini):")
    print(
        df[df["prioritas_survei_lanjutan"] == "Sedang (0 data)"]["provinsi"].to_string(index=False)
    )


if __name__ == "__main__":
    main()
