# 📈 Santorini Seismic Activity 🇬🇷

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-150458?style=for-the-badge&logo=Matplotlib&logoColor=white)](https://matplotlib.org/)

This Streamlit app visualizes seismic activity data near Santorini, Greece. It fetches earthquake data from the [Geophysics Department of the University of Athens](http://www.geophysics.geol.uoa.gr/stations/maps/recent_gr.html), filters it for events near Santorini, and displays a plot of earthquake magnitude over time.

## Features

- Fetches real-time earthquake data.
- Filters data for events near Santorini.
- Plots earthquake magnitude over time.
- Shows a polynomial trendline to visualize the overall trend of seismic activity.

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/sgkouzias/Santorini-Earthquake-Monitor.git
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```
This will open the app in your web browser.

## Data Source

The earthquake data is sourced from the [Geophysics Department of the University of Athens](http://www.geophysics.geol.uoa.gr/stations/maps/recent_gr.html).

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

![Logo](logo.jpg)
