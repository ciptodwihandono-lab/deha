# Observasi kukang jawa & vegetasi

Data lapangan hasil survei kukang jawa (*Nycticebus javanicus*) dan vegetasi
pakan/pohon tidurnya.

## File

- `vegetasi_kukang_jawa.csv` — tabel utama, isi dari catatan lapangan.
- `spesies_referensi_kukang_jawa.csv` — daftar jenis pohon pakan & pohon
  tidur kukang jawa (sumber: LFP Slow Loris Translocation Guide, ada di
  Google Drive folder "Kukang"). Dipakai sebagai acuan mengisi kolom
  `kategori` di atas.
- `photos/` — simpan foto lapangan di sini dengan nama file yang sama
  seperti yang tertulis di kolom `nama_file_foto`. Foto tidak di-commit ke
  git (lihat `.gitignore`) karena ukurannya besar — foto asli tetap di
  Google Drive, cukup rujuk nama filenya di sini.

## Cara mengisi `vegetasi_kukang_jawa.csv`

| Kolom | Isi |
| --- | --- |
| `id` | nomor urut |
| `tanggal` | format `YYYY-MM-DD` |
| `waktu` | jam pengamatan (opsional) |
| `nama_lokal` | nama lokal tumbuhan |
| `nama_ilmiah` | nama ilmiah (cocokkan dengan `spesies_referensi_kukang_jawa.csv` bila memungkinkan) |
| `kategori` | `pohon_pakan`, `pohon_tidur`, atau `lainnya` |
| `koordinat_dms` | koordinat dari catatan lapangan/GPS, format bebas — mis. `6°12'57.2"S 106°49'12.4"E` |
| `lat`, `lon` | **kosongkan saja**, akan otomatis terisi oleh script |
| `nama_file_foto` | nama file foto di folder `photos/` |
| `pengamat` | nama pencatat |
| `catatan` | catatan tambahan |

Kolom `koordinat_dms` menerima format derajat-menit-detik yang cukup
fleksibel (pemisah `°`, `'`, `"`, spasi, atau huruf `o`/`m`/`s` seperti pada
catatan GPS manual), asal urutannya derajat-menit-detik-arah
(N/S/E/W), lintang dulu baru bujur.

## Proses jadi peta

```
data/raw/observations/vegetasi_kukang_jawa.csv (isi koordinat_dms)
    → scripts/python/convert_coordinates.py
        → mengisi kolom lat/lon otomatis
        → data/processed/vegetasi_kukang_jawa.geojson
            → buka di QGIS, atau proses lanjut dengan scripts/r/map_indonesia.R
```

Jalankan:

```bash
python3 scripts/python/convert_coordinates.py
```

Baris yang kolom `koordinat_dms`-nya masih kosong akan dilewati (dan
disebutkan jumlahnya di output) — isi dulu dari catatan lapangan, lalu
jalankan ulang.
