import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

BASE_URL = "http://www.geophysics.geol.uoa.gr/stations/maps/"
DATA_URLS = {
    "Last 2 Days": "recent_eq_2d_el.htm",
    "Last 10 Days": "recent_eq_10d_el.htm",
    "Last 20 Days": "recent_eq_20d_el.htm"
}

@st.cache_data(show_spinner=False)
def fetch_data(time_range):
    """
    Fetch and process the seismic data for the given time range.
    Returns a DataFrame filtered for the Santorini area and shallow earthquakes.
    """
    url = BASE_URL + DATA_URLS[time_range]
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'iso-8859-7'
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    if len(tables) < 3:
        st.error("Insufficient tables found on the page.")
        return None
    
    table = tables[2]
    data = []
    for row in table.find_all('tr')[1:]:
        row_data = [td.get_text(strip=True) for td in row.find_all('td')]
        if row_data:
            data.append(row_data)
    
    if not data:
        st.error("No data found in the extracted table.")
        return None   
  
    # Ensure we take only the first 6 columns in case of extra ones
    expected_columns = ["Origin Time (GMT)", "Epicenter", "Latitude", "Longitude", "Depth (km)", "Magnitude"]
    df = pd.DataFrame([row[2:] for row in data], columns=expected_columns)
    df = df.iloc[:, :len(expected_columns)]  # Trim to expected columns
    
    if df.shape[1] != len(expected_columns):
        st.error(f"Unexpected table format. Expected {len(expected_columns)} columns, got {df.shape[1]}.")
        return None
    
    df.columns = expected_columns
    df = df[df['Epicenter'].str.contains('Θήρας', na=False)]
    df = df[pd.to_numeric(df['Depth (km)'], errors='coerce') < 100]
    
    return df

def generate_plot(df, time_range):
    """Generate a matplotlib plot for the given DataFrame."""
    try:
        time = np.array([datetime.strptime(ts, '%d/%m/%Y %H:%M:%S') for ts in df['Origin Time (GMT)']])
        magnitude = df['Magnitude'].astype(float)
    except Exception as e:
        st.error(f"Error processing data: {e}")
        return None
    
    coefficients = np.polyfit(range(len(time)), magnitude, 2)
    quadratic_trend = np.poly1d(coefficients)(range(len(time)))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(time, magnitude, label='Magnitude')
    ax.plot(time, quadratic_trend, linestyle='--', color='red', label='Quadratic Trend')
    ax.set_xlabel('Date')
    ax.set_ylabel('Magnitude')
    ax.set_title(f'Seismic Activity near Santorini - {time_range}')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M' if time_range == "Last 2 Days" else '%d/%m'))
    
    plt.legend(loc='upper left')
    plt.tight_layout()
    
    return fig

def main():
    st.title("Santorini Seismic Activity Dashboard")
    st.write("Fetches and visualizes real-time earthquake data for the Santorini area.")
    
    cols = st.columns(len(DATA_URLS))
    for col, (time_range, url) in zip(cols, DATA_URLS.items()):
        with col:
            if st.button(f"Generate Plot ({time_range})"):
                with st.spinner(f"Fetching data for {time_range}..."):
                    df = fetch_data(time_range)
            
                if df is not None and not df.empty:
                    fig = generate_plot(df, time_range)
                    if fig:
                        st.pyplot(fig)
                else:
                    st.error("No data available to plot.")

if __name__ == "__main__":
    main()
