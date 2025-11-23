# DV Streamlit Assignment 🌍

## Environmental Pollution Analysis Dashboard

## 📖 Overview

## This project is an interactive Environmental Pollution Dashboard built using Python and Streamlit. It

## visualizes air quality data (AQI, PM2.5, PM10, etc.) across various cities, allowing users to track

## pollution trends, compare environmental metrics, and derive actionable insights through dynamic

## charts and geospatial maps.

## ✨ Key Features

## 📊 Interactive KPI Board: Real-time display of Average AQI, Peak PM2.5, Lowest Humidity, and

## overall air quality status.

## 🔍 Smart Filters: Sidebar controls to filter data by City, Date Range, and specific AQI levels.

## 📈 Dynamic Visualizations:

## Trend Analysis: Line charts tracking pollutants (AQI, NO2, SO2, etc.) over time.

## City Comparison: Color-coded bar charts comparing average AQI.

## Correlation Analysis: Scatter plots correlating Temperature vs. PM2.5 levels.

## 🗺 Geospatial Mapping: Visualizes pollution hotspots on a map (requires lat/lon data).

## 📥 Data Export: Download filtered datasets directly as CSV files.

## 🚦 Live Status Indicators: Conditional formatting highlights hazardous air quality levels instantly.

## 🔄 Auto-Refresh: Optional simulation mode to refresh data every minute.

## 🛠 Installation & Setup

## 1. Prerequisites

## Ensure you have Python installed. You will need the following libraries:

```
streamlit
pandas
plotly
```
## 2. Install Dependencies

## Run the following command in your terminal to install the required packages:

```
pip install streamlit pandas plotly
```
## 3. Data Setup

### Ensure your dataset is named environment_pollution_data.csv and is placed in the root directory.

### The CSV should contain the following columns:

```
Column Description
City Name of the city
Date Date of recording (YYYY-MM-DD)
AQI Air Quality Index
PM2.5 Particulate Matter < 2.5 μm
PM10 Particulate Matter < 10 μm
Temperature Temperature in Celsius
Humidity Humidity Percentage
lat Latitude (Optional, for map)
lon Longitude (Optional, for map)
```
## 🚀 How to Run

### Navigate to the project directory in your terminal and execute:

```
streamlit run pollution_dashboard.py
```
### The application will launch automatically in your default web browser.

## 📂 Project Structure

```
DV_Streamlit_Assignment/│
├──├── environment_pollution_data.csv # Source dataset pollution_dashboard.py # Main application code
└── README.md # Project documentation
```
## 💡 Insights generated

### The dashboard automatically calculates and displays:

### The city with the highest pollution levels in the selected range.

### The city with the cleanest air.

### Warnings for Unhealthy or Hazardous AQI days.

### Created for the Data Visualization Streamlit Assignment.
