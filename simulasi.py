import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import plotly.express as px
import plotly.graph_objects as go

# Konfigurasi halaman
st.set_page_config(
    page_title="Simulasi Laboratorium Kimia Profesional",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi state
def init_state():
    if 'campuran' not in st.session_state:
        st.session_state.campuran = []
    if 'reaksi' not in st.session_state:
        st.session_state.reaksi = ""
    if 'warna' not in st.session_state:
        st.session_state.warna = "#FFFFFF"
    if 'suhu' not in st.session_state:
        st.session_state.suhu = 25
    if 'gambar_reaksi' not in st.session_state:
        st.session_state.gambar_reaksi = None
    if 'log_percobaan' not in st.session_state:
        st.session_state.log_percobaan = []
    if 'volume_total' not in st.session_state:
        st.session_state.volume_total = 0

init_state()

# Database senyawa kimia lengkap (50+ senyawa)
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
    "Asam Klorida (HCl)": {"warna": "#FFFFFF", "jenis": "asam kuat", "densitas": 1.18, "reaktivitas": 8, "pH": 0},
    "Asam Sulfat (H₂SO₄)": {"warna": "#F5F5F5", "jenis": "asam kuat", "densitas": 1.84, "reaktivitas": 9, "pH": 0},
    "Asam Nitrat (HNO₃)": {"warna": "#FFFFF0", "jenis": "asam kuat", "densitas": 1.51, "reaktivitas": 8, "pH": 1},
    "Asam Asetat (CH₃COOH)": {"warna": "#F5F5DC", "jenis": "asam lemah", "densitas": 1.05, "reaktivitas": 5, "pH": 3},
    
    # Basa
    "Natrium Hidroksida (NaOH)": {"warna": "#FFFFFF", "jenis": "basa kuat", "densitas": 2.13, "reaktivitas": 7, "pH": 14},
    "Kalium Hidroksida (KOH)": {"warna": "#FFFFFF", "jenis": "basa kuat", "densitas": 2.04, "reaktivitas": 7, "pH": 14},
    "Kalsium Hidroksida (Ca(OH)₂)": {"warna": "#FFFFFF", "jenis": "basa kuat", "densitas": 2.21, "reaktivitas": 6, "pH": 12},
    "Amonia (NH₃)": {"warna": "#F0F8FF", "jenis": "basa lemah", "densitas": 0.73, "reaktivitas": 5, "pH": 11},
    
    # Garam
    "Natrium Klorida (NaCl)": {"warna": "#FFFFFF", "jenis": "garam", "densitas": 2.16, "reaktivitas": 1},
    "Kalium Nitrat (KNO₃)": {"warna": "#FFFFFF", "jenis": "garam", "densitas": 2.11, "reaktivitas": 2},
    "Tembaga Sulfat (CuSO₄)": {"warna": "#00B4D8", "jenis": "garam", "densitas": 3.60, "reaktivitas": 4},
    "Besi Sulfat (FeSO₄)": {"warna": "#76D7EA", "jenis": "garam", "densitas": 3.65, "reaktivitas": 5},
    
    # Pelarut
    "Air (H₂O)": {"warna": "#ADD8E6", "jenis": "pelarut", "densitas": 1.00, "reaktivitas": 0, "pH": 7},
    "Etanol (C₂H₅OH)": {"warna": "#F0FFF0", "jenis": "pelarut", "densitas": 0.79, "reaktivitas": 2},
    "Aseton (C₃H₆O)": {"warna": "#FFF0F5", "jenis": "pelarut", "densitas": 0.79, "reaktivitas": 3},
    
    # Indikator
    "Fenolftalein": {"warna": "#FFFFFF", "jenis": "indikator", "densitas": 1.28, "reaktivitas": 1},
    "Metil Merah": {"warna": "#FF0000", "jenis": "indikator", "densitas": 1.20, "reaktivitas": 1},
    "Bromotimol Biru": {"warna": "#0000FF", "jenis": "indikator", "densitas": 1.25, "reaktivitas": 1},
    
    # Senyawa organik
    "Glukosa (C₆H₁₂O₆)": {"warna": "#FFFFFF", "jenis": "karbohidrat", "densitas": 1.54, "reaktivitas": 3},
    "Sukrosa (C₁₂H₂₂O₁₁)": {"warna": "#FFFFFF", "jenis": "karbohidrat", "densitas": 1.59, "reaktivitas": 2},
    "Asam Sitrat (C₆H₈O₇)": {"warna": "#FFFFFF", "jenis": "asam organik", "densitas": 1.67, "reaktivitas": 4},
    "Etilen Glikol (C₂H₆O₂)": {"warna": "#F0F8FF", "jenis": "alkohol", "densitas": 1.11, "reaktivitas": 3},
    
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
    "Kromium (Cr)": {"warna": "#C0C0C0", "jenis": "logam", "densitas": 7.19, "reaktivitas": 4}
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
    
    # Reaksi suhu tinggi
    if suhu > 200:
        return f"Dekomposisi termal: {zat1} + {zat2} → Senyawa terurai"
    
    return f"Tidak ada reaksi yang teramati antara {zat1} dan {zat2} pada suhu {suhu}°C"

# Fungsi untuk menggambar labu Erlenmeyer
def gambar_erlenmeyer(warna_cairan, volume_total, max_volume=300):
    # Tinggi cairan berdasarkan volume (asumsi: 1mL = 1px tinggi)
    tinggi_cairan = min(volume_total, max_volume)
    
    # Buat gambar kosong
    img = Image.new('RGBA', (400, 500), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Gambar labu Erlenmeyer
    # Leher labu
    draw.rectangle([(180, 50), (220, 200)], fill="#E0E0E0", outline="black", width=2)
    
    # Badan labu (segitiga terbalik)
    draw.polygon([(100, 200), (300, 200), (200, 450)], fill="#E0E0E0", outline="black", width=2)
    
    # Cairan dalam labu
    if volume_total > 0:
        # Hitung posisi cairan
        y_start = 200 - tinggi_cairan
        if y_start < 50:  # Jika melebihi leher labu
            # Cairan di leher labu
            draw.rectangle([(180, max(50, y_start)), (220, 200)], fill=warna_cairan, outline="black", width=1)
            
            # Cairan di badan labu
            if y_start < 200:
                # Hitung koordinat segitiga terbalik untuk cairan
                points = []
                base_y = 200
                for x in range(100, 301):
                    # Hitung y untuk titik x tertentu di segitiga
                    if x < 200:
                        y_tri = 200 + (x - 100) * 250 / 100
                    else:
                        y_tri = 200 + (300 - x) * 250 / 100
                    
                    if base_y - tinggi_cairan < y_tri:
                        points.append((x, base_y - tinggi_cairan))
                
                if points:
                    points.append((300, 200))
                    points.append((100, 200))
                    draw.polygon(points, fill=warna_cairan, outline="black", width=1)
        else:
            # Cairan hanya di leher labu
            draw.rectangle([(180, y_start), (220, 200)], fill=warna_cairan, outline="black", width=1)
    
    # Gambar dasar
    draw.ellipse([(150, 450), (250, 460)], fill="gray", outline="black", width=1)
    
    return img

# Fungsi untuk membuat visualisasi reaksi
def buat_visualisasi_reaksi(reaksi_text, warna_campuran):
    # Buat gambar dengan latar belakang putih
    img = Image.new('RGB', (800, 400), color="white")
    draw = ImageDraw.Draw(img)
    
    # Gambar labu Erlenmeyer
    erlenmeyer = gambar_erlenmeyer(warna_campuran, st.session_state.volume_total)
    img.paste(erlenmeyer, (50, 50), erlenmeyer)
    
    # Gambar panah reaksi
    draw.line([(350, 250), (450, 250)], fill="black", width=3)
    draw.polygon([(450, 250), (440, 245), (440, 255)], fill="black")
    
    # Gambar hasil reaksi (misal: gelembung gas, endapan, dll)
    if "Gas Hidrogen" in reaksi_text:
        # Gambar gelembung gas
        for i in range(5):
            x = 500 + i * 50
            y = 200 - i * 20
            draw.ellipse([(x, y), (x+30, y+30)], fill="#ADD8E6", outline="black")
            draw.text((x+10, y+10), "H₂", fill="black", font=ImageFont.load_default(20))
    
    if "Endapan" in reaksi_text:
        # Gambar endapan
        draw.ellipse([(500, 300), (700, 350)], fill="#00B4D8", outline="black")
        draw.text((550, 320), "Endapan", fill="black", font=ImageFont.load_default(20))
    
    if "Oksida" in reaksi_text:
        # Gambar logam oksida
        draw.rectangle([(500, 200), (700, 300)], fill="#B5651D", outline="black")
        draw.text((550, 250), "Oksida Logam", fill="white", font=ImageFont.load_default(20))
    
    # Tambahkan teks reaksi
    draw.text((50, 20), reaksi_text, fill="black", font=ImageFont.load_default(24))
    
    return img

# UI Aplikasi
st.title("🧪 Simulasi Laboratorium Kimia Profesional")
st.markdown("""
*Aplikasi ini mensimulasikan percampuran zat kimia di laboratorium.*
Tambahkan zat ke dalam labu Erlenmeyer, atur suhu, dan lihat reaksi yang terjadi!
""")

# Sidebar untuk input
with st.sidebar:
    st.header("⚗ Kontrol Percobaan")
    zat = st.selectbox("Pilih Zat Kimia", list(SENYAWA_KIMIA.keys()))
    volume = st.slider("Volume (mL)", 1, 300, 100)
    suhu = st.slider("Suhu (°C)", -20, 500, 25)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Tambahkan ke Labu", use_container_width=True):
            st.session_state.campuran.append({
                "zat": zat,
                "volume": volume,
                "warna": SENYAWA_KIMIA[zat]["warna"],
                "densitas": SENYAWA_KIMIA[zat]["densitas"]
            })
            st.session_state.volume_total += volume
            st.session_state.suhu = suhu
            st.success(f"{volume}mL {zat} ditambahkan!")
            
    with col2:
        if st.button("🧼 Bersihkan Labu", use_container_width=True, type="primary"):
            st.session_state.campuran = []
            st.session_state.reaksi = ""
            st.session_state.warna = "#FFFFFF"
            st.session_state.gambar_reaksi = None
            st.session_state.log_percobaan.append("Labu dibersihkan")
            st.session_state.volume_total = 0
            st.success("Labu siap untuk percobaan baru!")

# Tampilan utama
tab1, tab2, tab3 = st.tabs(["Lab Percobaan", "Log Eksperimen", "Tabel Periodik"])

with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🧫 Labu Erlenmeyer")
        
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
            
            st.session_state.warna = current_color
            
            # Gambar labu Erlenmeyer
            labu_img = gambar_erlenmeyer(current_color, st.session_state.volume_total)
            st.image(labu_img, caption=f"Volume: {st.session_state.volume_total}mL", use_column_width=True)
            
            # Tampilkan informasi
            st.write(f"*Suhu:* {st.session_state.suhu}°C")
            st.color_picker("Warna Campuran", current_color, disabled=True)
            
            # Tampilkan daftar zat
            st.write("*Komposisi:*")
            for i, zat in enumerate(st.session_state.campuran, 1):
                st.write(f"{i}. {zat['zat']} ({zat['volume']}mL)")
            
            # Tombol reaksi
            if len(st.session_state.campuran) >= 2:
                if st.button("🔥 Mulai Reaksi!", type="primary", use_container_width=True):
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
        else:
            st.info("Labu kosong. Tambahkan zat kimia dari panel kontrol di samping.")
            st.image(gambar_erlenmeyer("#FFFFFF", 0), caption="Labu kosong", use_column_width=True)

    with col2:
        st.subheader("📊 Hasil Reaksi & Visualisasi")
        
        if st.session_state.reaksi:
            st.success(f"*Reaksi Terjadi!*")
            st.info(f"{st.session_state.reaksi}")
            
            if st.session_state.gambar_reaksi:
                st.image(st.session_state.gambar_reaksi, caption="Visualisasi Reaksi", use_column_width=True)
            
            # Penjelasan reaksi
            st.subheader("🔍 Penjelasan Ilmiah")
            if "netralisasi" in st.session_state.reaksi.lower():
                st.markdown("""
                *Reaksi Netralisasi:*
                - Terjadi antara asam dan basa
                - Menghasilkan garam dan air
                - Persamaan umum: Asam + Basa → Garam + Air
                - Contoh: HCl + NaOH → NaCl + H₂O
                """)
            elif "logam-asam" in st.session_state.reaksi.lower():
                st.markdown("""
                *Reaksi Logam dengan Asam:*
                - Logam bereaksi dengan asam menghasilkan garam dan gas hidrogen
                - Persamaan umum: Logam + Asam → Garam + H₂(g)
                - Gas hidrogen mudah terbakar
                - Contoh: Zn + 2HCl → ZnCl₂ + H₂
                """)
            elif "endapan" in st.session_state.reaksi.lower():
                st.markdown("""
                *Reaksi Pengendapan:*
                - Terjadi ketika dua larutan bereaksi membentuk padatan tak larut
                - Endapan biasanya berwarna dan dapat disaring
                - Contoh: AgNO₃ + NaCl → AgCl(s) + NaNO₃
                """)
            elif "oksidasi" in st.session_state.reaksi.lower():
                st.markdown("""
                *Reaksi Oksidasi Logam:*
                - Logam bereaksi dengan oksigen membentuk oksida logam
                - Umumnya terjadi pada suhu tinggi
                - Contoh: 2Mg + O₂ → 2MgO
                """)
        else:
            st.info("Belum ada reaksi. Tambahkan minimal 2 zat dan klik 'Mulai Reaksi'.")
            st.image(gambar_erlenmeyer("#FFFFFF", 0), caption="Menunggu reaksi", use_column_width=True)

with tab2:
    st.subheader("📝 Log Percobaan")
    
    if st.session_state.log_percobaan:
        st.write("*Riwayat Percobaan:*")
        for i, log in enumerate(st.session_state.log_percobaan, 1):
            st.code(f"{i}. {log}")
        
        if st.button("🧹 Bersihkan Log", type="secondary"):
            st.session_state.log_percobaan = []
            st.success("Log percobaan telah dibersihkan!")
    else:
        st.info("Belum ada catatan percobaan. Lakukan beberapa reaksi untuk mencatatnya.")

with tab3:
    st.subheader("🧪 Tabel Periodik Interaktif")
    
    # Buat dataframe untuk tabel periodik
    data = []
    for senyawa, props in SENYAWA_KIMIA.items():
        data.append({
            "Senyawa": senyawa,
            "Jenis": props["jenis"],
            "Warna": props["warna"],
            "Densitas": props["densitas"],
            "Reaktivitas": props["reaktivitas"]
        })
    
    df = pd.DataFrame(data)
    
    # Tampilkan tabel dengan warna latar
    st.dataframe(
        df.style.applymap(lambda x: f"background-color: {x}", subset=["Warna"]),
        use_container_width=True
    )
    
    # Grafik interaktif
    st.subheader("📈 Visualisasi Sifat Kimia")
    fig = px.scatter(
        df, 
        x="Reaktivitas", 
        y="Densitas", 
        color="Jenis",
        hover_name="Senyawa",
        size="Densitas",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.divider()
st.caption("© 2023 Simulasi Laboratorium Kimia | Dibuat dengan Streamlit")
