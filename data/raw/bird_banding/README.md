# Lokasi Bird Banding

Titik lokasi kegiatan bird banding (penangkapan-penandaan burung) untuk
mendukung program KEHATI PROPER. Disiapkan dulu di sini sebelum peta
lokasi gaya karya ilmiah dibuat (lihat
`scripts/python/peta_lokasi_song_meter.py` sebagai contoh skrip serupa
untuk titik Song Meter Micro 2 -- nanti dibuat skrip senada untuk titik
bird banding setelah semua titik terkumpul).

## File

- `lokasi_bird_banding.csv` — tabel titik lokasi: kode, nama lokasi,
  kecamatan, kab/kota, provinsi, koordinat (WGS 84, dari geotag foto
  lapangan), tanggal, nama file foto, catatan singkat kondisi lokasi.
- `photos/` — foto lapangan dengan nama file sama seperti kolom
  `nama_file_foto`. **Tidak di-commit ke git** (lihat `.gitignore`,
  sama seperti `data/raw/observations/photos/`) karena ukurannya besar
  — simpan foto asli di Google Drive atau penyimpanan terpisah, cukup
  rujuk nama filenya di CSV.

## Kolom di `lokasi_bird_banding.csv`

| Kolom | Isi |
| --- | --- |
| `kode_lokasi` | Kode unik titik (mis. KRMMA01) |
| `nama_lokasi` | Nama lokasi/desa |
| `kecamatan`, `kab_kota`, `provinsi` | Wilayah administratif |
| `lat`, `lon` | Koordinat WGS 84, **dari geotag foto lapangan** (bukan estimasi) |
| `tanggal`, `waktu` | Waktu foto diambil (proxy waktu pemasangan) |
| `nama_file_foto` | Nama file foto di `photos/` (atau Google Drive) |
| `catatan` | Catatan kondisi lokasi/alat |

## Titik yang sudah tercatat

1. **KRMMA01** — Gunung Anyar Tambak, Kec. Gunung Anyar, Kota Surabaya,
   Jawa Timur (-7.32801374, 112.81985045) — 14 Oktober 2026, 08:09:57.
   Catatan: lokasi pemasangan jaring kabut (mist net), ±500 m dari
   titik Song Meter Micro 2 SM-01 di lokasi yang sama (Gunung Anyar
   Tambak) -- berguna untuk integrasi data akustik vs bird banding
   (lihat `docs/laporan_sementara_song_meter_micro2.md` Bagian 2 & 8).
2. **KRMMA02-1** — Jalan Tambak Medokan Ayu Gang XI, Medokan Ayu,
   Kec. Rungkut, Kota Surabaya, Jawa Timur (-7.32881932, 112.81977516)
   — 14 Oktober 2026, 08:11:41.
   Catatan: titik jaring kabut di jalur mangrove tepi tambak, ±100 m
   dari KRMMA01 (sama-sama area Gunung Anyar/Medokan Ayu, kecamatan
   administratif beda: Gunung Anyar vs Rungkut).
3. **KRMMA04** — Gunung Anyar Tambak, Kec. Gunung Anyar, Kota Surabaya,
   Jawa Timur (-7.32826062, 112.82044359) — 14 Oktober 2026, 09:04:53.
   Catatan: titik jaring kabut di jalur mangrove tepi tambak, satu
   kawasan dengan KRMMA01. (KRMMA03 belum diterima -- nomor urut
   melompat dari 02 ke 04, bukan kesalahan pencatatan di sini.)

*(tambahkan titik baru di sini dan di CSV setiap ada foto lokasi baru)*
