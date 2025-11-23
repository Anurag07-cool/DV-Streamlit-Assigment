import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. Setup and Data Loading
st.set_page_config(page_title="Environmental Pollution Dashboard", layout="wide")

# Auto-refresh logic (Optional Enhancement)
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False

def toggle_refresh():
    st.session_state.auto_refresh = not st.session_state.auto_refresh

# Function to load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("environment_pollution_data.csv", parse_dates=["Date"])
        return df
    except FileNotFoundError:
        st.error("File 'environment_pollution_data.csv' not found. Please ensure the file is in the same directory.")
        return pd.DataFrame()

df = load_data()

# Conditional Formatting Function for AQI
def highlight_aqi(val):
    if val <= 50:
        color = 'background-color: #00e400; color: black' # Good
    elif val <= 100:
        color = 'background-color: #ffff00; color: black' # Moderate
    elif val <= 200:
        color = 'background-color: #ff7e00; color: black' # Poor
    elif val <= 300:
        color = 'background-color: #ff0000; color: white' # Unhealthy
    else:
        color = 'background-color: #7e0023; color: white' # Hazardous
    return color

if not df.empty:
    # 2. Sidebar Filters
    st.sidebar.header("Filters")

    # Auto-refresh control
    st.sidebar.checkbox("Enable Auto-Refresh (1 min)", value=st.session_state.auto_refresh, on_change=toggle_refresh)

    # City Selection
    all_cities = df["City"].unique()
    selected_cities = st.sidebar.multiselect("Select City", all_cities, default=all_cities)

    # Date Range
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    
    if min_date == max_date:
        st.sidebar.write(f"Date available: {min_date}")
        start_date, end_date = min_date, max_date
    else:
        date_range = st.sidebar.date_input("Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
        if len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date, end_date = min_date, max_date

    # Pollutant Range
    min_aqi = int(df["AQI"].min())
    max_aqi = int(df["AQI"].max())
    aqi_range = st.sidebar.slider("Select AQI Range", min_value=0, max_value=500, value=(min_aqi, max_aqi))

    # Filtering Logic
    filtered_df = df[
        (df["City"].isin(selected_cities)) &
        (df["Date"].dt.date >= start_date) &
        (df["Date"].dt.date <= end_date) &
        (df["AQI"].between(aqi_range[0], aqi_range[1]))
    ]

    # 3. Main Dashboard Layout
    st.title("🌍 Environmental Pollution Dashboard")
    st.markdown("Analyze air quality trends, pollution levels, and environmental factors across different cities.")

    # Dataset Overview
    with st.expander("Dataset Overview"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Raw Data Preview")
            st.dataframe(df.head())
        with col2:
            st.subheader("Statistical Summary")
            st.dataframe(df.describe())

    # KPIs Section
    st.subheader("Key Performance Indicators")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    if not filtered_df.empty:
        avg_aqi = filtered_df["AQI"].mean()
        max_pm25 = filtered_df["PM2.5"].max()
        min_humidity = filtered_df["Humidity"].min()
        
        # AQI Level Indicator
        if avg_aqi <= 50: status, color = "Good", "normal"
        elif avg_aqi <= 100: status, color = "Moderate", "off"
        elif avg_aqi <= 200: status, color = "Poor", "inverse"
        elif avg_aqi <= 300: status, color = "Unhealthy", "inverse"
        else: status, color = "Hazardous", "inverse"

        kpi1.metric("Avg AQI", f"{avg_aqi:.1f}", delta_color=color)
        kpi2.metric("Highest PM2.5", f"{max_pm25} µg/m³")
        kpi3.metric("Lowest Humidity", f"{min_humidity}%")
        kpi4.metric("Overall Status", status)
    else:
        st.warning("No data available for the selected filters.")

    st.markdown("---")

    # Charts Section
    if not filtered_df.empty:
        col_chart1, col_chart2 = st.columns(2)

        # Chart 1: Bar Chart
        with col_chart1:
            st.subheader("Average AQI by City")
            avg_aqi_city = filtered_df.groupby("City")["AQI"].mean().reset_index()
            fig_bar = px.bar(
                avg_aqi_city, x="City", y="AQI", color="AQI", 
                color_continuous_scale="RdYlGn_r", title="Average AQI Comparison"
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Chart 2: Scatter Plot
        with col_chart2:
            st.subheader("PM2.5 vs Temperature")
            fig_scatter = px.scatter(
                filtered_df, x="Temperature", y="PM2.5", color="City", size="AQI", 
                hover_data=["Humidity"], title="Relationship: Pollution vs Temperature"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        # Chart 3: Line Chart (Trends)
        st.subheader("Pollution Trends Over Time")
        pollutant = st.selectbox("Select Pollutant for Trend", ["AQI", "PM2.5", "PM10", "NO2", "SO2"])
        fig_line = px.line(
            filtered_df, x="Date", y=pollutant, color="City", markers=True, 
            title=f"{pollutant} Levels Over Time"
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Map Visualization (Optional Enhancement)
        if 'lat' in filtered_df.columns and 'lon' in filtered_df.columns:
            st.subheader("📍 Pollution Map")
            # Streamlit map requires 'lat' and 'lon' columns. 
            # We scale the circle size by AQI for better visualization (simulated by repeating rows or just standard dots)
            st.map(filtered_df, size=20, color='#FF0000')

        # Data Table with Conditional Formatting (Optional Enhancement)
        st.subheader("Filtered Data with AQI Indicators")
        styled_df = filtered_df.style.map(highlight_aqi, subset=['AQI'])
        st.dataframe(styled_df, use_container_width=True)
        
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv, file_name='pollution_data.csv', mime='text/csv')

        # Insights Section
        st.subheader("💡 Insights")
        highest_aqi_city = filtered_df.loc[filtered_df["AQI"].idxmax()]["City"]
        lowest_aqi_city = filtered_df.loc[filtered_df["AQI"].idxmin()]["City"]
        st.info(f"The most polluted city in this selection is **{highest_aqi_city}**. **{lowest_aqi_city}** has the cleanest air currently.")

    # Auto-refresh handling
    if st.session_state.auto_refresh:
        time.sleep(60)
        st.rerun()

    else:
        st.error("Please adjust filters to show data.")