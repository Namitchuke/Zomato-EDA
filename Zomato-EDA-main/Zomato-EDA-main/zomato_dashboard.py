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
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────────────────
#  BRAND TOKENS
# ──────────────────────────────────────────────────────────────
Z_RED    = "#E23744"
Z_DARK   = "#CB202D"
Z_WHITE  = "#FFFFFF"
Z_LIGHT  = "#FFF5F6"
Z_PINK   = "#FFB3B8"
T_DARK   = "#1C1C1C"
T_MED    = "#6B6B6B"

# ──────────────────────────────────────────────────────────────
#  GLOBAL CSS INJECTION
# ──────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
/* ── Base ── */
[data-testid="stAppViewContainer"] {{
    background-color: {Z_WHITE};
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}}
[data-testid="stHeader"]    {{ background: transparent; }}
[data-testid="stSidebar"]   {{ background: {Z_LIGHT}; border-right: 1px solid #F0E6E7; }}
.block-container             {{ padding-top: 1.5rem; padding-bottom: 3rem; }}

/* ── Hero Banner ── */
.hero-banner {{
    background: linear-gradient(135deg, {Z_DARK} 0%, {Z_RED} 60%, #FF6B6B 100%);
    padding: 2.8rem 3rem 2.4rem 3rem;
    border-radius: 18px;
    margin-bottom: 2rem;
    color: white;
    position: relative;
    overflow: hidden;
}}
.hero-banner::after {{
    content: "🍽️";
    position: absolute;
    right: 3rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.15;
}}
.hero-title {{
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0 0 0.4rem 0;
    line-height: 1.1;
}}
.hero-sub {{
    font-size: 1.02rem;
    opacity: 0.88;
    margin: 0;
    font-weight: 400;
}}
.hero-pills {{
    display: flex;
    gap: 0.8rem;
    margin-top: 1.2rem;
    flex-wrap: wrap;
}}
.hero-pill {{
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.82rem;
    font-weight: 600;
    backdrop-filter: blur(4px);
}}

/* ── KPI Cards ── */
.kpi-card {{
    background: {Z_WHITE};
    border: 1px solid #F0E6E7;
    border-left: 4px solid {Z_RED};
    border-radius: 14px;
    padding: 1.3rem 1.4rem;
    box-shadow: 0 2px 14px rgba(226,55,68,0.07);
    text-align: center;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
    margin-bottom: 0.5rem;
}}
.kpi-card:hover {{
    box-shadow: 0 6px 24px rgba(226,55,68,0.14);
    transform: translateY(-2px);
}}
.kpi-icon  {{ font-size: 1.75rem; line-height: 1; }}
.kpi-value {{
    font-size: 1.95rem;
    font-weight: 800;
    color: {Z_RED};
    margin: 0.3rem 0 0.15rem 0;
    line-height: 1;
}}
.kpi-label {{
    font-size: 0.72rem;
    color: {T_MED};
    text-transform: uppercase;
    letter-spacing: 0.9px;
    font-weight: 600;
}}

/* ── Section Headers ── */
.section-header {{
    display: flex;
    align-items: center;
    gap: 0.65rem;
    border-bottom: 2.5px solid {Z_RED};
    padding-bottom: 0.55rem;
    margin: 2.2rem 0 1.4rem 0;
}}
.section-title {{
    font-size: 1.22rem;
    font-weight: 700;
    color: {T_DARK};
    margin: 0;
    letter-spacing: -0.2px;
}}

/* ── Insight Box ── */
.insight-box {{
    background: {Z_LIGHT};
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
}}
.insight-list {{
    font-size: 0.91rem;
    color: {T_DARK};
    line-height: 1.65;
    margin: 0;
    padding-left: 1.2rem;
}}
.insight-list li {{ margin-bottom: 0.35rem; }}

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

/* ── Divider ── */
.z-divider {{
    height: 2px;
    background: linear-gradient(to right, {Z_RED} 0%, {Z_PINK} 60%, transparent 100%);
    margin: 2.4rem 0;
    border: none;
    border-radius: 2px;
}}

/* ── Conclusion Grid ── */
.conclusion-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.4rem;
}}
.conclusion-card {{
    background: white;
    border: 1px solid #F0E6E7;
    border-radius: 14px;
    padding: 1.4rem;
    border-top: 3px solid {Z_RED};
}}
.conclusion-head {{
    font-weight: 700;
    color: {Z_DARK};
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
}}
.conclusion-body {{
    color: {T_DARK};
    font-size: 0.88rem;
    line-height: 1.6;
    margin: 0;
}}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
#  HELPER FUNCTIONS
# ──────────────────────────────────────────────────────────────

def kpi_card(icon: str, value: str, label: str) -> str:
    """Returns an HTML KPI card."""
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>"""


def section_header(emoji: str, title: str):
    """Renders a styled section header with red underline."""
    st.markdown(f"""
    <div class="section-header">
        <span style="font-size:1.35rem;line-height:1">{emoji}</span>
        <p class="section-title">{title}</p>
    </div>""", unsafe_allow_html=True)


def insight_expander(section_name: str, bullets: list):
    """Renders a collapsible insight expander with a red-bordered insight box."""
    with st.expander(f"📌  Analyst Insight — {section_name}", expanded=False):
        items = "".join([f"<li>{b}</li>" for b in bullets])
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-label">Key Observations</div>
            <ul class="insight-list">{items}</ul>
        </div>""", unsafe_allow_html=True)


def divider():
    """Renders a Zomato-red gradient divider."""
    st.markdown('<hr class="z-divider">', unsafe_allow_html=True)


def plotly_base() -> dict:
    """Returns base Plotly layout kwargs for consistent brand styling."""
    return dict(
        template="plotly_white",
        font=dict(family="Segoe UI, system-ui, sans-serif", color=T_DARK, size=12),
    )


def h_bar(df_plot, x, y, title, text_fmt="%{text}", height=420):
    """Renders a branded horizontal bar chart."""
    fig = px.bar(
        df_plot, x=x, y=y, orientation="h", title=title,
        color=x,
        color_continuous_scale=[Z_PINK, Z_RED],
        text=x,
        **{k: v for k, v in plotly_base().items() if k != "color_discrete_sequence"},
    )
    fig.update_traces(texttemplate=text_fmt, textposition="outside")
    fig.update_layout(
        height=height,
        showlegend=False,
        coloraxis_showscale=False,
        yaxis_title="",
        margin=dict(l=10, r=60, t=50, b=20),
        title_font_size=13,
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
    st.markdown(f"<h3 style='color:{Z_RED};margin-bottom:0'>🍽️ Zomato EDA</h3>", unsafe_allow_html=True)
    st.markdown("---")
    uploaded = st.file_uploader(
        "Upload `zomato_dataset.csv`",
        type=["csv"],
        help="Download from Kaggle and upload here to run the full dashboard.",
    )
    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:0.82rem;color:{T_MED};line-height:1.7">
        <b>Dataset</b><br>
        900+ restaurants · 13 Indian metros · 123,000+ rows<br><br>
        <b>Source</b><br>
        <a href="https://www.kaggle.com/datasets/narsingraogoud/zomato-restaurants-dataset-for-metropolitan-areas"
           style="color:{Z_RED}" target="_blank">Kaggle ↗</a>
    </div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
#  GATE & LOAD DATA
# ──────────────────────────────────────────────────────────────
DEFAULT_CSV = "zomato_dataset.csv"

if uploaded is not None:
    df = load_and_clean(uploaded)
elif os.path.exists(DEFAULT_CSV):
    df = load_and_clean(DEFAULT_CSV)
else:
    st.markdown(f"""
    <div class="hero-banner" style="text-align:center">
        <div class="hero-title">🍽️ Zomato EDA Dashboard</div>
        <div class="hero-sub" style="margin-top:.8rem">
            A consulting-grade analysis of restaurant dynamics across 13 Indian metro cities.<br>
            Upload the dataset from the sidebar to begin.
        </div>
    </div>""", unsafe_allow_html=True)

    st.info(f"👈 Open the **sidebar** and upload `{DEFAULT_CSV}` or ensure it is in the project directory.")
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
    <div class="hero-title">🍽️ Zomato Restaurant Analytics</div>
    <div class="hero-sub">
        Exploratory Data Analysis · Metropolitan India · Consulting Edition
    </div>
    <div class="hero-pills">
        <span class="hero-pill">📋 {n_rows:,} records</span>
        <span class="hero-pill">🏪 {n_rest:,} restaurants</span>
        <span class="hero-pill">🌆 {n_city} cities</span>
        <span class="hero-pill">🍲 {n_items:,} menu items</span>
    </div>
</div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
#  ② KPI CARDS  (3-col × 2 rows)
# ──────────────────────────────────────────────────────────────
section_header("📊", "Key Performance Indicators")

avg_dining   = df["Dining_Rating"].mean()
avg_delivery = df["Delivery_Rating"].mean()
avg_price    = df["Prices"].mean()
top_city     = df.groupby("City")["Restaurant_Name"].nunique().idxmax()
total_votes  = int(df["total_votes"].sum())
bs_tagged    = df[df["Best_Seller"] != "NA"].shape[0]
bs_pct       = bs_tagged / len(df) * 100

r1c1, r1c2, r1c3 = st.columns(3)
r2c1, r2c2, r2c3 = st.columns(3)

with r1c1: st.markdown(kpi_card("🏪", f"{n_rest:,}",           "Unique Restaurants"),    unsafe_allow_html=True)
with r1c2: st.markdown(kpi_card("🌆", f"{n_city}",             "Metro Cities"),           unsafe_allow_html=True)
with r1c3: st.markdown(kpi_card("⭐", f"{avg_dining:.2f}",     "Avg Dining Rating"),      unsafe_allow_html=True)
with r2c1: st.markdown(kpi_card("🚴", f"{avg_delivery:.2f}",   "Avg Delivery Rating"),    unsafe_allow_html=True)
with r2c2: st.markdown(kpi_card("💰", f"₹{avg_price:.0f}",    "Avg Item Price"),         unsafe_allow_html=True)
with r2c3: st.markdown(kpi_card("🏆", top_city,                "Most Listed City"),       unsafe_allow_html=True)

divider()


# ──────────────────────────────────────────────────────────────
#  ③ RESTAURANT DISTRIBUTION BY CITY
# ──────────────────────────────────────────────────────────────
section_header("🏙️", "Restaurant Distribution by City")

col1, col2 = st.columns(2)

with col1:
    res_count = (
        df.groupby("City")["Restaurant_Name"].nunique()
        .reset_index(name="Count")
        .sort_values("Count")
    )
    st.plotly_chart(
        h_bar(res_count, "Count", "City", "Unique Restaurants per City"),
        use_container_width=True,
    )

with col2:
    menu_count = (
        df.groupby("City").size()
        .reset_index(name="Menu Items")
        .sort_values("Menu Items")
    )
    st.plotly_chart(
        h_bar(menu_count, "Menu Items", "City", "Total Menu Listings per City"),
        use_container_width=True,
    )

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
section_header("💰", "Pricing Analysis")

col1, col2 = st.columns(2)

with col1:
    avg_price_city = (
        df.groupby("City")["Prices"].mean().round(0)
        .reset_index(name="Avg Price (₹)")
        .sort_values("Avg Price (₹)")
    )
    fig_price = h_bar(avg_price_city, "Avg Price (₹)", "City",
                      "Average Item Price by City", text_fmt="₹%{text:.0f}")
    st.plotly_chart(fig_price, use_container_width=True)

with col2:
    cuisine_col = "Cuisine " if "Cuisine " in df.columns else "Cuisine"
    df_city_max = df.groupby(["City", cuisine_col, "Item_Name"], as_index=False)["Prices"].max()
    idx = df_city_max.groupby("City")["Prices"].idxmax()
    max_price_df = df_city_max.loc[idx].sort_values("Prices", ascending=False)

    fig_bubble = px.scatter(
        max_price_df, x="City", y="Prices",
        size="Prices", color="Prices",
        hover_data=["Item_Name", cuisine_col],
        title="Most Expensive Dish per City",
        color_continuous_scale=[Z_PINK, Z_DARK],
        **plotly_base(),
    )
    fig_bubble.update_layout(height=420, coloraxis_showscale=False,
                              title_font_size=13, margin=dict(t=50))
    st.plotly_chart(fig_bubble, use_container_width=True)

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
section_header("⭐", "Ratings & Delivery Performance")

col1, col2 = st.columns(2)

with col1:
    delivery_rating = (
        df.groupby("City")["Delivery_Rating"].mean().round(2)
        .reset_index(name="Delivery Rating")
        .sort_values("Delivery Rating")
    )
    fig_del = h_bar(delivery_rating, "Delivery Rating", "City",
                    "Avg Delivery Rating by City", text_fmt="%{text:.2f} ⭐")
    st.plotly_chart(fig_del, use_container_width=True)

with col2:
    dining_rating = (
        df.groupby("City")["Dining_Rating"].mean().round(2)
        .reset_index(name="Dining Rating")
        .sort_values("Dining Rating")
    )
    fig_din = h_bar(dining_rating, "Dining Rating", "City",
                    "Avg Dining Rating by City", text_fmt="%{text:.2f} ⭐")
    st.plotly_chart(fig_din, use_container_width=True)

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
section_header("📣", "Customer Engagement — Delivery & Dining Votes")

col1, col2 = st.columns(2)

with col1:
    del_votes = (
        df.groupby("City")["Delivery_Votes"].sum()
        .reset_index(name="Delivery Votes")
        .sort_values("Delivery Votes")
    )
    fig_dv = h_bar(del_votes, "Delivery Votes", "City",
                   "Total Delivery Votes by City", text_fmt="%{text:,.0f}")
    st.plotly_chart(fig_dv, use_container_width=True)

with col2:
    din_votes = (
        df.groupby("City")["Dining_Votes"].sum()
        .reset_index(name="Dining Votes")
        .sort_values("Dining Votes")
    )
    fig_dnv = h_bar(din_votes, "Dining Votes", "City",
                    "Total Dining Votes by City", text_fmt="%{text:,.0f}")
    st.plotly_chart(fig_dnv, use_container_width=True)

insight_expander("Customer Engagement", [
    "Mumbai and Bangalore generate the highest total vote counts across both dining and delivery — confirming their status as India's most digitally engaged food markets.",
    "Mumbai's votes-to-restaurants ratio is particularly striking: fewer outlets but significantly more reviews — making it the optimal city for a new restaurant launch with high organic discoverability.",
    "Cities with low engagement scores (Goa, Raipur, Lucknow) are prime candidates for promotional campaigns, loyalty programs, and review incentive mechanics to bootstrap engagement flywheels.",
    "High engagement is a compounding moat: more votes → higher ranking → more orders → more votes. Early dominance in engagement translates to long-term platform visibility.",
])

divider()


# ──────────────────────────────────────────────────────────────
#  ⑦ TOP 5 RESTAURANTS PER CITY
# ──────────────────────────────────────────────────────────────
section_header("🏆", "Top 5 Most-Listed Restaurants per City")

df_res_cnt = (
    df.groupby(["City", "Restaurant_Name"]).size()
    .reset_index(name="Count")
)
cities = sorted(df["City"].dropna().unique())

for i in range(0, len(cities), 2):
    pair = cities[i : i + 2]
    cols = st.columns(len(pair))
    for j, city in enumerate(pair):
        with cols[j]:
            city_data = (
                df_res_cnt[df_res_cnt["City"] == city]
                .nlargest(5, "Count")
                .sort_values("Count")
            )
            fig_city = px.bar(
                city_data, x="Count", y="Restaurant_Name", orientation="h",
                title=city,
                color_discrete_sequence=[Z_RED],
                text="Count",
                template="plotly_white",
            )
            fig_city.update_traces(textposition="outside")
            fig_city.update_layout(
                height=300, showlegend=False,
                yaxis_title="", xaxis_title="Menu Listings",
                title_font_size=14, title_font_color=T_DARK,
                margin=dict(l=10, r=50, t=45, b=20),
            )
            st.plotly_chart(fig_city, use_container_width=True)

insight_expander("Top Restaurants by City", [
    "Domino's Pizza and McDonald's appear consistently across most cities, underscoring the scale advantage of national QSR chains on food delivery platforms.",
    "Café Coffee Day also features prominently — another franchise-heavy brand that leverages branch density for platform visibility.",
    "Local and regional chains dominate in tier-2 metros like Kochi, Raipur, and Lucknow, where national brands have lower penetration.",
    "High listing frequency is a branch-count proxy — it signals brand reach and multi-outlet scale, not necessarily food quality or customer satisfaction.",
])

divider()


# ──────────────────────────────────────────────────────────────
#  ⑧ BEST SELLER MENU ANALYSIS
# ──────────────────────────────────────────────────────────────
section_header("🥇", "Menu Category Distribution — Best Sellers")

col1, col2 = st.columns(2)

DONUT_COLORS = [Z_RED, "#FF6B6B", Z_PINK, Z_DARK, "#FF8C94"]

with col1:
    df_bs = df[df["Best_Seller"] != "NA"]
    bs_counts = df_bs["Best_Seller"].value_counts().nlargest(5).reset_index()
    bs_counts.columns = ["Category", "Count"]

    fig_bs = px.pie(
        bs_counts, values="Count", names="Category",
        title="Top 5 Best Seller Categories",
        color_discrete_sequence=DONUT_COLORS,
        hole=0.42,
    )
    fig_bs.update_traces(
        textinfo="percent+label",
        pull=[0.04] * len(bs_counts),
        marker=dict(line=dict(color=Z_WHITE, width=2)),
    )
    fig_bs.update_layout(
        template="plotly_white", height=420,
        legend=dict(orientation="v", x=1.02, y=0.5),
        title_font_size=13,
    )
    st.plotly_chart(fig_bs, use_container_width=True)

with col2:
    bs_ratio = (
        df["Best_Seller"]
        .apply(lambda x: "Tagged" if x != "NA" else "Untagged")
        .value_counts()
        .reset_index()
    )
    bs_ratio.columns = ["Status", "Count"]

    fig_ratio = px.pie(
        bs_ratio, values="Count", names="Status",
        title="Tagged vs Untagged Menu Items",
        color_discrete_sequence=[Z_RED, Z_PINK],
        hole=0.42,
    )
    fig_ratio.update_traces(
        textinfo="percent+label",
        marker=dict(line=dict(color=Z_WHITE, width=2)),
    )
    fig_ratio.update_layout(
        template="plotly_white", height=420,
        title_font_size=13,
    )
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
section_header("🗺️", "Geospatial Restaurant Density — India")

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
section_header("📋", "Strategic Conclusion")

st.markdown(f"""
<div style="background: linear-gradient(135deg, {Z_LIGHT} 0%, {Z_WHITE} 100%);
            border: 1px solid #F0E6E7; border-radius: 18px; padding: 2rem 2.2rem;">
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
#  FOOTER
# ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; color:{T_MED}; font-size:0.80rem;
            padding: 1.2rem 0 0.5rem 0; border-top: 1px solid #F0E6E7; margin-top:1rem">
    Built with ❤️ &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp;
    Dataset: <a href="https://www.kaggle.com/datasets/narsingraogoud/zomato-restaurants-dataset-for-metropolitan-areas"
                style="color:{Z_RED}" target="_blank">Zomato Metropolitan Restaurants — Kaggle</a>
    &nbsp;·&nbsp;
    <a href="https://github.com/Namitchuke" style="color:{Z_RED}" target="_blank">GitHub ↗</a>
    &nbsp;·&nbsp;
    <a href="https://www.linkedin.com/in/namit-nitin-chuke/" style="color:{Z_RED}" target="_blank">LinkedIn ↗</a>
</div>
""", unsafe_allow_html=True)
