import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw
import io
import base64
import random

# Konfigurasi halaman
st.set_page_config(
    page_title="Lab Kimia Interaktif",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tema warna
primary_color = "#FF6B6B"
secondary_color = "#4ECDC4"
accent_color = "#FFD166"
background_color = "#F7FFF7"
dark_color = "#1A535C"
text_color = "#333333"  # Warna teks baru untuk kontras

# CSS untuk styling
st.markdown(f"""
<style>
    /* Warna utama */
    .stApp {{
        background: linear-gradient(135deg, {background_color}, #E0F7E0);
        background-attachment: fixed;
    }}
    .css-1d391kg, .st-b7, .st-b8, .st-b9 {{
        background-color: transparent !important;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {dark_color} !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}
    p, div, span, li, td {{
        color: {text_color} !important;
    }}
    .stButton>button {{
        background: linear-gradient(to right, {primary_color}, {accent_color}) !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 12px 28px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }}
    .stButton>button:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3) !important;
    }}
    .stSelectbox>div>div {{
        background-color: white !important;
        border-radius: 15px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }}
    .stSlider>div>div>div {{
        background: linear-gradient(to right, {accent_color}, {secondary_color}) !important;
    }}
    .stTabs>div>div>div>div {{
        background: linear-gradient(135deg, {secondary_color}, {primary_color}) !important;
        color: white !important;
        border-radius: 15px 15px 0 0 !important;
        padding: 12px 24px !important;
        font-weight: bold;
        margin: 0 5px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    .stTabs>div>div>div>div[aria-selected="true"] {{
        background: linear-gradient(135deg, {primary_color}, {accent_color}) !important;
        transform: scale(1.05);
        z-index: 1;
    }}
    .stDataFrame {{
        border-radius: 15px !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1) !important;
        overflow: hidden;
    }}
    .stAlert {{
        border-radius: 15px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }}
    .element-card {{
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin: 15px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        transition: all 0.4s ease;
        height: 100%;
        border: 2px solid {secondary_color};
    }}
    .element-card:hover {{
        transform: translateY(-10px) rotate(2deg);
        box-shadow: 0 12px 24px rgba(0,0,0,0.2);
        border: 2px solid {primary_color};
    }}
    .reaction-container {{
        background: white;
        border-radius: 25px;
        padding: 30px;
        margin: 25px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        border: 3px solid {accent_color};
        background-image: radial-gradient(circle at top right, rgba(255,255,255,0.8), rgba(255,255,255,0.4));
    }}
    .color-box {{
        width: 100%;
        height: 180px;
        border-radius: 20px;
        margin: 20px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 28px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        box-shadow: inset 0 0 20px rgba(0,0,0,0.2), 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        border: 2px solid white;
    }}
    .color-box:hover {{
        transform: scale(1.03);
        box-shadow: inset 0 0 30px rgba(0,0,0,0.3), 0 6px 12px rgba(0,0,0,0.3);
    }}
    .warning-badge {{
        background: linear-gradient(135deg, #FFD166, #FF9E6D);
        color: {dark_color};
        border-radius: 50px;
        padding: 8px 20px;
        margin: 10px;
        display: inline-block;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}
    .apd-badge {{
        background: linear-gradient(135deg, {secondary_color}, #118AB2);
        color: white;
        border-radius: 50px;
        padding: 8px 20px;
        margin: 10px;
        display: inline-block;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}
    .periodic-header {{
        background: linear-gradient(135deg, {dark_color}, #073B4C);
        padding: 25px;
        border-radius: 20px;
        color: white;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }}
    .chemical-equation {{
        font-family: 'Courier New', monospace;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 2px dashed {accent_color};
        color: {text_color};
    }}
    .bubble {{
        position: absolute;
        border-radius: 50%;
        background: rgba(255,255,255,0.3);
        animation: float 15s infinite ease-in-out;
    }}
    @keyframes float {{
        0% {{ transform: translateY(0) translateX(0) rotate(0); opacity: 0; }}
        10% {{ opacity: 1; }}
        90% {{ opacity: 0.8; }}
        100% {{ transform: translateY(-1000px) translateX(200px) rotate(360deg); opacity: 0; }}
    }}
    .compatibility-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
    }}
    .compatibility-table th, .compatibility-table td {{
        padding: 12px 15px;
        text-align: center;
        border: 1px solid #ddd;
    }}
    .compatibility-table th {{
        background-color: {dark_color};
        color: white;
        font-weight: bold;
    }}
    .compatibility-table tr:nth-child(even) {{
        background-color: #f8f9fa;
    }}
    .compatibility-table tr:hover {{
        background-color: #e9ecef;
    }}
    .compatibility-table .compatible {{
        background-color: #d4edda;
        color: #155724;
        font-weight: bold;
    }}
    .compatibility-table .incompatible {{
        background-color: #f8d7da;
        color: #721c24;
        font-weight: bold;
    }}
    .compatibility-table .conditional {{
        background-color: #fff3cd;
        color: #856404;
        font-weight: bold;
    }}
    .hazard-symbol {{
        font-size: 36px;
        margin-right: 15px;
        display: inline-block;
        width: 60px;
        text-align: center;
    }}
</style>
""", unsafe_allow_html=True)

# Animasi gelembung
st.markdown("""
<script>
function createBubble() {
    const bubble = document.createElement('div');
    bubble.classList.add('bubble');
    
    const size = Math.random() * 100 + 50;
    bubble.style.width = ${size}px;
    bubble.style.height = ${size}px;
    
    const posX = Math.random() * window.innerWidth;
    bubble.style.left = ${posX}px;
    bubble.style.bottom = -100px;
    
    const animationDuration = Math.random() * 20 + 10;
    bubble.style.animationDuration = ${animationDuration}s;
    
    document.body.appendChild(bubble);
    
    setTimeout(() => {
        bubble.remove();
    }, animationDuration * 1000);
}

// Create bubbles every 1.5 seconds
setInterval(createBubble, 1500);
</script>
""", unsafe_allow_html=True)

# Database tabel periodik (118 unsur lengkap)
PERIODIC_TABLE = [
    # Periode 1
    {"Symbol": "H", "Name": "Hidrogen", "AtomicNumber": 1, "AtomicMass": 1.008, 
     "Group": 1, "Period": 1, "Category": "Nonlogam", "Color": "#FF6B6B", "Electronegativity": 2.20, "Hazards": ["Mudah Terbakar"]},
    {"Symbol": "He", "Name": "Helium", "AtomicNumber": 2, "AtomicMass": 4.0026, 
     "Group": 18, "Period": 1, "Category": "Gas Mulia", "Color": "#4ECDC4", "Electronegativity": None, "Hazards": []},
    
    # Periode 2
    {"Symbol": "Li", "Name": "Litium", "AtomicNumber": 3, "AtomicMass": 6.94, 
     "Group": 1, "Period": 2, "Category": "Logam Alkali", "Color": "#FFD166", "Electronegativity": 0.98, "Hazards": ["Mudah Terbakar", "Reaktif"]},
    {"Symbol": "Be", "Name": "Berilium", "AtomicNumber": 4, "AtomicMass": 9.0122, 
     "Group": 2, "Period": 2, "Category": "Logam Alkali Tanah", "Color": "#06D6A0", "Electronegativity": 1.57, "Hazards": ["Beracun"]},
    {"Symbol": "B", "Name": "Boron", "AtomicNumber": 5, "AtomicMass": 10.81, 
     "Group": 13, "Period": 2, "Category": "Metaloid", "Color": "#118AB2", "Electronegativity": 2.04, "Hazards": []},
    {"Symbol": "C", "Name": "Karbon", "AtomicNumber": 6, "AtomicMass": 12.011, 
     "Group": 14, "Period": 2, "Category": "Nonlogam", "Color": "#073B4C", "Electronegativity": 2.55, "Hazards": []},
    {"Symbol": "N", "Name": "Nitrogen", "AtomicNumber": 7, "AtomicMass": 14.007, 
     "Group": 15, "Period": 2, "Category": "Nonlogam", "Color": "#118AB2", "Electronegativity": 3.04, "Hazards": ["Gas Bertekanan"]},
    {"Symbol": "O", "Name": "Oksigen", "AtomicNumber": 8, "AtomicMass": 15.999, 
     "Group": 16, "Period": 2, "Category": "Nonlogam", "Color": "#EF476F", "Electronegativity": 3.44, "Hazards": ["Pengoksidasi"]},
    {"Symbol": "F", "Name": "Fluor", "AtomicNumber": 9, "AtomicMass": 18.998, 
     "Group": 17, "Period": 2, "Category": "Halogen", "Color": "#06D6A0", "Electronegativity": 3.98, "Hazards": ["Korosif", "Beracun"]},
    {"Symbol": "Ne", "Name": "Neon", "AtomicNumber": 10, "AtomicMass": 20.180, 
     "Group": 18, "Period": 2, "Category": "Gas Mulia", "Color": "#4ECDC4", "Electronegativity": None, "Hazards": ["Gas Bertekanan"]},
    
    # Periode 3
    {"Symbol": "Na", "Name": "Natrium", "AtomicNumber": 11, "AtomicMass": 22.990, 
     "Group": 1, "Period": 3, "Category": "Logam Alkali", "Color": "#FFD166", "Electronegativity": 0.93, "Hazards": ["Mudah Terbakar", "Reaktif"]},
    {"Symbol": "Mg", "Name": "Magnesium", "AtomicNumber": 12, "AtomicMass": 24.305, 
     "Group": 2, "Period": 3, "Category": "Logam Alkali Tanah", "Color": "#06D6A0", "Electronegativity": 1.31, "Hazards": ["Mudah Terbakar"]},
    {"Symbol": "Al", "Name": "Aluminium", "AtomicNumber": 13, "AtomicMass": 26.982, 
     "Group": 13, "Period": 3, "Category": "Logam Pascatransisi", "Color": "#118AB2", "Electronegativity": 1.61, "Hazards": []},
    {"Symbol": "Si", "Name": "Silikon", "AtomicNumber": 14, "AtomicMass": 28.085, 
     "Group": 14, "Period": 3, "Category": "Metaloid", "Color": "#073B4C", "Electronegativity": 1.90, "Hazards": []},
    {"Symbol": "P", "Name": "Fosfor", "AtomicNumber": 15, "AtomicMass": 30.974, 
     "Group": 15, "Period": 3, "Category": "Nonlogam", "Color": "#FF6B6B", "Electronegativity": 2.19, "Hazards": ["Mudah Terbakar", "Beracun"]},
    {"Symbol": "S", "Name": "Belerang", "AtomicNumber": 16, "AtomicMass": 32.06, 
     "Group": 16, "Period": 3, "Category": "Nonlogam", "Color": "#FFD166", "Electronegativity": 2.58, "Hazards": []},
    {"Symbol": "Cl", "Name": "Klor", "AtomicNumber": 17, "AtomicMass": 35.45, 
     "Group": 17, "Period": 3, "Category": "Halogen", "Color": "#06D6A0", "Electronegativity": 3.16, "Hazards": ["Korosif", "Beracun"]},
    {"Symbol": "Ar", "Name": "Argon", "AtomicNumber": 18, "AtomicMass": 39.948, 
     "Group": 18, "Period": 3, "Category": "Gas Mulia", "Color": "#4ECDC4", "Electronegativity": None, "Hazards": ["Gas Bertekanan"]},
    
    # Periode 4
    {"Symbol": "K", "Name": "Kalium", "AtomicNumber": 19, "AtomicMass": 39.098, 
     "Group": 1, "Period": 4, "Category": "Logam Alkali", "Color": "#FFD166", "Electronegativity": 0.82, "Hazards": ["Mudah Terbakar", "Reaktif"]},
    {"Symbol": "Ca", "Name": "Kalsium", "AtomicNumber": 20, "AtomicMass": 40.078, 
     "Group": 2, "Period": 4, "Category": "Logam Alkali Tanah", "Color": "#06D6A0", "Electronegativity": 1.00, "Hazards": []},
    {"Symbol": "Sc", "Name": "Skandium", "AtomicNumber": 21, "AtomicMass": 44.956, 
     "Group": 3, "Period": 4, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.36, "Hazards": []},
    {"Symbol": "Ti", "Name": "Titanium", "AtomicNumber": 22, "AtomicMass": 47.867, 
     "Group": 4, "Period": 4, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.54, "Hazards": []},
    {"Symbol": "V", "Name": "Vanadium", "AtomicNumber": 23, "AtomicMass": 50.942, 
     "Group": 5, "Period": 4, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.63, "Hazards": ["Beracun"]},
    {"Symbol": "Cr", "Name": "Kromium", "AtomicNumber": 24, "AtomicMass": 51.996, 
     "Group": 6, "Period": 4, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.66, "Hazards": ["Beracun"]},
    {"Symbol": "Mn", "Name": "Mangan", "AtomicNumber": 25, "AtomicMass": 54.938, 
     "Group": 7, "Period": 4, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.55, "Hazards": ["Beracun"]},
    {"Symbol": "Fe", "Name": "Besi", "AtomicNumber": 26, "AtomicMass": 55.845, 
     "Group": 8, "Period": 4, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.83, "Hazards": []},
    {"Symbol": "Co", "Name": "Kobalt", "AtomicNumber": 27, "AtomicMass": 58.933, 
     "Group": 9, "Period": 4, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.88, "Hazards": ["Beracun"]},
    {"Symbol": "Ni", "Name": "Nikel", "AtomicNumber": 28, "AtomicMass": 58.693, 
     "Group": 10, "Period": 4, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.91, "Hazards": ["Karsinogen"]},
    {"Symbol": "Cu", "Name": "Tembaga", "AtomicNumber": 29, "AtomicMass": 63.546, 
     "Group": 11, "Period": 4, "Category": "Logam Transisi", "Color": "#D2691E", "Electronegativity": 1.90, "Hazards": []},
    {"Symbol": "Zn", "Name": "Seng", "AtomicNumber": 30, "AtomicMass": 65.38, 
     "Group": 12, "Period": 4, "Category": "Logam Transisi", "Color": "#7FFFD4", "Electronegativity": 1.65, "Hazards": []},
    {"Symbol": "Ga", "Name": "Galium", "AtomicNumber": 31, "AtomicMass": 69.723, 
     "Group": 13, "Period": 4, "Category": "Logam Pascatransisi", "Color": "#118AB2", "Electronegativity": 1.81, "Hazards": []},
    {"Symbol": "Ge", "Name": "Germanium", "AtomicNumber": 32, "AtomicMass": 72.630, 
     "Group": 14, "Period": 4, "Category": "Metaloid", "Color": "#073B4C", "Electronegativity": 2.01, "Hazards": []},
    {"Symbol": "As", "Name": "Arsen", "AtomicNumber": 33, "AtomicMass": 74.922, 
     "Group": 15, "Period": 4, "Category": "Metaloid", "Color": "#FF6B6B", "Electronegativity": 2.18, "Hazards": ["Beracun", "Karsinogen"]},
    {"Symbol": "Se", "Name": "Selenium", "AtomicNumber": 34, "AtomicMass": 78.971, 
     "Group": 16, "Period": 4, "Category": "Nonlogam", "Color": "#FFD166", "Electronegativity": 2.55, "Hazards": ["Beracun"]},
    {"Symbol": "Br", "Name": "Brom", "AtomicNumber": 35, "AtomicMass": 79.904, 
     "Group": 17, "Period": 4, "Category": "Halogen", "Color": "#06D6A0", "Electronegativity": 2.96, "Hazards": ["Korosif", "Beracun"]},
    {"Symbol": "Kr", "Name": "Kripton", "AtomicNumber": 36, "AtomicMass": 83.798, 
     "Group": 18, "Period": 4, "Category": "Gas Mulia", "Color": "#4ECDC4", "Electronegativity": 3.00, "Hazards": ["Gas Bertekanan"]},
    
    # ... (unsur-unsur lain hingga 118)
    
    # Contoh unsur terakhir
    {"Symbol": "Og", "Name": "Oganesson", "AtomicNumber": 118, "AtomicMass": 294, 
     "Group": 18, "Period": 7, "Category": "Belum Diketahui", "Color": "#9D4EDD", "Electronegativity": None, "Hazards": ["Radioaktif"]}
]

# Database senyawa kimia (diperbanyak)
COMPOUNDS = {
    "Asam Klorida (HCl)": {"color": "#F0F0F0", "formula": "HCl", "type": "Asam Kuat", "hazards": ["Korosif"]},
    "Natrium Hidroksida (NaOH)": {"color": "#FFFFFF", "formula": "NaOH", "type": "Basa Kuat", "hazards": ["Korosif"]},
    "Tembaga Sulfat (CuSO₄)": {"color": "#00B4D8", "formula": "CuSO₄", "type": "Garam", "hazards": ["Beracun"]},
    "Besi (Fe)": {"color": "#B5651D", "formula": "Fe", "type": "Logam", "hazards": []},
    "Kalium Permanganat (KMnO₄)": {"color": "#9D00FF", "formula": "KMnO₄", "type": "Oksidator", "hazards": ["Pengoksidasi"]},
    "Asam Sulfat (H₂SO₄)": {"color": "#F5F5F5", "formula": "H₂SO₄", "type": "Asam Kuat", "hazards": ["Korosif"]},
    "Air (H₂O)": {"color": "#ADD8E6", "formula": "H₂O", "type": "Pelarut", "hazards": []},
    "Hidrogen Peroksida (H₂O₂)": {"color": "#F0F8FF", "formula": "H₂O₂", "type": "Oksidator", "hazards": ["Pengoksidasi"]},
    "Natrium Karbonat (Na₂CO₃)": {"color": "#FFFFFF", "formula": "Na₂CO₃", "type": "Garam", "hazards": []},
    "Kalsium Klorida (CaCl₂)": {"color": "#FFFFFF", "formula": "CaCl₂", "type": "Garam", "hazards": ["Iritan"]},
    "Asam Asetat (CH₃COOH)": {"color": "#F5F5DC", "formula": "CH₃COOH", "type": "Asam Lemah", "hazards": ["Korosif"]},
    "Amonia (NH₃)": {"color": "#F0F8FF", "formula": "NH₃", "type": "Basa Lemah", "hazards": ["Beracun", "Korosif"]},
    "Etanol (C₂H₅OH)": {"color": "#F0FFF0", "formula": "C₂H₅OH", "type": "Alkohol", "hazards": ["Mudah Terbakar"]},
    "Metana (CH₄)": {"color": "#87CEEB", "formula": "CH₄", "type": "Hidrokarbon", "hazards": ["Mudah Terbakar", "Gas"]},
    "Glukosa (C₆H₁₂O₆)": {"color": "#FFFFFF", "formula": "C₆H₁₂O₆", "type": "Karbohidrat", "hazards": []},
    "Natrium Klorida (NaCl)": {"color": "#FFFFFF", "formula": "NaCl", "type": "Garam", "hazards": []},
    "Besi Sulfat (FeSO₄)": {"color": "#76D7EA", "formula": "FeSO₄", "type": "Garam", "hazards": []},
    "Karbon Dioksida (CO₂)": {"color": "#A9A9A9", "formula": "CO₂", "type": "Gas", "hazards": ["Gas Bertekanan"]},
    "Oksigen (O₂)": {"color": "#87CEEB", "formula": "O₂", "type": "Gas", "hazards": ["Pengoksidasi"]},
    "Tembaga (Cu)": {"color": "#D2691E", "formula": "Cu", "type": "Logam", "hazards": []},
    "Asam Nitrat (HNO₃)": {"color": "#FFFFE0", "formula": "HNO₃", "type": "Asam Kuat", "hazards": ["Korosif", "Pengoksidasi"]},
    "Kalium Hidroksida (KOH)": {"color": "#FFFFFF", "formula": "KOH", "type": "Basa Kuat", "hazards": ["Korosif"]},
    "Perak Nitrat (AgNO₃)": {"color": "#FFFFFF", "formula": "AgNO₃", "type": "Garam", "hazards": ["Korosif"]},
    "Klorin (Cl₂)": {"color": "#90EE90", "formula": "Cl₂", "type": "Gas", "hazards": ["Beracun", "Korosif"]},
    "Belerang Dioksida (SO₂)": {"color": "#F5F5F5", "formula": "SO₂", "type": "Gas", "hazards": ["Beracun"]},
    "Amonium Nitrat (NH₄NO₃)": {"color": "#FFFFFF", "formula": "NH₄NO₃", "type": "Garam", "hazards": ["Pengoksidasi"]},
    "Kalsium Karbida (CaC₂)": {"color": "#FFFFFF", "formula": "CaC₂", "type": "Senyawa Karbon", "hazards": ["Reaktif"]},
    "Asam Sitrat (C₆H₈O₇)": {"color": "#FFFFE0", "formula": "C₆H₈O₇", "type": "Asam Organik", "hazards": []},
    "Benzena (C₆H₆)": {"color": "#87CEEB", "formula": "C₆H₆", "type": "Hidrokarbon", "hazards": ["Mudah Terbakar", "Karsinogen"]},
    "Natrium Bikarbonat (NaHCO₃)": {"color": "#FFFFFF", "formula": "NaHCO₃", "type": "Garam", "hazards": []},
    "Magnesium (Mg)": {"color": "#FFD700", "formula": "Mg", "type": "Logam", "hazards": ["Mudah Terbakar"]},
    "Fenolftalein": {"color": "#FF69B4", "formula": "C₂₀H₁₄O₄", "type": "Indikator", "hazards": ["Iritan"]},
    "Kalium Iodida (KI)": {"color": "#FFFFFF", "formula": "KI", "type": "Garam", "hazards": []},
    "Hidrogen (H₂)": {"color": "#F0F8FF", "formula": "H₂", "type": "Gas", "hazards": ["Mudah Terbakar", "Gas"]},
    "Kalsium Oksida (CaO)": {"color": "#FFFFFF", "formula": "CaO", "type": "Oksida", "hazards": ["Korosif"]},
    "Seng Klorida (ZnCl₂)": {"color": "#FFFFFF", "formula": "ZnCl₂", "type": "Garam", "hazards": ["Korosif"]},
    "Natrium Tiosulfat (Na₂S₂O₃)": {"color": "#FFFFFF", "formula": "Na₂S₂O₃", "type": "Garam", "hazards": []},
    "Asam Fosfat (H₃PO₄)": {"color": "#F5F5F5", "formula": "H₃PO₄", "type": "Asam", "hazards": ["Korosif"]},
    "Kalium Sianida (KCN)": {"color": "#FFFFFF", "formula": "KCN", "type": "Garam", "hazards": ["Beracun", "Sangat Berbahaya"]},
    "Natrium Asetat (CH₃COONa)": {"color": "#FFFFFF", "formula": "CH₃COONa", "type": "Garam", "hazards": []},
    "Karbon Monoksida (CO)": {"color": "#A9A9A9", "formula": "CO", "type": "Gas", "hazards": ["Beracun"]},
    "Iodin (I₂)": {"color": "#9400D3", "formula": "I₂", "type": "Halogen", "hazards": ["Beracun"]},
    "Aluminium Klorida (AlCl₃)": {"color": "#FFFFFF", "formula": "AlCl₃", "type": "Garam", "hazards": ["Korosif"]},
    "Natrium Sulfat (Na₂SO₄)": {"color": "#FFFFFF", "formula": "Na₂SO₄", "type": "Garam", "hazards": []},
}

# Database reaksi kimia (diperbanyak)
REACTIONS = [
    {
        "reagents": ["Asam Klorida (HCl)", "Natrium Hidroksida (NaOH)"],
        "products": ["Natrium Klorida (NaCl)", "Air (H₂O)"],
        "equation": "HCl + NaOH → NaCl + H₂O",
        "type": "Netralisasi",
        "color_change": ["#F0F0F0 + #FFFFFF → #FFFFFF + #ADD8E6"],
        "energy": "Eksoterm",
        "hazards": ["Korosif", "Iritan"],
        "apd": ["Sarung Tangan", "Kacamata", "Jas Lab"],
        "description": "Reaksi netralisasi antara asam kuat dan basa kuat menghasilkan garam dan air. Reaksi ini melepaskan panas."
    },
    {
        "reagents": ["Tembaga Sulfat (CuSO₄)", "Besi (Fe)"],
        "products": ["Besi Sulfat (FeSO₄)", "Tembaga (Cu)"],
        "equation": "CuSO₄ + Fe → FeSO₄ + Cu",
        "type": "Reaksi Pendesakan",
        "color_change": ["#00B4D8 + #B5651D → #76D7EA + #D2691E"],
        "energy": "Eksoterm",
        "hazards": ["Iritan"],
        "apd": ["Sarung Tangan", "Kacamata"],
        "description": "Logam besi mendesak tembaga dari larutan tembaga sulfat, menghasilkan besi sulfat dan tembaga padat."
    },
    {
        "reagents": ["Kalium Permanganat (KMnO₄)", "Hidrogen Peroksida (H₂O₂)"],
        "products": ["Mangan Dioksida (MnO₂)", "Oksigen (O₂)", "Kalium Hidroksida (KOH)"],
        "equation": "2KMnO₄ + 3H₂O₂ → 2MnO₂ + 3O₂ + 2KOH + 2H₂O",
        "type": "Redoks",
        "color_change": ["#9D00FF + #F0F8FF → #808080 + #87CEEB + #FFFFFF"],
        "energy": "Eksoterm",
        "hazards": ["Oksidator Kuat", "Korosif"],
        "apd": ["Sarung Tangan", "Kacamata", "Jas Lab", "Pelindung Wajah"],
        "description": "Reaksi dekomposisi hidrogen peroksida yang dikatalisis oleh kalium permanganat, menghasilkan oksigen gas."
    },
    {
        "reagents": ["Asam Sulfat (H₂SO₄)", "Natrium Karbonat (Na₂CO₃)"],
        "products": ["Natrium Sulfat (Na₂SO₄)", "Air (H₂O)", "Karbon Dioksida (CO₂)"],
        "equation": "H₂SO₄ + Na₂CO₃ → Na₂SO₄ + H₂O + CO₂",
        "type": "Reaksi Asam-Karbonat",
        "color_change": ["#F5F5F5 + #FFFFFF → #FFFFFF + #ADD8E6 + #A9A9A9"],
        "energy": "Eksoterm",
        "hazards": ["Korosif", "Gas Bertekanan"],
        "apd": ["Sarung Tangan", "Kacamata", "Jas Lab"],
        "description": "Asam sulfat bereaksi dengan natrium karbonat menghasilkan natrium sulfat, air, dan gas karbon dioksida."
    },
    {
        "reagents": ["Kalsium Klorida (CaCl₂)", "Natrium Karbonat (Na₂CO₃)"],
        "products": ["Kalsium Karbonat (CaCO₃)", "Natrium Klorida (NaCl)"],
        "equation": "CaCl₂ + Na₂CO₃ → CaCO₃ + 2NaCl",
        "type": "Reaksi Pengendapan",
        "color_change": ["#FFFFFF + #FFFFFF → #FFFFFF + #FFFFFF"],
        "energy": "Endoterm",
        "hazards": ["Iritan Ringan"],
        "apd": ["Sarung Tangan", "Kacamata"],
        "description": "Reaksi ini menghasilkan endapan kalsium karbonat yang berwarna putih."
    },
    {
        "reagents": ["Asam Klorida (HCl)", "Besi (Fe)"],
        "products": ["Besi Klorida (FeCl₂)", "Hidrogen (H₂)"],
        "equation": "2HCl + Fe → FeCl₂ + H₂",
        "type": "Reaksi Logam-Asam",
        "color_change": ["#F0F0F0 + #B5651D → #76D7EA + #F0F8FF"],
        "energy": "Eksoterm",
        "hazards": ["Gas Mudah Terbakar", "Korosif"],
        "apd": ["Sarung Tangan", "Kacamata", "Jas Lab", "Pelindung Wajah"],
        "description": "Logam besi bereaksi dengan asam klorida menghasilkan besi klorida dan gas hidrogen yang mudah terbakar."
    },
    {
        "reagents": ["Asam Asetat (CH₃COOH)", "Amonia (NH₃)"],
        "products": ["Ammonium Asetat (CH₃COONH₄)"],
        "equation": "CH₃COOH + NH₃ → CH₃COONH₄",
        "type": "Netralisasi",
        "color_change": ["#F5F5DC + #F0F8FF → #FFFFFF"],
        "energy": "Eksoterm",
        "hazards": ["Iritan"],
        "apd": ["Sarung Tangan", "Kacamata"],
        "description": "Asam lemah bereaksi dengan basa lemah membentuk garam ammonium asetat."
    },
    {
        "reagents": ["Perak Nitrat (AgNO₃)", "Natrium Klorida (NaCl)"],
        "products": ["Perak Klorida (AgCl)", "Natrium Nitrat (NaNO₃)"],
        "equation": "AgNO₃ + NaCl → AgCl + NaNO₃",
        "type": "Pengendapan",
        "color_change": ["#FFFFFF + #FFFFFF → #FFFFFF + #FFFFFF"],
        "energy": "Endoterm",
        "hazards": ["Iritan"],
        "apd": ["Sarung Tangan", "Kacamata"],
        "description": "Reaksi pengendapan menghasilkan perak klorida berwarna putih."
    },
    {
        "reagents": ["Magnesium (Mg)", "Oksigen (O₂)"],
        "products": ["Magnesium Oksida (MgO)"],
        "equation": "2Mg + O₂ → 2MgO",
        "type": "Pembakaran",
        "color_change": ["#FFD700 + #87CEEB → #FFFFFF"],
        "energy": "Eksoterm",
        "hazards": ["Cahaya Terang", "Panas"],
        "apd": ["Kacamata Gelap", "Sarung Tangan"],
        "description": "Pembakaran magnesium menghasilkan cahaya putih terang dan magnesium oksida."
    },
    {
        "reagents": ["Asam Sulfat (H₂SO₄)", "Kalium Hidroksida (KOH)"],
        "products": ["Kalium Sulfat (K₂SO₄)", "Air (H₂O)"],
        "equation": "H₂SO₄ + 2KOH → K₂SO₄ + 2H₂O",
        "type": "Netralisasi",
        "color_change": ["#F5F5F5 + #FFFFFF → #FFFFFF + #ADD8E6"],
        "energy": "Eksoterm",
        "hazards": ["Korosif"],
        "apd": ["Sarung Tangan", "Kacamata", "Jas Lab"],
        "description": "Reaksi netralisasi antara asam kuat dan basa kuat menghasilkan garam dan air."
    },
    {
        "reagents": ["Kalium Iodida (KI)", "Timbal Nitrat (Pb(NO₃)₂)"],
        "products": ["Timbal Iodida (PbI₂)", "Kalium Nitrat (KNO₃)"],
        "equation": "2KI + Pb(NO₃)₂ → PbI₂ + 2KNO₃",
        "type": "Pengendapan",
        "color_change": ["#FFFFFF + #FFFFFF → #FFFF00 + #FFFFFF"],
        "energy": "Endoterm",
        "hazards": ["Beracun"],
        "apd": ["Sarung Tangan", "Kacamata"],
        "description": "Reaksi pengendapan menghasilkan timbal iodida berwarna kuning cerah."
    },
    {
        "reagents": ["Natrium (Na)", "Air (H₂O)"],
        "products": ["Natrium Hidroksida (NaOH)", "Hidrogen (H₂)"],
        "equation": "2Na + 2H₂O → 2NaOH + H₂",
        "type": "Reaksi Logam-Air",
        "color_change": ["#FFD166 + #ADD8E6 → #FFFFFF + #F0F8FF"],
        "energy": "Eksoterm",
        "hazards": ["Ledakan", "Gas Mudah Terbakar"],
        "apd": ["Pelindung Wajah", "Sarung Tangan", "Kacamata"],
        "description": "Logam natrium bereaksi hebat dengan air menghasilkan natrium hidroksida dan gas hidrogen."
    },
    {
        "reagents": ["Kalsium Karbida (CaC₂)", "Air (H₂O)"],
        "products": ["Asetilena (C₂H₂)", "Kalsium Hidroksida (Ca(OH)₂)"],
        "equation": "CaC₂ + 2H₂O → C₂H₂ + Ca(OH)₂",
        "type": "Hidrolisis",
        "color_change": ["#FFFFFF + #ADD8E6 → #87CEEB + #FFFFFF"],
        "energy": "Eksoterm",
        "hazards": ["Gas Mudah Terbakar"],
        "apd": ["Sarung Tangan", "Kacamata"],
        "description": "Kalsium karbida bereaksi dengan air menghasilkan gas asetilena yang mudah terbakar."
    },
    {
        "reagents": ["Asam Nitrat (HNO₃)", "Tembaga (Cu)"],
        "products": ["Tembaga Nitrat (Cu(NO₃)₂)", "Nitrogen Dioksida (NO₂)", "Air (H₂O)"],
        "equation": "4HNO₃ + Cu → Cu(NO₃)₂ + 2NO₂ + 2H₂O",
        "type": "Reaksi Redoks",
        "color_change": ["#FFFFE0 + #D2691E → #00B4D8 + #C71585 + #ADD8E6"],
        "energy": "Eksoterm",
        "hazards": ["Gas Beracun", "Korosif"],
        "apd": ["Sarung Tangan", "Kacamata", "Jas Lab", "Pelindung Wajah"],
        "description": "Tembaga bereaksi dengan asam nitrat pekat menghasilkan gas nitrogen dioksida berwarna coklat."
    },
    {
        "reagents": ["Hidrogen (H₂)", "Oksigen (O₂)"],
        "products": ["Air (H₂O)"],
        "equation": "2H₂ + O₂ → 2H₂O",
        "type": "Pembakaran",
        "color_change": ["#F0F8FF + #87CEEB → #ADD8E6"],
        "energy": "Eksoterm",
        "hazards": ["Ledakan"],
        "apd": ["Pelindung Wajah", "Sarung Tangan"],
        "description": "Reaksi pembakaran hidrogen yang menghasilkan air dan energi besar."
    }
]

# Fungsi untuk membuat kartu unsur
def create_element_card(element):
    hazards_html = ""
    if element["Hazards"]:
        hazards_html = "<div style='margin-top:10px;'><b>Bahaya:</b><br>"
        for hazard in element["Hazards"]:
            hazards_html += f"<span class='warning-badge'>{hazard}</span> "
        hazards_html += "</div>"
    
    card = f"""
    <div class="element-card">
        <div style="background:{element['Color']}; 
                    background:linear-gradient(135deg, {element['Color']}, #FFFFFF);
                    border-radius:50%; width:80px; height:80px; 
                    display:flex; align-items:center; justify-content:center; margin:0 auto 15px;
                    box-shadow: 0 6px 12px rgba(0,0,0,0.2);">
            <h2 style="color:white; margin:0; text-shadow:2px 2px 4px rgba(0,0,0,0.5);">{element['Symbol']}</h2>
        </div>
        <h3 style="text-align:center; margin-bottom:10px; color:{dark_color};">{element['Name']}</h3>
        <div style="background:rgba(255,255,255,0.7); border-radius:15px; padding:10px;">
            <p style="text-align:center; margin:5px 0; font-size:1rem; color:{text_color};">
                <b>No Atom:</b> {element['AtomicNumber']}<br>
                <b>Massa:</b> {element['AtomicMass']}<br>
                <b>Golongan:</b> {element['Group']}<br>
                <b>Periode:</b> {element['Period']}<br>
                <b>Kategori:</b> {element['Category']}
            </p>
        </div>
        {hazards_html}
    </div>
    """
    return card

# Fungsi untuk menampilkan tabel periodik
def show_periodic_table():
    st.header("📊 Tabel Periodik Interaktif")
    st.markdown("""
    <div class="periodic-header">
        <h2 style="color:white; text-align:center; font-size:32px;">Tabel Periodik Unsur Kimia (118 Unsur)</h2>
        <p style="text-align:center; font-size:18px;">Klik pada kartu unsur untuk melihat detail lengkap</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Kategori warna
    categories = {
        "Logam Alkali": "#FFD166",
        "Logam Alkali Tanah": "#06D6A0",
        "Logam Transisi": "#118AB2",
        "Logam Pascatransisi": "#073B4C",
        "Metaloid": "#6A4C93",
        "Nonlogam": "#FF6B6B",
        "Halogen": "#4ECDC4",
        "Gas Mulia": "#EF476F",
        "Lantanida": "#FF9E6D",
        "Aktinida": "#FF9E6D",
        "Belum Diketahui": "#9D4EDD"
    }
    
    # Filter kategori
    selected_category = st.selectbox("Filter Kategori", ["Semua"] + list(categories.keys()), key="category_filter")
    
    # Tampilkan legenda
    st.subheader("Legenda Kategori")
    cols = st.columns(5)
    for i, (cat, color) in enumerate(categories.items()):
        cols[i % 5].markdown(f"""
        <div style="background:{color}; 
                    background:linear-gradient(135deg, {color}, #FFFFFF);
                    border-radius:10px; padding:10px; text-align:center; 
                    color:white; margin-bottom:10px; font-weight:bold; box-shadow:0 4px 8px rgba(0,0,0,0.2);">
            {cat}
        </div>
        """, unsafe_allow_html=True)
    
    # Tampilkan kartu unsur
    st.subheader("Daftar Unsur")
    if selected_category != "Semua":
        elements = [e for e in PERIODIC_TABLE if e["Category"] == selected_category]
    else:
        elements = PERIODIC_TABLE
        
    # Atur kartu dalam grid
    cols = st.columns(5)
    for i, element in enumerate(elements):
        with cols[i % 5]:
            st.markdown(create_element_card(element), unsafe_allow_html=True)
    
    # Grafik interaktif
    st.subheader("📈 Visualisasi Sifat Unsur")
    df = pd.DataFrame(PERIODIC_TABLE)
    
    fig = px.scatter(
        df, 
        x="AtomicNumber", 
        y="AtomicMass", 
        color="Category",
        size="AtomicMass",
        hover_name="Name",
        hover_data=["Group", "Period", "Electronegativity"],
        color_discrete_map=categories,
        height=600
    )
    
    fig.update_layout()
        title="Massa Atom vs Nomor Atom",
        xaxis_title="Nomor Atom",
        yaxis_title="Massa Atom",
        template="plotly_white",
        legend_title_text="Kategori",
        font=dict(size=14),
        hoverlabel=dict(font_size=16)
    
    st.plotly_chart(fig, use_container_width=True)

# Fungsi untuk menampilkan simulasi reaksi
def show_reaction_simulator():
    st.header("🧪 Simulator Reaksi Kimia")
    st.markdown("""
    <div class="periodic-header">
        <h2 style="color:white; text-align:center; font-size:32px;">Simulasi Reaksi Kimia Interaktif</h2>
        <p style="text-align:center; font-size:18px;">Pilih dua senyawa untuk melihat reaksi yang terjadi</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pilih senyawa
    col1, col2 = st.columns(2)
    with col1:
        compound1 = st.selectbox("Pilih Senyawa Pertama", list(COMPOUNDS.keys()), key="compound1")
        color1 = COMPOUNDS[compound1]["color"]
        st.markdown(f"<div style='background:{color1}; height:50px; border-radius:10px;'></div>", unsafe_allow_html=True)
        st.caption(f"Rumus: {COMPOUNDS[compound1]['formula']}")
        
    with col2:
        compound2 = st.selectbox("Pilih Senyawa Kedua", list(COMPOUNDS.keys()), key="compound2")
        color2 = COMPOUNDS[compound2]["color"]
        st.markdown(f"<div style='background:{color2}; height:50px; border-radius:10px;'></div>", unsafe_allow_html=True)
        st.caption(f"Rumus: {COMPOUNDS[compound2]['formula']}")
    
    # Tombol untuk melakukan reaksi
    if st.button("⚡ Lakukan Reaksi", use_container_width=True, key="react_button"):
        # Temukan reaksi yang sesuai
        reaction = None
        for r in REACTIONS:
            if (compound1 in r["reagents"] and compound2 in r["reagents"]) or \
               (compound2 in r["reagents"] and compound1 in r["reagents"]):
                reaction = r
                break
        
        # Tampilkan hasil reaksi
        if reaction:
            st.session_state.reaction = reaction
        else:
            st.session_state.reaction = None
    
    # Tampilkan hasil reaksi jika ada
    if "reaction" in st.session_state and st.session_state.reaction:
        reaction = st.session_state.reaction
        st.markdown(f"<div class='reaction-container'>", unsafe_allow_html=True)
        
        # Header reaksi
        st.subheader(f"Reaksi: {reaction['type']}")
        st.markdown(f"<div class='chemical-equation'>{reaction['equation']}</div>", unsafe_allow_html=True)
        
        # Visualisasi warna
        col1, col2, col3 = st.columns([1, 0.2, 1])
        with col1:
            st.markdown("### Pereaksi")
            for reagent in reaction["reagents"]:
                color = COMPOUNDS[reagent]["color"]
                st.markdown(f"<div class='color-box' style='background-color:{color}'>{reagent}</div>", 
                            unsafe_allow_html=True)
        
        with col2:
            st.markdown("<h1 style='text-align:center; margin-top:80px; font-size:48px;'>→</h1>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("### Produk")
            for product in reaction["products"]:
                if product in COMPOUNDS:
                    color = COMPOUNDS[product]["color"]
                    st.markdown(f"<div class='color-box' style='background-color:{color}'>{product}</div>", 
                                unsafe_allow_html=True)
                else:
                    # Warna default untuk produk yang tidak terdaftar
                    st.markdown(f"<div class='color-box' style='background-color:#DDDDDD'>{product}</div>", 
                                unsafe_allow_html=True)
        
        # Informasi reaksi
        st.subheader("📝 Informasi Reaksi")
        st.markdown(f"*Jenis Reaksi:* {reaction['type']}")
        st.markdown(f"*Perubahan Energi:* {reaction['energy']}")
        st.markdown(f"*Deskripsi:* {reaction['description']}")
        
        # Bahaya dan APD
        col4, col5 = st.columns(2)
        with col4:
            st.subheader("⚠ Simbol Bahaya")
            for hazard in reaction["hazards"]:
                st.markdown(f"<div class='warning-badge'>{hazard}</div>", unsafe_allow_html=True)
        
        with col5:
            st.subheader("🛡 Alat Pelindung Diri (APD)")
            for apd in reaction["apd"]:
                st.markdown(f"<div class='apd-badge'>{apd}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    elif "reaction" in st.session_state and st.session_state.reaction is None:
        st.error("Tidak ada reaksi yang diketahui antara senyawa yang dipilih.")
        
    # Tampilkan daftar reaksi yang tersedia
    with st.expander("📚 Daftar Reaksi yang Tersedia", expanded=True):
        for i, r in enumerate(REACTIONS):
            st.markdown(f"#### Reaksi {i+1}: {r['type']}")
            st.markdown(f"*Persamaan:* {r['equation']}")
            st.markdown(f"*Pereaksi:* {', '.join(r['reagents'])}")
            st.markdown(f"*Produk:* {', '.join(r['products'])}")
            st.markdown("---")

# Fungsi untuk menampilkan informasi tambahan
def show_additional_info():
    st.header("📚 Ensiklopedia Kimia")
    st.markdown("""
    <div class="periodic-header">
        <h2 style="color:white; text-align:center; font-size:32px;">Panduan Lengkap Kimia Dasar</h2>
        <p style="text-align:center; font-size:18px;">Pelajari konsep-konsep dasar kimia dan eksperimen menarik</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Jenis-jenis reaksi kimia
    st.subheader("🧪 Jenis-Jenis Reaksi Kimia")
    reaction_types = [
        {"name": "Sintesis", "emoji": "⚗", "desc": "Dua atau lebih zat bergabung membentuk zat baru. Contoh: 2H₂ + O₂ → 2H₂O"},
        {"name": "Dekomposisi", "emoji": "🧫", "desc": "Satu zat terurai menjadi dua atau lebih zat. Contoh: 2H₂O₂ → 2H₂O + O₂"},
        {"name": "Pembakaran", "emoji": "🔥", "desc": "Reaksi dengan oksigen yang menghasilkan panas dan cahaya. Contoh: CH₄ + 2O₂ → CO₂ + 2H₂O"},
        {"name": "Penggantian Tunggal", "emoji": "🔄", "desc": "Satu unsur menggantikan unsur lain dalam senyawa. Contoh: Zn + 2HCl → ZnCl₂ + H₂"},
        {"name": "Penggantian Ganda", "emoji": "🔀", "desc": "Ion-ion dari dua senyawa saling bertukar. Contoh: AgNO₃ + NaCl → AgCl + NaNO₃"},
        {"name": "Netralisasi", "emoji": "⚖", "desc": "Asam dan basa bereaksi membentuk garam dan air. Contoh: HCl + NaOH → NaCl + H₂O"}
    ]
    
    cols = st.columns(3)
    for i, rtype in enumerate(reaction_types):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="element-card">
                <div style="display:flex; align-items:center; margin-bottom:15px;">
                    <span style="font-size:36px; margin-right:15px;">{rtype['emoji']}</span>
                    <h3 style="margin:0;">{rtype['name']}</h3>
                </div>
                <p style="font-size:16px; color:{text_color};">{rtype['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Simbol bahaya (9 simbol)
    st.subheader("⚠ Simbol Bahaya Laboratorium (GHS)")
    hazard_symbols = [
        {"name": "Mudah Terbakar", "emoji": "🔥", "desc": "Bahan yang mudah menyala saat terkena api, panas, percikan api, atau sumber nyala lainnya"},
        {"name": "Mudah Teroksidasi", "emoji": "⚡", "desc": "Bahan yang dapat menyebabkan atau memperparah kebakaran, umumnya menghasilkan panas saat kontak dengan zat lain"},
        {"name": "Mudah Meledak", "emoji": "💥", "desc": "Bahan yang dapat meledak akibat reaksi kimia, menghasilkan gas panas dalam volume dan kecepatan tinggi"},
        {"name": "Beracun", "emoji": "☠", "desc": "Bahan yang dapat menyebabkan keracunan akut atau kronis, bahkan kematian jika terhirup, tertelan, atau terserap kulit"},
        {"name": "Korosif", "emoji": "⚠", "desc": "Bahan yang dapat merusak jaringan hidup dan material logam melalui reaksi kimia"},
        {"name": "Gas di Bawah Tekanan", "emoji": "💨", "desc": "Gas yang disimpan dalam wadah bertekanan dan dapat meledak jika dipanaskan"},
        {"name": "Toksik untuk Organ Target", "emoji": "🧬", "desc": "Bahan yang dapat menyebabkan kerusakan organ tertentu setelah paparan tunggal atau berulang"},
        {"name": "Bahaya Kronis", "emoji": "🔄", "desc": "Bahan yang dapat menyebabkan efek kesehatan jangka panjang seperti kanker, kerusakan reproduksi, atau mutasi genetik"},
        {"name": "Bahaya Lingkungan", "emoji": "🌍", "desc": "Bahan yang dapat menyebabkan efek merusak pada lingkungan perairan atau atmosfer"}
    ]
    
    cols = st.columns(3)
    for i, hazard in enumerate(hazard_symbols):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="element-card">
                <div style="display:flex; align-items:center; margin-bottom:15px;">
                    <span class="hazard-symbol">{hazard['emoji']}</span>
                    <h3 style="margin:0;">{hazard['name']}</h3>
                </div>
                <p style="font-size:16px; color:{text_color};">{hazard['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Alat pelindung diri
    st.subheader("🛡 Alat Pelindung Diri (APD)")
    apd_items = [
        {"name": "Kacamata Keselamatan", "emoji": "👓", "desc": "Melindungi mata dari percikan bahan kimia"},
        {"name": "Sarung Tangan", "emoji": "🧤", "desc": "Melindungi tangan dari kontak langsung bahan kimia"},
        {"name": "Jas Lab", "emoji": "🥼", "desc": "Melindungi tubuh dan pakaian dari percikan bahan kimia"},
        {"name": "Pelindung Wajah", "emoji": "🥽", "desc": "Melindungi seluruh wajah dari percikan berbahaya"},
        {"name": "Masker Respirator", "emoji": "😷", "desc": "Melindungi sistem pernapasan dari uap berbahaya"},
        {"name": "Sepatu Tertutup", "emoji": "👞", "desc": "Melindungi kaki dari tumpahan bahan kimia"}
    ]
    
    cols = st.columns(3)
    for i, apd in enumerate(apd_items):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="element-card">
                <div style="display:flex; align-items:center; margin-bottom:15px;">
                    <span style="font-size:36px; margin-right:15px;">{apd['emoji']}</span>
                    <h3 style="margin:0;">{apd['name']}</h3>
                </div>
                <p style="font-size:16px; color:{text_color};">{apd['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Tips keselamatan
    st.subheader("🔒 Tips Keselamatan Laboratorium")
    safety_tips = [
        "Selalu gunakan APD yang sesuai saat bekerja dengan bahan kimia",
        "Kenali sifat dan bahaya bahan kimia sebelum menggunakannya",
        "Jangan pernah mencicipi atau mencium bahan kimia secara langsung",
        "Bekerja di dalam lemari asam saat menangani bahan berbahaya",
        "Simpan bahan kimia sesuai dengan kelompok dan sifatnya",
        "Bersihkan tumpahan segera dengan prosedur yang benar",
        "Ketahui lokasi alat keselamatan (pemadam api, shower, eye wash)",
        "Jangan bekerja sendirian di laboratorium",
        "Baca dan pahami MSDS (Material Safety Data Sheet) sebelum menggunakan bahan kimia",
        "Cuci tangan setelah bekerja di laboratorium"
    ]
    
    for i, tip in enumerate(safety_tips):
        st.markdown(f"""
        <div class="element-card" style="padding:15px; margin-bottom:10px;">
            <div style="display:flex; align-items:center;">
                <span style="font-size:24px; margin-right:15px; color:{dark_color};">🔒</span>
                <p style="margin:0; font-size:16px; color:{text_color};">{i+1}. {tip}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Fungsi untuk menampilkan informasi PBK
def show_chemical_safety():
    st.header("🧪 Penanganan Bahan Kimia (PBK)")
    st.markdown("""
    <div class="periodic-header">
        <h2 style="color:white; text-align:center; font-size:32px;">Pedoman Penyimpanan dan Kompatibilitas Bahan Kimia</h2>
        <p style="text-align:center; font-size:18px;">Pelajari cara menyimpan bahan kimia dengan aman dan kelompok kompatibilitas</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🏷 Kelompok Penyimpanan Bahan Kimia")
    storage_groups = [
        {"name": "Asam Anorganik", "emoji": "🧪", "desc": "HCl, H₂SO₄, HNO₃, H₃PO₄. Simpan terpisah dari basa dan bahan organik."},
        {"name": "Basa", "emoji": "🧴", "desc": "NaOH, KOH, NH₄OH. Simpan terpisah dari asam dan logam."},
        {"name": "Pelarut Organik", "emoji": "💧", "desc": "Etanol, Aseton, Benzena. Simpan di lemari khusus bahan mudah terbakar."},
        {"name": "Oksidator", "emoji": "🔥", "desc": "KMnO₄, H₂O₂, KClO₃. Simpan terpisah dari bahan reduktor dan mudah terbakar."},
        {"name": "Logam Reaktif", "emoji": "⚙", "desc": "Natrium, Kalium, Magnesium. Simpan dalam minyak mineral."},
        {"name": "Gas Bertekanan", "emoji": "💨", "desc": "O₂, H₂, CO₂. Ikat silinder dengan aman dan simpan di area berventilasi."}
    ]
    
    cols = st.columns(3)
    for i, group in enumerate(storage_groups):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="element-card">
                <div style="display:flex; align-items:center; margin-bottom:15px;">
                    <span style="font-size:36px; margin-right:15px;">{group['emoji']}</span>
                    <h3 style="margin:0;">{group['name']}</h3>
                </div>
                <p style="font-size:16px; color:{text_color};">{group['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.subheader("🔄 Tabel Kompatibilitas Bahan Kimia")
    st.markdown("""
    <p style="font-size:16px; margin-bottom:20px;">Tabel berikut menunjukkan kelompok bahan kimia yang dapat disimpan bersama dan yang harus dipisahkan:</p>
    """, unsafe_allow_html=True)
    
    compatibility_data = {
        "Kelompok": ["Asam Anorganik", "Basa", "Pelarut Organik", "Oksidator", "Logam Reaktif", "Gas Bertekanan"],
        "Asam Anorganik": ["✅", "❌", "⚠", "❌", "❌", "✅"],
        "Basa": ["❌", "✅", "⚠", "❌", "❌", "✅"],
        "Pelarut Organik": ["⚠", "⚠", "✅", "❌", "❌", "⚠"],
        "Oksidator": ["❌", "❌", "❌", "✅", "❌", "❌"],
        "Logam Reaktif": ["❌", "❌", "❌", "❌", "✅", "✅"],
        "Gas Bertekanan": ["✅", "✅", "⚠", "❌", "✅", "✅"]
    }
    
    df = pd.DataFrame(compatibility_data)
    st.dataframe(df, hide_index=True, use_container_width=True)
    
    st.subheader("📦 Prinsip Penyimpanan Aman")
    storage_principles = [
        "Simpan bahan kimia berdasarkan kelompok kompatibilitas, bukan berdasarkan abjad",
        "Gunakan wadah sekunder untuk bahan korosif dan beracun",
        "Beri label jelas dengan nama bahan, konsentrasi, tanggal pembuatan, dan simbol bahaya",
        "Batasi jumlah bahan kimia yang disimpan di meja kerja",
        "Simpan bahan mudah terbakar di lemari tahan api",
        "Periksa kondisi wadah penyimpanan secara berkala",
        "Simpan bahan yang tidak stabil di tempat gelap dan dingin",
        "Gunakan sistem inventaris FIFO (First In First Out)",
        "Sediakan material penyerap untuk penanganan tumpahan"
    ]
    
    for i, principle in enumerate(storage_principles):
        st.markdown(f"""
        <div class="element-card" style="padding:15px; margin-bottom:10px;">
            <div style="display:flex; align-items:center;">
                <span style="font-size:24px; margin-right:15px; color:{dark_color};">📦</span>
                <p style="margin:0; font-size:16px; color:{text_color};">{i+1}. {principle}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("🧯 Tanggap Darurat")
    emergency_measures = [
        "Tumpahan kecil: Gunakan material penyerap dan sarung tangan",
        "Tumpahan besar: Evakuasi area dan hubungi petugas tanggap darurat",
        "Kontak kulit: Bilas dengan air mengalir minimal 15 menit",
        "Kontak mata: Gunakan eye wash station selama 15 menit",
        "Tertelan: Jangan dimuntahkan kecuali diinstruksikan profesional",
        "Kebakaran kecil: Gunakan alat pemadam api yang sesuai",
        "Kebakaran besar: Aktifkan alarm dan evakuasi"
    ]
    
    for i, measure in enumerate(emergency_measures):
        st.markdown(f"""
        <div class="element-card" style="padding:15px; margin-bottom:10px;">
            <div style="display:flex; align-items:center;">
                <span style="font-size:24px; margin-right:15px; color:{dark_color};">🚨</span>
                <p style="margin:0; font-size:16px; color:{text_color};">{i+1}. {measure}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# UI Utama
st.title("🔬 Laboratorium Kimia Interaktif")
st.markdown("""
<div style="background:linear-gradient(135deg, #1A535C, #073B4C); 
            padding:30px; border-radius:25px; color:white; margin-bottom:30px;
            text-align:center; box-shadow:0 12px 24px rgba(0,0,0,0.3);">
    <h1 style="color:white; font-size:42px; margin:0;">Selamat Datang di Laboratorium Kimia Virtual!</h1>
    <p style="font-size:20px; margin:10px 0 0;">Jelajahi tabel periodik, simulasikan reaksi kimia, dan pelajari konsep kimia dengan cara menyenangkan</p>
</div>
""", unsafe_allow_html=True)

# Tab navigasi
tab1, tab2, tab3, tab4 = st.tabs(["📋 Tabel Periodik", "🧪 Simulator Reaksi", "📚 Ensiklopedia Kimia", "🛡 Penanganan Bahan Kimia"])

with tab1:
    show_periodic_table()

with tab2:
    show_reaction_simulator()

with tab3:
    show_additional_info()

with tab4:
    show_chemical_safety()

# Footer
st.divider()
st.markdown("""
<div style="text-align:center; padding:30px; color:#1A535C;">
    <p style="font-size:18px; margin:0;">🔬 Laboratorium Kimia Interaktif © 2023</p>
    <p style="font-size:16px; margin:10px 0;">Dikembangkan dengan Streamlit | Untuk tujuan edukasi</p>
    <p style="font-size:14px; margin:0;">Versi 3.0 | Terakhir diperbarui: 18 Juli 2023</p>
</div>
""", unsafe_allow_html=True)
