# Laporan Sintesis: Sebaran dan Status Burung Pantai Bermigrasi di Indonesia

*Disusun dari data AWC (Asian Waterbird Census) Indonesia 2026 dan IWC
(International Waterbird Census) 1989-2025, sebagai bagian dari proyek
pemetaan sebaran burung pantai bermigrasi seluruh Indonesia.*

## 1. Ringkasan Eksekutif

- **113 lokasi survei** tersebar di **26 provinsi** berhasil diverifikasi
  dari sensus AWC Indonesia 2026, mencatat **235 jenis** burung air (baris
  berkeputusan verifikasi "OK"/"1").
- Lokasi dengan kekayaan spesies tertinggi: **Ecotourism Mangroves
  Wonorejo, Jawa Timur** (57 spesies), diikuti **Lahan Basah Lanrae,
  Sulawesi Barat** (49 spesies).
- **6 spesies berstatus Endangered/Critically Endangered (IUCN)**
  tercatat, termasuk Kedidi Besar (*Calidris tenuirostris*), Gajahan
  Timur (*Numenius madagascariensis*), dan Trinil Nordmann (*Tringa
  guttifer*) — tiga spesies flyway prioritas EAAF.
- Analisis tren jangka panjang (data IWC 1989-2025) menunjukkan **Gajahan
  Timur menurun ~2,6%/tahun** (arah konsisten dengan laporan penurunan
  62% di Semenanjung Banyuasin), meski belum signifikan secara statistik
  nasional (p=0,28).
- Peta grid resmi (100km x 100km, proyeksi Albers Equal-Area)
  menunjukkan konsentrasi intensitas survei tertinggi di **Kalimantan
  Barat, DKI Jakarta, dan Jawa Tengah/Jawa Timur**.
- **Kota Administrasi Jakarta Utara** dan **Kabupaten Kapuas Hulu**
  adalah kabupaten/kota dengan kekayaan spesies tergabung tertinggi
  (69 dan 51 spesies).

## 2. Latar Belakang & Tujuan

Indonesia berada di jalur terbang Asia Timur-Australasia (East
Asian-Australasian Flyway/EAAF), rute migrasi bagi jutaan burung pantai
setiap tahun. Proyek ini disusun untuk memetakan sebaran, kekayaan
spesies, dan status konservasi burung pantai bermigrasi di seluruh
Indonesia, sebagai dukungan data untuk upaya konservasi KEHATI
(keanekaragaman hayati) nasional. Latar belakang ilmiah lengkap (jalur
EAAF, situs kunci, status spesies prioritas) ada di
`docs/referensi_burung_pantai_dan_kehati_indonesia.md`.

## 3. Sumber Data

| Dataset | Cakupan | Jumlah baris (setelah verifikasi) | Catatan |
| --- | --- | --- | --- |
| AWC Indonesia 2026 | Sensus tahunan, sebagian besar tahun 2026 (2.587 dari 2.655 baris; sisanya baris 2025/2023 adalah entri susulan) | 2.587 baris terverifikasi ("OK"/"1"), 113 lokasi, 235 spesies | Snapshot satu musim sensus, bukan seri waktu |
| IWC 1989-2025 | Historis nasional | 22.170 baris, 1.056 lokasi, 517 spesies, 1989-2025 | Dipakai khusus untuk analisis **tren** karena mencakup banyak tahun |

Kedua file sumber asli mengandung data pribadi kontributor/pengamat
(nama, email, no. HP) sehingga **tidak dapat di-commit ke git** — hanya
versi anonim (`*_anonim.xlsx` / `*_anonim.csv`) yang tersimpan di repo
ini. Detail di README masing-masing folder (`data/raw/awc_indonesia_2026/`,
`data/raw/iwc_indonesia_2020_2025/`).

**Kenapa tren populasi pakai IWC, bukan AWC**: AWC 2026 pada dasarnya
adalah potret satu musim sensus (2.587 dari 2.655 baris adalah tahun
2026) sehingga tidak bisa dipakai sendirian untuk menghitung tren
antar-tahun — perlu minimal beberapa tahun data untuk melihat naik/turun
populasi. IWC menyediakan rentang 1989-2025 yang cukup panjang untuk itu.
AWC 2026 berperan sebagai **potret kondisi terkini** (kekayaan spesies,
sebaran lokasi, status konservasi terbaru) yang melengkapi tren historis
dari IWC — keduanya saling melengkapi, bukan saling menggantikan.

## 4. Metode Analisis

1. **Analisis diversitas** (`scripts/python/analisis_diversitas_awc.py`) —
   indeks Shannon-Wiener dan kekayaan spesies per lokasi & per provinsi,
   dari data AWC 2026.
2. **Rekap semua spesies** (`scripts/python/rekap_semua_spesies_awc.py`) —
   tabel lengkap 235 spesies dengan status IUCN, total individu, jumlah
   lokasi.
3. **Analisis tren** (`scripts/python/analisis_tren_iwc.py`) — regresi
   log-linear (OLS) pada rata-rata individu per lokasi tersurvei per
   tahun, dari data IWC 1989-2025, untuk 3 spesies prioritas EAAF.
4. **Peta grid resmi** (`scripts/python/peta_grid_resmi_awc.py`) — grid
   100km x 100km dalam proyeksi Albers Equal-Area khusus Indonesia
   (`+proj=aea +lat_1=-8 +lat_2=6 +lat_0=-2 +lon_0=118`), diwarnai
   berdasarkan jumlah lokasi survei per sel (proxy intensitas
   pengamatan), plus rekap 50 kabupaten/kota sebagai halaman kedua.

## 5. Temuan Kunci

### 5.1 Skala Survei

- **113 lokasi** survei tersebar di **26 provinsi**.
- **235 jenis** burung air tercatat (baris terverifikasi).

### 5.2 Kekayaan Spesies & Keragaman

**Top 5 lokasi (kekayaan spesies)**

| Lokasi | Provinsi | Kekayaan spesies | Shannon-H | Total individu |
| --- | --- | --- | --- | --- |
| Ecotourism Mangroves Wonorejo | Jawa Timur | 57 | 2,58 | 1.051 |
| Lahan Basah Lanrae | Sulawesi Barat | 49 | 2,70 | 1.422 |
| Dusun Bondan, Segara Anakan | Jawa Tengah | 48 | 1,16 | 5.518 |
| Krayapan, Kendal | Jawa Tengah | 40 | 2,88 | 336 |
| Bagan Serdang | Sumatra Utara | 40 | 2,18 | 10.738 |

**Top 5 provinsi (rata-rata kekayaan spesies per lokasi)**

| Provinsi | Jumlah lokasi | Rata-rata kekayaan spesies | Rata-rata Shannon-H | Total individu |
| --- | --- | --- | --- | --- |
| Sulawesi Barat | 1 | 49,0 | 2,70 | 1.422 |
| Sumatra Utara | 3 | 32,3 | 2,10 | 17.970 |
| Nusa Tenggara Barat | 2 | 30,5 | 3,09 | 329 |
| Kalimantan Utara | 1 | 28,0 | 1,72 | 863 |
| Jawa Tengah | 13 | 20,9 | 1,52 | 13.761 |

Grafik lengkap: `outputs/figures/awc_top_lokasi_kekayaan_spesies.png`,
`outputs/figures/awc_sebaran_shannon.png`.

### 5.3 Spesies Dominan & Prioritas Konservasi

**Spesies dengan total individu terbanyak**: Cerekpasir Tibet
(*Anarhynchus atrifrons*, 8.667 individu), Kuntul Kecil (*Egretta
garzetta*, 8.560), Blekok Sawah (*Ardeola speciosa*, 5.743). Grafik
lengkap: `outputs/figures/awc_top40_spesies_individu.png`.

**Spesies berstatus Endangered/Critically Endangered (IUCN)**:

| Nama Indonesia | Nama ilmiah | Status IUCN | Total individu | Jumlah lokasi |
| --- | --- | --- | --- | --- |
| Kedidi Besar | *Calidris tenuirostris* | EN | 2.204 | 6 |
| Cerekpasir Mongolia | *Anarhynchus mongolus* | EN | 439 | 10 |
| Bangau Bluwok | *Mycteria cinerea* | EN | 173 | 10 |
| Gajahan Timur | *Numenius madagascariensis* | EN | 76 | 13 |
| Kacamata Jawa | *Zosterops flavus* | EN | 5 | 1 |
| Trinil Nordmann | *Tringa guttifer* | EN | 5 | 2 |

Tabel lengkap 235 spesies: `data/processed/awc_rekap_semua_spesies.csv`.

### 5.4 Peta Intensitas Survei (Grid Resmi)

Peta grid (`outputs/figures/peta_grid_resmi_awc.pdf`, halaman 1) memakai
proxy **jumlah lokasi survei per sel 100km x 100km** (bukan jumlah
individu/spesies, karena data pengamat individual sudah dianonimkan).
Sel dengan intensitas tertinggi (7-9 lokasi) berada di **Kalimantan
Barat** dan **DKI Jakarta**; detail Jawa-Bali (inset) menunjukkan Jawa
Tengah dan Jawa Timur juga cukup intensif disurvei.

Rekap 50 kabupaten/kota (halaman 2 PDF yang sama) — **Top 5 berdasarkan
kekayaan spesies gabungan**:

| Kabupaten/Kota | Jumlah lokasi | Kekayaan spesies | Total individu |
| --- | --- | --- | --- |
| Kota Administrasi Jakarta Utara | 6 | 69 | 2.427 |
| Kabupaten Kapuas Hulu | 6 | 51 | 492 |
| Kota Bontang | 4 | 49 | 545 |
| Kabupaten Banyuwangi | 4 | 34 | 985 |
| Kabupaten Banyuasin | 4 | 31 | 2.358 |

Catatan: peta ini belum pakai poligon batas kabupaten/kota resmi (lihat
`data/raw/boundaries/README.md` untuk sumber BIG/GADM kalau dibutuhkan
versi peta penuh per kabupaten).

### 5.5 Tren Populasi Historis (IWC 1989-2025)

| Spesies | Rentang tahun data | Laju perubahan/tahun | p-value | Signifikan? |
| --- | --- | --- | --- | --- |
| Trinil Nordmann (*Tringa guttifer*) | 2002-2025 (9 th data) | -0,45% | 0,95 | Tidak |
| Gajahan Timur (*Numenius madagascariensis*) | 1989-2025 (25 th data) | **-2,63%** | 0,28 | Tidak (nasional) |
| Kedidi Besar (*Calidris tenuirostris*) | 1990-2024 (15 th data) | +2,24% | 0,58 | Tidak |

Arah penurunan Gajahan Timur konsisten dengan laporan penurunan tajam
(62%) di Semenanjung Banyuasin (Sumatra Selatan) dari literatur, meski
secara nasional belum signifikan statistik — kemungkinan karena cakupan
lokasi survei yang tidak konsisten antar tahun (1-15 lokasi/tahun).
Grafik per spesies: `outputs/figures/tren_*.png`.

## 6. Keterbatasan Data

- **AWC 2026** = potret satu musim sensus, bukan seri waktu → tidak
  bisa dipakai sendiri untuk tren.
- **IWC 1989-2025** = cakupan lokasi antar-tahun tidak konsisten (bias
  jumlah lokasi disurvei), sehingga tren dihitung dari rata-rata
  individu per lokasi tersurvei, bukan total mentah.
- **Batas wilayah** (`indonesia_provinsi.geojson`) memakai data lama
  (masih "Irian Jaya", belum ada Kalimantan Utara) — hanya untuk label
  visual, bukan analisis administratif resmi.
- **Grid intensitas survei** memakai proxy "jumlah lokasi per sel",
  bukan "jumlah pengamat" (data pengamat individual sudah dianonimkan
  untuk privasi).
- Belum ada data poligon batas kabupaten/kota resmi di repo ini untuk
  versi peta kabupaten/kota berbasis peta (baru bar chart).

## 7. Rekomendasi

1. **Prioritaskan pemantauan lanjutan** di situs dengan kekayaan spesies
   tinggi sekaligus banyak spesies terancam: Ecotourism Mangroves
   Wonorejo (Jatim), Bagan Serdang (Sumut), dan kawasan pesisir
   Banyuasin (Sumsel) — konsisten dengan status Important Bird Area (IBA)
   yang sudah didokumentasikan di literatur.
2. **Tindak lanjuti tren penurunan Gajahan Timur** dengan survei
   tambahan di lokasi-lokasi historisnya untuk memperkuat signifikansi
   statistik, terutama di Semenanjung Banyuasin.
3. **Perluas cakupan survei** ke provinsi dengan data minim (mis. Riau,
   Sulawesi Tengah — hanya 1 lokasi tercatat) untuk gambaran nasional
   yang lebih representatif.
4. **Lengkapi data batas administratif resmi** (BIG/GADM) untuk analisis
   dan peta kabupaten/kota yang lebih akurat di masa depan.

## 8. Referensi & Lampiran

- Literatur ilmiah lengkap: `docs/referensi_burung_pantai_dan_kehati_indonesia.md`
- Data mentah (anonim): `data/raw/awc_indonesia_2026/`, `data/raw/iwc_indonesia_2020_2025/`
- Data olahan: `data/processed/awc_diversitas_per_lokasi.csv`,
  `awc_diversitas_per_provinsi.csv`, `awc_rekap_semua_spesies.csv`,
  `awc_rekap_kabupaten_kota.csv`, `tren_spesies_prioritas.csv`,
  `awc_grid_resmi_100km.geojson`
- Grafik & peta: `outputs/figures/` (lihat daftar file di atas)
- Skrip analisis: `scripts/python/analisis_diversitas_awc.py`,
  `rekap_semua_spesies_awc.py`, `analisis_tren_iwc.py`,
  `peta_grid_resmi_awc.py`
