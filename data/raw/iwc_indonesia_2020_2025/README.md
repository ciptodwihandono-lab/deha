# Ekspor IWC (International Waterbird Census) Indonesia

Data ekspor dari database global **International Waterbird Census (IWC)**
yang dikoordinasikan Wetlands International — AWC (Asian Waterbird
Census) adalah bagian regional dari program ini untuk Asia.

File: `iwc-export_2020-2025.csv`

## Cakupan

- **22.170 baris** data hitungan burung air
- **1.056 lokasi** unik di Indonesia (`sitecode`/`sitename`)
- **517 spesies** unik
- Rentang tahun: **1989–2025** (meski nama file fokus 2020-2025, data
  historis lebih lama ikut terekspor)
- Lokasi disurvei per tahun (5 tahun terakhir): 2020 = 124, 2021 = 213,
  2022 = 180, 2023 = 173, 2024 = 82, 2025 = 97

## Kolom

| Kolom | Keterangan |
| --- | --- |
| `sitecode`, `sitename` | kode & nama lokasi survei |
| `day`, `month`, `year` | tanggal survei |
| `speciescode`, `speciesname` | kode & nama ilmiah spesies |
| `count` | jumlah individu tercatat |
| `count_type` | tipe hitungan (mis. `W` = whole count) |
| `coverage`, `quality`, `method` | metadata metodologi survei |
| `water`, `ice`, `tidal`, `weather` | kondisi lingkungan saat survei |
| `disturbed` | ada tidaknya gangguan saat survei |
| `participants` | **nama pengamat/relawan** yang ikut survei |
| `outlier`, `site_redundant` | penanda kualitas data |

## Catatan penting — data pribadi

Kolom **`participants`** berisi **748 nama asli individu** pengamat di
seluruh Indonesia yang berpartisipasi dalam sensus 1989–2025. Ini data
pribadi (nama orang), mirip situasi dengan
`data/raw/awc_indonesia_2026/` — file CSV aslinya **sengaja tidak
otomatis di-commit** ke git melalui proses otomatis, menunggu keputusan
pemilik repo soal cara terbaik menanganinya (commit manual apa adanya,
atau buat versi tanpa kolom `participants` untuk versi publik/analisis).

## Relevansi untuk proyek

Data ini jauh lebih kaya dari sekadar AWC 2026 — mencakup histori multi-
tahun yang bisa dipakai untuk analisis **tren populasi** per spesies/
lokasi (bukan cuma snapshot satu tahun), sangat relevan untuk proyek
pemetaan sebaran burung pantai bermigrasi seluruh Indonesia. Lihat juga
`docs/referensi_burung_pantai_dan_kehati_indonesia.md` untuk konteks
situs-situs penting (Berbak-Sembilang, Wasur, Banyuasin, Pantai Cemara)
yang bisa dicocokkan dengan `sitecode`/`sitename` di data ini.
