import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk

# Load data
DATA_URL = "2017_Crashes_10000_sample.csv"
data = pd.read_csv(DATA_URL)

# Streamlit application layout
st.title("Massachusetts Motor Vehicle Crashes 2017 Data Explorer")

# Sidebar widgets for user input
accident_severity = st.sidebar.selectbox("Select accident severity:", options=data['CRASH_SEVERITY_DESCR'].unique())

max_speed = st.sidebar.slider("Maximum speed limit:", min_value=0, max_value=100, value=50)

# Filter data based on user input
filtered_data = data[(data['CRASH_SEVERITY_DESCR'] == accident_severity) & (data['SPEED_LIMIT'] <= max_speed)]

# Display data table
st.write("Filtered Crashes Data", filtered_data)

# Create and display charts
fig, ax = plt.subplots()
ax.hist(filtered_data['SPEED_LIMIT'], bins=20, color='skyblue', edgecolor='black')
ax.set_title('Distribution of Speed Limits in Crashes')
ax.set_xlabel('Speed Limit (mph)')
ax.set_ylabel('Number of Crashes')
st.pyplot(fig)

# Create and display map
filtered_data = filtered_data.dropna(subset=['LAT', 'LON'])
st.map(filtered_data[['LAT', 'LON']])

# Summary report
st.write("Summary Report")
st.write("Maximum Speed Limit in Crashes:", filtered_data['SPEED_LIMIT'].max())
st.write("Minimum Speed Limit in Crashes:", filtered_data['SPEED_LIMIT'].min())
st.write("Most Common Accident Severity:", filtered_data['CRASH_SEVERITY_DESCR'].mode()[0])

# PyDeck map with custom layers
layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_data,
    get_position='[LON, LAT]',
    get_color='[200, 30, 0, 160]',
    get_radius=100,
)
view_state = pdk.ViewState(LAT=data['LAT'].mean(), LON=data['LON'].mean(), zoom=10)
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# Add narrative
st.write("The above histogram shows the distribution of speed limits in crashes where the severity is '{}' and the speed limit does not exceed {} mph.".format(accident_severity, max_speed))
st.write("The map visualizes the locations of these crashes. Red dots represent crash sites.")
