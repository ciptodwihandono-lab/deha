# Basemap Citra Satelit Esri untuk Peta Indonesia

Referensi layanan basemap citra satelit yang dipakai di proyek ini —
gratis, tanpa API key, cukup untuk kebutuhan visualisasi peta Indonesia
(kukang jawa Kiarapayung, sebaran burung pantai, batas wilayah, dll).

## Layanan: Esri World Imagery

- **Nama**: Esri World Imagery (via ArcGIS Online)
- **URL XYZ tile**:
  ```
  https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}
  ```
- **Biaya**: gratis untuk penggunaan umum, **tidak perlu API key/akun**
- **Cakupan**: global, termasuk resolusi tinggi untuk sebagian besar
  wilayah Indonesia
- **Atribusi**: wajib cantumkan "Esri, Maxar, Earthstar Geographics" (atau
  teks atribusi yang tampil otomatis di aplikasi seperti QGIS) kalau peta
  dipakai untuk publikasi/laporan resmi

## Cara pakai per tool

### QGIS (paling sering dipakai di proyek ini)

Lewat menu, **tanpa scripting**:

1. Panel **Browser** → klik kanan **XYZ Tiles** → **New Connection**
2. Name: `Esri Satellite`, URL: (lihat URL di atas)
3. Klik OK, lalu double-click koneksinya di Browser panel

Detail lengkap + langkah tambah data titik di atasnya: lihat
`qgis/README.md`.

### Python (matplotlib + contextily)

```python
import contextily as cx

# gdf harus dalam CRS proyeksi (mis. EPSG:3857) sebelum add_basemap
cx.add_basemap(ax, source=cx.providers.Esri.WorldImagery, crs=gdf.crs)
```

Lihat contoh lengkap di `scripts/python/peta_vegetasi_satelit.py`.

**Catatan**: perlu `pip install contextily`. Kalau berjalan di lingkungan
dengan pembatasan jaringan (mis. sandbox/CI), permintaan ke
`server.arcgisonline.com` bisa diblokir — coba jalankan dari komputer
dengan akses internet normal.

### R

Tidak ada package R yang dipakai di proyek ini untuk basemap satelit
secara langsung (`sf`/`ggspatial` sempat menimbulkan masalah instalasi
Rtools di Windows — lihat riwayat proyek). Kalau tetap dibutuhkan di R,
package `ggspatial::annotation_map_tile()` atau `maptiles` bisa memuat
URL XYZ yang sama di atas, tapi keduanya menambah dependency `sf`/`terra`.
Alternatif yang sudah dipakai: buat peta tanpa basemap di R
(`scripts/r/map_vegetasi_kukang.R`), lalu pakai QGIS kalau butuh versi
dengan citra satelit.

## Peta grid sebaran burung pantai (AWC) + satelit Esri di QGIS

Peta grid resmi (`outputs/figures/peta_grid_resmi_awc.pdf`) dibuat di
Python tanpa basemap (jaringan sandbox ini memblokir server tile Esri).
Untuk versi dengan citra satelit, buka file-file berikut di QGIS **di
komputer sendiri** (bukan di sandbox ini):

1. Tambahkan basemap dulu (lihat langkah "QGIS" di atas): **Browser** →
   klik kanan **XYZ Tiles** → **New Connection** → Name `Esri Satellite`,
   URL `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}`
   → double-click untuk load, taruh paling bawah di panel Layers.
2. **Layer → Add Layer → Add Vector Layer**, pilih
   `data/processed/awc_grid_resmi_100km.geojson` (grid 100km x 100km
   dengan atribut `jumlah_lokasi`, `kekayaan_spesies`, `total_individu`).
3. Klik kanan layer grid → **Properties → Symbology** → pilih
   **Graduated**, Value = `jumlah_lokasi`, Color ramp = `YlOrRd` (sama
   seperti versi PNG/PDF), Mode = `Natural Breaks` atau `Equal Interval`.
4. Di tab **Symbology**, set **Opacity** layer grid ke sekitar 60-70%
   supaya citra satelit di bawahnya tetap kelihatan.
5. (Opsional) tambahkan `data/raw/boundaries/indonesia_provinsi.geojson`
   di atas grid untuk label nama provinsi (klik kanan → **Properties →
   Labels** → Single Labels → field nama provinsi).
6. Set CRS project ke `EPSG:3857` (Web Mercator, dipakai basemap XYZ)
   lewat ikon CRS di pojok kanan bawah, atau biarkan QGIS reproject
   on-the-fly (default sudah aktif).
7. Export peta lewat **Project → Import/Export → Export Map to Image**
   (atau **New Print Layout** kalau mau tambah skala batang, north arrow,
   legenda formal).

File titik lokasi survei asli (kalau mau ditampilkan juga sebagai layer
terpisah, bukan grid) ada di sheet `COUNT` pada
`data/raw/awc_indonesia_2026/awc_indonesia_2026_anonim.xlsx`, kolom
`Latitude (DD)` / `Longitude (DD)` — bisa di-import ke QGIS lewat
**Layer → Add Layer → Add Delimited Text Layer** setelah diekspor ke CSV.

## Alternatif basemap lain (kalau Esri bermasalah)

| Sumber | URL XYZ | Catatan |
| --- | --- | --- |
| OpenStreetMap (jalan/label, bukan satelit) | `https://tile.openstreetmap.org/{z}/{x}/{y}.png` | Gratis, tanpa API key, tapi bukan citra satelit |
| Google Satellite (tidak resmi) | `https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}` | Berisiko melanggar Term of Service Google untuk penggunaan di luar Google Maps |

Esri World Imagery tetap pilihan utama karena resmi mendukung akses XYZ
langsung tanpa API key untuk penggunaan seperti ini.
