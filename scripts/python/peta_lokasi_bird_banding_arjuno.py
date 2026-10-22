"""
Peta Lokasi Titik Bird Banding (ARJ/Arjuno) -- Bulukerto, Kec. Bumiaji,
Kota Batu, Jawa Timur -- gaya jurnal ilmiah dengan foto jaring per titik.

Klaster terpisah dari KRMMA (Surabaya, ~50 km jauhnya, saat ini tidak
dipakai -- lihat data/raw/bird_banding/README.md). Sama seperti skrip
KRMMA: titik-titik berdekatan, jadi dipakai peta situasi lokal (posisi
relatif dalam meter, bukan basemap/citra -- tidak ada akses jaringan
peta di sandbox ini) + inset konteks kota/provinsi + panel foto.

Beda dari versi KRMMA: legenda dipindah jadi panel terpisah di kolom
kanan (bukan ditumpuk di dalam Panel A) supaya tidak bertabrakan dengan
titik di layout manapun -- masalah yang sempat terjadi di peta KRMMA
saat titiknya berubah posisi.
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
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA_DIR = os.path.join(ROOT, "data", "raw", "boundaries", "geojson-political-indonesia")
PHOTO_DIR = os.path.join(ROOT, "data", "raw", "bird_banding", "photos")
OUTPUT = os.path.join(ROOT, "outputs", "figures", "peta_lokasi_bird_banding_ARJ")

# ======================= KONFIGURASI =======================
PROVINSI = "Jawa Timur"
KAB_KOTA_FOKUS = "Batu"  # ejaan NAME_2 di GADM untuk Kota Batu
JUDUL = "Peta Lokasi Titik Bird Banding (ARJ) -- Bulukerto, Kec. Bumiaji, Kota Batu"
TANGGAL_KEGIATAN = "15 Oktober 2026"

TITIK = [
    dict(id="ARJ01", nama="Jalan Tanpa Nama, Bulukerto", kec="Kec. Bumiaji",
         lat=-7.80382128, lon=112.55224873, tanggal="15-10-2026", waktu="10:26:24",
         catatan="Titik jaring kabut di jalur hutan",
         foto=os.path.join(PHOTO_DIR, "ARJ01.jpg")),
    dict(id="ARJ02", nama="Jalan Tanpa Nama, Bulukerto", kec="Kec. Bumiaji",
         lat=-7.80373312, lon=112.55238674, tanggal="15-10-2026", waktu="10:25:47",
         catatan="Titik jaring kabut di jalur hutan",
         foto=os.path.join(PHOTO_DIR, "ARJ02.jpg")),
    dict(id="ARJ03", nama="Jalan Tanpa Nama, Bulukerto", kec="Kec. Bumiaji",
         lat=-7.80274849, lon=112.55313883, tanggal="15-10-2026", waktu="10:21:25",
         catatan="Titik jaring kabut di jalur hutan",
         foto=os.path.join(PHOTO_DIR, "ARJ03.jpg")),
    dict(id="ARJ04", nama="Jalan Tanpa Nama, Bulukerto", kec="Kec. Bumiaji",
         lat=-7.804833, lon=112.551181, tanggal="15-10-2026", waktu=None,
         catatan="Titik jaring kabut -- koordinat dari GPS manual (DMS)",
         foto=None),
    dict(id="ARJ05", nama="Jalan Tanpa Nama, Bulukerto", kec="Kec. Bumiaji",
         lat=-7.804858, lon=112.551128, tanggal="15-10-2026", waktu=None,
         catatan="Titik jaring kabut -- koordinat dari GPS manual (DMS)",
         foto=None),
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
assert len(kab_fokus), f"'{KAB_KOTA_FOKUS}' tidak ditemukan di GADM NAME_2 untuk {PROVINSI}"


def north_arrow(ax, x, y, size, fontsize=9):
    ax.annotate("", xy=(x, y + size), xytext=(x, y), xycoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", lw=1.3, color="k", mutation_scale=12))
    ax.text(x, y + size + 0.02, "U", transform=ax.transAxes, ha="center", va="bottom",
            fontsize=fontsize, fontweight="bold", path_effects=halo)


# ================= FIGURE =================
fig = plt.figure(figsize=(16.5, 11.5), dpi=300)
fig.suptitle(JUDUL, fontsize=15, fontweight="bold", y=0.985)
fig.text(0.5, 0.945, f"Kegiatan pendukung program KEHATI PROPER -- {TANGGAL_KEGIATAN}",
         fontsize=10, ha="center", style="italic", color="#444")

# ---------- Panel A: peta situasi lokal (posisi relatif titik, satuan meter) ----------
axA = fig.add_axes([0.035, 0.41, 0.44, 0.46])

pad = 45
xs = [t["x_m"] for t in TITIK]; ys = [t["y_m"] for t in TITIK]
xlim = (min(xs) - pad, max(xs) + pad)
ylim = (min(ys) - pad, max(ys) + pad)
axA.set_xlim(xlim); axA.set_ylim(ylim)
axA.set_aspect("equal")
axA.set_facecolor("#f4f1e8")
axA.add_patch(Rectangle((xlim[0], ylim[0]), xlim[1] - xlim[0], ylim[1] - ylim[0],
                         facecolor="#f4f1e8", edgecolor="none", zorder=0))

# simbol vegetasi hutan: titik sistematis (grid + jitter kecil) -- konvensi
# kartografi topografi standar untuk vegetasi/woodland. ILUSTRATIF dari foto
# lapangan (area hutan dataran tinggi lereng Gunung Arjuno), bukan survei.
rng = np.random.default_rng(11)
gx, gy = np.meshgrid(np.arange(xlim[0], xlim[1], 9), np.arange(ylim[0], ylim[1], 9))
gx = gx + rng.uniform(-2.5, 2.5, gx.shape)
gy = gy + rng.uniform(-2.5, 2.5, gy.shape)
veg_pts = np.column_stack([gx.ravel(), gy.ravel()])
axA.scatter(veg_pts[:, 0], veg_pts[:, 1], s=6, marker="o", color="#2e7d32",
            alpha=0.85, zorder=1.5, linewidths=0)

# offset label per titik (bukan seragam) -- beberapa titik berdekatan
# (ARJ01/ARJ02 ~18m, ARJ04/ARJ05 ~7m) jadi label perlu diarahkan menjauh
# satu sama lain supaya tidak bertabrakan.
LABEL_OFFSET = {
    "ARJ01": ((-12, -16), "right", "top"),
    "ARJ02": ((12, 14), "left", "bottom"),
    "ARJ03": ((10, 10), "left", "bottom"),
    "ARJ04": ((-14, -10), "right", "top"),
    "ARJ05": ((12, 14), "left", "bottom"),
}
for t in TITIK:
    axA.scatter(t["x_m"], t["y_m"], marker="^", s=220, color=PT, edgecolor="white",
                linewidth=1.3, zorder=10)
    off, ha, va = LABEL_OFFSET.get(t["id"], ((10, 10), "left", "bottom"))
    axA.annotate(f"{t['id']}", (t["x_m"], t["y_m"]), off, textcoords="offset points",
                 ha=ha, va=va, fontsize=10, fontweight="bold", color=PT, path_effects=halo, zorder=11)

axA.set_xlabel("Jarak timur-barat dari titik tengah (meter)", fontsize=8.5)
axA.set_ylabel("Jarak utara-selatan dari titik tengah (meter)", fontsize=8.5)
axA.tick_params(labelsize=7.5)
axA.grid(True, color="#c9c3b0", lw=0.4, ls=(0, (4, 3)), alpha=0.6, zorder=4)
axA.set_title("A. Peta Situasi -- Posisi Titik Jaring", fontsize=10.5, fontweight="bold", loc="left")

# skala batang (meter)
sb_len = 50
sb_x0 = xlim[0] + (xlim[1] - xlim[0]) * 0.06
sb_y0 = ylim[0] + (ylim[1] - ylim[0]) * 0.03
axA.plot([sb_x0, sb_x0 + sb_len], [sb_y0, sb_y0], color="k", lw=3, solid_capstyle="butt", zorder=20)
axA.text(sb_x0 + sb_len / 2, sb_y0 + (ylim[1] - ylim[0]) * 0.018, f"{sb_len} m",
         ha="center", fontsize=8, path_effects=halo, zorder=21)
north_arrow(axA, 0.08, 0.80, 0.07)

axA.text(0.985, 0.02,
         "Titik jaring: posisi relatif dari koordinat GPS (akurat).\n"
         "*Elemen bertanda bintang: ILUSTRATIF dari foto lapangan,\n"
         "bukan hasil survei/GPS track/citra satelit.",
         transform=axA.transAxes, fontsize=6.5, color="#333", ha="right", va="bottom",
         bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#999", alpha=0.85))

# ---------- Panel B: inset konteks Jawa Timur / Kota Batu ----------
axB = fig.add_axes([0.495, 0.765, 0.20, 0.13])
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
axB.text(0.5, -0.08, "Bintang = lokasi klaster titik ARJ\n(Kota Batu, lereng G. Arjuno)",
         transform=axB.transAxes, ha="center", va="top", fontsize=6.3, color="#444")

# ---------- Panel legenda (terpisah dari Panel A, tidak akan bertabrakan titik) ----------
axL = fig.add_axes([0.495, 0.615, 0.20, 0.13]); axL.axis("off")
axL.add_patch(Rectangle((0, 0), 1, 1, transform=axL.transAxes, fill=False, ec="#999", lw=0.7))
axL.text(0.07, 0.88, "LEGENDA", fontsize=8.5, fontweight="bold", transform=axL.transAxes, va="top")
axL.scatter([0.11], [0.62], s=24, marker="o", color="#2e7d32", transform=axL.transAxes, zorder=5)
axL.text(0.19, 0.62, "Vegetasi hutan*", fontsize=7, va="center", transform=axL.transAxes)
axL.scatter([0.11], [0.32], s=90, marker="^", color=PT, edgecolor="white", transform=axL.transAxes, zorder=5)
axL.text(0.19, 0.32, "Titik jaring", fontsize=7, va="center", transform=axL.transAxes)

# ---------- Panel tabel koordinat ----------
axT = fig.add_axes([0.495, 0.37, 0.20, 0.225]); axT.axis("off")
axT.add_patch(Rectangle((0, 0), 1, 1, transform=axT.transAxes, fill=False, ec="k", lw=0.7))
axT.text(0.06, 0.95, "TABEL TITIK", fontsize=8.5, fontweight="bold", transform=axT.transAxes, va="top")
rowh = 0.145
for i, t in enumerate(TITIK):
    y = 0.82 - i * rowh
    waktu_str = t["waktu"] if t["waktu"] else "jam tdk tercatat"
    axT.text(0.06, y, t["id"], fontsize=7.5, fontweight="bold", color=PT, transform=axT.transAxes, va="top")
    axT.text(0.06, y - 0.055, f"{t['lat']:.6f}, {t['lon']:.6f}", fontsize=6.0, transform=axT.transAxes, va="top")
    axT.text(0.06, y - 0.10, f"{t['tanggal']} {waktu_str}", fontsize=6.0, color="#555", transform=axT.transAxes, va="top")
axT.text(0.06, 0.02, "Datum WGS 84. Koordinat dari geotag foto lapangan / GPS manual.",
         fontsize=5.6, style="italic", color="#555", transform=axT.transAxes, va="bottom")

# ---------- Panel foto jaring per titik (baris bawah) ----------
# hanya titik yang sudah ada foto lapangan yang ditampilkan di sini
TITIK_FOTO = [t for t in TITIK if t["foto"] is not None]
n = len(TITIK_FOTO)
gap = 0.015
pw = (1 - 0.06 - gap * (n - 1)) / n
for i, t in enumerate(TITIK_FOTO):
    x0 = 0.03 + i * (pw + gap)
    axP = fig.add_axes([x0, 0.075, pw, 0.265])
    try:
        img = mpimg.imread(t["foto"])
        axP.imshow(img)
    except Exception as e:
        axP.text(0.5, 0.5, f"Foto tidak dapat dimuat:\n{e}", ha="center", va="center", fontsize=7, wrap=True)
    axP.set_xticks([]); axP.set_yticks([])
    for s in axP.spines.values():
        s.set_linewidth(1.1); s.set_edgecolor(PT)
    axP.set_title(f"{t['id']}", fontsize=10, fontweight="bold", color=PT, pad=4)
    waktu_str = t["waktu"] if t["waktu"] else "jam tidak tercatat"
    axP.text(0.5, -0.05, f"{t['nama']}, {t['kec']}\n{t['tanggal']} {waktu_str} -- {t['catatan']}",
              transform=axP.transAxes, ha="center", va="top", fontsize=6.5)

fig.text(0.02, 0.012, "Sistem koordinat: Geografis, Datum WGS 84  |  "
         "Sumber batas administrasi: GADM (via rifani/geojson-political-indonesia)  |  "
         "Dibuat: Oktober 2026", fontsize=7, color="#333")

fig.savefig(OUTPUT + ".png", dpi=300, bbox_inches=None)
fig.savefig(OUTPUT + ".pdf", bbox_inches=None)
print("Tersimpan:", OUTPUT + ".png / .pdf")
