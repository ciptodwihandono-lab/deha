# Lokasi Bird Banding

Titik lokasi kegiatan bird banding (penangkapan-penandaan burung) untuk
mendukung program KEHATI PROPER. Disiapkan dulu di sini sebelum peta
lokasi gaya karya ilmiah dibuat (lihat
`scripts/python/peta_lokasi_song_meter.py` sebagai contoh skrip serupa
untuk titik Song Meter Micro 2; `scripts/python/peta_lokasi_bird_banding.py`
untuk klaster KRMMA -- perlu diperluas/dibuat terpisah untuk klaster ARJ
karena lokasinya jauh berbeda, lihat catatan di bagian Klaster Lokasi).

> **PERMINTAAN KHUSUS UNTUK PETA INI (beda dari peta Song Meter)**:
> peta bird banding harus menampilkan **foto jaring/lokasi sebagai
> inset/panel foto di tiap titik** (gaya jurnal ilmiah / layout QGIS
> dengan foto lapangan), bukan cuma simbol titik polos seperti peta
> Song Meter sebelumnya. Perlu file foto asli (bukan cuma nama
> filenya) tersedia saat peta dibuat -- kalau sesi kerja ini sudah
> berakhir sebelum peta dibuat, foto perlu diupload ulang ke chat.

## File

- `lokasi_bird_banding.csv` / `lokasi_bird_banding.geojson` — tabel
  titik lokasi: kode, nama lokasi, kecamatan, kab/kota, provinsi,
  koordinat (WGS 84, dari geotag foto lapangan), tanggal, nama file
  foto, catatan singkat kondisi lokasi. GeoJSON siap drag-drop ke QGIS.
- `photos/` — foto lapangan dengan nama file sama seperti kolom
  `nama_file_foto`. **Tidak di-commit ke git** (lihat `.gitignore`,
  sama seperti `data/raw/observations/photos/`) karena ukurannya besar
  — simpan foto asli di Google Drive atau penyimpanan terpisah, cukup
  rujuk nama filenya di CSV.

## Kolom di `lokasi_bird_banding.csv`

| Kolom | Isi |
| --- | --- |
| `kode_lokasi` | Kode unik titik (mis. KRMMA01, ARJ01) |
| `nama_lokasi` | Nama lokasi/desa |
| `kecamatan`, `kab_kota`, `provinsi` | Wilayah administratif |
| `lat`, `lon` | Koordinat WGS 84, **dari geotag foto lapangan** (bukan estimasi) |
| `tanggal`, `waktu` | Waktu foto diambil (proxy waktu pemasangan) |
| `nama_file_foto` | Nama file foto di `photos/` (atau Google Drive) |
| `catatan` | Catatan kondisi lokasi/alat |

## Klaster lokasi

Dua klaster terpisah jauh (~50 km, beda kota) -- jangan digabung dalam
satu peta "posisi relatif meter" seperti `peta_lokasi_bird_banding.py`
yang ada sekarang (itu cuma untuk klaster KRMMA). Klaster ARJ perlu
peta terpisah atau pakai pendekatan koordinat asli (bukan jarak
relatif) kalau mau digabung jadi satu peta nasional/provinsi.

### Klaster KRMMA — Gunung Anyar Tambak / Medokan Ayu, Kota Surabaya

> **STATUS: TIDAK AKTIF DIPAKAI.** Atas instruksi user, klaster ini
> tetap disimpan di data (CSV/GeoJSON/foto) tapi **tidak dipakai** untuk
> peta/laporan saat ini -- fokus kerja sekarang di klaster ARJ
> (Arjuno) di bawah.

1. **KRMMA01** — Gunung Anyar Tambak, Kec. Gunung Anyar (-7.32896386,
   112.82101954) — 14 Oktober 2026, 08:03:41. Titik jaring kabut, tim
   memeriksa jaring & kantong burung.
2. **KRMMA02-1** — Jalan Tambak Medokan Ayu Gang XI, Medokan Ayu,
   Kec. Rungkut (-7.32881932, 112.81977516) — 14 Oktober 2026, 08:11:41.
   Titik jaring kabut di jalur mangrove tepi tambak.
3. **KRMMA04** — Gunung Anyar Tambak, Kec. Gunung Anyar (-7.32826062,
   112.82044359) — 14 Oktober 2026, 09:04:53. Titik jaring kabut di
   jalur mangrove tepi tambak.

Berguna untuk integrasi data akustik vs bird banding (klaster ini
±100-500 m dari titik Song Meter Micro 2 SM-01, lihat
`docs/laporan_sementara_song_meter_micro2.md` Bagian 2 & 8).

*(Kode KRMMA03 sempat dipakai untuk titik di klaster ini lalu dicabut
-- titik itu ternyata salah catat, lokasi sebenarnya ada di klaster ARJ
di bawah dengan kode ARJ03. Foto lama KRMMA03 sudah dihapus dari
`photos/`.)*

### Klaster ARJ (Arjuno) — Bulukerto, Kec. Bumiaji, Kota Batu

**Klaster aktif saat ini.** Dekat dengan titik Song Meter Micro 2 SM-02
(Sumbergondo, Kec. Bumiaji, Kota Batu), kawasan lereng Gunung Arjuno.

1. **ARJ01** — Jalan Tanpa Nama, Bulukerto (-7.80382128, 112.55224873)
   — 15 Oktober 2026, 10:26:24. Titik jaring kabut di jalur hutan.
2. **ARJ02** — Jalan Tanpa Nama, Bulukerto (-7.80373312, 112.55238674)
   — 15 Oktober 2026, 10:25:47. Titik jaring kabut di jalur hutan.
3. **ARJ03** — Jalan Tanpa Nama, Bulukerto (-7.80274849, 112.55313883)
   — 15 Oktober 2026, 10:21:25. Titik jaring kabut di jalur hutan.
   *(Awalnya sempat tercatat keliru sebagai KRMMA03 di klaster
   Surabaya -- dikoreksi user jadi ARJ03.)*

*(tambahkan titik baru di sini dan di CSV/GeoJSON setiap ada foto lokasi baru)*
