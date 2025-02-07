import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

@st.cache_data(show_spinner=False)
def fetch_data():
    """
    Fetches and processes the seismic data from the source.
    Returns a DataFrame after filtering for the Santorini area and shallow earthquakes.
    """
    # URL of the site
    url = "http://www.geophysics.geol.uoa.gr/stations/maps/recent_eq_10d_el.htm"
    
    # Fetch the content of the page
    response = requests.get(url)
    response.raise_for_status()
    
    # Set the proper encoding (try iso-8859-7 for Greek pages)
    response.encoding = 'iso-8859-7'
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all table elements
    tables = soup.find_all('table')
    if len(tables) < 3:
        st.error("Less than 3 tables found on the page.")
        return None
    
    # Select table 3 (index 2)
    table = tables[2]
    
    # Extract table headers, if present
    headers = []
    header_row = table.find('tr')
    if header_row:
        headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
    
    # Extract table rows
    data = []
    rows = table.find_all('tr')
    for row in rows:
        # Skip rows that contain headers
        if row.find_all('th'):
            continue
        row_data = [td.get_text(strip=True) for td in row.find_all('td')]
        if row_data:
            data.append(row_data)
    
    # Create a DataFrame
    if data:
        if headers and len(headers) == len(data[0]):
            df = pd.DataFrame(data, columns=headers)
        else:
            df = pd.DataFrame(data)
    else:
        st.error("No data rows found in table 3.")
        return None

    # Filter data for Santorini area and depth less than 100 km
    df_santorini = df[df['Επίκεντρο'].str.contains('Θήρας')]
    filtered_df = df_santorini[df_santorini['Βάθος(χμ)'].astype(np.float32) < 100.]
    
    return filtered_df

def generate_plot(df):
    """
    Generates a matplotlib plot for the given DataFrame.
    """
    try:
        # Reverse the order of time and magnitude for plotting
        time_strings = df['Χρόνος Γένεσης(GMT)'].values[::-1]
        time = np.array([datetime.strptime(ts, '%d/%m/%Y %H:%M:%S') for ts in time_strings])
        magnitude = df['Μέγ.'].values[::-1].astype(np.float32)
    except Exception as e:
        st.error("Error processing date/time or magnitude data.")
        st.error(e)
        return None
    
    # Compute the quadratic trendline (polynomial of degree 2)
    coefficients = np.polyfit(range(len(time)), magnitude, 2)
    polynomial = np.poly1d(coefficients)
    quadratic_trend = polynomial(range(len(time)))
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(time, magnitude, label='Magnitude')
    ax.plot(time, quadratic_trend, linestyle='--', color='red', label='Quadratic Trend')
    ax.set_xlabel('Ημερομηνία - Ώρα')
    ax.set_ylabel('Μέγεθος')
    ax.set_title('Σεισμική Ακολουθία στην Σαντορίνη')
    
    # Format the x-axis dates
    date_format = mdates.DateFormatter('%d/%m %H:%M')
    ax.xaxis.set_major_formatter(date_format)
    plt.legend()
    plt.tight_layout()
    
    return fig

def main():
    st.title("Santorini Seismic Activity Dashboard")
    st.write("This Streamlit app fetches and visualizes real-time earthquake data for the Santorini area provided by the Geophysics Department of the University of Athens.")
    
    # Button to trigger data fetching and plotting
    if st.button("Generate Seismic Plot"):
        with st.spinner("Fetching and processing data..."):
            df = fetch_data()
        
        if df is not None and not df.empty:
            fig = generate_plot(df)
            if fig:
                st.pyplot(fig)
        else:
            st.error("No data available to plot.")

if __name__ == "__main__":
    main()
