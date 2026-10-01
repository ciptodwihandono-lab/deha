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

### 5.6 Analisis Kesenjangan Cakupan Survei (Tindak Lanjut Rekomendasi #3)

Membandingkan provinsi yang tercakup AWC 2026 dengan daftar **38 provinsi
resmi Indonesia** (pasca pemekaran Papua 2022) menghasilkan gambaran gap
yang jauh lebih tajam dari perkiraan awal:

- **12 dari 38 provinsi (32%) sama sekali tidak punya data lokasi
  survei AWC 2026**: Kepulauan Bangka Belitung, Bengkulu, Lampung,
  Kalimantan Selatan, Sulawesi Utara, **Sulawesi Tenggara**, Maluku,
  Papua, Papua Barat, Papua Tengah, Papua Pegunungan, Papua Barat Daya.
- **8 provinsi lain** baru punya 1-2 lokasi (data minim): Riau,
  Kepulauan Riau, Jambi, Banten, Kalimantan Utara, Sulawesi Tengah,
  Sulawesi Selatan, Gorontalo, Sulawesi Barat, NTB, DI Yogyakarta.
- **Temuan prioritas tinggi**: **Sulawesi Tenggara** nol data survei,
  padahal provinsi ini adalah lokasi **Taman Nasional Rawa Aopa
  Watumohai** — salah satu dari 6 situs Ramsar Indonesia yang relevan
  untuk burung migran (lihat
  `docs/referensi_burung_pantai_dan_kehati_indonesia.md`). Situs Ramsar
  lain (Danau Sentarum, Tanjung Puting, Wasur, Pulau Rambut,
  Berbak-Sembilang) semuanya **sudah** tercakup data AWC 2026 di
  provinsinya masing-masing — Rawa Aopa Watumohai jadi satu-satunya
  situs Ramsar burung migran yang belum tersentuh sensus ini.
- 11 provinsi nol-data lainnya belum punya situs spesifik yang
  terdokumentasi di referensi proyek ini, tapi tetap layak diperiksa
  karena berkarakter pesisir/kepulauan (mis. seluruh wilayah Papua di
  luar Papua Selatan, dan Maluku).

Tabel lengkap 38 provinsi dengan klasifikasi prioritas:
`data/processed/awc_gap_survei_provinsi.csv`. Grafik:
`outputs/figures/awc_gap_survei_provinsi.png`. Skrip:
`scripts/python/analisis_gap_survei_awc.py`.

### 5.7 Kesenjangan Status Perlindungan (IUCN vs Status Nasional)

Menyilangkan status IUCN global dengan status perlindungan hukum
nasional (`StaNas`) pada 13 spesies berstatus terancam (EN/VU/CR)
menghasilkan temuan tajam: **7 dari 13 spesies terancam (54%) belum
berstatus "Protected" secara nasional**, termasuk spesies dengan
populasi tercatat terbesar di seluruh dataset:

| Nama Indonesia | Nama ilmiah | Status IUCN | Total individu | Status nasional |
| --- | --- | --- | --- | --- |
| Kedidi Besar | *Calidris tenuirostris* | EN | 2.204 | **Non-protected** |
| Cerekpasir Mongolia | *Anarhynchus mongolus* | EN | 439 | **Non-protected** |
| Kedidi Golgol | *Calidris ferruginea* | VU | 437 | **Non-protected** |
| Cerek Besar | *Pluvialis squatarola* | VU | 320 | **Non-protected** |
| Kerak Kerbau | *Acridotheres javanicus* | VU | 230 | **Non-protected** |
| Kedidi Ekor-panjang | *Calidris acuminata* | VU | 14 | **Non-protected** |
| Cica-koreng Selatan | *Poodytes albolimbatus* | VU | 2 | **Non-protected** |

Sebagai pembanding, 6 spesies terancam lain (termasuk Bangau Bluwok,
Gajahan Timur, Trinil Nordmann) sudah berstatus "Protected". Kedidi
Besar jadi temuan paling signifikan: spesies EN dengan jumlah individu
tercatat terbanyak (2.204) di seluruh dataset AWC 2026, tapi tidak
mendapat perlindungan hukum nasional. Tabel lengkap:
`data/processed/awc_gap_status_perlindungan.csv`, grafik:
`outputs/figures/awc_gap_status_perlindungan.png`, skrip:
`scripts/python/analisis_status_perlindungan_awc.py`.

### 5.8 Sebaran per Spesies Prioritas (Status Endangered)

Peta titik individual (bukan agregat grid) untuk 6 spesies berstatus
IUCN Endangered menunjukkan pola sebaran yang berbeda-beda: Kedidi
Besar sangat terkonsentrasi (1.699 individu di hanya 6 lokasi, mayoritas
di satu lokasi Sumatera), sementara Gajahan Timur lebih tersebar (72
individu di 13 lokasi berbeda). Trinil Nordmann dan Kacamata Jawa
masing-masing hanya tercatat di 1-2 lokasi dengan jumlah individu
sangat kecil (5 individu) — konsisten dengan status kelangkaannya.
Peta: `outputs/figures/peta_spesies_prioritas_awc.png`, skrip:
`scripts/python/peta_spesies_prioritas_awc.py`.

### 5.9 Komposisi Kelompok Burung Air per Provinsi

Secara nasional, kelompok **Kuntul & Cangak** (famili Ardeidae)
mendominasi rata-rata komposisi provinsi (30,8%), diikuti **"Jenis Lain
Non-Burung Air"** (19%) dan **Burung Pantai (Cerek)** (17,4%). Komposisi
bervariasi tajam antar-provinsi: Kepulauan Riau dan Riau hampir 100%
didominasi Burung Pantai (Cerek), sementara Kalimantan Barat dan Papua
Selatan didominasi kelompok "Jenis Lain Non-Burung Air". Variasi ini
mencerminkan perbedaan tipe habitat (mangrove vs lahan basah pedalaman
vs pesisir berpasir) di tiap lokasi survei. Tabel:
`data/processed/awc_komposisi_kelompok_provinsi.csv`, grafik:
`outputs/figures/awc_komposisi_kelompok_provinsi.png`, skrip:
`scripts/python/komposisi_kelompok_awc.py`.

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
3. **Perluas cakupan survei** ke provinsi yang belum tercakup sama
   sekali (12 provinsi, lihat 5.6) — prioritaskan **Sulawesi Tenggara**
   (TN Rawa Aopa Watumohai, situs Ramsar yang belum pernah tersentuh
   sensus AWC), lalu provinsi kepulauan/pesisir lain seperti Maluku,
   Kepulauan Bangka Belitung, dan wilayah-wilayah Papua di luar Papua
   Selatan.
4. **Lengkapi data batas administratif resmi** (BIG/GADM) untuk analisis
   dan peta kabupaten/kota yang lebih akurat di masa depan.
5. **Dorong penetapan status perlindungan nasional** untuk 7 spesies
   terancam (EN/VU) yang masih "Non-protected" (lihat 5.7), terutama
   Kedidi Besar (*Calidris tenuirostris*) yang populasinya tercatat
   paling besar (2.204 individu) di seluruh dataset tapi belum
   dilindungi hukum nasional.

## 8. Referensi & Lampiran

- Literatur ilmiah lengkap: `docs/referensi_burung_pantai_dan_kehati_indonesia.md`
- Data mentah (anonim): `data/raw/awc_indonesia_2026/`, `data/raw/iwc_indonesia_2020_2025/`
- Data olahan: `data/processed/awc_diversitas_per_lokasi.csv`,
  `awc_diversitas_per_provinsi.csv`, `awc_rekap_semua_spesies.csv`,
  `awc_rekap_kabupaten_kota.csv`, `tren_spesies_prioritas.csv`,
  `awc_grid_resmi_100km.geojson`, `awc_gap_survei_provinsi.csv`,
  `awc_gap_status_perlindungan.csv`, `awc_komposisi_kelompok_provinsi.csv`
- Grafik & peta: `outputs/figures/` (lihat daftar file di atas)
- Skrip analisis: `scripts/python/analisis_diversitas_awc.py`,
  `rekap_semua_spesies_awc.py`, `analisis_tren_iwc.py`,
  `peta_grid_resmi_awc.py`, `analisis_gap_survei_awc.py`,
  `analisis_status_perlindungan_awc.py`, `peta_spesies_prioritas_awc.py`,
  `komposisi_kelompok_awc.py`
