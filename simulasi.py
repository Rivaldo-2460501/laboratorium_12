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

# Database tabel periodik
PERIODIC_TABLE = [
    {"Symbol": "H", "Name": "Hydrogen", "AtomicNumber": 1, "AtomicMass": 1.008, 
     "Group": 1, "Period": 1, "Category": "Nonmetal", "Color": "#FF6B6B", "Electronegativity": 2.20},
    {"Symbol": "He", "Name": "Helium", "AtomicNumber": 2, "AtomicMass": 4.0026, 
     "Group": 18, "Period": 1, "Category": "Noble Gas", "Color": "#4ECDC4", "Electronegativity": None},
    {"Symbol": "Li", "Name": "Lithium", "AtomicNumber": 3, "AtomicMass": 6.94, 
     "Group": 1, "Period": 2, "Category": "Alkali Metal", "Color": "#FFD166", "Electronegativity": 0.98},
    {"Symbol": "Be", "Name": "Beryllium", "AtomicNumber": 4, "AtomicMass": 9.0122, 
     "Group": 2, "Period": 2, "Category": "Alkaline Earth Metal", "Color": "#06D6A0", "Electronegativity": 1.57},
    {"Symbol": "B", "Name": "Boron", "AtomicNumber": 5, "AtomicMass": 10.81, 
     "Group": 13, "Period": 2, "Category": "Metalloid", "Color": "#118AB2", "Electronegativity": 2.04},
    {"Symbol": "C", "Name": "Carbon", "AtomicNumber": 6, "AtomicMass": 12.011, 
     "Group": 14, "Period": 2, "Category": "Nonmetal", "Color": "#073B4C", "Electronegativity": 2.55},
    {"Symbol": "N", "Name": "Nitrogen", "AtomicNumber": 7, "AtomicMass": 14.007, 
     "Group": 15, "Period": 2, "Category": "Nonmetal", "Color": "#118AB2", "Electronegativity": 3.04},
    {"Symbol": "O", "Name": "Oxygen", "AtomicNumber": 8, "AtomicMass": 15.999, 
     "Group": 16, "Period": 2, "Category": "Nonmetal", "Color": "#EF476F", "Electronegativity": 3.44},
    {"Symbol": "F", "Name": "Fluorine", "AtomicNumber": 9, "AtomicMass": 18.998, 
     "Group": 17, "Period": 2, "Category": "Halogen", "Color": "#06D6A0", "Electronegativity": 3.98},
    {"Symbol": "Ne", "Name": "Neon", "AtomicNumber": 10, "AtomicMass": 20.180, 
     "Group": 18, "Period": 2, "Category": "Noble Gas", "Color": "#4ECDC4", "Electronegativity": None},
    {"Symbol": "Na", "Name": "Sodium", "AtomicNumber": 11, "AtomicMass": 22.990, 
     "Group": 1, "Period": 3, "Category": "Alkali Metal", "Color": "#FFD166", "Electronegativity": 0.93},
    {"Symbol": "Mg", "Name": "Magnesium", "AtomicNumber": 12, "AtomicMass": 24.305, 
     "Group": 2, "Period": 3, "Category": "Alkaline Earth Metal", "Color": "#06D6A0", "Electronegativity": 1.31},
    {"Symbol": "Al", "Name": "Aluminum", "AtomicNumber": 13, "AtomicMass": 26.982, 
     "Group": 13, "Period": 3, "Category": "Post-Transition Metal", "Color": "#118AB2", "Electronegativity": 1.61},
    {"Symbol": "Si", "Name": "Silicon", "AtomicNumber": 14, "AtomicMass": 28.085, 
     "Group": 14, "Period": 3, "Category": "Metalloid", "Color": "#073B4C", "Electronegativity": 1.90},
    {"Symbol": "P", "Name": "Phosphorus", "AtomicNumber": 15, "AtomicMass": 30.974, 
     "Group": 15, "Period": 3, "Category": "Nonmetal", "Color": "#FF6B6B", "Electronegativity": 2.19},
    {"Symbol": "S", "Name": "Sulfur", "AtomicNumber": 16, "AtomicMass": 32.06, 
     "Group": 16, "Period": 3, "Category": "Nonmetal", "Color": "#FFD166", "Electronegativity": 2.58},
    {"Symbol": "Cl", "Name": "Chlorine", "AtomicNumber": 17, "AtomicMass": 35.45, 
     "Group": 17, "Period": 3, "Category": "Halogen", "Color": "#06D6A0", "Electronegativity": 3.16},
    {"Symbol": "Ar", "Name": "Argon", "AtomicNumber": 18, "AtomicMass": 39.948, 
     "Group": 18, "Period": 3, "Category": "Noble Gas", "Color": "#4ECDC4", "Electronegativity": None},
    {"Symbol": "K", "Name": "Potassium", "AtomicNumber": 19, "AtomicMass": 39.098, 
     "Group": 1, "Period": 4, "Category": "Alkali Metal", "Color": "#FFD166", "Electronegativity": 0.82},
    {"Symbol": "Ca", "Name": "Calcium", "AtomicNumber": 20, "AtomicMass": 40.078, 
     "Group": 2, "Period": 4, "Category": "Alkaline Earth Metal", "Color": "#06D6A0", "Electronegativity": 1.00},
    {"Symbol": "Fe", "Name": "Iron", "AtomicNumber": 26, "AtomicMass": 55.845, 
     "Group": 8, "Period": 4, "Category": "Transition Metal", "Color": "#B5651D", "Electronegativity": 1.83},
    {"Symbol": "Cu", "Name": "Copper", "AtomicNumber": 29, "AtomicMass": 63.546, 
     "Group": 11, "Period": 4, "Category": "Transition Metal", "Color": "#D2691E", "Electronegativity": 1.90},
    {"Symbol": "Zn", "Name": "Zinc", "AtomicNumber": 30, "AtomicMass": 65.38, 
     "Group": 12, "Period": 4, "Category": "Transition Metal", "Color": "#7FFFD4", "Electronegativity": 1.65},
    {"Symbol": "Ag", "Name": "Silver", "AtomicNumber": 47, "AtomicMass": 107.87, 
     "Group": 11, "Period": 5, "Category": "Transition Metal", "Color": "#C0C0C0", "Electronegativity": 1.93},
    {"Symbol": "Au", "Name": "Gold", "AtomicNumber": 79, "AtomicMass": 196.97, 
     "Group": 11, "Period": 6, "Category": "Transition Metal", "Color": "#FFD700", "Electronegativity": 2.54},
]

# Database senyawa kimia
COMPOUNDS = {
    "Asam Klorida (HCl)": {"color": "#F0F0F0", "formula": "HCl", "type": "Asam Kuat"},
    "Natrium Hidroksida (NaOH)": {"color": "#FFFFFF", "formula": "NaOH", "type": "Basa Kuat"},
    "Tembaga Sulfat (CuSO₄)": {"color": "#00B4D8", "formula": "CuSO₄", "type": "Garam"},
    "Besi (Fe)": {"color": "#B5651D", "formula": "Fe", "type": "Logam"},
    "Kalium Permanganat (KMnO₄)": {"color": "#9D00FF", "formula": "KMnO₄", "type": "Oksidator"},
    "Asam Sulfat (H₂SO₄)": {"color": "#F5F5F5", "formula": "H₂SO₄", "type": "Asam Kuat"},
    "Air (H₂O)": {"color": "#ADD8E6", "formula": "H₂O", "type": "Pelarut"},
    "Hidrogen Peroksida (H₂O₂)": {"color": "#F0F8FF", "formula": "H₂O₂", "type": "Oksidator"},
    "Natrium Karbonat (Na₂CO₃)": {"color": "#FFFFFF", "formula": "Na₂CO₃", "type": "Garam"},
    "Kalsium Klorida (CaCl₂)": {"color": "#FFFFFF", "formula": "CaCl₂", "type": "Garam"},
    "Asam Asetat (CH₃COOH)": {"color": "#F5F5DC", "formula": "CH₃COOH", "type": "Asam Lemah"},
    "Amonia (NH₃)": {"color": "#F0F8FF", "formula": "NH₃", "type": "Basa Lemah"},
    "Etanol (C₂H₅OH)": {"color": "#F0FFF0", "formula": "C₂H₅OH", "type": "Alkohol"},
    "Metana (CH₄)": {"color": "#87CEEB", "formula": "CH₄", "type": "Hidrokarbon"},
    "Glukosa (C₆H₁₂O₆)": {"color": "#FFFFFF", "formula": "C₆H₁₂O₆", "type": "Karbohidrat"},
    "Natrium Klorida (NaCl)": {"color": "#FFFFFF", "formula": "NaCl", "type": "Garam"},
    "Besi Sulfat (FeSO₄)": {"color": "#76D7EA", "formula": "FeSO₄", "type": "Garam"},
    "Karbon Dioksida (CO₂)": {"color": "#A9A9A9", "formula": "CO₂", "type": "Gas"},
    "Oksigen (O₂)": {"color": "#87CEEB", "formula": "O₂", "type": "Gas"},
    "Tembaga (Cu)": {"color": "#D2691E", "formula": "Cu", "type": "Logam"},
}

# Database reaksi kimia
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
]

# Fungsi untuk membuat kartu unsur
def create_element_card(element):
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
            <p style="text-align:center; margin:5px 0; font-size:1rem;">
                <b>No Atom:</b> {element['AtomicNumber']}<br>
                <b>Massa:</b> {element['AtomicMass']}<br>
                <b>Golongan:</b> {element['Group']}<br>
                <b>Periode:</b> {element['Period']}<br>
                <b>Kategori:</b> {element['Category']}
            </p>
        </div>
    </div>
    """
    return card

# Fungsi untuk menampilkan tabel periodik
def show_periodic_table():
    st.header("📊 Tabel Periodik Interaktif")
    st.markdown("""
    <div class="periodic-header">
        <h2 style="color:white; text-align:center; font-size:32px;">Tabel Periodik Unsur Kimia</h2>
        <p style="text-align:center; font-size:18px;">Klik pada kartu unsur untuk melihat detail lengkap</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Kategori warna
    categories = {
        "Alkali Metal": "#FFD166",
        "Alkaline Earth Metal": "#06D6A0",
        "Transition Metal": "#118AB2",
        "Post-Transition Metal": "#073B4C",
        "Metalloid": "#6A4C93",
        "Nonmetal": "#FF6B6B",
        "Halogen": "#4ECDC4",
        "Noble Gas": "#EF476F",
        "Lanthanide": "#FF9E6D",
        "Actinide": "#FF9E6D"
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
    
    fig.update_layout(
        title="Massa Atom vs Nomor Atom",
        xaxis_title="Nomor Atom",
        yaxis_title="Massa Atom",
        template="plotly_white",
        legend_title_text="Kategori",
        font=dict(size=14),
        hoverlabel=dict(font_size=16)
    )
    
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
        
    with col2:
        compound2 = st.selectbox("Pilih Senyawa Kedua", list(COMPOUNDS.keys()), key="compound2")
        color2 = COMPOUNDS[compound2]["color"]
        st.markdown(f"<div style='background:{color2}; height:50px; border-radius:10px;'></div>", unsafe_allow_html=True)
    
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
                <p style="font-size:16px;">{rtype['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Simbol bahaya
    st.subheader("⚠ Simbol Bahaya Laboratorium")
    hazard_symbols = [
        {"name": "Korosif", "emoji": "⚠", "desc": "Dapat merusak jaringan hidup dan material"},
        {"name": "Mudah Terbakar", "emoji": "🔥", "desc": "Mudah menyala saat terkena api atau panas"},
        {"name": "Beracun", "emoji": "☠", "desc": "Dapat menyebabkan kerusakan kesehatan atau kematian"},
        {"name": "Iritan", "emoji": "🧴", "desc": "Dapat menyebabkan iritasi pada kulit atau mata"},
        {"name": "Oksidator", "emoji": "⚡", "desc": "Dapat menyebabkan kebakaran dengan bahan mudah terbakar"},
        {"name": "Radioaktif", "emoji": "☢", "desc": "Memancarkan radiasi berbahaya"}
    ]
    
    cols = st.columns(3)
    for i, hazard in enumerate(hazard_symbols):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="element-card">
                <div style="display:flex; align-items:center; margin-bottom:15px;">
                    <span style="font-size:36px; margin-right:15px;">{hazard['emoji']}</span>
                    <h3 style="margin:0;">{hazard['name']}</h3>
                </div>
                <p style="font-size:16px;">{hazard['desc']}</p>
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
                <p style="font-size:16px;">{apd['desc']}</p>
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
                <span style="font-size:24px; margin-right:15px;">🔒</span>
                <p style="margin:0; font-size:16px;">{i+1}. {tip}</p>
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
tab1, tab2, tab3 = st.tabs(["Tabel Periodik", "Simulator Reaksi", "Ensiklopedia Kimia"])

with tab1:
    show_periodic_table()

with tab2:
    show_reaction_simulator()

with tab3:
    show_additional_info()

# Footer
st.divider()
st.markdown("""
<div style="text-align:center; padding:30px; color:#1A535C;">
    <p style="font-size:18px; margin:0;">🔬 Laboratorium Kimia Interaktif © 2023</p>
    <p style="font-size:16px; margin:10px 0;">Dikembangkan dengan Streamlit | Untuk tujuan edukasi</p>
    <p style="font-size:14px; margin:0;">Versi 2.0 | Terakhir diperbarui: 18 Juli 2023</p>
</div>
""", unsafe_allow_html=True)
