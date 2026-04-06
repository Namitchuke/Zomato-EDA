import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(page_title="Zomato Analytics Dashboard", page_icon="🍴", layout="wide")

st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Cache data loading
@st.cache_data
def load_data():
    df = pd.read_csv("zomato_dataset.csv")
    
    # Cleaning Logic from Notebook
    df['City'] = df['City'].str.strip().str.title()
    locality_to_bangalore = {
        'Banaswadi': 'Bangalore', 'Ulsoor': 'Bangalore', 
        'Magrath Road': 'Bangalore', 'Malleshwaram': 'Bangalore'
    }
    df['City'] = df['City'].replace(locality_to_bangalore)
    
    # Votes
    df['total_votes'] = df['Dining_Votes'] + df['Delivery_Votes']
    
    # Numeric conversion for ratings
    df['Dining_Rating'] = pd.to_numeric(df['Dining_Rating'], errors='coerce')
    df['Delivery_Rating'] = pd.to_numeric(df['Delivery_Rating'], errors='coerce')
    
    # Null value adjustments
    df["Best_Seller"] = df["Best_Seller"].fillna("NA")
    
    return df

# Initialize session state for data
df = load_data()

# Header
st.title("🍴 Zomato Data Analysis Dashboard")
st.markdown("Exploring the restaurant landscape across major Indian cities.")

# Sidebar Filters
st.sidebar.header("Filter Data")
cities = st.sidebar.multiselect("Select Cities", options=sorted(df['City'].unique()), default=sorted(df['City'].unique())[:5])

if not cities:
    st.error("Please select at least one city.")
    st.stop()

filtered_df = df[df['City'].isin(cities)]

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Restaurants", f"{filtered_df['Restaurant_Name'].nunique():,}")
with col2:
    st.metric("Total Votes", f"{filtered_df['total_votes'].sum():,}")
with col3:
    st.metric("Avg Dining Rating", f"{filtered_df['Dining_Rating'].mean():.2f}⭐")
with col4:
    st.metric("Avg Price", f"₹{filtered_df['Prices'].mean():.1f}")

st.markdown("---")

# Visualizations Row 1
c1, c2 = st.columns(2)

with c1:
    st.subheader("🏙️ Restaurants by City")
    res_count = filtered_df.groupby('City')['Restaurant_Name'].nunique().reset_index(name='Count').sort_values(by='Count', ascending=False)
    fig1 = px.bar(res_count, x='Count', y='City', orientation='h', 
                 color='Count', color_continuous_scale='Viridis',
                 labels={'Count': 'Number of Restaurants'})
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("🗳️ Total Votes by City")
    votes_city = filtered_df.groupby('City')['total_votes'].sum().reset_index().sort_values(by='total_votes', ascending=False)
    fig2 = px.bar(votes_city, x='City', y='total_votes', 
                 color='total_votes', color_continuous_scale='Magma',
                 labels={'total_votes': 'Total Votes'})
    st.plotly_chart(fig2, use_container_width=True)

# Map Section
st.subheader("📍 Restaurant Hotspots")
# City coordinates from Notebook
city_coords = {
    'Hyderabad': (17.3850, 78.4867), 'Jaipur': (26.9124, 75.7873), 'Mumbai': (19.0761, 72.8774),
    'Chennai': (13.0827, 80.2707), 'Bangalore': (12.9716, 77.5946), 'Ahmedabad': (23.0225, 72.5714),
    'Kolkata': (22.5726, 88.3639), 'Pune': (18.5204, 73.8567), 'Kochi': (9.9312, 76.2673),
    'Raipur': (21.2514, 81.6300), 'Lucknow': (26.8467, 80.9462), 'New Delhi': (28.6139, 77.2090), 'Goa': (15.2993, 74.1240)
}

map_df = filtered_df.groupby('City')['Restaurant_Name'].count().reset_index(name='Count')
map_df = map_df[map_df['City'].isin(city_coords.keys())]

m = folium.Map(location=[22.9734, 78.6569], zoom_start=5, tiles="CartoDB positron")
for _, row in map_df.iterrows():
    lat, lon = city_coords[row['City']]
    folium.CircleMarker(
        location=[lat, lon],
        radius=row['Count'] / 500,
        popup=f"{row['City']}: {row['Count']} records",
        color='#FF4B4B',
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

st_folium(m, width=1200, height=500)

# Visualizations Row 2
c3, c4 = st.columns(2)

with c3:
    st.subheader("🍰 Top 5 Best Sellers")
    df_new = filtered_df[filtered_df["Best_Seller"] != 'NA']
    bestseller = df_new['Best_Seller'].value_counts().nlargest(5).reset_index()
    fig3 = px.pie(bestseller, names='index', values='Best_Seller', 
                 hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.subheader("💰 Most Expensive Dishes by Category")
    expensive = filtered_df.groupby(['City', 'Cuisine ', 'Item_Name'])['Prices'].max().reset_index().nlargest(10, 'Prices')
    st.dataframe(expensive.style.background_gradient(subset=['Prices'], cmap='YlOrRd'), use_container_width=True)

# Raw Data Section
with st.expander("View Raw Data"):
    st.write(filtered_df.head(100))

st.sidebar.markdown("---")
st.sidebar.info("Developed for Zomato EDA Project")
