# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk

# Load data from a CSV file into a pandas DataFrame
DATA_URL = "2017_Crashes_10000_sample.csv"
data = pd.read_csv(DATA_URL)


# Set the title of the Streamlit application
st.title("Massachusetts Motor Vehicle Crashes 2017 Data Explorer")

# Create a dropdown list in the sidebar for city selection
# The options for the dropdown are the unique values in the 'CITY_TOWN_NAME' column of the dataset
city = st.sidebar.selectbox("Select city:", options=data['CITY_TOWN_NAME'].unique())

# Create a multiselect list in the sidebar for cause selection
# The options for the multiselect are the unique values in the 'MANR_COLL_DESCR' column of the dataset
causes = st.sidebar.multiselect("Select possible causes:", options=data['MANR_COLL_DESCR'].unique())

# Filter the data based on the user's city and cause selections
# This is done using pandas' boolean indexing feature
filtered_data = data[(data['CITY_TOWN_NAME'] == city) & (data['MANR_COLL_DESCR'].isin(causes))]

# Display the filtered data in a table
st.write("Filtered Crashes Data", filtered_data)

# Create a bar chart showing the number of crashes by cause
# This is done using matplotlib
fig, ax = plt.subplots()
cause_counts = filtered_data['MANR_COLL_DESCR'].value_counts()
ax.bar(cause_counts.index, cause_counts.values, color='skyblue')
ax.set_title('Number of Crashes by Cause')
ax.set_xlabel('Cause')
ax.set_ylabel('Number of Crashes')

# Display the bar chart in the Streamlit application
st.pyplot(fig)

# Remove rows with missing 'LAT' or 'LON' values from the filtered data
filtered_data = filtered_data.dropna(subset=['LAT', 'LON'])

# Create a map showing the locations of the crashes
# This is done using Streamlit's st.map function, which takes a DataFrame with 'LAT' and 'LON' columns
st.map(filtered_data[['LAT', 'LON']])

# Calculate and display the most common cause of crashes in the filtered data
# This is done using pandas' mode function, which returns the most frequently occurring value(s)
modes = filtered_data['MANR_COLL_DESCR'].mode()
if len(modes) > 0:
    st.write("Most Common Cause of Crashes:", modes[0])
else:
    st.write("No common cause of crashes found.")

# Create a more advanced map visualization using PyDeck
# This map includes a custom layer that represents the locations of the crashes as red dots
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
# This text explains what the histograms and map show
st.write("The above histograms show the distribution of crashes by city and cause where the city is '{}' and the causes include {}".format(city, causes))
st.write("The map visualizes the locations of these crashes. Red dots represent crash sites.")
