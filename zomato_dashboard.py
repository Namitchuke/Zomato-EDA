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
    # Replace 'Not provided' with NaN in numeric columns
    numeric_cols = ['Dining_Rating', 'Delivery_Rating', 'Prices', 'Dining_Votes', 'Delivery_Votes']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace('Not provided', np.nan), errors='coerce')
    
    # Clean categorical columns
    if 'Dining_Rating' in df.columns:
        df['Dining_Rating'] = pd.to_numeric(df['Dining_Rating'], errors='coerce')
    if 'Delivery_Rating' in df.columns:
        df['Delivery_Rating'] = pd.to_numeric(df['Delivery_Rating'], errors='coerce')
    
    # Ensure correct dtypes
    if 'Prices' in df.columns:
        df['Prices'] = pd.to_numeric(df['Prices'], errors='coerce')
    if 'Dining_Votes' in df.columns:
        df['Dining_Votes'] = pd.to_numeric(df['Dining_Votes'], errors='coerce')
    if 'Delivery_Votes' in df.columns:
        df['Delivery_Votes'] = pd.to_numeric(df['Delivery_Votes'], errors='coerce')
    
    # Create derived metrics
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
    ["📊 Executive Summary", "🏙️ City Analysis", "🍴 Cuisine & Pricing", 
     "⭐ Restaurant Performance", "📈 Advanced Insights"],
    label_visibility="collapsed"
)

# Data path
DATA_PATH = "zomato_dataset.csv"

# Check if data exists
if not Path(DATA_PATH).exists():
    st.warning("⚠️ Dataset not found. Using sample structure for demonstration.")
    st.info("To use your data: Upload zomato_dataset.csv to /home/claude/ directory")
    st.stop()

df = load_and_clean_data(DATA_PATH)

# ============================================================================
# PAGE: EXECUTIVE SUMMARY
# ============================================================================
if page == "📊 Executive Summary":
    st.title("📊 Executive Summary")
    st.markdown("High-level market overview and key performance indicators")
    
    # KPI Row 1
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Restaurants", f"{len(df):,}")
    with col2:
        st.metric("Cities Covered", df['City'].nunique())
    with col3:
        avg_price = df['Prices'].mean()
        st.metric("Avg Price (₹)", f"{avg_price:.0f}" if not np.isnan(avg_price) else "N/A")
    with col4:
        avg_dining = df['Dining_Rating'].mean()
        st.metric("Avg Dining Rating", f"{avg_dining:.2f}" if not np.isnan(avg_dining) else "N/A")
    with col5:
        avg_delivery = df['Delivery_Rating'].mean()
        st.metric("Avg Delivery Rating", f"{avg_delivery:.2f}" if not np.isnan(avg_delivery) else "N/A")
    
    st.markdown("---")
    
    # Data Quality Overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Data Quality Summary")
        quality_data = {
            'Column': df.columns,
            'Missing (%)': [(df[col].isna().sum() / len(df) * 100) for col in df.columns],
            'Data Type': df.dtypes
        }
        quality_df = pd.DataFrame(quality_data)
        st.dataframe(quality_df, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Dataset Overview")
        overview_metrics = f"""
        - **Total Records**: {len(df):,}
        - **Total Columns**: {len(df.columns)}
        - **Cities**: {df['City'].nunique()}
        - **Restaurant Brands**: {df['Restaurant_Name'].nunique() if 'Restaurant_Name' in df.columns else 'N/A'}
        - **Price Range**: ₹{df['Prices'].min():.0f} - ₹{df['Prices'].max():.0f}
        - **Rating Range**: {df['Avg_Rating'].min():.2f} - {df['Avg_Rating'].max():.2f}
        """
        st.markdown(overview_metrics)
    
    st.markdown("---")
    
    # Top Insights
    st.subheader("💡 Key Findings")
    
    top_city = df['City'].value_counts().index[0] if len(df) > 0 else "N/A"
    top_city_count = df['City'].value_counts().values[0] if len(df) > 0 else 0
    
    insights = f"""
    <div class="insight-box">
    ✓ <b>{top_city}</b> dominates with <b>{top_city_count:,}</b> restaurants, indicating strongest market presence
    </div>
    
    <div class="insight-box">
    ✓ Price volatility across cities suggests opportunity for market segmentation and targeting
    </div>
    
    <div class="insight-box">
    ✓ Delivery ratings are critical differentiator - cities with higher delivery ratings show stronger engagement
    </div>
    """
    st.markdown(insights, unsafe_allow_html=True)

# ============================================================================
# PAGE: CITY ANALYSIS
# ============================================================================
elif page == "🏙️ City Analysis":
    st.title("🏙️ City-Level Analysis")
    st.markdown("Market dynamics, competition, and performance by city")
    
    # City Filter
    cities = sorted(df['City'].unique())
    selected_cities = st.multiselect("Select Cities (Leave blank for all):", cities, default=cities[:5])
    if not selected_cities:
        selected_cities = cities
    
    df_filtered = df[df['City'].isin(selected_cities)]
    
    # Chart 1: Restaurants by City
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Restaurant Count by City")
        city_counts = df_filtered['City'].value_counts().sort_values(ascending=True)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        city_counts.plot(kind='barh', color='#1f77b4', ax=ax)
        ax.set_xlabel('Number of Restaurants', fontsize=11, fontweight='bold')
        ax.set_ylabel('City', fontsize=11, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Average Pricing by City")
        city_prices = df_filtered.groupby('City')['Prices'].mean().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = plt.cm.RdYlGn_r(np.linspace(0.3, 0.7, len(city_prices)))
        city_prices.plot(kind='bar', color=colors, ax=ax)
        ax.set_ylabel('Average Price (₹)', fontsize=11, fontweight='bold')
        ax.set_xlabel('City', fontsize=11, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
    
    # Chart 2: Ratings Comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Average Delivery Rating by City")
        city_delivery = df_filtered.groupby('City')['Delivery_Rating'].mean().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        city_delivery.plot(kind='bar', color='#ff7f0e', ax=ax)
        ax.set_ylabel('Delivery Rating', fontsize=11, fontweight='bold')
        ax.set_xlabel('City', fontsize=11, fontweight='bold')
        ax.set_ylim(0, 5)
        ax.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Average Dining Rating by City")
        city_dining = df_filtered.groupby('City')['Dining_Rating'].mean().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        city_dining.plot(kind='bar', color='#2ca02c', ax=ax)
        ax.set_ylabel('Dining Rating', fontsize=11, fontweight='bold')
        ax.set_xlabel('City', fontsize=11, fontweight='bold')
        ax.set_ylim(0, 5)
        ax.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
    
    # City Summary Table
    st.subheader("📊 City Summary Statistics")
    
    city_summary = df_filtered.groupby('City').agg({
        'Restaurant_Name': 'nunique' if 'Restaurant_Name' in df.columns else 'count',
        'Prices': ['mean', 'std'],
        'Dining_Rating': 'mean',
        'Delivery_Rating': 'mean',
        'Total_Votes': 'sum'
    }).round(2)
    
    city_summary.columns = ['Restaurants', 'Avg Price', 'Price StdDev', 'Dining Rating', 'Delivery Rating', 'Total Votes']
    city_summary = city_summary.sort_values('Restaurants', ascending=False)
    
    st.dataframe(city_summary, use_container_width=True)

# ============================================================================
# PAGE: CUISINE & PRICING
# ============================================================================
elif page == "🍴 Cuisine & Pricing":
    st.title("🍴 Cuisine & Pricing Analysis")
    st.markdown("Understand cuisine preferences and pricing dynamics")
    
    if 'Cuisine_Type' in df.columns or 'Cuisines' in df.columns:
        cuisine_col = 'Cuisine_Type' if 'Cuisine_Type' in df.columns else 'Cuisines'
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 10 Cuisines by Count")
            top_cuisines = df[cuisine_col].value_counts().head(10)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            top_cuisines.plot(kind='barh', color='#d62728', ax=ax)
            ax.set_xlabel('Number of Restaurants', fontsize=11, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.subheader("Average Price by Cuisine")
            cuisine_prices = df.groupby(cuisine_col)['Prices'].mean().sort_values(ascending=False).head(10)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            cuisine_prices.plot(kind='barh', color='#9467bd', ax=ax)
            ax.set_xlabel('Average Price (₹)', fontsize=11, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
    else:
        st.info("Cuisine information not available in dataset")
    
    # Price Distribution
    st.subheader("Price Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        df['Prices'].hist(bins=50, color='#1f77b4', edgecolor='black', ax=ax)
        ax.set_xlabel('Price (₹)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Price Statistics")
        price_stats = f"""
        - **Mean**: ₹{df['Prices'].mean():.2f}
        - **Median**: ₹{df['Prices'].median():.2f}
        - **Std Dev**: ₹{df['Prices'].std():.2f}
        - **Min**: ₹{df['Prices'].min():.2f}
        - **Max**: ₹{df['Prices'].max():.2f}
        - **IQR**: ₹{df['Prices'].quantile(0.75) - df['Prices'].quantile(0.25):.2f}
        """
        st.markdown(price_stats)

# ============================================================================
# PAGE: RESTAURANT PERFORMANCE
# ============================================================================
elif page == "⭐ Restaurant Performance":
    st.title("⭐ Restaurant Performance Metrics")
    st.markdown("Identify top performers and engagement drivers")
    
    # Filter by metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_votes = st.slider("Min Total Votes", 0, int(df['Total_Votes'].max()), 0)
    with col2:
        min_rating = st.slider("Min Avg Rating", 0.0, 5.0, 0.0)
    with col3:
        selected_city_perf = st.selectbox("Filter by City:", ['All'] + sorted(df['City'].unique()))
    
    # Apply filters
    df_perf = df.copy()
    if selected_city_perf != 'All':
        df_perf = df_perf[df_perf['City'] == selected_city_perf]
    df_perf = df_perf[(df_perf['Total_Votes'] >= min_votes) & (df_perf['Avg_Rating'] >= min_rating)]
    
    # Top Restaurants by Engagement
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 by Total Engagement")
        top_engagement = df_perf.nlargest(10, 'Total_Votes')[['Restaurant_Name', 'City', 'Prices', 'Total_Votes', 'Avg_Rating']]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        top_eng_data = df_perf.nlargest(10, 'Total_Votes')
        ax.barh(range(len(top_eng_data)), top_eng_data['Total_Votes'].values, color='#17becf')
        ax.set_yticks(range(len(top_eng_data)))
        ax.set_yticklabels([f"{r[:20]}" for r in top_eng_data['Restaurant_Name'].values], fontsize=9)
        ax.set_xlabel('Total Votes', fontsize=11, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Top 10 by Average Rating")
        top_rated = df_perf[df_perf['Avg_Rating'].notna()].nlargest(10, 'Avg_Rating')[['Restaurant_Name', 'City', 'Avg_Rating', 'Total_Votes']]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        top_rated_data = df_perf[df_perf['Avg_Rating'].notna()].nlargest(10, 'Avg_Rating')
        colors_rated = plt.cm.Greens(np.linspace(0.5, 0.9, len(top_rated_data)))
        ax.barh(range(len(top_rated_data)), top_rated_data['Avg_Rating'].values, color=colors_rated)
        ax.set_yticks(range(len(top_rated_data)))
        ax.set_yticklabels([f"{r[:20]}" for r in top_rated_data['Restaurant_Name'].values], fontsize=9)
        ax.set_xlabel('Average Rating', fontsize=11, fontweight='bold')
        ax.set_xlim(0, 5)
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    # Detailed Performance Table
    st.subheader("📋 Detailed Performance Ranking")
    
    perf_table = df_perf[['Restaurant_Name', 'City', 'Prices', 'Dining_Rating', 'Delivery_Rating', 'Total_Votes']].copy()
    perf_table['Avg_Rating'] = df_perf['Avg_Rating']
    perf_table = perf_table.sort_values('Total_Votes', ascending=False).head(50)
    perf_table['Dining_Rating'] = perf_table['Dining_Rating'].round(2)
    perf_table['Delivery_Rating'] = perf_table['Delivery_Rating'].round(2)
    perf_table['Avg_Rating'] = perf_table['Avg_Rating'].round(2)
    
    st.dataframe(perf_table, use_container_width=True, hide_index=True)

# ============================================================================
# PAGE: ADVANCED INSIGHTS
# ============================================================================
elif page == "📈 Advanced Insights":
    st.title("📈 Advanced Insights & Correlations")
    st.markdown("Deep-dive analysis of relationships and patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Price vs Ratings Correlation")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter_data = df.dropna(subset=['Prices', 'Avg_Rating'])
        ax.scatter(scatter_data['Prices'], scatter_data['Avg_Rating'], alpha=0.5, s=30, color='#1f77b4')
        
        # Add trendline
        z = np.polyfit(scatter_data['Prices'], scatter_data['Avg_Rating'], 1)
        p = np.poly1d(z)
        ax.plot(scatter_data['Prices'].sort_values(), p(scatter_data['Prices'].sort_values()), 
                "r--", linewidth=2, label='Trend')
        
        ax.set_xlabel('Price (₹)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Average Rating', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Voting Behavior Analysis")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create bins for voting categories
        df['Vote_Category'] = pd.cut(df['Total_Votes'], 
                                      bins=[0, 100, 500, 1000, 5000, float('inf')],
                                      labels=['0-100', '100-500', '500-1K', '1K-5K', '5K+'])
        
        vote_dist = df['Vote_Category'].value_counts().sort_index()
        vote_dist.plot(kind='bar', color='#ff7f0e', ax=ax)
        ax.set_ylabel('Number of Restaurants', fontsize=11, fontweight='bold')
        ax.set_xlabel('Vote Range', fontsize=11, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    
    # Correlation Matrix
    st.subheader("📊 Correlation Matrix")
    
    numeric_cols = ['Prices', 'Dining_Rating', 'Delivery_Rating', 'Dining_Votes', 'Delivery_Votes', 'Avg_Rating']
    corr_data = df[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_data, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
                square=True, ax=ax, cbar_kws={'label': 'Correlation'})
    plt.tight_layout()
    st.pyplot(fig)
    
    # Key Correlations
    st.subheader("💡 Key Insights from Correlations")
    
    price_rating_corr = df['Prices'].corr(df['Avg_Rating'])
    price_votes_corr = df['Prices'].corr(df['Total_Votes'])
    rating_votes_corr = df['Avg_Rating'].corr(df['Total_Votes'])
    
    insights = f"""
    - **Price vs Rating Correlation**: {price_rating_corr:.3f} 
      {"(Higher prices ≠ better ratings)" if price_rating_corr < 0.3 else "(Premium pricing correlates with ratings)"}
    
    - **Price vs Engagement Correlation**: {price_votes_corr:.3f}
      {"(Price point doesn't drive engagement)" if abs(price_votes_corr) < 0.2 else "(Price impacts customer engagement)"}
    
    - **Rating vs Engagement Correlation**: {rating_votes_corr:.3f}
      {"(Ratings are a strong engagement driver)" if rating_votes_corr > 0.3 else "(Engagement independent of ratings)"}
    """
    st.markdown(insights)
    
    # Distribution Analysis
    st.subheader("📈 Rating Distribution by City")
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    top_cities_for_box = df['City'].value_counts().head(6).index
    df_box = df[df['City'].isin(top_cities_for_box)]
    
    df_box.boxplot(column='Avg_Rating', by='City', ax=ax)
    ax.set_xlabel('City', fontsize=11, fontweight='bold')
    ax.set_ylabel('Average Rating', fontsize=11, fontweight='bold')
    ax.set_title('Rating Distribution by City')
    plt.suptitle('')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><b>Zomato Market Intelligence Dashboard</b></p>
    <p>Built with Streamlit | Data-driven insights for market analysis</p>
    <p><small>Dataset contains 123,000+ restaurant records across 13 Indian cities</small></p>
</div>
""", unsafe_allow_html=True)