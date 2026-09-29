# Ringkasan Analisis Statistik: Burung Pantai Bermigrasi Indonesia

Tiga pendekatan diterapkan sesuai karakteristik masing-masing dataset:
snapshot satu tahun (AWC 2026) dianalisis sebagai data komunitas, data
historis 36 tahun (IWC) dianalisis sebagai tren, dan spesies prioritas
dianalisis terpisah dari data agregat.

## 1. Analisis komunitas -- AWC Indonesia 2026

Script: `scripts/python/analisis_diversitas_awc.py`

- **113 lokasi** dianalisis (baris berkeputusan OK/1 saja, PARKIR dikeluarkan)
- Lokasi paling beragam: **Ecotourism Mangroves Wonorejo** (Jawa Timur,
  57 spesies), **Lahan Basah Lanrae** (Sulawesi Barat, 49 spesies),
  **Dusun Bondan, Segara Anakan** (Jawa Tengah, 48 spesies)
- Provinsi dengan total individu tertinggi: **Sumatra Utara** (17.970
  individu dari 3 lokasi), **Jawa Tengah** (13.761 dari 13 lokasi)
- Sebaran indeks Shannon-Wiener terpusat di 1.8-2.2 (keanekaragaman
  sedang-tinggi di sebagian besar lokasi)

Tabel lengkap: `data/processed/awc_diversitas_per_lokasi.csv`,
`data/processed/awc_diversitas_per_provinsi.csv`
Grafik: `outputs/figures/awc_top_lokasi_kekayaan_spesies.png`,
`outputs/figures/awc_sebaran_shannon.png`

## 2. Analisis tren -- IWC Indonesia 1989-2025

Script: `scripts/python/analisis_tren_iwc.py`

Regresi log-linear pada **rata-rata individu per lokasi per tahun**
(bukan total mentah -- lihat catatan metodologis di scriptnya soal
kenapa ini penting).

| Spesies | Tren/tahun | p-value | Signifikan? | Cakupan lokasi/tahun |
| --- | --- | --- | --- | --- |
| Nordmann's Greenshank | -0.5% | 0.95 | Tidak | 1-2 |
| Far Eastern Curlew | **-2.6%** | 0.28 | Tidak | 1-15 |
| Great Knot | +2.2% | 0.58 | Tidak | 1-9 |

**Tidak ada yang signifikan secara statistik** -- ini bukan berarti tidak
ada perubahan populasi nyata, tapi mencerminkan data nasional yang
jarang dan cakupan lokasi yang sangat tidak konsisten antar tahun (lihat
kolom cakupan). Ketidaksignifikanan = kurang bukti, bukan bukti "tidak
ada perubahan".

**Temuan penting**: arah tren Far Eastern Curlew (menurun) **konsisten**
dengan studi situs-spesifik di Banyuasin Peninsula yang mencatat
penurunan ~62% (2008-2019, lihat
`docs/referensi_burung_pantai_dan_kehati_indonesia.md`) -- data nasional
yang lebih jarang tidak bisa mendeteksinya secara signifikan, tapi
arahnya sejalan.

Tabel: `data/processed/tren_spesies_prioritas.csv`
Grafik: `outputs/figures/tren_tringa_guttifer.png`,
`outputs/figures/tren_numenius_madagascariensis.png`,
`outputs/figures/tren_calidris_tenuirostris.png`

## 3. Keterbatasan yang perlu diingat

- **Bukan model TRIM resmi** -- untuk publikasi ilmiah/laporan resmi,
  gunakan software TRIM atau paket R `rtrim` yang menangani data hilang
  lewat imputasi multiplikatif.
- **Data spesies prioritas sangat jarang** (6-76 lokasi unik sepanjang
  36 tahun, banyak tahun cuma 1 lokasi) -- kekuatan statistik rendah.
- **Tren nasional agregat bisa menyembunyikan tren lokal** yang berbeda
  arah atau lebih kuat -- selalu silang-cek dengan studi situs-spesifik.
- Satu titik data ekstrem (Far Eastern Curlew, Muara Sungai Banyuasin,
  1989, 1.103 individu dari 1 lokasi) berpengaruh besar pada model
  karena datanya sedikit -- ini bukan kesalahan data (situs itu memang
  situs terpenting untuk spesies ini), tapi menunjukkan rapuhnya model
  dengan data sesedikit ini.

## Cara reproduksi

```bash
python3 scripts/python/analisis_diversitas_awc.py
python3 scripts/python/analisis_tren_iwc.py
```

Dependency tambahan: `pip install statsmodels scipy`
