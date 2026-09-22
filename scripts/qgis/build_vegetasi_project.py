"""PyQGIS script: buat proyek QGIS untuk data vegetasi kukang jawa.

Cara pakai (di dalam QGIS, BUKAN terminal python biasa):
1. Buka QGIS -> menu Plugins -> Python Console.
2. Di Python Console, klik ikon "Show Editor", buka file ini, lalu klik Run.
   (atau paste isi file ini ke console langsung)
3. Proyek otomatis tersimpan di qgis/projects/vegetasi_kukang_kiarapayung.qgz
   dan terbuka di QGIS.

Script ini memuat data/processed/vegetasi_kukang_jawa.geojson, memberi
simbol warna berbeda per `kategori` (pohon_pakan/pohon_tidur/
belum_teridentifikasi/lainnya), dan label nama titik.
"""

from pathlib import Path

from qgis.core import (
    QgsCategorizedSymbolRenderer,
    QgsPalLayerSettings,
    QgsProject,
    QgsRendererCategory,
    QgsSymbol,
    QgsTextFormat,
    QgsVectorLayer,
    QgsVectorLayerSimpleLabeling,
)
from qgis.PyQt.QtGui import QColor

ROOT = Path(__file__).resolve().parents[2]
LAYER_PATH = ROOT / "data" / "processed" / "vegetasi_kukang_jawa.geojson"
PROJECT_PATH = ROOT / "qgis" / "projects" / "vegetasi_kukang_kiarapayung.qgz"

# Warna per kategori (nama_kategori -> kode warna).
KATEGORI_WARNA = {
    "pohon_pakan": "#2e7d32",       # hijau tua
    "pohon_tidur": "#8d6e63",       # coklat
    "belum_teridentifikasi": "#9e9e9e",  # abu-abu
    "lainnya": "#1565c0",           # biru
}


def build_renderer(layer: QgsVectorLayer) -> QgsCategorizedSymbolRenderer:
    categories = []
    for kategori, warna in KATEGORI_WARNA.items():
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        symbol.setColor(QColor(warna))
        symbol.setSize(4)
        categories.append(QgsRendererCategory(kategori, symbol, kategori))
    return QgsCategorizedSymbolRenderer("kategori", categories)


def build_labeling() -> QgsVectorLayerSimpleLabeling:
    settings = QgsPalLayerSettings()
    settings.fieldName = "titik"

    text_format = QgsTextFormat()
    text_format.setSize(9)
    settings.setFormat(text_format)

    return QgsVectorLayerSimpleLabeling(settings)


def main() -> None:
    layer = QgsVectorLayer(str(LAYER_PATH), "Vegetasi Kukang Jawa", "ogr")
    if not layer.isValid():
        raise RuntimeError(f"Gagal memuat layer: {LAYER_PATH}")

    layer.setRenderer(build_renderer(layer))
    layer.setLabeling(build_labeling())
    layer.setLabelsEnabled(True)

    project = QgsProject.instance()
    project.addMapLayer(layer)

    PROJECT_PATH.parent.mkdir(parents=True, exist_ok=True)
    project.write(str(PROJECT_PATH))
    print(f"Proyek tersimpan di {PROJECT_PATH}")


main()
