import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIG & COMPACT STYLING
# ============================================================================
st.set_page_config(page_title="Zomato Analytics", page_icon="🍴", layout="wide")

st.markdown("""
<style>
    .reportview-container .main .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    [data-testid="stMetricValue"] { font-size: 24px; font-weight: 700; color: #1f77b4; }
    [data-testid="stMetricLabel"] { font-size: 14px; }
    .main { background-color: #fcfcfc; }
    h1 { font-size: 28px !important; color: #2c3e50; margin-bottom: 10px; }
    h2 { font-size: 20px !important; color: #34495e; margin-top: 15px; margin-bottom: 10px; border-bottom: 2px solid #eee; }
    h3 { font-size: 16px !important; color: #1f77b4; }
    .insight-box { background-color: #f0f7ff; padding: 12px; border-radius: 6px; margin: 8px 0; border-left: 4px solid #1f77b4; font-size: 14px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { padding: 8px 16px; background-color: #f8f9fa; border-radius: 4px; border: 1px solid #ddd; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & CACHING
# ============================================================================
@st.cache_data
def load_and_clean_data(filepath):
    df = pd.read_csv(filepath)
    # Cleaning Numeric
    numeric_cols = ['Dining_Rating', 'Delivery_Rating', 'Prices', 'Dining_Votes', 'Delivery_Votes']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].replace('Not provided', np.nan), errors='coerce')
    # Standardizing Cities
    df['City'] = df['City'].str.strip().str.title()
    df['City'] = df['City'].replace({'Banaswadi': 'Bangalore', 'Ulsoor': 'Bangalore', 'Magrath Road': 'Bangalore', 'Malleshwaram': 'Bangalore'})
    # Metrics
    df['Total_Votes'] = df['Dining_Votes'].fillna(0) + df['Delivery_Votes'].fillna(0)
    df['Avg_Rating'] = df[['Dining_Rating', 'Delivery_Rating']].mean(axis=1)
    return df

# ============================================================================
# SIDEBAR NAVIGATION & GLOBAL FILTERS
# ============================================================================
with st.sidebar:
    st.markdown("### 🍴 Zomato Analytics")
    page = st.radio("Navigation", ["📊 Market Summary", "🔍 Performance Deep Dive"])
    st.markdown("---")
    # Global City Filter in Sidebar for better space usage
    df_raw = load_and_clean_data("zomato_dataset.csv")
    all_cities = sorted(df_raw['City'].unique())
    selected_cities = st.multiselect("Select Cities:", all_cities, default=all_cities[:5])
    if not selected_cities: selected_cities = all_cities
    df = df_raw[df_raw['City'].isin(selected_cities)]

# ============================================================================
# PAGE: MARKET SUMMARY
# ============================================================================
if page == "📊 Market Summary":
    st.markdown("<h1>📊 Market Summary & City Insights</h1>", unsafe_allow_html=True)
    
    # Compact Metrics Row
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Restaurants", f"{df['Restaurant_Name'].nunique():,}")
    m2.metric("Cities", df['City'].nunique())
    m3.metric("Avg Price", f"₹{df['Prices'].mean():.0f}")
    m4.metric("Avg Rating", f"{df['Avg_Rating'].mean():.1f}/5")
    m5.metric("Total Engagement", f"{df['Total_Votes'].sum()/1e6:.1f}M")

    # City Charts Row - Reduced Height
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🏙️ Restaurant Distribution")
        city_counts = df['City'].value_counts().head(10).sort_values()
        fig, ax = plt.subplots(figsize=(8, 4))
        city_counts.plot(kind='barh', color='#1f77b4', ax=ax)
        plt.tight_layout()
        st.pyplot(fig)
    
    with c2:
        st.markdown("### 💰 Average Prices by City")
        city_prices = df.groupby('City')['Prices'].mean().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(8, 4))
        city_prices.plot(kind='bar', color='#ff7f0e', ax=ax)
        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)

    # Detailed Stats in Expander to keep main view clean
    with st.expander("📝 View Detailed Data Summaries"):
        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown("### City Comparison Table")
            summary = df.groupby('City').agg({'Restaurant_Name':'nunique', 'Prices':'mean', 'Total_Votes':'sum'}).round(1)
            st.dataframe(summary.sort_values('Restaurant_Name', ascending=False), use_container_width=True)
        with col_r:
            st.markdown("### Data Completeness Overview")
            quality = pd.DataFrame({'Missing %': (df.isna().sum()/len(df)*100).round(1)})
            st.dataframe(quality, use_container_width=True)

# ============================================================================
# PAGE: PERFORMANCE DEEP-DIVE
# ============================================================================
else:
    st.markdown("<h1>🔍 Performance & Product Deep-Dive</h1>", unsafe_allow_html=True)
    
    # Sub-tabs for better organization
    t1, t2 = st.tabs(["Product Insights", "Performance Ranking"])
    
    with t1:
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            st.markdown("### 🍴 Top 10 Cuisines")
            if 'Cuisine ' in df.columns:
                top_cuisines = df['Cuisine '].value_counts().head(10)
                fig, ax = plt.subplots(figsize=(8, 4))
                top_cuisines.plot(kind='barh', color='#9467bd', ax=ax)
                plt.tight_layout()
                st.pyplot(fig)
        with c_p2:
            st.markdown("### 💳 Price Distribution")
            fig, ax = plt.subplots(figsize=(8, 4))
            df['Prices'].dropna().hist(bins=30, color='#17becf', ax=ax)
            plt.tight_layout()
            st.pyplot(fig)
            
        # Insights Box
        st.markdown("""
        <div class="insight-box">
            <b>Strategic Insight:</b> Demand is heavily concentrated in the top 5 cities and specific bestseller categories. Expansion should prioritize high-engagement urban centers.
        </div>
        """, unsafe_allow_html=True)

    with t2:
        # Mini-filters for the leaderboard
        st.markdown("### 🏆 Top Performing Restaurants")
        f1, f2 = st.columns(2)
        with f1: min_v = f1.number_input("Min Votes", 0, int(df['Total_Votes'].max()), 500)
        with f2: max_p = f2.number_input("Max Price (₹)", 0, int(df['Prices'].max()), int(df['Prices'].mean()*2))
        
        lead_df = df[(df['Total_Votes'] >= min_v) & (df['Prices'] <= max_p)]
        top_res = lead_df.drop_duplicates('Restaurant_Name').nlargest(30, 'Total_Votes')[['Restaurant_Name', 'City', 'Prices', 'Avg_Rating', 'Total_Votes']]
        st.dataframe(top_res, use_container_width=True, hide_index=True)

# Footer - Very small
st.markdown("<p style='text-align: center; color: #999; font-size: 11px; margin-top: 50px;'>Zomato Pulse Analytics | Concise Version</p>", unsafe_allow_html=True)