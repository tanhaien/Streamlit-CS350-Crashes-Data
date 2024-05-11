""" 
Name:       Your Name 
CS230:      Section XXX 
Data:       2017_Crashes_10000_sample.csv
URL:        Link to your web application on Streamlit Cloud (if posted)  
Description:     
This program visualizes the Massachusetts Motor Vehicle Crashes 2017 data. It allows the user to filter the data by city and cause, and it displays the filtered data in a table, a bar chart, and two maps. It also calculates and displays the most common cause of crashes in the filtered data.
"""

# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk

# [PY1] A function with two or more parameters, one of which has a default value
def load_data(url="2017_Crashes_10000_sample.csv"):
    return pd.read_csv(url)

# Load data from a CSV file into a pandas DataFrame
DATA_URL = "2017_Crashes_10000_sample.csv"
data = load_data(DATA_URL)

# [DA1] Clean the data
data = data.dropna(subset=['LAT', 'LON', 'CITY_TOWN_NAME', 'MANR_COLL_DESCR'])

# Set the title of the Streamlit application
st.title("Massachusetts Motor Vehicle Crashes 2017 Data Explorer")

# [ST1] Create a dropdown list in the sidebar for city selection
city = st.sidebar.selectbox("Select city:", options=data['CITY_TOWN_NAME'].unique())

# [ST2] Create a multiselect list in the sidebar for cause selection
causes = st.sidebar.multiselect("Select possible causes:", options=data['MANR_COLL_DESCR'].unique())

# [DA5] Filter the data based on the user's city and cause selections
filtered_data = data[(data['CITY_TOWN_NAME'] == city) & (data['MANR_COLL_DESCR'].isin(causes))]

# Display the filtered data in a table
st.write("Filtered Crashes Data", filtered_data)

# [VIZ1] Create a bar chart showing the number of crashes by cause
fig, ax = plt.subplots()
cause_counts = filtered_data['MANR_COLL_DESCR'].value_counts()
ax.bar(cause_counts.index, cause_counts.values, color='skyblue')
ax.set_title('Number of Crashes by Cause')
ax.set_xlabel('Cause')
ax.set_ylabel('Number of Crashes')

# Display the bar chart in the Streamlit application
st.pyplot(fig)

# [VIZ2] Create a map showing the locations of the crashes
st.map(filtered_data[['LAT', 'LON']])

# [DA3] Calculate and display the most common cause of crashes in the filtered data
modes = filtered_data['MANR_COLL_DESCR'].mode()
if len(modes) > 0:
    st.write("Most Common Cause of Crashes:", modes[0])
else:
    st.write("No common cause of crashes found.")

# [VIZ4] Create a more advanced map visualization using PyDeck
layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_data,
    get_position='[LON, LAT]',
    get_color='[200, 30, 0, 160]',
    get_radius=100,
)
view_state = pdk.ViewState(latitude=data['LAT'].mean(), longitude=data['LON'].mean(), zoom=10)
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# Add some narrative text to the application
st.write("The above histograms show the distribution of crashes by city and cause where the city is '{}' and the causes include {}".format(city, causes))
st.write("The map visualizes the locations of these crashes. Red dots represent crash sites.")
