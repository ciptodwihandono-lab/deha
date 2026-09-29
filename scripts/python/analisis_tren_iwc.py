"""Analisis tren populasi spesies prioritas dari data IWC Indonesia 1989-2025.

Beda dengan AWC 2026 (snapshot), data IWC ini multi-tahun sehingga bisa
dipakai untuk melihat **tren populasi** antar tahun -- pendekatan yang
dipakai di sini: regresi log-linear pada rata-rata individu per lokasi
per tahun (bukan total mentah, lihat catatan di bawah).

CATATAN METODOLOGIS -- PENTING:
1. Ini bukan model TRIM penuh (yang dipakai Wetlands International secara
   resmi untuk estimasi populasi flyway). TRIM menangani lokasi yang
   tidak disurvei tiap tahun lewat imputasi multiplikatif. Untuk angka
   resmi/publikasi ilmiah, pakai software TRIM asli atau paket R `rtrim`.
2. Jumlah lokasi yang disurvei sangat tidak konsisten antar tahun (mis.
   data Far Eastern Curlew: 1 lokasi di 1989 vs 15 lokasi di 2023) --
   regresi pada TOTAL individu mentah akan bias berat oleh cakupan survei,
   bukan perubahan populasi asli. Karena itu skrip ini memakai RATA-RATA
   individu per lokasi yang disurvei sebagai indeks utama, yang jauh
   lebih tahan (walau tidak sepenuhnya bebas) dari bias tersebut.
3. Hasil dari pendekatan sederhana ini bisa BERBEDA dari studi lokal yang
   lebih rinci (mis. Banyuasin Peninsula mencatat penurunan populasi Far
   Eastern Curlew ~62% 2008-2019 -- lihat
   docs/referensi_burung_pantai_dan_kehati_indonesia.md) karena data
   nasional yang diagregasi bisa menyembunyikan tren lokal yang berbeda
   arah. Selalu bandingkan dengan literatur situs-spesifik.

Workflow: data/raw/iwc_indonesia_2020_2025/iwc_indonesia_2020_2025_anonim.csv
-> this script -> data/processed/tren_spesies_prioritas.csv
                  outputs/figures/tren_<spesies>.png
"""

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "raw" / "iwc_indonesia_2020_2025" / "iwc_indonesia_2020_2025_anonim.csv"
OUT_TABLE = ROOT / "data" / "processed" / "tren_spesies_prioritas.csv"
FIG_DIR = ROOT / "outputs" / "figures"

# Spesies prioritas: status IUCN Endangered, tercatat di data IWC Indonesia
# (lihat docs/referensi_burung_pantai_dan_kehati_indonesia.md).
SPESIES_PRIORITAS = {
    "Tringa guttifer": "Nordmann's Greenshank",
    "Numenius madagascariensis": "Far Eastern Curlew",
    "Calidris tenuirostris": "Great Knot",
}

MIN_TAHUN_UNTUK_TREN = 5


def build_yearly_index(df: pd.DataFrame, species: str) -> pd.DataFrame:
    sub = df[df["speciesname"] == species]
    # maksimum per lokasi per tahun (hindari hitung ganda kalau ada >1 kunjungan)
    per_site_year = sub.groupby(["sitecode", "year"])["count"].max().reset_index()
    yearly = (
        per_site_year.groupby("year")
        .agg(
            total_individu=("count", "sum"),
            jumlah_lokasi=("sitecode", "nunique"),
            rata2_per_lokasi=("count", "mean"),
        )
        .reset_index()
    )
    yearly["rata2_per_lokasi"] = yearly["rata2_per_lokasi"].round(2)
    return yearly.sort_values("year").reset_index(drop=True)


def fit_trend(yearly: pd.DataFrame) -> tuple[dict, pd.Series]:
    # Regresi log-linear (OLS pada log rata2_per_lokasi) -- pendekatan
    # standar untuk indeks kelimpahan kontinu, lihat catatan metodologis.
    model = smf.ols("np.log(rata2_per_lokasi) ~ year", data=yearly).fit()
    coef = model.params["year"]
    pvalue = model.pvalues["year"]
    annual_growth_pct = (math.exp(coef) - 1) * 100
    fitted_original_scale = model.fittedvalues.apply(math.exp)
    result = {
        "koefisien_tahun": coef,
        "p_value": pvalue,
        "laju_perubahan_tahunan_persen": round(annual_growth_pct, 2),
        "signifikan_p<0.05": pvalue < 0.05,
    }
    return result, fitted_original_scale


def plot_trend(species: str, label: str, yearly: pd.DataFrame, fit: dict, fitted: pd.Series) -> Path:
    fig, ax = plt.subplots(figsize=(8, 5))
    x = yearly["year"]
    ax.bar(x, yearly["rata2_per_lokasi"], color="#1565c0", alpha=0.7, label="Rata-rata individu / lokasi (indeks tahunan)")
    ax.plot(x, fitted, color="#c62828", linewidth=2, label="Tren regresi log-linear")

    arah = "naik" if fit["koefisien_tahun"] > 0 else "turun"
    sig = "signifikan (p<0.05)" if fit["signifikan_p<0.05"] else "tidak signifikan"
    ax.set_title(
        f"{label} ({species})\nTren indikatif: {fit['laju_perubahan_tahunan_persen']:+.1f}%/tahun, {arah}, {sig}",
        fontsize=11,
    )
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Rata-rata individu per lokasi disurvei")
    ax.legend(loc="upper left", fontsize=8)

    ax2 = ax.twinx()
    ax2.plot(x, yearly["jumlah_lokasi"], color="gray", linestyle="--", marker="o", markersize=3, alpha=0.6)
    ax2.set_ylabel("Jumlah lokasi disurvei (garis putus-putus)", color="gray", fontsize=8)

    fig.tight_layout()
    slug = species.lower().replace(" ", "_").replace("'", "")
    fig_path = FIG_DIR / f"tren_{slug}.png"
    fig.savefig(fig_path, dpi=150)
    plt.close(fig)
    return fig_path


def main() -> None:
    df = pd.read_csv(INPUT_PATH)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    for species, label in SPESIES_PRIORITAS.items():
        yearly = build_yearly_index(df, species)
        if len(yearly) < MIN_TAHUN_UNTUK_TREN:
            print(f"{label} ({species}): cuma {len(yearly)} tahun data -- dilewati (data terlalu sedikit untuk tren)")
            continue

        fit, fitted = fit_trend(yearly)
        fig_path = plot_trend(species, label, yearly, fit, fitted)

        results.append(
            {
                "spesies": species,
                "nama_umum": label,
                "jumlah_tahun_data": len(yearly),
                "rentang_tahun": f"{yearly['year'].min()}-{yearly['year'].max()}",
                "total_lokasi_unik": df[df["speciesname"] == species]["sitecode"].nunique(),
                "min_max_lokasi_per_tahun": f"{yearly['jumlah_lokasi'].min()}-{yearly['jumlah_lokasi'].max()}",
                "laju_perubahan_tahunan_persen": fit["laju_perubahan_tahunan_persen"],
                "p_value": round(fit["p_value"], 4),
                "signifikan": fit["signifikan_p<0.05"],
                "grafik": str(fig_path.relative_to(ROOT)),
            }
        )
        print(
            f"{label}: {fit['laju_perubahan_tahunan_persen']:+.1f}%/tahun "
            f"(p={fit['p_value']:.4f}, {yearly['jumlah_lokasi'].min()}-{yearly['jumlah_lokasi'].max()} lokasi/tahun) "
            f"-> {fig_path.name}"
        )

    if results:
        OUT_TABLE.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(results).to_csv(OUT_TABLE, index=False)
        print(f"\nTabel ringkasan -> {OUT_TABLE}")


if __name__ == "__main__":
    main()
