# Survei KEHATI

Aplikasi web (PWA) untuk survei keanekaragaman hayati di lapangan, bekerja tanpa sinyal.
Diterbitkan di `/deha/kehati/`.

- Survei per lokasi: jam mulai/selesai, metode, cuaca, pengamat, jalur GPS.
- Catatan berbagai taksa (burung, mamalia, reptil, amfibi, kupu-kupu, capung, serangga, ikan,
  krustasea & moluska, tumbuhan) dengan daftar jenis acuan, status IUCN, dan perlindungan.
- Tombol kamera membuat titik foto berkoordinat; foto diberi watermark lokasi, jenis, koordinat, tanggal-jam.
- Peta (citra satelit / OSM) dengan titik, jalur, dan poligon luasan; luas dihitung dari poligon,
  jalur GPS keliling, atau transek (panjang × lebar).
- Analisis: S, N, Shannon-Wiener, Pielou, Simpson, Margalef, dominansi, frekuensi, Sørensen,
  dan INP vegetasi per tingkat.
- AI di HP (CLIP via transformers.js, model dipakai bersama Peta Survei dan Survei Cemara) untuk
  deskripsi habitat dan tebakan kelompok satwa dari foto.
- Ekspor ZIP: CSV (Excel), GeoJSON, KML, cadangan JSON, dan foto.
