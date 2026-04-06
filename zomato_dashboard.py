import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIG & STYLING
# ============================================================================
st.set_page_config(
    page_title="Zomato Market Intelligence Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    [data-testid="stMetricValue"] { font-size: 32px; }
    [data-testid="stMetricLabel"] { font-size: 16px; }
    .main { background-color: #f8f9fa; }
    h1 { color: #1f77b4; margin-bottom: 20px; }
    h2 { color: #2c3e50; margin-top: 25px; margin-bottom: 15px; }
    .insight-box { background-color: #e3f2fd; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #1f77b4; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & CACHING
# ============================================================================
@st.cache_data
def load_and_clean_data(filepath):
    """Load CSV and apply intelligent dtype conversion"""
    df = pd.read_csv(filepath)
    
    # ✅ Handle 'Not provided' values BEFORE dtype conversion
    numeric_cols = ['Dining_Rating', 'Delivery_Rating', 'Prices', 'Dining_Votes', 'Delivery_Votes']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].replace('Not provided', np.nan), errors='coerce')
    
    # Ensure correct categories and derived metrics
    df['City'] = df['City'].str.strip().str.title()
    locality_to_bangalore = {'Banaswadi': 'Bangalore', 'Ulsoor': 'Bangalore', 'Magrath Road': 'Bangalore', 'Malleshwaram': 'Bangalore'}
    df['City'] = df['City'].replace(locality_to_bangalore)
    
    df['Total_Votes'] = df['Dining_Votes'].fillna(0) + df['Delivery_Votes'].fillna(0)
    df['Avg_Rating'] = df[['Dining_Rating', 'Delivery_Rating']].mean(axis=1)
    
    return df

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
st.sidebar.markdown("### 🍽️ Zomato Analytics Dashboard")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    ["📊 Market Overview & City Analysis", "🍳 Product & Performance Deep Dive"],
    label_visibility="collapsed"
)

# Data path
DATA_PATH = "zomato_dataset.csv"

# Check if data exists
if not Path(DATA_PATH).exists():
    st.error(f"⚠️ Dataset not found: `{DATA_PATH}`. Please upload the CSV to the project directory.")
    st.stop()

df = load_and_clean_data(DATA_PATH)

# ============================================================================
# PAGE: MARKET OVERVIEW
# ============================================================================
if page == "📊 Market Overview & City Analysis":
    st.title("📊 Market Overview & City Insights")
    st.markdown("High-level market landscape and demographic comparison")
    
    # KPI Row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("Total Restaurants", f"{df['Restaurant_Name'].nunique():,}")
    with col2: st.metric("Cities Covered", df['City'].nunique())
    with col3: st.metric("Avg Price (₹)", f"₹{df['Prices'].mean():.0f}")
    with col4: st.metric("Avg Dining Rating", f"{df['Dining_Rating'].mean():.2f}/5")
    with col5: st.metric("Avg Delivery Rating", f"{df['Delivery_Rating'].mean():.2f}/5")
    
    st.markdown("---")
    
    # City Filters for Charts
    cities = sorted(df['City'].unique())
    selected_cities = st.multiselect("Select Cities for Analysis:", cities, default=cities[:8])
    if not selected_cities: selected_cities = cities
    df_filtered = df[df['City'].isin(selected_cities)]

    # City Charts Row
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Restaurant Count by City")
        city_counts = df_filtered['City'].value_counts().sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        city_counts.plot(kind='barh', color='#1f77b4', ax=ax)
        ax.set_xlabel('Count')
        st.pyplot(fig)
    
    with c2:
        st.subheader("Average Pricing by City")
        city_prices = df_filtered.groupby('City')['Prices'].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        city_prices.plot(kind='bar', color='#ff7f0e', ax=ax)
        ax.set_ylabel('Avg Price (₹)')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

    # City Ratings Row
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Dining Rating Comparison")
        city_dining = df_filtered.groupby('City')['Dining_Rating'].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        city_dining.plot(kind='bar', color='#2ca02c', ax=ax)
        st.pyplot(fig)
    
    with c4:
        st.subheader("Engagement (Total Votes) by City")
        city_votes = df_filtered.groupby('City')['Total_Votes'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        city_votes.plot(kind='bar', color='#d62728', ax=ax)
        st.pyplot(fig)

    # Data Quality Expander
    with st.expander("🔍 View Detailed City Statistics & Data Quality"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### City Summary Table")
            summary = df_filtered.groupby('City').agg({'Restaurant_Name':'nunique', 'Prices':'mean', 'Total_Votes':'sum'}).round(2)
            st.dataframe(summary, use_container_width=True)
        with col2:
            st.markdown("### Data Completeness")
            quality = pd.DataFrame({'Column': df.columns, 'Missing (%)': (df.isna().sum()/len(df)*100).round(2)})
            st.dataframe(quality, use_container_width=True, hide_index=True)

# ============================================================================
# PAGE: DEEP DIVE Analysis
# ============================================================================
else:
    st.title("🍳 Product & Performance Deep Dive")
    st.markdown("Detailed analysis of cuisines, pricing behavior, and ranking")
    
    # Cuisine & Pricing Tab
    t1, t2, t3 = st.tabs(["🍴 Cuisines & Prices", "⭐ Performance Ranking", "📈 Correlations"])
    
    with t1:
        st.subheader("Top Performers by Category")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Top 10 Cuisines by Count")
            if 'Cuisine ' in df.columns: # Noticed the trailing space in notebook cells
                top_cuisines = df['Cuisine '].value_counts().head(10)
                fig, ax = plt.subplots(figsize=(10, 6))
                top_cuisines.plot(kind='barh', color='#9467bd', ax=ax)
                st.pyplot(fig)
        with col2:
            st.markdown("### Price Distribution")
            fig, ax = plt.subplots(figsize=(10, 6))
            df['Prices'].hist(bins=50, color='#17becf', ax=ax)
            ax.set_xlabel("Price (₹)")
            st.pyplot(fig)
            
    with t2:
        st.subheader("Leaderboard")
        col_f1, col_f2 = st.columns(2)
        with col_f1: min_votes = st.slider("Min Total Votes", 0, int(df['Total_Votes'].max()), 100)
        with col_f2: min_price = st.slider("Max Price Point", int(df['Prices'].min()), int(df['Prices'].max()), int(df['Prices'].max()))
        
        df_lead = df[(df['Total_Votes'] >= min_votes) & (df['Prices'] <= min_price)]
        st.markdown(f"**Found {len(df_lead)} items matching criteria**")
        perf_table = df_lead.nlargest(50, 'Total_Votes')[['Restaurant_Name', 'City', 'Prices', 'Dining_Rating', 'Avg_Rating', 'Total_Votes']]
        st.dataframe(perf_table.drop_duplicates(subset=['Restaurant_Name']), use_container_width=True, hide_index=True)

    with t3:
        st.subheader("Advanced Insights")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("### Price vs Ratings Correlation")
            fig, ax = plt.subplots(figsize=(10, 6))
            df_scatter = df.dropna(subset=['Prices', 'Avg_Rating'])
            sns.regplot(data=df_scatter.sample(min(2000, len(df_scatter))), x='Prices', y='Avg_Rating', 
                        scatter_kws={'alpha':0.4, 's':20}, line_kws={'color':'red'}, ax=ax)
            st.pyplot(fig)
        with col_c2:
            st.markdown("### Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(10, 8))
            num_cols = ['Prices', 'Dining_Rating', 'Delivery_Rating', 'Dining_Votes', 'Delivery_Votes', 'Avg_Rating']
            sns.heatmap(df[num_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
            st.pyplot(fig)
        
        st.markdown("""
        <div class="insight-box">
            <h4>💡 Summary Recommendation for Expansion</h4>
            <p>Based on current pricing and rating correlations, markets with high engagement (Votes) but lower average ratings (e.g. Bangalore or Jaipur) 
            present the best opportunity for premium quality entrants to capture market share.</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 10px;'>
    <p><b>Zomato Market Intelligence Insight Dashboard</b> | Refined 2-Page Structure</p>
</div>
""", unsafe_allow_html=True)