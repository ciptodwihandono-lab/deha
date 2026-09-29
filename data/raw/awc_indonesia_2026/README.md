# Verifikasi Data AWC Indonesia 2026

Data hasil **Asian Waterbird Census (AWC) Indonesia 2026** — sensus
tahunan burung air/pantai di berbagai lokasi lahan basah Indonesia,
sudah melalui proses verifikasi spesies.

File:

- `Verifikasi_Data_AWC_Indonesia_2026_FINAL.xlsx` — **file asli lengkap**
  (ada nama koordinator/pengamat, email, No. HP) — **tidak di-commit ke
  git**, hanya untuk dipakai lokal.
- `awc_indonesia_2026_anonim.xlsx` — versi tanpa data kontak pribadi,
  aman dan sudah masuk git, dipakai untuk semua analisis/pemetaan.

## Isi tiap sheet

- **`Loc_Fiks`** — daftar 128 lokasi sensus: kode formulir, ID lokasi,
  nama lokasi, koordinat (Latitude/Longitude DD).
- **`COUNT`** — data mentah hasil hitungan per lokasi (2.655 baris):
  nama Indonesia, nama Inggris (AviList), nama ilmiah, keputusan
  verifikasi (`OK` / `1` / `PARKIR`), catatan verifikasi, inisial
  verifikator, jumlah individu, nama lembaga pengamat.
- **`Sheet1`** — kosong.
- **`Laporan Verifikasi`** — ringkasan proses verifikasi: acuan protokol
  (Protokol Verifikasi Data AWC Indonesia ver. 20 Januari 2026), acuan
  sebaran (peta eBird + teks sebaran Clements/AviList).
- **`Tindak Lanjut Kontributor`** — daftar baris berkeputusan `1` atau
  `PARKIR` yang perlu ditindaklanjuti/dikonfirmasi ke pengirim data
  (lembaga, kode unik, spesies, jumlah, lokasi, apa yang perlu dicek).
- **`Rekap Spesies Final`** — rekap final per spesies setelah verifikasi
  (`OK` + `1`, `PARKIR` dikeluarkan): kelompok, nama Indonesia/ilmiah/
  Inggris, jumlah lokasi, total individu (dihitung dari maksimum per
  lokasi untuk menghindari hitung ganda antar-sesi), status IUCN.

## Catatan penting — data pribadi

File asli punya 3 kolom identitas personal yang **dihapus** di versi
anonim: `Koordinator` (di `Loc_Fiks`), `Pengamat Utama` (di `COUNT`), dan
`Pengamat utama` + `Email` + `No. HP` (di `Tindak Lanjut Kontributor`).
Ditemukan juga 2 kolom tersembunyi di ujung kanan sheet `Loc_Fiks`
("Alamat Email", "Custom.Data.HP") dan `COUNT` ("Custom.Data.HP",
kolom di sebelahnya) yang juga berisi email/nomor HP — ikut dihapus.
Nama lembaga (`Nama Lembaga`) tetap dipertahankan karena bukan data
personal individu.

## Catatan lain

- Burung laut (kelompok Burung Laut dan Camar & Dara Laut) tidak
  diverifikasi dan tidak masuk ke rekap final.
- Proyek ini terpisah dari data kukang jawa (`observations/`) dan
  batas wilayah (`boundaries/`) di folder `data/raw/` lainnya — sama-sama
  disimpan di repo ini tapi domainnya berbeda (burung air nasional vs.
  primata + vegetasi lokal Kiarapayung).
