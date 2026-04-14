# ============================================================
#  🍽️  ZOMATO EDA DASHBOARD  —  Streamlit App
#  Author : Namit Nitin Chuke
#  GitHub : https://github.com/Namitchuke
#  LinkedIn: https://www.linkedin.com/in/namit-nitin-chuke/
#  Dataset : Zomato Metropolitan Restaurants (Kaggle)
#
#  Requirements:
#    pip install streamlit pandas numpy plotly folium streamlit-folium
#
#  Run:
#    streamlit run zomato_dashboard.py
# ============================================================

import warnings
warnings.filterwarnings("ignore")

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

# ──────────────────────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Zomato EDA Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────────────────
#  BRAND TOKENS (Dark Mode Edition)
# ──────────────────────────────────────────────────────────────
Z_RED      = "#FF3D4E"
Z_DARK     = "#E23744"
Z_WHITE    = "#FFFFFF"
Z_DARK_BG  = "#0F0F0F"
Z_CARD_BG  = "#1A1A1A"
Z_LIGHT    = "#252525"
Z_PINK     = "#FFB3B8"
T_WHITE    = "#FFFFFF"
T_GRAY     = "#A0A0A0"
T_DARK     = "#E5E5E5"

# ──────────────────────────────────────────────────────────────
#  GLOBAL CSS INJECTION
# ──────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');

/* ── Base ── */
[data-testid="stAppViewContainer"] {{
    background-color: {Z_DARK_BG};
    font-family: 'Outfit', sans-serif;
    color: {T_WHITE};
}}
[data-testid="stHeader"]    {{ background: transparent; }}
[data-testid="stSidebar"]   {{ background: {Z_CARD_BG}; border-right: 1px solid #333; }}
.block-container             {{ padding-top: 1.5rem; padding-bottom: 3rem; }}

/* ── Text Visibility Fix ── */
p, span, div, label {{
    color: {T_WHITE} !important;
}}
h1, h2, h3, h4 {{
    color: {T_WHITE} !important;
}}

/* ── Hero Banner ── */
.hero-banner {{
    background: linear-gradient(135deg, #1A1A1A 0%, {Z_RED} 100%);
    padding: 3rem 3rem;
    border-radius: 24px;
    margin-bottom: 2.5rem;
    color: white !important;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    border: 1px solid rgba(255,255,255,0.05);
}}
.hero-title {{
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -1px;
    margin: 0 0 0.5rem 0;
    color: white !important;
}}
.hero-sub {{
    font-size: 1.15rem;
    opacity: 0.9;
    margin: 0;
    font-weight: 500;
    color: white !important;
}}
.hero-pills {{
    display: flex;
    gap: 0.8rem;
    margin-top: 1.8rem;
    flex-wrap: wrap;
}}
.hero-pill {{
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: 0.5rem 1.2rem;
    font-size: 0.85rem;
    font-weight: 600;
    backdrop-filter: blur(12px);
    display: flex;
    align-items: center;
    gap: 0.6rem;
    color: white !important;
}}

/* ── KPI Cards ── */
.kpi-card {{
    background: {Z_CARD_BG};
    border: 1px solid #333;
    border-radius: 20px;
    padding: 1.8rem 1.4rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    text-align: center;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    margin-bottom: 1rem;
}}
.kpi-card:hover {{
    box-shadow: 0 15px 40px rgba(255,61,78,0.15);
    transform: translateY(-8px);
    border-color: {Z_RED};
}}
.kpi-icon-row {{ 
    margin-bottom: 1rem;
    display: flex;
    justify-content: center;
    opacity: 0.9;
}}
.kpi-value {{
    font-size: 2.4rem;
    font-weight: 800;
    color: {Z_RED} !important;
    margin: 0.5rem 0 0.2rem 0;
    line-height: 1;
}}
.kpi-label {{
    font-size: 0.85rem;
    color: {T_GRAY} !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
}}

/* ── Section Headers ── */
.section-header {{
    display: flex;
    align-items: center;
    gap: 0.8rem;
    border-bottom: 1px solid #333;
    padding-bottom: 0.6rem;
    margin: 0.5rem 0 1.2rem 0;
}}
.section-icon {{
    display: flex;
    align-items: center;
    justify-content: center;
    background: {Z_LIGHT};
    padding: 0.6rem;
    border-radius: 12px;
    border: 1px solid #444;
}}
.section-title {{
    font-size: 1.6rem;
    font-weight: 700;
    color: {T_WHITE} !important;
    margin: 0;
    letter-spacing: -0.5px;
}}

/* ── Insight Box ── */
.insight-box {{
    background: #252525;
    border-left: 4px solid {Z_RED};
    border-radius: 0 12px 12px 0;
    padding: 1.1rem 1.5rem;
    margin-top: 0.4rem;
}}
.insight-label {{
    font-size: 0.73rem;
    font-weight: 800;
    color: {Z_DARK};
    text-transform: uppercase;
    letter-spacing: 0.9px;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}}
.insight-list {{
    font-size: 0.91rem;
    color: {T_DARK};
    line-height: 1.65;
    margin: 0;
    padding-left: 1.2rem;
}}
.insight-list li {{ margin-bottom: 0.35rem; }}

/* ── Sidebar ── */
.sidebar-title {{
    color: {Z_RED} !important;
    font-weight: 800;
    font-size: 1.7rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}}
[data-testid="stSidebar"] label {{
    color: {T_WHITE} !important;
}}
[data-testid="stFileUploader"] {{
    background: #222;
    border-radius: 12px;
    padding: 10px;
}}

/* ── Charts ── */
[data-testid="stPlotlyChart"] {{
    background: {Z_CARD_BG};
    border-radius: 20px;
    overflow: hidden;
    padding: 10px;
    border: 1px solid #333;
}}

/* ── Expander ── */
[data-testid="stExpander"] {{
    border: 1px solid #F0E6E7 !important;
    border-radius: 10px !important;
    overflow: hidden;
}}
[data-testid="stExpander"] summary {{
    font-weight: 600;
    color: {Z_DARK};
    font-size: 0.88rem;
}}

.z-divider {{
    height: 1px;
    background: linear-gradient(to right, {Z_RED} 0%, {Z_PINK} 60%, transparent 100%);
    margin: 1.2rem 0 0.5rem 0;
    border: none;
    border-radius: 2px;
    opacity: 0.5;
}}

/* ── Conclusion Grid ── */
.conclusion-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.4rem;
}}
.conclusion-card {{
    background: {Z_CARD_BG};
    border: 1px solid #333;
    border-radius: 18px;
    padding: 1.6rem;
    border-top: 3px solid {Z_RED};
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}}
.conclusion-head {{
    font-weight: 700;
    color: {Z_RED};
    font-size: 1rem;
    margin-bottom: 0.6rem;
}}
.conclusion-body {{
    color: {T_GRAY};
    font-size: 0.9rem;
    line-height: 1.65;
    margin: 0;
}}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
#  ICON SYSTEM (Lucide-inspired SVGs)
# ──────────────────────────────────────────────────────────────
ICONS = {
    "store": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    "map-pin": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
    "star": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    "truck": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-5h-7v7Z"/><path d="M13 9h4"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/></svg>',
    "coins": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="8" r="6"/><path d="M18.09 10.37A6 6 0 1 1 10.34 18.06"/><path d="M7 6h1v4"/><path d="m16.71 13.88.7.71-2.82 2.82"/></svg>',
    "award": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15.477 12.89 1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526"/><circle cx="12" cy="8" r="6"/></svg>',
    "map": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" y1="3" x2="9" y2="18"/><line x1="15" y1="6" x2="15" y2="21"/></svg>',
    "bar-chart-3": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>',
    "message-square": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "badge-check": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/><path d="m9 12 2 2 4-4"/></svg>',
    "clipboard-check": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/></svg>',
    "lightbulb": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A5 5 0 0 0 8 8c0 1.3.5 2.6 1.5 3.5.8.8 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>',
    "utensils": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/></svg>'
}

def get_icon(name: str, color: str = "currentColor") -> str:
    """Returns SVG string with replaced color."""
    return ICONS.get(name, "").replace('currentColor', color)


# ──────────────────────────────────────────────────────────────
#  HELPER FUNCTIONS
# ──────────────────────────────────────────────────────────────

def kpi_card(icon_name: str, value: str, label: str) -> str:
    """Returns an HTML KPI card with SVG icon."""
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon-row">{get_icon(icon_name, Z_RED)}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>"""


def section_header(icon_name: str, title: str):
    """Renders a styled section header with SVG and red underline."""
    st.markdown(f"""
    <div class="section-header">
        <div class="section-icon">{get_icon(icon_name, Z_RED)}</div>
        <p class="section-title">{title}</p>
    </div>""", unsafe_allow_html=True)


def insight_expander(section_name: str, bullets: list):
    """Renders a collapsible insight expander with a modern stylized box."""
    with st.expander(f"Analyst Insight — {section_name}", expanded=False):
        items = "".join([f"<li>{b}</li>" for b in bullets])
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-label">{get_icon('lightbulb', Z_DARK)} &nbsp; Key Observations</div>
            <ul class="insight-list">{items}</ul>
        </div>""", unsafe_allow_html=True)


def divider():
    """Renders a Zomato-red gradient divider."""
    st.markdown('<hr class="z-divider">', unsafe_allow_html=True)


def plotly_base() -> dict:
    """Returns base Plotly layout kwargs for Dark Mode branding."""
    return dict(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit, sans-serif", color=T_WHITE, size=12),
    )


def h_bar(df_plot, x, y, title, text_fmt="%{text}", height=420, margin_r=70, margin_l=160, text_col=None):
    """Renders a branded horizontal bar chart."""
    if text_col is None:
        text_col = x
    fig = px.bar(
        df_plot, x=x, y=y, orientation="h", title=title,
        color=x,
        color_continuous_scale=[Z_PINK, Z_RED],
        text=text_col,
        template="plotly_dark"
    )
    fig.update_traces(texttemplate=text_fmt, textposition="outside", cliponaxis=False)
    fig.update_layout(
        height=height,
        font=plotly_base()["font"],
        showlegend=False,
        coloraxis_showscale=False,
        yaxis_title="",
        margin=dict(l=margin_l, r=margin_r, t=50, b=20),
        title_font_size=15,
    )
    return fig


# ──────────────────────────────────────────────────────────────
#  DATA LOADING & PREPROCESSING
# ──────────────────────────────────────────────────────────────

@st.cache_data(show_spinner="Processing dataset…")
def load_and_clean(file) -> pd.DataFrame:
    df = pd.read_csv(file)

    # Standardise city column
    df["City"] = df["City"].str.strip().str.title()
    locality_map = {
        "Banaswadi": "Bangalore",
        "Ulsoor": "Bangalore",
        "Magrath Road": "Bangalore",
        "Malleshwaram": "Bangalore",
    }
    df["City"] = df["City"].replace(locality_map)

    # Coerce ratings
    df["Dining_Rating"]   = pd.to_numeric(df["Dining_Rating"],   errors="coerce")
    df["Delivery_Rating"] = pd.to_numeric(df["Delivery_Rating"], errors="coerce")

    # Fill nulls
    df["Best_Seller"] = df["Best_Seller"].fillna("NA")

    # Engineered features
    df["total_votes"]  = df["Dining_Votes"]   + df["Delivery_Votes"]
    df["Total_rating"] = df["Dining_Rating"]   + df["Delivery_Rating"]

    return df


# ──────────────────────────────────────────────────────────────
#  SIDEBAR
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f'<div class="sidebar-title">{get_icon("award")} Project Portfolio</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Designer & Sources Section
    st.markdown(f"""
    <div style="background:rgba(255,61,78,0.05); border-radius:12px; padding:1.2rem; border:1px solid rgba(255,61,78,0.1)">
        <p style="font-weight:700; color:{Z_RED}; margin-bottom:0.8rem; font-size:0.9rem">DEVELOPER CONTEXT</p>
        <div style="font-size:0.85rem; color:{T_WHITE}; line-height:1.8">
            <b>{get_icon("map-pin", Z_RED)} Based in</b>: India<br>
            <b>{get_icon("star", Z_RED)} Expertise</b>: Data Analyst<br>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Professional Links
    st.markdown(f"""
    <div style="display:flex; flex-direction:column; gap:0.6rem">
        <a href="https://github.com/Namitchuke" target="_blank" style="text-decoration:none">
            <div style="background:#222; padding:0.6rem 1rem; border-radius:8px; display:flex; align-items:center; gap:0.7rem; border:1px solid #333">
                {get_icon("message-square", Z_RED)} <span style="color:white; font-size:0.85rem">GitHub Profile</span>
            </div>
        </a>
        <a href="https://www.linkedin.com/in/namit-nitin-chuke/" target="_blank" style="text-decoration:none">
            <div style="background:#222; padding:0.6rem 1rem; border-radius:8px; display:flex; align-items:center; gap:0.7rem; border:1px solid #333">
                {get_icon("award", Z_RED)} <span style="color:white; font-size:0.85rem">LinkedIn Expert</span>
            </div>
        </a>
        <a href="mailto:namitchuke.work@gmail.com" target="_blank" style="text-decoration:none">
            <div style="background:#222; padding:0.6rem 1rem; border-radius:8px; display:flex; align-items:center; gap:0.7rem; border:1px solid #333">
                {get_icon("truck", Z_RED)} <span style="color:white; font-size:0.85rem">Email Collaboration</span>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:0.82rem; color:{T_GRAY}; line-height:1.7">
        <p style="font-weight:700; color:{Z_RED}">DATA SOURCE</p>
        <a href="https://www.kaggle.com/datasets/narsingraogoud/zomato-restaurants-dataset-for-metropolitan-areas"
           style="color:{Z_RED}; text-decoration:none" target="_blank">{get_icon("map", Z_RED)} Zomato Kaggle Dataset ↗</a>
    </div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
#  GATE & LOAD DATA
# ──────────────────────────────────────────────────────────────
DEFAULT_CSV = "zomato_dataset.csv"

if os.path.exists(DEFAULT_CSV):
    df = load_and_clean(DEFAULT_CSV)
else:
    st.markdown(f"""
    <div class="hero-banner" style="text-align:center">
        <div class="hero-title">Zomato Restaurant Analytics</div>
        <div class="hero-sub" style="margin-top:.8rem">
            High-performance data intelligence for the Indian food service industry.<br>
            Please ensure `{DEFAULT_CSV}` is present in the project directory.
        </div>
    </div>""", unsafe_allow_html=True)
    st.stop()


# ──────────────────────────────────────────────────────────────
#  ① HERO BANNER
# ──────────────────────────────────────────────────────────────
n_rows  = df.shape[0]
n_rest  = df["Restaurant_Name"].nunique()
n_city  = df["City"].nunique()
n_items = df["Item_Name"].nunique()

st.markdown(f"""
<div class="hero-banner">
    <div class="hero-title">Zomato Restaurant Analytics</div>
    <div class="hero-sub">
        Advanced EDA • Metropolitan India • Professional Edition
    </div>
    <div class="hero-pills">
        <span class="hero-pill">{get_icon('clipboard-check', 'white')} {n_rows:,} records</span>
        <span class="hero-pill">{get_icon('store', 'white')} {n_rest:,} restaurants</span>
        <span class="hero-pill">{get_icon('map-pin', 'white')} {n_city} cities</span>
        <span class="hero-pill">{get_icon('utensils', 'white')} {n_items:,} menu items</span>
    </div>
</div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
#  ② KPI CARDS  (3-col × 2 rows)
# ──────────────────────────────────────────────────────────────
section_header("bar-chart-3", "Key Performance Indicators")

avg_dining   = df["Dining_Rating"].mean()
avg_delivery = df["Delivery_Rating"].mean()
avg_price    = df["Prices"].mean()
top_city     = df.groupby("City")["Restaurant_Name"].nunique().idxmax()
total_votes  = int(df["total_votes"].sum())
bs_tagged    = df[df["Best_Seller"] != "NA"].shape[0]
bs_pct       = bs_tagged / len(df) * 100

r1c1, r1c2, r1c3 = st.columns(3)
r2c1, r2c2, r2c3 = st.columns(3)

with r1c1: st.markdown(kpi_card("store", f"{n_rest:,}",           "Unique Restaurants"),    unsafe_allow_html=True)
with r1c2: st.markdown(kpi_card("map-pin", f"{n_city}",             "Metro Cities"),           unsafe_allow_html=True)
with r1c3: st.markdown(kpi_card("star", f"{avg_dining:.2f}",     "Avg Dining Rating"),      unsafe_allow_html=True)
with r2c1: st.markdown(kpi_card("truck", f"{avg_delivery:.2f}",   "Avg Delivery Rating"),    unsafe_allow_html=True)
with r2c2: st.markdown(kpi_card("coins", f"₹{avg_price:.0f}",    "Avg Item Price"),         unsafe_allow_html=True)
with r2c3: st.markdown(kpi_card("award", top_city,                "Most Listed City"),       unsafe_allow_html=True)

divider()


# ──────────────────────────────────────────────────────────────
#  ③ RESTAURANT DISTRIBUTION BY CITY
# ──────────────────────────────────────────────────────────────
section_header("map-pin", "Restaurant Distribution by City")

col1, col2 = st.columns(2)

with col1:
    res_count = (
        df.groupby("City")["Restaurant_Name"].nunique()
        .reset_index(name="Count")
    )
    res_count["City_Bold"] = "<b>" + res_count["City"] + "</b>"
    fig_res_tree = px.treemap(res_count, path=[px.Constant("<b>India</b>"), "City_Bold"], values="Count",
                              color="Count", color_continuous_scale=[Z_PINK, Z_RED],
                              title="Unique Restaurants per City")
    fig_res_tree.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                               margin=dict(t=50, l=10, r=10, b=10), font=plotly_base()["font"], coloraxis_showscale=False)
    fig_res_tree.update_traces(textinfo="label+value+percent parent")
    st.plotly_chart(fig_res_tree, use_container_width=True)

with col2:
    menu_count = (
        df.groupby("City").size()
        .reset_index(name="Menu Items")
    )
    menu_count["City_Bold"] = "<b>" + menu_count["City"] + "</b>"
    fig_menu_tree = px.treemap(menu_count, path=[px.Constant("<b>India</b>"), "City_Bold"], values="Menu Items",
                               color="Menu Items", color_continuous_scale=[Z_PINK, Z_RED],
                               title="Total Menu Listings per City")
    fig_menu_tree.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                                margin=dict(t=50, l=10, r=10, b=10), font=plotly_base()["font"], coloraxis_showscale=False)
    fig_menu_tree.update_traces(textinfo="label+value+percent parent")
    st.plotly_chart(fig_menu_tree, use_container_width=True)

insight_expander("Restaurant Distribution", [
    "Hyderabad leads with the highest count of unique restaurants, reflecting a mature, competitive delivery market with deep platform penetration.",
    "Jaipur and Mumbai follow closely — strong consumer demand and high Zomato adoption characterise both cities.",
    "Goa, Lucknow, and Raipur have significantly fewer listings, representing high-potential, low-competition expansion targets.",
    "Mumbai's vote-to-restaurant ratio is disproportionately high — fewer outlets but far more reviews — signalling premium engagement density and ideal launch conditions for a new venture.",
])

divider()


# ──────────────────────────────────────────────────────────────
#  ④ PRICING ANALYSIS
# ──────────────────────────────────────────────────────────────
section_header("coins", "Pricing Analysis")

col1, col2 = st.columns(2)

with col1:
    avg_price_city = (
        df.groupby("City")["Prices"].mean().round(0)
        .reset_index(name="Avg Price (₹)")
        .sort_values("Avg Price (₹)")
    )
    fig_price = h_bar(avg_price_city, "Avg Price (₹)", "City",
                      "Average Item Price by City", text_fmt="₹%{text:.0f}")
    fig_price.update_traces(marker_color=Z_RED)
    st.plotly_chart(fig_price, use_container_width=True)

with col2:
    cuisine_col = "Cuisine " if "Cuisine " in df.columns else "Cuisine"
    df_city_max = df.groupby(["City", cuisine_col, "Item_Name"], as_index=False)["Prices"].max()
    idx = df_city_max.groupby("City")["Prices"].idxmax()
    max_price_df = df_city_max.loc[idx].sort_values("Prices", ascending=True)

    fig_max_price = h_bar(max_price_df, "Prices", "City",
                          "Most Expensive Dish per City", text_fmt="₹%{text:.0f}", margin_r=80)
    
    # Add dish details to hover data
    fig_max_price.update_traces(
        customdata=max_price_df[["Item_Name", cuisine_col]],
        hovertemplate="<b>%{y}</b><br>Dish: %{customdata[0]}<br>Cuisine: %{customdata[1]}<br>Price: ₹%{x}<extra></extra>"
    )
    st.plotly_chart(fig_max_price, use_container_width=True)

insight_expander("Pricing Analysis", [
    "Mumbai commands the highest average item price (₹304), reflecting its affluent consumer base and premium market positioning.",
    "Raipur and Lucknow sit in the moderate range — budget-sensitive demographics that respond strongly to value deals and combo offers.",
    "The most expensive individual dishes typically belong to large-format or specialty categories: seafood platters, biryani-for-two, and grilled meats.",
    "Significant price disparity across cities enables geo-targeted menu pricing strategies for multi-city restaurant chains — a leakage many brands currently miss.",
])

divider()


# ──────────────────────────────────────────────────────────────
#  ⑤ RATINGS & DELIVERY PERFORMANCE
# ──────────────────────────────────────────────────────────────
section_header("star", "Ratings & Delivery Performance")

col1, col2 = st.columns(2)

# Combined dataframe for ratings
ratings_df = df.groupby("City")[["Dining_Rating", "Delivery_Rating"]].mean().round(2).reset_index()
ratings_df = ratings_df.sort_values("Dining_Rating")

fig_ratings = go.Figure()
# Add horizontal lines
for i in range(len(ratings_df)):
    fig_ratings.add_trace(go.Scatter(
        x=[ratings_df["Delivery_Rating"].iloc[i], ratings_df["Dining_Rating"].iloc[i]],
        y=[ratings_df["City"].iloc[i], ratings_df["City"].iloc[i]],
        mode="lines", line=dict(color="#555", width=2),
        showlegend=False
    ))
# Add Delivery points
fig_ratings.add_trace(go.Scatter(
    x=ratings_df["Delivery_Rating"], y=ratings_df["City"],
    mode="markers", marker=dict(color=Z_PINK, size=12),
    name="Delivery Rating 🚚"
))
# Add Dining points
fig_ratings.add_trace(go.Scatter(
    x=ratings_df["Dining_Rating"], y=ratings_df["City"],
    mode="markers", marker=dict(color=Z_RED, size=12),
    name="Dining Rating 🍽️"
))

fig_ratings.update_layout(
    template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=140, r=40, t=50, b=20),
    xaxis=dict(title="Rating ⭐", range=[3.0, 5.0]),
    yaxis=dict(title=""),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    font=plotly_base()["font"]
)
st.plotly_chart(fig_ratings, use_container_width=True)

insight_expander("Ratings & Delivery Performance", [
    "Pune, Hyderabad, and Jaipur lead in average delivery ratings — evidence of strong last-mile logistics, partner compliance, and operational rigor.",
    "Several cities show a measurable gap between dining and delivery ratings, indicating that in-person excellence doesn't automatically transfer to delivery operations.",
    "Cities with below-average delivery ratings (Goa, Raipur) would benefit from targeted SLA enforcement, delivery partner training, and feedback incentive programs.",
    "High delivery ratings correlate positively with higher delivery vote counts — rating credibility is self-reinforcing in mature, engaged markets.",
])

divider()


# ──────────────────────────────────────────────────────────────
#  ⑥ CUSTOMER ENGAGEMENT — VOTES
# ──────────────────────────────────────────────────────────────
section_header("message-square", "Customer Engagement — Delivery & Dining Votes")

col1, col2 = st.columns(2)

with col1:
    del_votes = (
        df.groupby("City")["Delivery_Votes"].sum()
        .reset_index(name="Delivery Votes")
        .sort_values("Delivery Votes")
    )
    total_del = del_votes["Delivery Votes"].sum()
    del_votes["Label"] = del_votes["Delivery Votes"].apply(lambda v: f"{v/1e6:.2f}M ({v/total_del*100:.1f}%)" if v>=1e6 else f"{v/1000:.0f}k ({v/total_del*100:.1f}%)")
    fig_dv = h_bar(del_votes, "Delivery Votes", "City",
                   "Total Delivery Votes by City", margin_r=130, text_col="Label")
    st.plotly_chart(fig_dv, use_container_width=True)

with col2:
    din_votes = (
        df.groupby("City")["Dining_Votes"].sum()
        .reset_index(name="Dining Votes")
        .sort_values("Dining Votes")
    )
    total_din = din_votes["Dining Votes"].sum()
    din_votes["Label"] = din_votes["Dining Votes"].apply(lambda v: f"{v/1e6:.2f}M ({v/total_din*100:.1f}%)" if v>=1e6 else f"{v/1000:.0f}k ({v/total_din*100:.1f}%)")
    fig_dnv = h_bar(din_votes, "Dining Votes", "City",
                    "Total Dining Votes by City", margin_r=130, text_col="Label")
    st.plotly_chart(fig_dnv, use_container_width=True)

insight_expander("Customer Engagement", [
    "Mumbai and Bangalore generate the highest total vote counts across both dining and delivery — confirming their status as India's most digitally engaged food markets.",
    "Mumbai's votes-to-restaurants ratio is particularly striking: fewer outlets but significantly more reviews — making it the optimal city for a new restaurant launch with high organic discoverability.",
    "Cities with low engagement scores (Goa, Raipur, Lucknow) are prime candidates for promotional campaigns, loyalty programs, and review incentive mechanics to bootstrap engagement flywheels.",
    "High engagement is a compounding moat: more votes → higher ranking → more orders → more votes. Early dominance in engagement translates to long-term platform visibility.",
])

divider()




# ──────────────────────────────────────────────────────────────
#  ⑧ BEST SELLER MENU ANALYSIS
# ──────────────────────────────────────────────────────────────
section_header("badge-check", "Menu Category Distribution — Best Sellers")

col1, col2 = st.columns(2)

DONUT_COLORS = [Z_RED, "#FF6B6B", Z_PINK, Z_DARK, "#FF8C94"]

with col1:
    df_bs = df[df["Best_Seller"] != "NA"]
    bs_counts = df_bs["Best_Seller"].value_counts().nlargest(5).reset_index()
    bs_counts.columns = ["Category", "Count"]
    total_bs = bs_counts["Count"].sum()
    bs_counts["Label"] = bs_counts.apply(lambda row: f"{row['Category']}<br>{row['Count']:,} ({row['Count']/total_bs*100:.1f}%)", axis=1)

    fig_bs = px.pie(
        bs_counts, values="Count", names="Category", title="Top 5 Best Seller Categories",
        color_discrete_sequence=DONUT_COLORS, hole=0.5
    )
    fig_bs.update_traces(text=bs_counts["Label"], textinfo="text", textposition="outside", marker=dict(line=dict(color=Z_DARK_BG, width=2)))
    fig_bs.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         showlegend=False, margin=dict(t=50, b=30, l=100, r=100), font=plotly_base()["font"])
    st.plotly_chart(fig_bs, use_container_width=True)

with col2:
    bs_ratio = (
        df["Best_Seller"].apply(lambda x: "Tagged" if x != "NA" else "Untagged").value_counts().reset_index()
    )
    bs_ratio.columns = ["Status", "Count"]
    total_ratio = bs_ratio["Count"].sum()
    bs_ratio["Label"] = bs_ratio.apply(
        lambda row: f"{row['Status']}<br>{row['Count']/1000:.1f}k ({row['Count']/total_ratio*100:.1f}%)" if row['Count']>=1000 
        else f"{row['Status']}<br>{row['Count']:,} ({row['Count']/total_ratio*100:.1f}%)", axis=1
    )

    fig_ratio = px.pie(
        bs_ratio, values="Count", names="Status", title="Tagged vs Untagged Items",
        color_discrete_sequence=[Z_RED, Z_PINK], hole=0.5
    )
    fig_ratio.update_traces(text=bs_ratio["Label"], textinfo="text", textposition="outside", marker=dict(line=dict(color=Z_DARK_BG, width=2)))
    fig_ratio.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            showlegend=False, margin=dict(t=50, b=30, l=60, r=60), font=plotly_base()["font"])
    st.plotly_chart(fig_ratio, use_container_width=True)

insight_expander("Best Seller Analysis", [
    "'BESTSELLER' is the dominant tag, showing that restaurants primarily rely on Zomato's recommendation system to surface popular items.",
    "'MUST TRY' items — though fewer — carry higher perceived premium value and may correlate with higher price points and conversion rates.",
    "The large share of untagged menu items represents a missed marketing opportunity for restaurant operators who underutilise the platform's curation tools.",
    "Strategic tagging drives search-ranking visibility and order conversion — Zomato should incentivise operators to tag high-performing items to improve platform-wide GMV.",
])

divider()


# ──────────────────────────────────────────────────────────────
#  ⑨ GEOSPATIAL MAP
# ──────────────────────────────────────────────────────────────
section_header("map", "Geospatial Restaurant Density — India")

CITY_COORDS = {
    "Hyderabad":  (17.385, 78.486),
    "Jaipur":     (26.912, 75.787),
    "Mumbai":     (19.076, 72.877),
    "Chennai":    (13.082, 80.270),
    "Bangalore":  (12.971, 77.594),
    "Ahmedabad":  (23.022, 72.571),
    "Kolkata":    (22.572, 88.363),
    "Pune":       (18.520, 73.856),
    "Kochi":      (9.931,  76.267),
    "Raipur":     (21.251, 81.629),
    "Lucknow":    (26.846, 80.946),
    "New Delhi":  (28.613, 77.209),
    "Goa":        (15.299, 74.123),
}

city_agg = (
    df.groupby("City")
    .agg(
        Restaurants=("Restaurant_Name", "nunique"),
        Avg_Price=("Prices", "mean"),
        Avg_Delivery=("Delivery_Rating", "mean"),
        Total_Votes=("total_votes", "sum"),
    )
    .reset_index()
)
city_agg["Lat"] = city_agg["City"].map(lambda c: CITY_COORDS.get(c, (20, 78))[0])
city_agg["Lon"] = city_agg["City"].map(lambda c: CITY_COORDS.get(c, (20, 78))[1])

india_map = folium.Map(location=[22.97, 78.65], zoom_start=5, tiles="CartoDB positron")

for _, row in city_agg.iterrows():
    radius = max(float(row["Restaurants"]) * 0.07, 8)
    popup_html = f"""
    <div style="font-family:Segoe UI,sans-serif;min-width:160px">
        <b style="color:{Z_RED};font-size:1rem">{row['City']}</b><br>
        <hr style="margin:4px 0;border-color:#eee">
        🏪 <b>{int(row['Restaurants'])}</b> restaurants<br>
        💰 ₹<b>{row['Avg_Price']:.0f}</b> avg price<br>
        🚴 <b>{row['Avg_Delivery']:.2f}</b> delivery rating<br>
        👍 <b>{int(row['Total_Votes']):,}</b> total votes
    </div>"""
    folium.CircleMarker(
        location=(row["Lat"], row["Lon"]),
        radius=radius,
        popup=folium.Popup(popup_html, max_width=220),
        tooltip=f"{row['City']} — {int(row['Restaurants'])} restaurants",
        color=Z_DARK,
        weight=2,
        fill=True,
        fill_color=Z_RED,
        fill_opacity=0.65,
    ).add_to(india_map)

st_folium(india_map, width=None, height=500, use_container_width=True)

insight_expander("Geospatial Analysis", [
    "South and West Indian cities (Hyderabad, Bangalore, Mumbai, Chennai, Pune) form the core cluster of Zomato's restaurant network — a coastal, high-income metro belt.",
    "North Indian markets like New Delhi and Lucknow are under-indexed relative to their population and economic size, suggesting a northern market gap that competitors could exploit.",
    "Goa is a notable outlier: a small restaurant base serving significant seasonal tourism demand — an ideal target for a curated, premium dining playbook.",
    "Geographic clustering in coastal metros aligns with higher internet penetration, younger demographics, and greater urban disposable income — the core Zomato user profile.",
])

divider()


# ──────────────────────────────────────────────────────────────
#  ⑩ STRATEGIC CONCLUSION
# ──────────────────────────────────────────────────────────────
section_header("clipboard-check", "Strategic Conclusion")

st.markdown(f"""
<div style="background: linear-gradient(135deg, {Z_DARK_BG} 0%, {Z_CARD_BG} 100%);
            border: 1px solid #333; border-radius: 24px; padding: 2.2rem 2.4rem;">
    <div class="conclusion-grid">
        <div class="conclusion-card">
            <div class="conclusion-head">🏙️ Market Size & Saturation</div>
            <p class="conclusion-body">
                Hyderabad, Jaipur, and Mumbai dominate in restaurant density. 
                Lucknow and Raipur offer first-mover advantage with minimal QSR competition 
                and growing digital adoption.
            </p>
        </div>
        <div class="conclusion-card">
            <div class="conclusion-head">🚀 Launch Recommendation</div>
            <p class="conclusion-body">
                Mumbai is the highest-conviction launch city: premium pricing tolerance, 
                a vocal and active reviewer base, and high organic discoverability 
                driven by an exceptional vote-to-restaurant ratio.
            </p>
        </div>
        <div class="conclusion-card">
            <div class="conclusion-head">⭐ Operational Benchmark</div>
            <p class="conclusion-body">
                Pune and Hyderabad lead in delivery ratings — their operational playbooks 
                (SLA enforcement, partner training, packaging standards) should be 
                templated and replicated across underperforming cities.
            </p>
        </div>
        <div class="conclusion-card">
            <div class="conclusion-head">💡 Platform Product Insight</div>
            <p class="conclusion-body">
                Bestseller tagging drives measurable search visibility and conversion uplift. 
                Zomato should build gamified nudges to encourage operators to strategically 
                tag high-performing items — directly improving platform-wide GMV.
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
#  ⑪ UPCOMING STRATEGIES & ROADMAP
# ──────────────────────────────────────────────────────────────
section_header("award", "Upcoming Strategies & Forward Outlook")

st.markdown(f"""
<div style="background: linear-gradient(135deg, {Z_DARK_BG} 0%, #000000 100%);
            border: 1px solid #333; border-radius: 24px; padding: 2.2rem 2.4rem;">
    <div class="conclusion-grid">
        <div class="conclusion-card">
            <div class="conclusion-head">🤖 AI-Driven Hyper-Personalization</div>
            <p class="conclusion-body">
                Leveraging machine learning to predict city-specific menu trends. 
                Integrating dynamic pricing models in mature cities like Mumbai 
                to optimize GMV during peak demand surges.
            </p>
        </div>
        <div class="conclusion-card">
            <div class="conclusion-head">🏙️ Tier-2 Micro-Market Expansion</div>
            <p class="conclusion-body">
                Aggressive expansion in low-competition, high-potential hubs (Raipur, Lucknow). 
                Focusing on exclusive partnerships with regional culinary legends to 
                bootstrap trust and platform loyalty.
            </p>
        </div>
        <div class="conclusion-card">
            <div class="conclusion-head">🚲 Logistics Operational Rigor</div>
            <p class="conclusion-body">
                Replicating Pune's high-efficiency delivery playbook across the coastal belt. 
                Reducing the dining-vs-delivery rating gap through kitchen-side tech 
                integrations and standardized packaging audits.
            </p>
        </div>
        <div class="conclusion-card">
            <div class="conclusion-head">💎 Premium Loyalty & Retension</div>
            <p class="conclusion-body">
                Curating 'Must Try' selections into premium subscription tiers. 
                Incentivizing review density in low-engagement cities through gamified 
                customer feedback flywheels.
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
#  FOOTER
# ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; color:{T_GRAY}; font-size:0.80rem;
            padding: 1.2rem 0 0.5rem 0; border-top: 1px solid #333; margin-top:2rem">
    Built with ❤️, Streamlit,
    Dataset: <a href="https://www.kaggle.com/datasets/narsingraogoud/zomato-restaurants-dataset-for-metropolitan-areas"
                style="color:{Z_RED}" target="_blank">Zomato Kaggle Dataset</a>
    , 
    <a href="https://github.com/Namitchuke" style="color:{Z_RED}" target="_blank">GitHub ↗</a>
    , 
    <a href="https://www.linkedin.com/in/namit-nitin-chuke/" style="color:{Z_RED}" target="_blank">LinkedIn ↗</a>
</div>
""", unsafe_allow_html=True)
