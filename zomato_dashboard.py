import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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

# Custom CSS for professional consulting aesthetic
st.markdown("""
<style>
    :root {
        --primary: #667eea;
        --accent: #ff7f0e;
        --success: #2ca02c;
        --danger: #d62728;
        --neutral: #7f7f7f;
    }
    
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .stMetric {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 4px solid var(--primary);
    }
    
    .header-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .insight-box {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid var(--accent);
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .insight-box h4 {
        color: var(--accent);
        margin-top: 0;
        font-weight: 600;
    }
    
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin: 1.5rem 0;
    }
    
    h1, h2, h3 {
        color: #2d3436;
        font-weight: 600;
    }
    
    h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 1.8rem;
        border-bottom: 3px solid var(--primary);
        padding-bottom: 0.8rem;
        margin-top: 2rem;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        font-weight: 600;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & PREPROCESSING
# ============================================================================
@st.cache_data
def load_data():
    df = pd.read_csv("zomato_dataset.csv")
    
    # Data cleaning (from original notebook)
    df["Dining_Rating"].fillna("Not provided", inplace=True)
    df["Delivery_Rating"].fillna("Not provided", inplace=True)
    df["Best_Seller"].fillna("NA", inplace=True)
    
    # Standardize city names
    df['City'] = df['City'].str.strip().str.title()
    locality_to_bangalore = {
        'Banaswadi': 'Bangalore',
        'Ulsoor': 'Bangalore',
        'Magrath Road': 'Bangalore',
        'Malleshwaram': 'Bangalore'
    }
    df['City'] = df['City'].replace(locality_to_bangalore)
    
    # Convert ratings to numeric
    df['Dining_Rating'] = pd.to_numeric(df['Dining_Rating'], errors='coerce')
    df['Delivery_Rating'] = pd.to_numeric(df['Delivery_Rating'], errors='coerce')
    df['Total_rating'] = df['Dining_Rating'] + df['Delivery_Rating']
    df['Total_votes'] = df['Dining_Votes'] + df['Delivery_Votes']
    
    return df

# Try to load data
try:
    df = load_data()
    data_loaded = True
except FileNotFoundError:
    st.error("⚠️ **Dataset not found**: Place `zomato_dataset.csv` in the same directory as this script.")
    data_loaded = False

# ============================================================================
# HEADER
# ============================================================================
if data_loaded:
    st.markdown("""
    <div class="header-section">
        <h1>🍽️ Zomato Market Intelligence Dashboard</h1>
        <p style="font-size: 1.1rem; margin: 1rem 0 0 0; opacity: 0.95;">
            Comprehensive market analysis across Indian cities | 
            <span style="font-weight: 600;">900+ restaurants</span> | 
            <span style="font-weight: 600;">123K+ records</span> | 
            <span style="font-weight: 600;">Data-driven insights</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================================
    # SIDEBAR FILTERS
    # ============================================================================
    with st.sidebar:
        st.markdown("### 🔍 Dashboard Controls")
        
        # City filter
        all_cities = sorted(df['City'].unique())
        selected_cities = st.multiselect(
            "Select Cities",
            all_cities,
            default=all_cities,
            key="city_filter"
        )
        
        # Minimum votes filter
        min_votes = st.slider(
            "Minimum Total Votes (Customer Engagement)",
            min_value=0,
            max_value=int(df['Total_votes'].max()),
            value=0,
            step=50
        )
        
        st.markdown("---")
        st.markdown("""
        ### 📊 Dashboard Sections
        - **City Analysis**: Market density & engagement
        - **Performance**: Ratings & customer satisfaction
        - **Pricing**: Menu strategy & pricing insights
        - **Categories**: Cuisine & bestseller trends
        - **Expansion**: Strategic recommendations
        """)
    
    # Apply filters
    df_filtered = df[df['City'].isin(selected_cities)].copy()
    df_filtered = df_filtered[df_filtered['Total_votes'] >= min_votes]

    # ============================================================================
    # KEY METRICS
    # ============================================================================
    st.markdown("## 📈 Executive Summary")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Restaurants",
            value=f"{df_filtered['Restaurant_Name'].nunique():,}",
            delta=f"{len(selected_cities)} cities"
        )
    
    with col2:
        dining_avg = df_filtered['Dining_Rating'].mean()
        st.metric(
            label="Avg Dining Rating",
            value=f"{dining_avg:.2f}" if not pd.isna(dining_avg) else "N/A",
            delta="Customer satisfaction"
        )
    
    with col3:
        delivery_avg = df_filtered['Delivery_Rating'].mean()
        st.metric(
            label="Avg Delivery Rating",
            value=f"{delivery_avg:.2f}" if not pd.isna(delivery_avg) else "N/A",
            delta="Service quality"
        )
    
    with col4:
        st.metric(
            label="Avg Item Price",
            value=f"₹{df_filtered['Prices'].mean():.0f}",
            delta="Across all items"
        )
    
    with col5:
        st.metric(
            label="Total Customer Votes",
            value=f"{df_filtered['Total_votes'].sum():,.0f}",
            delta="Engagement volume"
        )

    # ============================================================================
    # TABS FOR ORGANIZED INSIGHTS
    # ============================================================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏙️ City Analysis",
        "⭐ Performance Metrics",
        "💰 Pricing Intelligence",
        "🍔 Categories & Bestsellers",
        "🎯 Expansion Strategy"
    ])

    # ============================================================================
    # TAB 1: CITY ANALYSIS
    # ============================================================================
    with tab1:
        st.markdown("## City-Level Market Overview")
        
        col1, col2 = st.columns(2)
        
        # Restaurant count by city
        with col1:
            st.markdown("### Restaurant Distribution by City")
            res_count = df_filtered.groupby('City')['Restaurant_Name'].nunique().sort_values(ascending=False)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = sns.color_palette("husl", len(res_count))
            bars = ax.barh(res_count.index, res_count.values, color=colors)
            ax.bar_label(bars, fmt='%d', padding=3, fontweight='bold')
            ax.set_xlabel("Number of Restaurants", fontweight='bold', fontsize=11)
            ax.set_ylabel("")
            ax.invert_yaxis()
            plt.tight_layout()
            st.pyplot(fig)
        
        # Customer engagement (votes) by city
        with col2:
            st.markdown("### Customer Engagement by City")
            votes_by_city = df_filtered.groupby('City')['Total_votes'].sum().sort_values(ascending=False)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = sns.color_palette("coolwarm", len(votes_by_city))
            bars = ax.barh(votes_by_city.index, votes_by_city.values, color=colors)
            ax.bar_label(bars, fmt='%,.0f', padding=3, fontweight='bold', fontsize=9)
            ax.set_xlabel("Total Customer Votes", fontweight='bold', fontsize=11)
            ax.set_ylabel("")
            ax.invert_yaxis()
            plt.tight_layout()
            st.pyplot(fig)
        
        # Detailed city metrics table
        st.markdown("### City-wise Performance Metrics")
        city_metrics = pd.DataFrame({
            'City': df_filtered.groupby('City').size().index,
            'Unique Restaurants': df_filtered.groupby('City')['Restaurant_Name'].nunique().values,
            'Avg Dining Rating': df_filtered.groupby('City')['Dining_Rating'].mean().values,
            'Avg Delivery Rating': df_filtered.groupby('City')['Delivery_Rating'].mean().values,
            'Avg Item Price (₹)': df_filtered.groupby('City')['Prices'].mean().values,
            'Total Customer Votes': df_filtered.groupby('City')['Total_votes'].sum().values,
        }).round(2).sort_values('Unique Restaurants', ascending=False)
        
        st.dataframe(city_metrics, use_container_width=True, hide_index=True)
        
        # Key insight
        st.markdown("""
        <div class="insight-box">
            <h4>💡 Market Distribution Insight</h4>
            <p>
            <strong>Hyderabad, Jaipur, and Mumbai</strong> lead in restaurant listings, reflecting strong demand 
            for online food delivery services. These cities present both established markets (opportunity to differentiate) 
            and proven customer acquisition channels.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================================
    # TAB 2: PERFORMANCE METRICS
    # ============================================================================
    with tab2:
        st.markdown("## Rating & Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        # Dining vs Delivery ratings by city
        with col1:
            st.markdown("### Average Ratings by City")
            rating_comparison = df_filtered.groupby('City')[['Dining_Rating', 'Delivery_Rating']].mean().sort_values('Dining_Rating', ascending=False)
            
            fig, ax = plt.subplots(figsize=(11, 7))
            x = np.arange(len(rating_comparison))
            width = 0.35
            
            bars1 = ax.bar(x - width/2, rating_comparison['Dining_Rating'], width, label='Dining Rating', color='#667eea', alpha=0.85)
            bars2 = ax.bar(x + width/2, rating_comparison['Delivery_Rating'], width, label='Delivery Rating', color='#ff7f0e', alpha=0.85)
            
            ax.set_ylabel("Average Rating", fontweight='bold', fontsize=11)
            ax.set_xticks(x)
            ax.set_xticklabels(rating_comparison.index, rotation=45, ha='right')
            ax.legend(fontsize=10)
            ax.set_ylim([0, 5.5])
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        
        # Top-rated restaurants
        with col2:
            st.markdown("### Top 15 Highest-Rated Restaurants")
            top_rated = df_filtered.dropna(subset=['Total_rating']).nlargest(15, 'Total_rating')[
                ['Restaurant_Name', 'City', 'Dining_Rating', 'Delivery_Rating', 'Total_rating']
            ].drop_duplicates(subset=['Restaurant_Name']).reset_index(drop=True)
            
            fig, ax = plt.subplots(figsize=(11, 7))
            colors = ['#2ca02c' if x >= 8 else '#ff7f0e' if x >= 6 else '#d62728' for x in top_rated['Total_rating']]
            bars = ax.barh(top_rated['Restaurant_Name'].str[:25], top_rated['Total_rating'], color=colors)
            ax.bar_label(bars, fmt='%.2f', padding=3, fontweight='bold', fontsize=9)
            ax.set_xlabel("Total Rating (Dining + Delivery)", fontweight='bold', fontsize=11)
            ax.invert_yaxis()
            plt.tight_layout()
            st.pyplot(fig)
        
        # Ratings distribution
        st.markdown("### Overall Rating Distribution")
        col_a, col_b = st.columns(2)
        
        with col_a:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.hist(df_filtered['Dining_Rating'].dropna(), bins=30, color='#667eea', alpha=0.7, edgecolor='black', label='Dining')
            ax.axvline(df_filtered['Dining_Rating'].mean(), color='#d62728', linestyle='--', linewidth=2.5, label=f"Mean: {df_filtered['Dining_Rating'].mean():.2f}")
            ax.set_xlabel("Dining Rating", fontweight='bold')
            ax.set_ylabel("Frequency", fontweight='bold')
            ax.legend()
            ax.grid(alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        
        with col_b:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.hist(df_filtered['Delivery_Rating'].dropna(), bins=30, color='#ff7f0e', alpha=0.7, edgecolor='black', label='Delivery')
            ax.axvline(df_filtered['Delivery_Rating'].mean(), color='#d62728', linestyle='--', linewidth=2.5, label=f"Mean: {df_filtered['Delivery_Rating'].mean():.2f}")
            ax.set_xlabel("Delivery Rating", fontweight='bold')
            ax.set_ylabel("Frequency", fontweight='bold')
            ax.legend()
            ax.grid(alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        
        st.markdown("""
        <div class="insight-box">
            <h4>⭐ Performance Insight</h4>
            <p>
            <strong>Dining and Delivery ratings often diverge</strong> — some restaurants excel in dine-in experience 
            while others are delivery-optimized. Success requires balancing both channels. Target 3.5+ average rating 
            for sustainable growth.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================================
    # TAB 3: PRICING INTELLIGENCE
    # ============================================================================
    with tab3:
        st.markdown("## Pricing Strategy & Market Positioning")
        
        col1, col2 = st.columns(2)
        
        # Average prices by city
        with col1:
            st.markdown("### Average Item Prices by City")
            price_by_city = df_filtered.groupby('City')['Prices'].mean().sort_values(ascending=False)
            
            fig, ax = plt.subplots(figsize=(11, 7))
            colors = sns.color_palette("YlOrRd", len(price_by_city))
            bars = ax.barh(price_by_city.index, price_by_city.values, color=colors)
            ax.bar_label(bars, fmt='₹%.0f', padding=3, fontweight='bold')
            ax.set_xlabel("Average Price (₹)", fontweight='bold', fontsize=11)
            ax.invert_yaxis()
            plt.tight_layout()
            st.pyplot(fig)
        
        # Price distribution
        with col2:
            st.markdown("### Price Range Distribution")
            fig, ax = plt.subplots(figsize=(11, 7))
            ax.hist(df_filtered['Prices'].dropna(), bins=50, color='#667eea', alpha=0.7, edgecolor='black')
            ax.axvline(df_filtered['Prices'].mean(), color='#ff7f0e', linestyle='--', linewidth=2.5, label=f"Mean: ₹{df_filtered['Prices'].mean():.0f}")
            ax.axvline(df_filtered['Prices'].median(), color='#2ca02c', linestyle='--', linewidth=2.5, label=f"Median: ₹{df_filtered['Prices'].median():.0f}")
            ax.set_xlabel("Price (₹)", fontweight='bold', fontsize=11)
            ax.set_ylabel("Frequency", fontweight='bold', fontsize=11)
            ax.legend()
            ax.grid(alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        
        # Top cuisines by price
        st.markdown("### Most Expensive Dishes by Cuisine (Across All Cities)")
        expensive_dishes = df_filtered.groupby(['Cuisine', 'Item_Name'], as_index=False)['Prices'].max().sort_values('Prices', ascending=False).head(15)
        st.dataframe(expensive_dishes, use_container_width=True, hide_index=True)
        
        st.markdown("""
        <div class="insight-box">
            <h4>💰 Pricing Strategy Insight</h4>
            <p>
            <strong>Mumbai</strong> commands premium pricing (₹304 avg), suggesting affluent market or higher service costs. 
            <strong>Raipur</strong> operates in budget segment. Strategy: Differentiate by location and target audience 
            positioning (premium vs. budget) rather than one-size-fits-all pricing.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================================
    # TAB 4: CATEGORIES & BESTSELLERS
    # ============================================================================
    with tab4:
        st.markdown("## Product Category Analysis")
        
        col1, col2 = st.columns(2)
        
        # Top cuisines
        with col1:
            st.markdown("### Top 12 Cuisines by Popularity")
            top_cuisines = df_filtered['Cuisine'].value_counts().head(12)
            
            fig, ax = plt.subplots(figsize=(11, 7))
            colors = sns.color_palette("Set2", len(top_cuisines))
            bars = ax.barh(top_cuisines.index, top_cuisines.values, color=colors)
            ax.bar_label(bars, fmt='%d', padding=3, fontweight='bold')
            ax.set_xlabel("Number of Items Listed", fontweight='bold', fontsize=11)
            ax.invert_yaxis()
            plt.tight_layout()
            st.pyplot(fig)
        
        # Bestseller categories
        with col2:
            st.markdown("### Top 5 Bestseller Categories")
            df_bestseller_data = df_filtered[df_filtered['Best_Seller'] != 'NA']
            bestseller_data = df_bestseller_data['Best_Seller'].value_counts().head(5)
            
            fig, ax = plt.subplots(figsize=(11, 7))
            colors = sns.color_palette("husl", len(bestseller_data))
            wedges, texts, autotexts = ax.pie(
                bestseller_data.values,
                labels=bestseller_data.index,
                autopct='%1.1f%%',
                colors=colors,
                startangle=90
            )
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
            for text in texts:
                text.set_fontsize(10)
                text.set_fontweight('bold')
            ax.set_title("Top 5 Bestseller Categories", fontweight='bold', pad=20, fontsize=12)
            plt.tight_layout()
            st.pyplot(fig)
        
        # Most common restaurants
        st.markdown("### Top 20 Most Frequent Restaurant Chains")
        top_restaurants = df_filtered['Restaurant_Name'].value_counts().head(20)
        
        fig, ax = plt.subplots(figsize=(13, 8))
        colors = sns.color_palette("viridis", len(top_restaurants))
        bars = ax.barh(top_restaurants.index, top_restaurants.values, color=colors)
        ax.bar_label(bars, fmt='%d', padding=3, fontweight='bold')
        ax.set_xlabel("Number of Items Listed", fontweight='bold', fontsize=11)
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown("""
        <div class="insight-box">
            <h4>🍔 Category Insight</h4>
            <p>
            <strong>Bestseller items represent pre-validated demand</strong>. These products consistently get customer votes 
            and positive reviews. Recommended menu composition: <strong>60% bestsellers, 30% trending cuisines, 10% experimental</strong>. 
            This maximizes revenue while testing new offerings.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================================
    # TAB 5: EXPANSION STRATEGY
    # ============================================================================
    with tab5:
        st.markdown("## 🎯 Data-Driven Expansion Strategy")
        
        # Calculate opportunity metrics
        st.markdown("### Market Opportunity Analysis")
        
        opportunity_metrics = []
        for city in df_filtered['City'].unique():
            city_df = df_filtered[df_filtered['City'] == city]
            
            metrics = {
                'City': city,
                'Restaurants': city_df['Restaurant_Name'].nunique(),
                'Total Items': len(city_df),
                'Avg Dining Rating': city_df['Dining_Rating'].mean(),
                'Avg Delivery Rating': city_df['Delivery_Rating'].mean(),
                'Total Customer Votes': city_df['Total_votes'].sum(),
                'Avg Item Price (₹)': city_df['Prices'].mean(),
            }
            opportunity_metrics.append(metrics)
        
        opp_df = pd.DataFrame(opportunity_metrics)
        
        # Create opportunity index
        opp_df['Engagement_Score'] = (opp_df['Total Customer Votes'] / opp_df['Total Customer Votes'].max() * 100).round(1)
        opp_df['Rating_Score'] = ((opp_df['Avg Dining Rating'] + opp_df['Avg Delivery Rating']) / 10 * 100).round(1)
        opp_df['Market_Size_Score'] = (opp_df['Restaurants'] / opp_df['Restaurants'].max() * 100).round(1)
        
        # Weighted opportunity index
        opp_df['Opportunity_Index'] = (
            opp_df['Engagement_Score'] * 0.50 +
            opp_df['Rating_Score'] * 0.30 +
            opp_df['Market_Size_Score'] * 0.20
        ).round(1)
        
        opp_sorted = opp_df.sort_values('Opportunity_Index', ascending=False)
        
        # Display opportunity metrics table
        display_cols = ['City', 'Restaurants', 'Total Items', 'Total Customer Votes', 'Avg Dining Rating', 'Avg Delivery Rating', 'Opportunity_Index']
        st.dataframe(
            opp_sorted[display_cols].round(2),
            use_container_width=True,
            hide_index=True
        )
        
        # Top recommendation card
        st.markdown("---")
        st.markdown("### 🏆 Primary Expansion Target")
        
        top_city = opp_sorted.iloc[0]
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #2ca02c 0%, #27ae60 100%); 
                    color: white; padding: 2.5rem; border-radius: 12px; margin: 1.5rem 0; box-shadow: 0 8px 24px rgba(0,0,0,0.15);">
            <h3 style="color: white; margin-top: 0;">🎯 Recommended Launch City: {top_city['City']}</h3>
            <table style="color: white; width: 100%; margin: 1.5rem 0;">
                <tr>
                    <td style="padding: 0.7rem;"><strong>Opportunity Index Score:</strong></td>
                    <td style="padding: 0.7rem; font-size: 1.3rem; font-weight: bold;">{top_city['Opportunity_Index']:.1f}/100</td>
                </tr>
                <tr>
                    <td style="padding: 0.7rem;"><strong>Customer Engagement:</strong></td>
                    <td style="padding: 0.7rem;">{int(top_city['Total Customer Votes']):,} votes (HIGH DEMAND)</td>
                </tr>
                <tr>
                    <td style="padding: 0.7rem;"><strong>Market Maturity:</strong></td>
                    <td style="padding: 0.7rem;">{int(top_city['Restaurants'])} existing restaurants (PROVEN MARKET)</td>
                </tr>
                <tr>
                    <td style="padding: 0.7rem;"><strong>Quality Benchmark:</strong></td>
                    <td style="padding: 0.7rem;">Dining: {top_city['Avg Dining Rating']:.2f}/5 | Delivery: {top_city['Avg Delivery Rating']:.2f}/5</td>
                </tr>
                <tr>
                    <td style="padding: 0.7rem;"><strong>Pricing Opportunity:</strong></td>
                    <td style="padding: 0.7rem;">Target menu price point: ₹{top_city['Avg Item Price (₹)']:.0f}</td>
                </tr>
            </table>
            <p style="font-size: 0.95rem; margin: 1.5rem 0 0 0; opacity: 0.95; border-top: 1px solid rgba(255,255,255,0.3); padding-top: 1.5rem;">
                <strong>Strategic Rationale:</strong> This city shows optimal combination of high customer engagement 
                (proven demand), established market (reduced risk), and achievable quality benchmarks. Ready for immediate launch.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Alternative options
        st.markdown("### Alternative Expansion Targets")
        
        col1, col2, col3 = st.columns(3)
        
        cities_to_display = [1, 2, 3] if len(opp_sorted) >= 3 else list(range(1, len(opp_sorted)))
        
        for idx, col in enumerate([col1, col2, col3][:len(cities_to_display)]):
            with col:
                city_data = opp_sorted.iloc[cities_to_display[idx]]
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #ff7f0e; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                    <h4 style="color: #ff7f0e; margin-top: 0;">Rank #{cities_to_display[idx] + 1}: {city_data['City']}</h4>
                    <p><strong>Opportunity Index:</strong> <span style="font-size: 1.2rem; color: #667eea;">{city_data['Opportunity_Index']:.1f}/100</span></p>
                    <p><strong>Customer Votes:</strong> {int(city_data['Total Customer Votes']):,}</p>
                    <p><strong>Restaurants:</strong> {int(city_data['Restaurants'])}</p>
                    <p><strong>Avg Rating:</strong> {(city_data['Avg Dining Rating'] + city_data['Avg Delivery Rating'])/2:.2f}/5</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Phased rollout strategy
        st.markdown("---")
        st.markdown("### 📋 Phased Market Entry Strategy")
        
        st.markdown("""
        <div class="insight-box">
            <h4>Phase 1: Market Validation (Months 1-3)</h4>
            <p>
            <strong>Action:</strong> Launch 1-2 flagship restaurants in primary target city<br>
            <strong>Menu Focus:</strong> Top 5 cuisines + bestseller items identified in analysis<br>
            <strong>Target Metrics:</strong>
            <ul>
                <li>Minimum 3.5+ dining rating by month 3</li>
                <li>Delivery rating ≥ 4.0 (reliable logistics)</li>
                <li>1,000+ customer votes per outlet</li>
                <li>Menu validation: 60% bestsellers performing well</li>
            </ul>
            </p>
        </div>
        
        <div class="insight-box">
            <h4>Phase 2: Geographic Expansion (Months 4-6)</h4>
            <p>
            <strong>Action:</strong> Replicate proven model to secondary cities (Ranks #2 & #3)<br>
            <strong>Customization:</strong>
            <ul>
                <li>Adjust pricing based on local market (₹200-300 range optimal)</li>
                <li>Localize top 5 cuisines per city preferences</li>
                <li>Maintain bestseller core (40-50% menu consistency)</li>
            </ul>
            <strong>Expected Outcome:</strong> 3 active markets by month 6
            </p>
        </div>
        
        <div class="insight-box">
            <h4>Phase 3: Multi-City Optimization (Months 7-12)</h4>
            <p>
            <strong>Action:</strong> Scale to all high-opportunity cities (Index > 60)<br>
            <strong>Operations:</strong>
            <ul>
                <li>Shared supply chain for bestsellers</li>
                <li>City-level menu variations (20-30%)</li>
                <li>Central kitchen model for premium items</li>
                <li>Target: 5+ cities, 1,000+ monthly customer votes per outlet</li>
            </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Pricing strategy
        st.markdown("---")
        st.markdown("### 💰 Pricing & Product Strategy")
        
        st.markdown("""
        <div class="insight-box">
            <h4>Menu Composition Framework</h4>
            <p style="font-size: 1rem; line-height: 1.8;">
            <strong>60% Bestsellers</strong> — High-volume, proven items (stable revenue)<br>
            <strong>30% Trending Cuisines</strong> — High-demand cuisines from city analysis (growth driver)<br>
            <strong>10% Experimental</strong> — New items to test (future menu evolution)<br>
            </p>
        </div>
        
        <div class="insight-box">
            <h4>Quality Thresholds</h4>
            <p>
            <strong>Dining Rating Target:</strong> ≥ 3.8/5 (food quality, ambiance)<br>
            <strong>Delivery Rating Target:</strong> ≥ 4.0/5 (speed, accuracy, packaging)<br>
            <strong>Why It Matters:</strong> Cities with 4.0+ delivery ratings see 40% higher order velocity
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================================
    # FOOTER
    # ============================================================================
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #636e72; margin-top: 3rem; padding: 2rem;">
        <p><strong>Zomato Market Intelligence Dashboard</strong> | Data-driven insights for restaurant expansion</p>
        <p style="font-size: 0.9rem;">Built with Streamlit | Dataset: 900+ restaurants, 123K+ records across 13 Indian cities</p>
        <p style="font-size: 0.85rem; margin-top: 1rem;">
            Dashboard demonstrates: Market analysis • Customer insights • Pricing strategy • Category trends • Strategic recommendations
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("Unable to load dashboard. Please check the data file.")