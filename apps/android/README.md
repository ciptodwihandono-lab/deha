# Aplikasi Android Survei Cemara (APK)

Workflow `.github/workflows/android-survei.yml` membungkus
`apps/survei-pantai-cemara/` menjadi aplikasi Android dengan
[Capacitor](https://capacitorjs.com). Isi aplikasinya sama persis dengan versi
web, tetapi terpasang sebagai aplikasi sungguhan dan semua file ada di dalam
APK, jadi tidak perlu sinyal sama sekali.

## Unduh dan pasang di HP

1. Di HP, buka:
   https://github.com/ciptodwihandono-lab/deha/releases/download/apk-latest/survei-cemara.apk
2. Setelah selesai diunduh, ketuk file `survei-cemara.apk`.
3. Bila muncul "Untuk keamanan, HP Anda tidak diizinkan memasang aplikasi
   tidak dikenal", ketuk **Setelan** lalu aktifkan **Izinkan dari sumber ini**
   untuk Chrome (atau aplikasi File), lalu kembali dan ketuk **Instal**.
4. Bila Play Protect memperingatkan aplikasi tak dikenal, pilih
   **Detail lainnya → Tetap instal**. Peringatan ini muncul karena aplikasi
   tidak berasal dari Play Store.
5. Buka **Survei Cemara** dari daftar aplikasi dan izinkan akses lokasi saat
   pertama kali menekan "Ambil GPS".

## Memperbarui

Setiap perubahan di `apps/survei-pantai-cemara/` pada branch utama membuat APK
baru di tautan yang sama. Pasang saja APK baru di atas yang lama; data survei
tetap ada karena APK selalu ditandatangani dengan kunci yang sama
(`debug.keystore`).

**Jangan copot (uninstall) aplikasi sebelum mengekspor data**, karena data
ikut terhapus.

## Ekspor di aplikasi Android

- **Bagikan ZIP**: membuka menu bagikan Android (WhatsApp, Drive, Gmail, dll.).
- **Simpan ZIP ke HP**: menyimpan ke folder `Documents/SurveiCemara/`. Bila
  HP menolak, menu bagikan akan muncul sebagai gantinya.

## Catatan kunci tanda tangan

`debug.keystore` (kata sandi `android`) sengaja disimpan di repo agar setiap
build bisa memperbarui aplikasi tanpa menghapus data. Kunci ini hanya cocok
untuk aplikasi internal tim yang dipasang manual, bukan untuk Play Store.
