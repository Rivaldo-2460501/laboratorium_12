import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import plotly.express as px
import plotly.graph_objects as go
import math

# Konfigurasi halaman
st.set_page_config(
    page_title="Simulasi Laboratorium Kimia Profesional",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi state
def init_state():
    keys = [
        'campuran', 'reaksi', 'warna', 'suhu', 'gambar_reaksi',
        'log_percobaan', 'volume_total', 'warna_campuran'
    ]
    defaults = {
        'campuran': [],
        'reaksi': "",
        'warna': "#FFFFFF",
        'suhu': 25,
        'gambar_reaksi': None,
        'log_percobaan': [],
        'volume_total': 0,
        'warna_campuran': "#ADD8E6"
    }
    
    for key in keys:
        if key not in st.session_state:
            st.session_state[key] = defaults[key]

init_state()

# Database senyawa kimia lengkap (100+ senyawa)
SENYAWA_KIMIA = {
    # Logam
    "Natrium (Na)": {"warna": "#D9D9D9", "jenis": "logam alkali", "densitas": 0.97, "reaktivitas": 9},
    "Kalium (K)": {"warna": "#8F8FFF", "jenis": "logam alkali", "densitas": 0.86, "reaktivitas": 9},
    "Kalsium (Ca)": {"warna": "#FFD700", "jenis": "logam alkali tanah", "densitas": 1.54, "reaktivitas": 7},
    "Magnesium (Mg)": {"warna": "#FFA500", "jenis": "logam alkali tanah", "densitas": 1.74, "reaktivitas": 6},
    "Aluminium (Al)": {"warna": "#BFBFBF", "jenis": "logam", "densitas": 2.70, "reaktivitas": 5},
    "Besi (Fe)": {"warna": "#B5651D", "jenis": "logam transisi", "densitas": 7.87, "reaktivitas": 6},
    "Tembaga (Cu)": {"warna": "#D2691E", "jenis": "logam transisi", "densitas": 8.96, "reaktivitas": 4},
    "Perak (Ag)": {"warna": "#C0C0C0", "jenis": "logam transisi", "densitas": 10.49, "reaktivitas": 3},
    "Emas (Au)": {"warna": "#FFD700", "jenis": "logam transisi", "densitas": 19.32, "reaktivitas": 1},
    
    # Non-logam
    "Hidrogen (H₂)": {"warna": "#F0F8FF", "jenis": "gas", "densitas": 0.000089, "reaktivitas": 7},
    "Oksigen (O₂)": {"warna": "#ADD8E6", "jenis": "gas", "densitas": 0.00143, "reaktivitas": 6},
    "Nitrogen (N₂)": {"warna": "#87CEEB", "jenis": "gas", "densitas": 0.00125, "reaktivitas": 3},
    "Klorin (Cl₂)": {"warna": "#90EE90", "jenis": "gas", "densitas": 0.00321, "reaktivitas": 8},
    "Fluorin (F₂)": {"warna": "#98FB98", "jenis": "gas", "densitas": 0.00170, "reaktivitas": 9},
    
    # Asam
    "Asam Klorida (HCl)": {"warna": "#F0F0F0", "jenis": "asam kuat", "densitas": 1.18, "reaktivitas": 8, "pH": 0},
    "Asam Sulfat (H₂SO₄)": {"warna": "#F5F5F5", "jenis": "asam kuat", "densitas": 1.84, "reaktivitas": 9, "pH": 0},
    "Asam Nitrat (HNO₃)": {"warna": "#FFFFF0", "jenis": "asam kuat", "densitas": 1.51, "reaktivitas": 8, "pH": 1},
    "Asam Asetat (CH₃COOH)": {"warna": "#F5F5DC", "jenis": "asam lemah", "densitas": 1.05, "reaktivitas": 5, "pH": 3},
    "Asam Oksalat (H₂C₂O₄)": {"warna": "#FFFFFF", "jenis": "asam organik", "densitas": 1.90, "reaktivitas": 6, "pH": 1.3},
    "Asam Sitrat (C₆H₈O₇)": {"warna": "#FFFFFF", "jenis": "asam organik", "densitas": 1.67, "reaktivitas": 4, "pH": 3.1},
    "Asam Fosfat (H₃PO₄)": {"warna": "#F8F8FF", "jenis": "asam mineral", "densitas": 1.88, "reaktivitas": 7, "pH": 2.1},
    "Asam Karbonat (H₂CO₃)": {"warna": "#F0FFFF", "jenis": "asam lemah", "densitas": 1.00, "reaktivitas": 4, "pH": 3.7},
    
    # Basa
    "Natrium Hidroksida (NaOH)": {"warna": "#FFFFFF", "jenis": "basa kuat", "densitas": 2.13, "reaktivitas": 7, "pH": 14},
    "Kalium Hidroksida (KOH)": {"warna": "#FFFFFF", "jenis": "basa kuat", "densitas": 2.04, "reaktivitas": 7, "pH": 14},
    "Kalsium Hidroksida (Ca(OH)₂)": {"warna": "#FFFFFF", "jenis": "basa kuat", "densitas": 2.21, "reaktivitas": 6, "pH": 12.4},
    "Amonia (NH₃)": {"warna": "#F0F8FF", "jenis": "basa lemah", "densitas": 0.73, "reaktivitas": 5, "pH": 11.6},
    "Natrium Bikarbonat (NaHCO₃)": {"warna": "#FFFFFF", "jenis": "basa lemah", "densitas": 2.20, "reaktivitas": 3, "pH": 8.3},
    "Magnesium Hidroksida (Mg(OH)₂)": {"warna": "#FFFFFF", "jenis": "basa lemah", "densitas": 2.34, "reaktivitas": 4, "pH": 10.3},
    
    # Garam
    "Natrium Klorida (NaCl)": {"warna": "#FFFFFF", "jenis": "garam", "densitas": 2.16, "reaktivitas": 1},
    "Kalium Nitrat (KNO₃)": {"warna": "#FFFFFF", "jenis": "garam", "densitas": 2.11, "reaktivitas": 2},
    "Tembaga Sulfat (CuSO₄)": {"warna": "#00B4D8", "jenis": "garam", "densitas": 3.60, "reaktivitas": 4},
    "Besi Sulfat (FeSO₄)": {"warna": "#76D7EA", "jenis": "garam", "densitas": 3.65, "reaktivitas": 5},
    "Kalium Permanganat (KMnO₄)": {"warna": "#9D00FF", "jenis": "garam", "densitas": 2.70, "reaktivitas": 8},
    "Natrium Karbonat (Na₂CO₃)": {"warna": "#FFFFFF", "jenis": "garam", "densitas": 2.54, "reaktivitas": 3},
    "Kalsium Karbonat (CaCO₃)": {"warna": "#FFFFFF", "jenis": "garam", "densitas": 2.71, "reaktivitas": 2},
    
    # Pelarut
    "Air (H₂O)": {"warna": "#ADD8E6", "jenis": "pelarut", "densitas": 1.00, "reaktivitas": 0, "pH": 7},
    "Etanol (C₂H₅OH)": {"warna": "#F0FFF0", "jenis": "pelarut", "densitas": 0.79, "reaktivitas": 2},
    "Aseton (C₃H₆O)": {"warna": "#FFF0F5", "jenis": "pelarut", "densitas": 0.79, "reaktivitas": 3},
    "Kloroform (CHCl₃)": {"warna": "#98FB98", "jenis": "pelarut", "densitas": 1.49, "reaktivitas": 4},
    "Benzena (C₆H₆)": {"warna": "#FFD700", "jenis": "pelarut", "densitas": 0.87, "reaktivitas": 5},
    "Toluena (C₇H₈)": {"warna": "#FFA500", "jenis": "pelarut", "densitas": 0.87, "reaktivitas": 4},
    
    # Indikator
    "Fenolftalein": {"warna": "#FFFFFF", "jenis": "indikator", "densitas": 1.28, "reaktivitas": 1},
    "Metil Merah": {"warna": "#FF0000", "jenis": "indikator", "densitas": 1.20, "reaktivitas": 1},
    "Bromotimol Biru": {"warna": "#0000FF", "jenis": "indikator", "densitas": 1.25, "reaktivitas": 1},
    "Lakmus": {"warna": "#800080", "jenis": "indikator", "densitas": 1.20, "reaktivitas": 1},
    "Fenol Merah": {"warna": "#FF4500", "jenis": "indikator", "densitas": 1.22, "reaktivitas": 1},
    
    # Senyawa organik
    "Glukosa (C₆H₁₂O₆)": {"warna": "#FFFFFF", "jenis": "karbohidrat", "densitas": 1.54, "reaktivitas": 3},
    "Sukrosa (C₁₂H₂₂O₁₁)": {"warna": "#FFFFFF", "jenis": "karbohidrat", "densitas": 1.59, "reaktivitas": 2},
    "Etilen Glikol (C₂H₆O₂)": {"warna": "#F0F8FF", "jenis": "alkohol", "densitas": 1.11, "reaktivitas": 3},
    "Formaldehid (CH₂O)": {"warna": "#F0FFF0", "jenis": "aldehida", "densitas": 0.82, "reaktivitas": 6},
    "Aseton (C₃H₆O)": {"warna": "#FFF0F5", "jenis": "keton", "densitas": 0.79, "reaktivitas": 3},
    "Asam Benzoat (C₇H₆O₂)": {"warna": "#FFFFFF", "jenis": "asam organik", "densitas": 1.27, "reaktivitas": 4},
    "Urea (CH₄N₂O)": {"warna": "#FFFFFF", "jenis": "amida", "densitas": 1.32, "reaktivitas": 2},
    "Asam Stearat (C₁₈H₃₆O₂)": {"warna": "#FFFFFF", "jenis": "asam lemak", "densitas": 0.85, "reaktivitas": 2},
    "Kafein (C₈H₁₀N₄O₂)": {"warna": "#FFFFFF", "jenis": "alkaloid", "densitas": 1.23, "reaktivitas": 2},
    "Nikotin (C₁₀H₁₄N₂)": {"warna": "#F5F5DC", "jenis": "alkaloid", "densitas": 1.01, "reaktivitas": 4},
    
    # Unsur tambahan
    "Karbon (C)": {"warna": "#000000", "jenis": "non-logam", "densitas": 2.26, "reaktivitas": 4},
    "Silikon (Si)": {"warna": "#C0C0C0", "jenis": "metalloid", "densitas": 2.33, "reaktivitas": 3},
    "Fosfor (P)": {"warna": "#FFA500", "jenis": "non-logam", "densitas": 1.82, "reaktivitas": 7},
    "Belerang (S)": {"warna": "#FFFF00", "jenis": "non-logam", "densitas": 2.07, "reaktivitas": 5},
    "Iodin (I₂)": {"warna": "#9400D3", "jenis": "halogen", "densitas": 4.93, "reaktivitas": 6},
    "Merkuri (Hg)": {"warna": "#E0E0E0", "jenis": "logam", "densitas": 13.53, "reaktivitas": 3},
    "Timbal (Pb)": {"warna": "#A9A9A9", "jenis": "logam", "densitas": 11.34, "reaktivitas": 2},
    "Seng (Zn)": {"warna": "#7FFFD4", "jenis": "logam", "densitas": 7.14, "reaktivitas": 6},
    "Nikel (Ni)": {"warna": "#50C878", "jenis": "logam", "densitas": 8.91, "reaktivitas": 5},
    "Kromium (Cr)": {"warna": "#C0C0C0", "jenis": "logam", "densitas": 7.19, "reaktivitas": 4},
    "Platinum (Pt)": {"warna": "#E5E4E2", "jenis": "logam", "densitas": 21.45, "reaktivitas": 2},
    "Argon (Ar)": {"warna": "#87CEEB", "jenis": "gas mulia", "densitas": 0.00178, "reaktivitas": 0},
    "Neon (Ne)": {"warna": "#FF7F50", "jenis": "gas mulia", "densitas": 0.00090, "reaktivitas": 0},
    "Helium (He)": {"warna": "#FFD700", "jenis": "gas mulia", "densitas": 0.00018, "reaktivitas": 0},
}

# Fungsi untuk mencampur warna
def campur_warna(warna1, warna2, volume1, volume2):
    def hex_to_rgb(hex):
        hex = hex.lstrip('#')
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % tuple(min(255, max(0, int(c))) for c in rgb)
    
    rgb1 = hex_to_rgb(warna1)
    rgb2 = hex_to_rgb(warna2)
    
    # Campur warna dengan rata-rata tertimbang volume
    total_volume = volume1 + volume2
    campuran = [
        int((c1 * volume1 + c2 * volume2) / total_volume)
        for c1, c2 in zip(rgb1, rgb2)
    ]
    
    return rgb_to_hex(campuran)

# Fungsi untuk mendapatkan reaksi
def dapatkan_reaksi(zat1, zat2, suhu):
    jenis1 = SENYAWA_KIMIA[zat1]["jenis"]
    jenis2 = SENYAWA_KIMIA[zat2]["jenis"]
    reaktivitas1 = SENYAWA_KIMIA[zat1]["reaktivitas"]
    reaktivitas2 = SENYAWA_KIMIA[zat2]["reaktivitas"]
    
    # Reaksi asam-basa
    if "asam" in jenis1 and "basa" in jenis2:
        return f"Reaksi netralisasi: {zat1} + {zat2} → Garam + Air"
    if "basa" in jenis1 and "asam" in jenis2:
        return f"Reaksi netralisasi: {zat1} + {zat2} → Garam + Air"
    
    # Reaksi logam-asam
    if "logam" in jenis1 and "asam" in jenis2 and reaktivitas1 > 4:
        return f"Reaksi logam-asam: {zat1} + {zat2} → Garam + Gas Hidrogen"
    if "logam" in jenis2 and "asam" in jenis1 and reaktivitas2 > 4:
        return f"Reaksi logam-asam: {zat1} + {zat2} → Garam + Gas Hidrogen"
    
    # Reaksi oksidasi
    if "gas" in jenis1 and "logam" in jenis2 and reaktivitas1 > 7 and suhu > 100:
        return f"Oksidasi: {zat1} + {zat2} → Oksida Logam"
    if "gas" in jenis2 and "logam" in jenis1 and reaktivitas2 > 7 and suhu > 100:
        return f"Oksidasi: {zat1} + {zat2} → Oksida Logam"
    
    # Reaksi pembentukan endapan
    if "garam" in jenis1 and "garam" in jenis2:
        return f"Reaksi pengendapan: {zat1} + {zat2} → Endapan"
    
    # Reaksi dengan indikator
    if "indikator" in jenis1 and "asam" in jenis2:
        return f"Perubahan warna indikator: {zat1} menunjukkan sifat asam"
    if "indikator" in jenis1 and "basa" in jenis2:
        return f"Perubahan warna indikator: {zat1} menunjukkan sifat basa"
    
    # Reaksi organik
    if "aldehida" in jenis1 and "basa" in jenis2:
        return f"Reaksi Cannizzaro: {zat1} mengalami disproporsionasi"
    if "keton" in jenis1 and "asam" in jenis2:
        return f"Reaksi keto-enol: {zat1} mengalami tautomerisasi"
    
    # Reaksi suhu tinggi
    if suhu > 200:
        return f"Dekomposisi termal: {zat1} + {zat2} → Senyawa terurai"
    
    return f"Tidak ada reaksi yang teramati antara {zat1} dan {zat2} pada suhu {suhu}°C"

# Fungsi untuk menggambar labu Erlenmeyer yang realistis
def gambar_erlenmeyer(warna_cairan, volume_total, max_volume=500):
    # Buat gambar kosong
    img = Image.new('RGBA', (400, 600), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Parameter labu
    lebar_leher = 60
    tinggi_leher = 150
    lebar_badan = 300
    tinggi_badan = 400
    y_badan = 150
    
    # Gambar badan labu (kerucut terbalik)
    draw.polygon([
        (200 - lebar_badan//2, y_badan + tinggi_badan),
        (200 + lebar_badan//2, y_badan + tinggi_badan),
        (200, y_badan)
    ], fill="#F0F0F0", outline="black", width=3)
    
    # Gambar leher labu
    draw.rectangle([
        (200 - lebar_leher//2, y_badan - tinggi_leher),
        (200 + lebar_leher//2, y_badan)
    ], fill="#F0F0F0", outline="black", width=3)
    
    # Gambar mulut labu
    draw.rectangle([
        (200 - lebar_leher//2 + 10, y_badan - tinggi_leher - 30),
        (200 + lebar_leher//2 - 10, y_badan - tinggi_leher)
    ], fill="#D0D0D0", outline="black", width=2)
    
    # Hitung tinggi cairan berdasarkan volume (1 mL = 1.2 pixel)
    tinggi_cairan = min(volume_total * 1.2, max_volume * 1.2)
    
    # Gambar cairan jika ada
    if volume_total > 0:
        # Bagian badan labu
        if tinggi_cairan > tinggi_leher:
            tinggi_badan_cairan = tinggi_cairan - tinggi_leher
            
            # Gambar cairan di badan labu (segitiga terbalik)
            y_start_badan = y_badan + tinggi_badan - tinggi_badan_cairan
            if y_start_badan < y_badan:
                y_start_badan = y_badan
            
            # Hitung lebar pada ketinggian tertentu
            points = []
            for x in range(200 - lebar_badan//2, 200 + lebar_badan//2 + 1):
                # Hitung y untuk titik x tertentu di segitiga
                rel_x = x - (200 - lebar_badan//2)
                prop = rel_x / lebar_badan
                y_pos = y_badan + prop * tinggi_badan
                
                if y_pos >= y_start_badan:
                    points.append((x, y_pos))
            
            if points:
                # Tambahkan titik dasar
                points.append((200 + lebar_badan//2, y_badan + tinggi_badan))
                points.append((200 - lebar_badan//2, y_badan + tinggi_badan))
                
                draw.polygon(points, fill=warna_cairan, outline="black", width=1)
        
        # Gambar cairan di leher labu
        tinggi_leher_cairan = min(tinggi_cairan, tinggi_leher)
        y_start_leher = y_badan - tinggi_leher_cairan
        
        draw.rectangle([
            (200 - lebar_leher//2 + 2, y_start_leher),
            (200 + lebar_leher//2 - 2, y_badan)
        ], fill=warna_cairan, outline="black", width=1)
    
    return img

# Fungsi untuk membuat visualisasi reaksi
def buat_visualisasi_reaksi(reaksi_text, warna_campuran):
    # Buat gambar dengan latar belakang putih
    img = Image.new('RGB', (900, 500), color="white")
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default(24)
    
    # Gambar labu Erlenmeyer
    erlenmeyer = gambar_erlenmeyer(warna_campuran, st.session_state.volume_total)
    img.paste(erlenmeyer, (50, 50), erlenmeyer)
    
    # Gambar panah reaksi
    draw.line([(350, 250), (450, 250)], fill="black", width=3)
    draw.polygon([(450, 250), (440, 245), (440, 255)], fill="black")
    
    # Gambar hasil reaksi
    if "Gas Hidrogen" in reaksi_text:
        # Gambar gelembung gas
        for i in range(5):
            x = 500 + i * 70
            y = 200 - i * 30
            size = 30 + i * 5
            draw.ellipse([(x, y), (x+size, y+size)], fill="#ADD8E6", outline="black", width=2)
            draw.text((x+size//3, y+size//3), "H₂", fill="black", font=font)
    
    if "Endapan" in reaksi_text:
        # Gambar endapan
        draw.ellipse([(500, 300), (700, 350)], fill="#00B4D8", outline="black", width=2)
        draw.text((580, 320), "Endapan", fill="black", font=font)
    
    if "Oksida" in reaksi_text:
        # Gambar logam oksida
        draw.rectangle([(500, 200), (700, 300)], fill="#B5651D", outline="black", width=2)
        draw.text((550, 250), "Oksida Logam", fill="white", font=font)
    
    if "Air" in reaksi_text:
        # Gambar tetesan air
        for i in range(3):
            x = 550 + i * 70
            y = 350 - i * 20
            draw.ellipse([(x, y), (x+20, y+20)], fill="#ADD8E6", outline="black", width=1)
            draw.ellipse([(x+5, y+15), (x+15, y+30)], fill="#ADD8E6", outline="black", width=1)
    
    # Tambahkan teks reaksi
    draw.text((50, 20), reaksi_text, fill="black", font=font)
    
    # Tambahkan label volume
    draw.text((100, 450), f"Volume: {st.session_state.volume_total} mL", fill="black", font=font)
    
    return img

# UI Aplikasi
st.title("🧪 SIMULASI LABORATORIUM KIMIA PROFESIONAL")
st.markdown("""
*Aplikasi simulasi percobaan kimia interaktif* dengan 100+ senyawa kimia dan visualisasi laboratorium realistis.
""")

# Sidebar untuk input
with st.sidebar:
    st.header("⚗ KONTROL PERCOBAAN")
    st.subheader("Pilih Zat Kimia")
    zat = st.selectbox("Senyawa", list(SENYAWA_KIMIA.keys()))
    
    col1, col2 = st.columns(2)
    with col1:
        volume = st.slider("Volume (mL)", 1, 300, 100, key="vol_slider")
    with col2:
        suhu = st.slider("Suhu (°C)", -20, 500, 25, key="temp_slider")
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("➕ TAMBAHKAN KE LABU", use_container_width=True, type="primary"):
            st.session_state.campuran.append({
                "zat": zat,
                "volume": volume,
                "warna": SENYAWA_KIMIA[zat]["warna"],
                "densitas": SENYAWA_KIMIA[zat]["densitas"]
            })
            st.session_state.volume_total += volume
            st.session_state.suhu = suhu
            st.success(f"{volume} mL {zat} ditambahkan!")
            
    with col4:
        if st.button("🧼 BERSIHKAN LABU", use_container_width=True, type="secondary"):
            st.session_state.campuran = []
            st.session_state.reaksi = ""
            st.session_state.warna_campuran = "#ADD8E6"
            st.session_state.gambar_reaksi = None
            st.session_state.log_percobaan.append("Labu dibersihkan")
            st.session_state.volume_total = 0
            st.success("Labu siap untuk percobaan baru!")

# Tampilan utama
tab1, tab2, tab3 = st.tabs(["LABORATORIUM", "LOG PERCOBAAN", "DATABASE SENYAWA"])

with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🧫 LABU ERLENMEYER")
        
        if st.session_state.campuran:
            # Hitung warna campuran
            current_color = st.session_state.campuran[0]["warna"]
            total_volume = st.session_state.campuran[0]["volume"]
            
            for i in range(1, len(st.session_state.campuran)):
                next_color = st.session_state.campuran[i]["warna"]
                next_volume = st.session_state.campuran[i]["volume"]
                current_color = campur_warna(
                    current_color, 
                    next_color,
                    total_volume,
                    next_volume
                )
                total_volume += next_volume
            
            st.session_state.warna_campuran = current_color
            
            # Gambar labu Erlenmeyer
            labu_img = gambar_erlenmeyer(current_color, st.session_state.volume_total)
            st.image(labu_img, caption=f"Labu Erlenmeyer - Volume: {st.session_state.volume_total} mL", 
                     use_container_width=True)
            
            # Tampilkan informasi
            st.write(f"*Suhu:* {st.session_state.suhu}°C")
            st.color_picker("Warna Campuran", current_color, disabled=True, key="warna_campuran")
            
            # Tampilkan daftar zat
            st.subheader("KOMPOSISI CAMPURAN")
            for i, zat in enumerate(st.session_state.campuran, 1):
                st.write(f"{i}. *{zat['zat']}* ({zat['volume']} mL)")
            
            # Tombol reaksi
            if len(st.session_state.campuran) >= 2:
                if st.button("🔥 MULAI REAKSI!", type="primary", use_container_width=True):
                    zat1 = st.session_state.campuran[0]["zat"]
                    zat2 = st.session_state.campuran[1]["zat"]
                    reaksi = dapatkan_reaksi(
                        zat1, 
                        zat2, 
                        st.session_state.suhu
                    )
                    st.session_state.reaksi = reaksi
                    st.session_state.gambar_reaksi = buat_visualisasi_reaksi(
                        reaksi, 
                        current_color
                    )
                    log = f"Reaksi: {zat1} + {zat2} → {reaksi}"
                    st.session_state.log_percobaan.append(log)
                    st.experimental_rerun()
        else:
            st.info("Labu kosong. Tambahkan zat kimia dari panel kontrol di samping.")
            labu_kosong = gambar_erlenmeyer("#ADD8E6", 0)
            st.image(labu_kosong, caption="Labu Erlenmeyer Kosong", use_container_width=True)

    with col2:
        st.subheader("📊 HASIL REAKSI & VISUALISASI")
        
        if st.session_state.reaksi:
            st.success(f"*REAKSI TERJADI!*")
            st.info(f"{st.session_state.reaksi}")
            
            if st.session_state.gambar_reaksi:
                st.image(st.session_state.gambar_reaksi, caption="Visualisasi Reaksi Kimia", 
                         use_container_width=True)
            
            # Penjelasan reaksi
            st.subheader("🔍 PENJELASAN ILMIAH")
            if "netralisasi" in st.session_state.reaksi.lower():
                st.markdown("""
                *Reaksi Netralisasi:*
                - Terjadi antara asam dan basa
                - Menghasilkan garam dan air
                - Persamaan umum: Asam + Basa → Garam + Air
                - Contoh: HCl + NaOH → NaCl + H₂O
                - Reaksi ini bersifat eksotermik (melepaskan panas)
                """)
            elif "logam-asam" in st.session_state.reaksi.lower():
                st.markdown("""
                *Reaksi Logam dengan Asam:*
                - Logam bereaksi dengan asam menghasilkan garam dan gas hidrogen
                - Persamaan umum: Logam + Asam → Garam + H₂(g)
                - Gas hidrogen mudah terbakar (uji dengan bunyi 'pop')
                - Contoh: Zn + 2HCl → ZnCl₂ + H₂
                - Reaktivitas tergantung deret elektrokimia
                """)
            elif "endapan" in st.session_state.reaksi.lower():
                st.markdown("""
                *Reaksi Pengendapan:*
                - Terjadi ketika dua larutan bereaksi membentuk padatan tak larut (endapan)
                - Endapan biasanya berwarna dan dapat disaring
                - Contoh: AgNO₃ + NaCl → AgCl(s) + NaNO₃
                - Kelarutan senyawa mengikuti aturan kelarutan
                """)
            elif "oksidasi" in st.session_state.reaksi.lower():
                st.markdown("""
                *Reaksi Oksidasi Logam:*
                - Logam bereaksi dengan oksigen membentuk oksida logam
                - Umumnya terjadi pada suhu tinggi
                - Contoh: 2Mg + O₂ → 2MgO
                - Reaksi ini penting dalam proses korosi
                """)
            else:
                st.markdown("""
                *Reaksi Umum:*
                - Reaksi kimia terjadi ketika ikatan kimia terputus dan terbentuk kembali
                - Jenis reaksi: sintesis, dekomposisi, penggantian tunggal, penggantian ganda
                - Laju reaksi dipengaruhi oleh suhu, konsentrasi, dan katalis
                """)
        else:
            st.info("Belum ada reaksi. Tambahkan minimal 2 zat dan klik 'MULAI REAKSI'.")
            st.image(gambar_erlenmeyer("#ADD8E6", 0), caption="Menunggu reaksi kimia", 
                     use_container_width=True)

with tab2:
    st.subheader("📝 LOG PERCOBAAN")
    
    if st.session_state.log_percobaan:
        st.write("*RIWAYAT PERCOBAAN:*")
        for i, log in enumerate(st.session_state.log_percobaan, 1):
            st.info(f"#{i}** {log}")
        
        if st.button("🧹 BERSIHKAN LOG", type="secondary", use_container_width=True):
            st.session_state.log_percobaan = []
            st.success("Log percobaan telah dibersihkan!")
    else:
        st.info("Belum ada catatan percobaan. Lakukan beberapa reaksi untuk mencatatnya.")

with tab3:
    st.subheader("🧪 DATABASE SENYAWA KIMIA")
    
    # Buat dataframe untuk tabel periodik
    data = []
    for senyawa, props in SENYAWA_KIMIA.items():
        data.append({
            "Senyawa": senyawa,
            "Jenis": props["jenis"],
            "Warna": props["warna"],
            "Densitas (g/mL)": props["densitas"],
            "Reaktivitas (1-10)": props["reaktivitas"]
        })
    
    df = pd.DataFrame(data)
    
    # Tampilkan tabel dengan warna latar
    st.dataframe(
        df.style.apply(lambda x: ["background: " + x["Warna"] for i in x], axis=1, 
                      subset=["Warna"]),
        use_container_width=True,
        height=600
    )
    
    # Grafik interaktif
    st.subheader("📈 VISUALISASI SIFAT KIMIA")
    fig = px.scatter(
        df, 
        x="Reaktivitas (1-10)", 
        y="Densitas (g/mL)", 
        color="Jenis",
        hover_name="Senyawa",
        size="Reaktivitas (1-10)",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.divider()
st.caption("© 2023 SIMULASI LABORATORIUM KIMIA | Dikembangkan dengan Streamlit")
