# Observasi kukang jawa & vegetasi

Data lapangan hasil survei kukang jawa (*Nycticebus javanicus*) dan vegetasi
pakan/pohon tidurnya, di **Taman Kehati Kiarapayung**.

> **PENTING — status identifikasi jenis:** kolom `nama_ilmiah_tentatif` dan
> `famili_tentatif` adalah hasil identifikasi visual dari foto (habitus,
> daun, kulit batang), bukan identifikasi oleh ahli botani atau spesimen
> herbarium. Prefiks `cf.` (*confer*) berarti "mirip dengan / kemungkinan".
> **Wajib diverifikasi** oleh ahli botani atau spesimen herbarium sebelum
> dipakai di naskah ilmiah final — lihat kolom `tingkat_keyakinan` dan
> `ciri_kunci_foto` untuk konteksnya.

## File

- `vegetasi_kukang_jawa.csv` — tabel utama, isi dari catatan lapangan +
  identifikasi tentatif dari foto.
- `spesies_referensi_kukang_jawa.csv` — daftar jenis pohon pakan & pohon
  tidur kukang jawa (sumber: LFP Slow Loris Translocation Guide, ada di
  Google Drive folder "Kukang"). Dipakai sebagai acuan mencocokkan
  `nama_ilmiah_tentatif`.
- `photos/` — simpan foto lapangan di sini dengan nama file yang sama
  seperti yang tertulis di kolom `nama_file_foto`. Foto tidak di-commit ke
  git (lihat `.gitignore`) karena ukurannya besar — foto asli tetap di
  Google Drive, cukup rujuk nama filenya di sini.

## Kolom di `vegetasi_kukang_jawa.csv`

| Kolom | Isi |
| --- | --- |
| `id` | nomor urut |
| `titik` | label titik survei (mis. "Vegetasi 1") |
| `lokasi` | nama lokasi survei |
| `tipe` | Pohon / Bambu (rumpun) / dll., dari pengamatan lapangan |
| `famili_tentatif` | famili tumbuhan, **tentatif** dari foto |
| `nama_ilmiah_tentatif` | nama ilmiah tentatif (prefiks `cf.` = kemungkinan), **wajib diverifikasi** |
| `tingkat_keyakinan` | Rendah / Sedang / Tinggi — seberapa yakin identifikasi tentatif ini |
| `kategori` | `pohon_pakan`, `pohon_tidur`, `lainnya`, atau `belum_teridentifikasi` — kategori kerja untuk analisis, lihat catatan di bawah |
| `koordinat_dms` | koordinat dari catatan lapangan/GPS **hanya jika formatnya derajat-menit-detik**, mis. `6°12'57.2"S 106°49'12.4"E` |
| `lat`, `lon` | isi langsung jika koordinat sudah desimal (mis. dari Google Maps, `-6.889217,107.762170`); **kosongkan** jika mengisi `koordinat_dms` — akan otomatis terisi oleh script |
| `ciri_kunci_foto` | ciri morfologi yang teramati dari foto (dasar identifikasi tentatif) |
| `nama_file_foto` | nama file foto di folder `photos/` |
| `pengamat` | nama pencatat |
| `catatan` | catatan tambahan, termasuk alasan tingkat keyakinan dan apa yang perlu diverifikasi ulang |

Kolom `kategori` diisi `pohon_pakan`/`pohon_tidur` hanya kalau
`nama_ilmiah_tentatif` cocok dengan daftar di
`spesies_referensi_kukang_jawa.csv` DAN `tingkat_keyakinan`-nya minimal
Sedang; selain itu pakai `belum_teridentifikasi` sampai ada konfirmasi ahli.

Ada dua cara mengisi koordinat, tergantung sumbernya:

- **Sudah desimal** (mis. disalin dari Google Maps: `-6.889217,107.762170`)
  → isi langsung ke kolom `lat` dan `lon`, kosongkan `koordinat_dms`.
- **Masih format derajat-menit-detik** (mis. dari alat GPS:
  `6°12'57.2"S 106°49'12.4"E`) → isi ke kolom `koordinat_dms`, kosongkan
  `lat`/`lon`, nanti otomatis dikonversi oleh script (pemisah bebas: `°`,
  `'`, `"`, spasi, atau huruf `o`/`m`/`s`, asal urutannya
  derajat-menit-detik-arah, lintang dulu baru bujur).

## Proses jadi peta

```
data/raw/observations/vegetasi_kukang_jawa.csv (isi koordinat_dms)
    → scripts/python/convert_coordinates.py
        → mengisi kolom lat/lon otomatis
        → data/processed/vegetasi_kukang_jawa.geojson
            → scripts/r/map_vegetasi_kukang.R → outputs/figures/*.png
            (atau buka manual di QGIS kalau mau, lihat qgis/README.md)
```

Jalankan:

```bash
python3 scripts/python/convert_coordinates.py
Rscript scripts/r/map_vegetasi_kukang.R
```

Baris yang kolom `koordinat_dms`-nya masih kosong akan dilewati (dan
disebutkan jumlahnya di output) — isi dulu dari catatan lapangan, lalu
jalankan ulang.

**Kenapa lewat R, bukan QGIS?** Membuat peta lewat R (`map_vegetasi_kukang.R`)
jauh lebih stabil daripada lewat Python Console QGIS — tidak ada masalah
paste/autocomplete/hang seperti di PyQGIS, tinggal jalankan satu perintah
dan hasilnya langsung jadi file gambar. Script PyQGIS di `scripts/qgis/`
tetap ada sebagai opsi kalau memang butuh buka datanya langsung sebagai
proyek `.qgz` di QGIS.
