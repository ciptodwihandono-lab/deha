"""Versi 'flat' dari build_vegetasi_project.py, aman untuk copy-paste
langsung ke baris perintah (>>>) Python Console QGIS.

Tidak ada def/if/for multi-baris sama sekali -- semua baris berdiri
sendiri -- supaya tidak rusak walau console menjalankan tiap baris satu
per satu begitu di-paste.

CARA PAKAI:
1. Ganti isi variabel ROOT di bawah ini ke folder proyek "deha" di
   komputer Anda (bukan folder di sandbox ini).
2. Select semua isi file ini, copy, lalu paste ke Python Console QGIS.
"""

from pathlib import Path
from qgis.core import QgsCategorizedSymbolRenderer, QgsPalLayerSettings, QgsProject, QgsRendererCategory, QgsSymbol, QgsTextFormat, QgsVectorLayer, QgsVectorLayerSimpleLabeling
from qgis.PyQt.QtGui import QColor
ROOT = Path(r"C:\GANTI\KE\FOLDER\deha")
LAYER_PATH = ROOT / "data" / "processed" / "vegetasi_kukang_jawa.geojson"
PROJECT_PATH = ROOT / "qgis" / "projects" / "vegetasi_kukang_kiarapayung.qgz"
layer = QgsVectorLayer(str(LAYER_PATH), "Vegetasi Kukang Jawa", "ogr")
assert layer.isValid(), "Gagal memuat layer: " + str(LAYER_PATH)
symbol_pakan = QgsSymbol.defaultSymbol(layer.geometryType())
symbol_pakan.setColor(QColor("#2e7d32"))
symbol_pakan.setSize(4)
symbol_tidur = QgsSymbol.defaultSymbol(layer.geometryType())
symbol_tidur.setColor(QColor("#8d6e63"))
symbol_tidur.setSize(4)
symbol_belum = QgsSymbol.defaultSymbol(layer.geometryType())
symbol_belum.setColor(QColor("#9e9e9e"))
symbol_belum.setSize(4)
symbol_lain = QgsSymbol.defaultSymbol(layer.geometryType())
symbol_lain.setColor(QColor("#1565c0"))
symbol_lain.setSize(4)
categories = [QgsRendererCategory("pohon_pakan", symbol_pakan, "pohon_pakan"), QgsRendererCategory("pohon_tidur", symbol_tidur, "pohon_tidur"), QgsRendererCategory("belum_teridentifikasi", symbol_belum, "belum_teridentifikasi"), QgsRendererCategory("lainnya", symbol_lain, "lainnya")]
renderer = QgsCategorizedSymbolRenderer("kategori", categories)
layer.setRenderer(renderer)
label_settings = QgsPalLayerSettings()
label_settings.fieldName = "titik"
text_format = QgsTextFormat()
text_format.setSize(9)
label_settings.setFormat(text_format)
labeling = QgsVectorLayerSimpleLabeling(label_settings)
layer.setLabeling(labeling)
layer.setLabelsEnabled(True)
project = QgsProject.instance()
project.addMapLayer(layer)
PROJECT_PATH.parent.mkdir(parents=True, exist_ok=True)
project.write(str(PROJECT_PATH))
print("Proyek tersimpan di " + str(PROJECT_PATH))
