# Verifikasi Data AWC Indonesia 2026

Data hasil **Asian Waterbird Census (AWC) Indonesia 2026** — sensus
tahunan burung air/pantai di berbagai lokasi lahan basah Indonesia,
sudah melalui proses verifikasi spesies.

File: `Verifikasi_Data_AWC_Indonesia_2026_FINAL.xlsx`

## Isi tiap sheet

- **`Loc_Fiks`** — daftar 128 lokasi sensus: kode formulir, ID lokasi,
  nama lokasi, koordinat (Latitude/Longitude DD), koordinator lapangan.
- **`COUNT`** — data mentah hasil hitungan per lokasi (2.655 baris):
  nama Indonesia, nama Inggris (AviList), nama ilmiah, keputusan
  verifikasi (`OK` / `1` / `PARKIR`), catatan verifikasi, inisial
  verifikator, jumlah individu.
- **`Sheet1`** — kosong.
- **`Laporan Verifikasi`** — ringkasan proses verifikasi: acuan protokol
  (Protokol Verifikasi Data AWC Indonesia ver. 20 Januari 2026), acuan
  sebaran (peta eBird + teks sebaran Clements/AviList).
- **`Tindak Lanjut Kontributor`** — daftar baris berkeputusan `1` atau
  `PARKIR` yang perlu ditindaklanjuti/dikonfirmasi ke pengirim data
  (pengamat, lembaga, kontak, kode unik, spesies, jumlah).
- **`Rekap Spesies Final`** — rekap final per spesies setelah verifikasi
  (`OK` + `1`, `PARKIR` dikeluarkan): kelompok, nama Indonesia/ilmiah/
  Inggris, jumlah lokasi, total individu (dihitung dari maksimum per
  lokasi untuk menghindari hitung ganda antar-sesi), status IUCN.

## Catatan

- Burung laut (kelompok Burung Laut dan Camar & Dara Laut) tidak
  diverifikasi dan tidak masuk ke rekap final.
- Proyek ini terpisah dari data kukang jawa (`observations/`) dan
  batas wilayah (`boundaries/`) di folder `data/raw/` lainnya — sama-sama
  disimpan di repo ini tapi domainnya berbeda (burung air nasional vs.
  primata + vegetasi lokal Kiarapayung).
