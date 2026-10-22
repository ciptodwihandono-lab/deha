"""
Peta Lokasi Titik Bird Banding (KRMMA) -- Gunung Anyar Tambak / Medokan Ayu,
Surabaya, Jawa Timur -- gaya jurnal ilmiah dengan foto jaring per titik.

Beda dari peta_lokasi_song_meter.py: titik-titik di sini sangat
berdekatan (radius ~150 m), jadi dipakai peta situasi lokal (sketsa
posisi relatif dalam meter, bukan peta jalan/basemap -- tidak ada akses
basemap citra di sandbox ini) + inset konteks kota/provinsi, DITAMBAH
panel foto jaring/lokasi untuk tiap titik (sesuai permintaan user).
"""
import os
import math
import numpy as np
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle, FancyArrowPatch
from shapely.geometry import Point

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA_DIR = os.path.join(ROOT, "data", "raw", "boundaries", "geojson-political-indonesia")
PHOTO_DIR = os.path.join(ROOT, "data", "raw", "bird_banding", "photos")
OUTPUT = os.path.join(ROOT, "outputs", "figures", "peta_lokasi_bird_banding_KRMMA")

# ======================= KONFIGURASI =======================
# Data titik & nama file foto bersumber dari data/raw/bird_banding/lokasi_bird_banding.csv
# (foto tidak ikut di-commit ke git -- lihat README di folder itu; taruh
# foto dengan nama persis seperti kolom nama_file_foto di PHOTO_DIR
# sebelum menjalankan skrip ini).
PROVINSI = "Jawa Timur"
KAB_KOTA_FOKUS = "Kota Surabaya"
JUDUL = "Peta Lokasi Titik Bird Banding (KRMMA) -- Gunung Anyar Tambak / Medokan Ayu, Surabaya"

TITIK = [
    dict(id="KRMMA01", nama="Gunung Anyar Tambak", kec="Kec. Gunung Anyar",
         lat=-7.32896386, lon=112.82101954, tanggal="14-10-2026", waktu="08:03:41",
         catatan="Tim memeriksa jaring & kantong burung",
         foto=os.path.join(PHOTO_DIR, "KRMMA01.jpg")),
    dict(id="KRMMA02-1", nama="Jl. Tambak Medokan Ayu Gang XI", kec="Kec. Rungkut",
         lat=-7.32881932, lon=112.81977516, tanggal="14-10-2026", waktu="08:11:41",
         catatan="Titik jaring di jalur mangrove tepi tambak",
         foto=os.path.join(PHOTO_DIR, "KRMMA02-1.jpg")),
    dict(id="KRMMA03", nama="Gunung Anyar Tambak", kec="Kec. Gunung Anyar",
         lat=-7.32801374, lon=112.81985045, tanggal="14-10-2026", waktu="08:09:57",
         catatan="Pemasangan jaring kabut (mist net)",
         foto=os.path.join(PHOTO_DIR, "KRMMA03.jpg")),
    dict(id="KRMMA04", nama="Gunung Anyar Tambak", kec="Kec. Gunung Anyar",
         lat=-7.32826062, lon=112.82044359, tanggal="14-10-2026", waktu="09:04:53",
         catatan="Titik jaring di jalur mangrove tepi tambak",
         foto=os.path.join(PHOTO_DIR, "KRMMA04.jpg")),
]
# =============================================================

plt.rcParams["font.family"] = "DejaVu Sans"
SEA, LAND, OTHER, HL = "#d6e9f5", "#f4f1e8", "#e4e0d6", "#f3d9a4"
EDGE, HLEDGE, PROVLINE, PT = "#8a8578", "#7a5a1a", "#3d3a33", "#c0392b"
halo = [pe.withStroke(linewidth=2.5, foreground="white")]

# ---------- hitung posisi relatif tiap titik dalam meter (lokal) ----------
mean_lat = sum(t["lat"] for t in TITIK) / len(TITIK)
mean_lon = sum(t["lon"] for t in TITIK) / len(TITIK)
m_per_deg_lat = 111320.0
m_per_deg_lon = 111320.0 * math.cos(math.radians(mean_lat))

for t in TITIK:
    t["x_m"] = (t["lon"] - mean_lon) * m_per_deg_lon
    t["y_m"] = (t["lat"] - mean_lat) * m_per_deg_lat

# ---------- data batas wilayah (untuk inset konteks) ----------
adm0 = gpd.read_file(os.path.join(DATA_DIR, "IDN_adm_0_country.json"))
adm1 = gpd.read_file(os.path.join(DATA_DIR, "IDN_adm_1_province.json"))
adm2 = gpd.read_file(os.path.join(DATA_DIR, "IDN_adm_2_kabkota.json"))
prov = adm1[adm1.NAME_1 == PROVINSI]
kabprov = adm2[adm2.NAME_1 == PROVINSI]
kab_fokus = adm2[(adm2.NAME_2 == KAB_KOTA_FOKUS) & (adm2.NAME_1 == PROVINSI)]


def dms(v, axis):
    h = ("LU" if v >= 0 else "LS") if axis == "y" else ("BT" if v >= 0 else "BB")
    v = abs(v); d = int(v); m = (v - d) * 60
    return f"{d}°{int(round(m)):02d}'{h}"


def north_arrow(ax, x, y, size, fontsize=9):
    ax.annotate("", xy=(x, y + size), xytext=(x, y), xycoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", lw=1.3, color="k", mutation_scale=12))
    ax.text(x, y + size + 0.02, "U", transform=ax.transAxes, ha="center", va="bottom",
            fontsize=fontsize, fontweight="bold", path_effects=halo)


# ================= FIGURE =================
fig = plt.figure(figsize=(16.5, 11.5), dpi=200)
fig.suptitle(JUDUL, fontsize=15, fontweight="bold", y=0.985)
fig.text(0.5, 0.945, "Kegiatan pendukung program KEHATI PROPER -- 14 Oktober 2026",
         fontsize=10, ha="center", style="italic", color="#444")

# ---------- Panel A: peta situasi lokal (posisi relatif titik, satuan meter) ----------
axA = fig.add_axes([0.035, 0.37, 0.46, 0.50])

pad = 35
xs = [t["x_m"] for t in TITIK]; ys = [t["y_m"] for t in TITIK]
xlim = (min(xs) - pad, max(xs) + pad)
ylim = (min(ys) - pad, max(ys) + pad)
axA.set_xlim(xlim); axA.set_ylim(ylim)
axA.set_aspect("equal")
axA.set_facecolor("#eef5ea")
axA.add_patch(Rectangle((xlim[0], ylim[0]), xlim[1] - xlim[0], ylim[1] - ylim[0],
                         facecolor="#eef5ea", edgecolor="none", zorder=0))

warna_kec = {"Kec. Gunung Anyar": "#1565c0", "Kec. Rungkut": "#2e7d32"}
for t in TITIK:
    c = warna_kec.get(t["kec"], PT)
    axA.scatter(t["x_m"], t["y_m"], marker="^", s=220, color=PT, edgecolor="white",
                linewidth=1.3, zorder=10)
    axA.annotate(f"{t['id']}", (t["x_m"], t["y_m"]), (10, 10), textcoords="offset points",
                 fontsize=10, fontweight="bold", color=PT, path_effects=halo, zorder=11)

axA.set_xlabel("Jarak timur-barat dari titik tengah (meter)", fontsize=8.5)
axA.set_ylabel("Jarak utara-selatan dari titik tengah (meter)", fontsize=8.5)
axA.tick_params(labelsize=7.5)
axA.grid(True, color="#b9c9b2", lw=0.4, ls=(0, (4, 3)), alpha=0.7)
axA.set_title("A. Peta Situasi -- Posisi Relatif Titik Jaring", fontsize=10.5, fontweight="bold", loc="left")

# skala batang (meter)
sb_len = 50
sb_x0 = xlim[0] + (xlim[1] - xlim[0]) * 0.06
sb_y0 = ylim[0] + (ylim[1] - ylim[0]) * 0.06
axA.plot([sb_x0, sb_x0 + sb_len], [sb_y0, sb_y0], color="k", lw=3, solid_capstyle="butt", zorder=20)
axA.text(sb_x0 + sb_len / 2, sb_y0 + (ylim[1] - ylim[0]) * 0.018, f"{sb_len} m",
         ha="center", fontsize=8, path_effects=halo, zorder=21)
north_arrow(axA, 0.93, 0.80, 0.10)

axA.text(0.985, 0.02, "Posisi relatif dari koordinat GPS\n(bukan basemap citra/jalan)",
         transform=axA.transAxes, fontsize=6.8, color="#555", ha="right", va="bottom")

# ---------- Panel B: inset konteks Jawa Timur / Surabaya ----------
axB = fig.add_axes([0.535, 0.645, 0.20, 0.20])
kabprov.plot(ax=axB, color=LAND, edgecolor=EDGE, lw=0.3)
kab_fokus.plot(ax=axB, color=HL, edgecolor=HLEDGE, lw=0.6)
prov.boundary.plot(ax=axB, color=PROVLINE, lw=0.7)
b = prov.total_bounds
padx = (b[2] - b[0]) * 0.04; pady = (b[3] - b[1]) * 0.04
axB.set_xlim(b[0] - padx, b[2] + padx); axB.set_ylim(b[1] - pady, b[3] + pady)
axB.set_facecolor(SEA)
axB.set_aspect(1 / math.cos(math.radians((b[1] + b[3]) / 2)))
axB.scatter(mean_lon, mean_lat, marker="*", s=90, color=PT, edgecolor="white", lw=0.8, zorder=10)
axB.set_xticks([]); axB.set_yticks([])
axB.set_xlabel(""); axB.set_ylabel("")
for s in axB.spines.values():
    s.set_linewidth(0.6)
axB.set_title("B. Konteks: Jawa Timur", fontsize=8.5, fontweight="bold", loc="left")
axB.text(0.5, -0.07, "Bintang = lokasi klaster titik KRMMA\n(Kota Surabaya)",
         transform=axB.transAxes, ha="center", va="top", fontsize=6.3, color="#444")

# ---------- Kotak legenda + tabel koordinat ----------
axT = fig.add_axes([0.535, 0.37, 0.20, 0.235]); axT.axis("off")
axT.add_patch(Rectangle((0, 0), 1, 1, transform=axT.transAxes, fill=False, ec="k", lw=0.7))
axT.text(0.06, 0.94, "TABEL TITIK", fontsize=8.5, fontweight="bold", transform=axT.transAxes, va="top")
rowh = 0.195
for i, t in enumerate(TITIK):
    y = 0.80 - i * rowh
    axT.text(0.06, y, t["id"], fontsize=8, fontweight="bold", color=PT, transform=axT.transAxes, va="top")
    axT.text(0.06, y - 0.065, f"{t['lat']:.6f}, {t['lon']:.6f}", fontsize=6.4, transform=axT.transAxes, va="top")
    axT.text(0.06, y - 0.12, f"{t['tanggal']} {t['waktu']}", fontsize=6.4, color="#555", transform=axT.transAxes, va="top")
axT.text(0.06, 0.02, "Datum WGS 84. Koordinat dari geotag foto lapangan.",
         fontsize=5.8, style="italic", color="#555", transform=axT.transAxes, va="bottom")

# ---------- Panel foto jaring per titik (baris bawah) ----------
n = len(TITIK)
gap = 0.015
pw = (1 - 0.06 - gap * (n - 1)) / n
for i, t in enumerate(TITIK):
    x0 = 0.03 + i * (pw + gap)
    axP = fig.add_axes([x0, 0.045, pw, 0.285])
    try:
        img = mpimg.imread(t["foto"])
        axP.imshow(img)
    except Exception as e:
        axP.text(0.5, 0.5, f"Foto tidak dapat dimuat:\n{e}", ha="center", va="center", fontsize=7, wrap=True)
    axP.set_xticks([]); axP.set_yticks([])
    for s in axP.spines.values():
        s.set_linewidth(1.1); s.set_edgecolor(PT)
    axP.set_title(f"{t['id']}", fontsize=10, fontweight="bold", color=PT, pad=4)
    axP.text(0.5, -0.05, f"{t['nama']}, {t['kec']}\n{t['tanggal']} {t['waktu']} -- {t['catatan']}",
              transform=axP.transAxes, ha="center", va="top", fontsize=6.8)

fig.text(0.02, 0.012, "Sistem koordinat: Geografis, Datum WGS 84  |  "
         "Sumber batas administrasi: GADM (via rifani/geojson-political-indonesia)  |  "
         "Dibuat: Oktober 2026", fontsize=7, color="#333")

fig.savefig(OUTPUT + ".png", dpi=200, bbox_inches=None)
fig.savefig(OUTPUT + ".pdf", bbox_inches=None)
print("Tersimpan:", OUTPUT + ".png / .pdf")
