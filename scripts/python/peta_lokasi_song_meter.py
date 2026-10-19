"""
Templat Peta Lokasi Titik Penelitian (gaya karya ilmiah) — EKSAI/LEAFA
Peta lokasi pemasangan Song Meter Micro 2 -- Gunung Anyar Tambak & Sumbergondo

Data batas wilayah: data/raw/boundaries/geojson-political-indonesia/
(GADM adm0/1/2 via rifani/geojson-political-indonesia, lihat README di
folder tersebut dan data/raw/boundaries/README.md untuk sumber & lisensi).
Elevasi titik BELUM disertakan (layanan SRTM/OpenTopoData tidak bisa
diakses dari sandbox ini saat peta ini dibuat) -- isi manual kalau ada
data GPS altitude, atau coba WebFetch opentopodata.org dari lingkungan
dengan akses jaringan normal.
"""
import os
import numpy as np
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter, MultipleLocator
from shapely.geometry import box as _box

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# ======================= KONFIGURASI =======================
DATA_DIR = os.path.join(ROOT, "data", "raw", "boundaries", "geojson-political-indonesia")
PROVINSI = "Jawa Timur"
JUDUL = "Lokasi Pemasangan Song Meter Micro 2 di Jawa Timur"
LABEL_TITIK = "Titik pemasangan Song Meter Micro 2"
JUDUL_TABEL = "TITIK PEMASANGAN"
OUTPUT = os.path.join(ROOT, "outputs", "figures", "peta_lokasi_song_meter")
CATATAN_TABEL = "Koordinat: geotag foto lapangan (WGS 84). *Elevasi tidak tersedia (layanan SRTM tidak dapat diakses saat pembuatan peta)."
SUMBER = "Sumber batas administrasi: GADM (via rifani/geojson-political-indonesia)"
TANGGAL_BUAT = "Oktober 2026"

TITIK = [
    dict(id="SM-01", nama="Gunung Anyar Tambak", kec="Kec. Gunung Anyar", kab="Kota Surabaya",
         lat=-7.32956474, lon=112.82117646, elev=None, tanggal="13-10-2026"),
    dict(id="SM-02", nama="Sumbergondo", kec="Kec. Bumiaji", kab="Batu",
         lat=-7.80261544, lon=112.55330048, elev=None, tanggal="15-10-2026"),
]
LABEL_UTAMA = {"LAUT JAWA": (112.1, -6.85), "SELAT MADURA": (113.15, -7.38),
               "SAMUDRA HINDIA": (112.4, -8.6), "Jawa Tengah": (111.05, -7.45),
               "Bali": (114.6, -8.30), "Madura": (113.3, -7.05)}
EXTENT_UTAMA = None
LABEL_TETANGGA = True
# ===========================================================

plt.rcParams["font.family"] = "DejaVu Sans"
SEA, LAND, OTHER, HL = "#d6e9f5", "#f4f1e8", "#e4e0d6", "#f3d9a4"
EDGE, HLEDGE, PROVLINE, PT = "#8a8578", "#7a5a1a", "#3d3a33", "#c0392b"
halo = [pe.withStroke(linewidth=2.5, foreground="white")]

adm0 = gpd.read_file(os.path.join(DATA_DIR, "IDN_adm_0_country.json"))
adm1 = gpd.read_file(os.path.join(DATA_DIR, "IDN_adm_1_province.json"))
adm2 = gpd.read_file(os.path.join(DATA_DIR, "IDN_adm_2_kabkota.json"))
prov = adm1[adm1.NAME_1 == PROVINSI]
kabprov = adm2[adm2.NAME_1 == PROVINSI]
assert len(prov), f"Provinsi '{PROVINSI}' tidak ada. Pilihan: {sorted(adm1.NAME_1)}"
for t in TITIK:
    assert t["kab"] in set(adm2.NAME_2), f"kab '{t['kab']}' tidak ada di GADM; cek ejaan NAME_2"


def nice(x, opts=(0.01, 0.02, 0.05, 0.1, 0.2, 0.25, 0.5, 1, 2)):
    return min(opts, key=lambda o: abs(o - x))


def nice_km(span_km):
    t = span_km / 5
    for o in (0.5, 1, 2, 2.5, 5, 10, 20, 25, 50, 100, 200):
        if o >= t:
            return o
    return 200


def dms(v, axis):
    h = ("LU" if v >= 0 else "LS") if axis == "y" else ("BT" if v >= 0 else "BB")
    v = abs(v); d = int(v); m = (v - d) * 60
    if abs(m - round(m)) < 1e-6:
        return f"{d}°{int(round(m)) % 60:02d}'{h}"
    return f"{d}°{int(m):02d}'{int(round((m - int(m)) * 60)):02d}\"{h}"


def frame(ax, xlim, ylim, fs=7, nticks=4):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_facecolor(SEA)
    step = nice((xlim[1] - xlim[0]) / nticks)
    ax.xaxis.set_major_locator(MultipleLocator(step))
    ax.yaxis.set_major_locator(MultipleLocator(step))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: dms(v, "x")))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: dms(v, "y")))
    ax.tick_params(labelsize=fs, direction="in", length=3, top=True, right=True,
                   labeltop=True, labelright=True)
    for lab in ax.get_yticklabels():
        lab.set_rotation(90); lab.set_va("center")
    ax.grid(True, color="#7a8a99", lw=0.4, ls=(0, (4, 3)), alpha=0.6)
    ax.set_aspect(1 / np.cos(np.radians(np.mean(ylim))))


def north(ax, x=0.93, y=0.84, size=0.09):
    ax.annotate("", xy=(x, y + size), xytext=(x, y), xycoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", lw=1.4, color="k", mutation_scale=14))
    ax.text(x, y + size + 0.015, "U", transform=ax.transAxes, ha="center", va="bottom",
            fontsize=9, fontweight="bold", path_effects=halo)


def scalebar(ax, x0=0.05, y0=0.05, segs=None):
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    kmdeg = 111.32 * np.cos(np.radians(np.mean(ylim)))
    km = nice_km((xlim[1] - xlim[0]) * kmdeg)
    segs = segs or (4 if km >= 20 else 2)
    frac = km / kmdeg / (xlim[1] - xlim[0])
    h = 0.012
    for i in range(segs):
        ax.add_patch(Rectangle((x0 + i * frac / segs, y0), frac / segs, h, transform=ax.transAxes,
                               fc="k" if i % 2 == 0 else "white", ec="k", lw=0.7, zorder=20))
    for i in range(segs + 1):
        ax.text(x0 + i * frac / segs, y0 + h + 0.008, f"{km * i / segs:g}" + (" km" if i == segs else ""),
                transform=ax.transAxes, ha="center", va="bottom", fontsize=6.5, zorder=21, path_effects=halo)


def pad_extent(b, pad=0.15, ratio=None):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    x0 -= w * pad; x1 += w * pad; y0 -= h * pad; y1 += h * pad
    if ratio:
        c = np.cos(np.radians((y0 + y1) / 2))
        W, H = (x1 - x0) * c, (y1 - y0)
        if W / H < ratio:
            d = (H * ratio / c - (x1 - x0)) / 2; x0 -= d; x1 += d
        else:
            d = ((x1 - x0) * c / ratio - (y1 - y0)) / 2; y0 -= d; y1 += d
    return (x0, x1), (y0, y1)


def kabtxt(n):
    if n.startswith("Kota"):
        return n
    return "Kota Batu" if n == "Batu" else f"Kab. {n}"


def base(ax, lw_kab=0.35):
    adm1.plot(ax=ax, color=OTHER, edgecolor=EDGE, lw=0.4)
    kabprov.plot(ax=ax, color=LAND, edgecolor=EDGE, lw=lw_kab)
    adm2[adm2.NAME_2.isin({t["kab"] for t in TITIK}) & (adm2.NAME_1 == PROVINSI)].plot(
        ax=ax, color=HL, edgecolor=HLEDGE, lw=0.8)
    prov.boundary.plot(ax=ax, color=PROVLINE, lw=0.9)


def core_bounds(g, minfrac=0.02):
    parts = [p for geom in g.geometry for p in getattr(geom, "geoms", [geom])]
    big = max(p.area for p in parts)
    keep = gpd.GeoSeries([p for p in parts if p.area >= big * minfrac], crs=g.crs)
    b = keep.total_bounds
    lons = [t["lon"] for t in TITIK]; lats = [t["lat"] for t in TITIK]
    return (min(b[0], *lons), min(b[1], *lats), max(b[2], *lons), max(b[3], *lats))


# ---------------- tata letak ----------------
fig = plt.figure(figsize=(11.69, 8.27), dpi=300)
nd = min(len(TITIK), 3)
mainw = 0.60 if nd else 0.90

ax = fig.add_axes([0.045, 0.27, mainw, 0.64])
eb = (EXTENT_UTAMA[0], EXTENT_UTAMA[2], EXTENT_UTAMA[1], EXTENT_UTAMA[3]) if EXTENT_UTAMA else core_bounds(prov)
xl, yl = pad_extent(eb, pad=0.03, ratio=mainw * 11.69 / (0.64 * 8.27))
base(ax)
frame(ax, xl, yl, nticks=7)
for t in TITIK:
    ax.scatter(t["lon"], t["lat"], marker="^", s=55, color=PT, edgecolor="white", lw=0.8, zorder=10)
for name, xy in LABEL_UTAMA.items():
    ax.text(*xy, name, fontsize=7, style="italic", ha="center", path_effects=halo,
            color="#4f6577" if name.isupper() else "#6b665c")
north(ax); scalebar(ax, x0=0.72)
ax.set_title(JUDUL, fontsize=12, fontweight="bold", pad=22)
ax.text(0.015, 0.975, "A", transform=ax.transAxes, fontsize=10, fontweight="bold", va="top", path_effects=halo)

gap = 0.065
ph = (0.66 - gap * (nd - 1)) / nd if nd else 0
for i, t in enumerate(TITIK[:nd]):
    letter = "BCD"[i]
    rect = [0.685, 0.915 - (i + 1) * ph - i * gap, 0.29, ph]
    a = fig.add_axes(rect)
    kab = adm2[(adm2.NAME_2 == t["kab"]) & (adm2.NAME_1 == PROVINSI)]
    ratio = rect[2] * 11.69 / (rect[3] * 8.27)
    dx, dy = pad_extent(kab.total_bounds, pad=0.12, ratio=ratio)
    base(a, lw_kab=0.6)
    frame(a, dx, dy, fs=6, nticks=3)
    a.scatter(t["lon"], t["lat"], s=90, marker="^", color=PT, edgecolor="white", lw=0.9, zorder=10)
    right = (t["lon"] - dx[0]) / (dx[1] - dx[0]) < 0.6
    a.annotate(f"{t['id']}\n{t['nama']}", (t["lon"], t["lat"]), (8 if right else -8, -4),
               textcoords="offset points", ha="left" if right else "right", va="top",
               fontsize=7, fontweight="bold", color=PT, path_effects=halo, zorder=11)
    c = kab.geometry.union_all().representative_point()
    a.text(c.x, c.y, kabtxt(t["kab"]).upper(), fontsize=6.5, ha="center", style="italic",
           color="#4a463e", path_effects=halo)
    if LABEL_TETANGGA:
        view = _box(dx[0], dy[0], dx[1], dy[1])
        for _, r in adm2[adm2.intersects(view) & (adm2.NAME_2 != t["kab"])].iterrows():
            part = r.geometry.intersection(view)
            if part.area / view.area > 0.08:
                p = part.representative_point()
                a.text(p.x, p.y, kabtxt(r.NAME_2), fontsize=6, ha="center", style="italic",
                       color="#6b665c", path_effects=halo)
    north(a, x=0.92, y=0.74, size=0.12)
    scalebar(a, x0=0.06, y0=0.06, segs=2)
    a.text(0.03, 0.96, letter, transform=a.transAxes, fontsize=10, fontweight="bold", va="top", path_effects=halo)
    ax.add_patch(Rectangle((dx[0], dy[0]), dx[1] - dx[0], dy[1] - dy[0], fill=False, ec="k", lw=0.8, zorder=12))
    ax.text(dx[1] + 0.02, dy[1], letter, fontsize=8, fontweight="bold", va="top", path_effects=halo, zorder=12)
    ax.annotate(t["id"], (t["lon"], t["lat"]), (dx[0] - 0.05, dy[0] - 0.08), ha="right", va="top",
                fontsize=8, fontweight="bold", color=PT, path_effects=halo,
                arrowprops=dict(arrowstyle="-", color=PT, lw=0.7), zorder=11)

axi = fig.add_axes([0.045, 0.035, 0.20, 0.205])
adm0.plot(ax=axi, color=OTHER, edgecolor=EDGE, lw=0.2)
prov.plot(ax=axi, color=PT, lw=0)
axi.set_xlim(94.5, 141.5); axi.set_ylim(-11.5, 6.5); axi.set_facecolor(SEA)
axi.set_xticks([]); axi.set_yticks([]); axi.set_aspect("equal")
axi.add_patch(Rectangle((xl[0], yl[0]), xl[1] - xl[0], yl[1] - yl[0], fill=False, ec="k", lw=0.8))
axi.text(0.5, 0.94, "INDONESIA", transform=axi.transAxes, ha="center", va="top", fontsize=6.5, fontweight="bold")

axl = fig.add_axes([0.26, 0.035, 0.24, 0.205]); axl.axis("off")
axl.add_patch(Rectangle((0, 0), 1, 1, transform=axl.transAxes, fill=False, ec="k", lw=0.8))
axl.text(0.03, 0.92, "LEGENDA", fontsize=9, fontweight="bold", va="top", transform=axl.transAxes)
items = [("tri", LABEL_TITIK), (HL, "Kab./kota lokasi titik"), (LAND, f"Kab./kota lain di {PROVINSI}"),
         (OTHER, "Provinsi lain"), (SEA, "Perairan"), ("line", "Batas provinsi"), ("thin", "Batas kabupaten/kota")]
for i, (kind, lab) in enumerate(items):
    y = 0.76 - i * 0.105
    if kind == "tri":
        axl.scatter(0.065, y, marker="^", s=55, color=PT, edgecolor="white", transform=axl.transAxes)
    elif kind in ("line", "thin"):
        axl.plot([0.04, 0.09], [y, y], color=PROVLINE if kind == "line" else EDGE,
                 lw=1.0 if kind == "line" else 0.6, transform=axl.transAxes)
    else:
        axl.add_patch(Rectangle((0.04, y - 0.035), 0.05, 0.07, transform=axl.transAxes, fc=kind, ec=EDGE, lw=0.5))
    axl.text(0.12, y, lab, fontsize=7.5, va="center", transform=axl.transAxes)

axt = fig.add_axes([0.515, 0.035, 0.46, 0.205]); axt.axis("off")
axt.add_patch(Rectangle((0, 0), 1, 1, transform=axt.transAxes, fill=False, ec="k", lw=0.8))
axt.text(0.02, 0.92, JUDUL_TABEL, fontsize=9, fontweight="bold", va="top", transform=axt.transAxes)
cols = [0.02, 0.10, 0.49, 0.625, 0.765, 0.865]
for cx, hd in zip(cols, ["Kode", "Lokasi", "Lintang", "Bujur", "Elevasi*", "Tanggal"]):
    axt.text(cx, 0.72, hd, fontsize=7.5, fontweight="bold", transform=axt.transAxes, va="center")
axt.plot([0.02, 0.98], [0.65, 0.65], color="k", lw=0.6, transform=axt.transAxes)
rowh = min(0.20, 0.52 / max(len(TITIK), 1))
for i, t in enumerate(TITIK):
    y = 0.55 - i * rowh
    vals = [t["id"], f"{t['nama']}, {t['kec']},\n{kabtxt(t['kab'])}", f"{t['lat']:.6f}°", f"{t['lon']:.6f}°",
            "-" if t.get("elev") is None else f"{t['elev']:,} m".replace(",", "."), t.get("tanggal", "-")]
    for cx, v in zip(cols, vals):
        axt.text(cx, y, v, fontsize=6.6 if len(TITIK) <= 3 else 5.8, transform=axt.transAxes, va="center",
                 color=PT if cx == cols[0] else "k", fontweight="bold" if cx == cols[0] else "normal")
axt.text(0.02, 0.06, CATATAN_TABEL, fontsize=6, style="italic", transform=axt.transAxes, color="#444")

fig.text(0.045, 0.012, f"Sistem koordinat: Geografis, Datum WGS 84  |  {SUMBER}  |  Dibuat: {TANGGAL_BUAT}",
         fontsize=6.5, color="#333")
for a_ in fig.axes:
    a_.set_xlabel(""); a_.set_ylabel("")
fig.savefig(OUTPUT + ".png", dpi=300)
fig.savefig(OUTPUT + ".pdf")
print("Tersimpan:", OUTPUT + ".png / .pdf")
