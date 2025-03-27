import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Set page settings
st.set_page_config(layout="wide")
st.title("District Six Historical Map")
st.markdown("Explore the historical buildings and memories of District Six.")

# ✅ Load the updated CSV
df = pd.read_csv("district6_sites.csv")

# ✅ Create a map centered on District Six
m = folium.Map(location=[-33.9304, 18.4244], zoom_start=16)

# ✅ Add markers for each location
for _, row in df.iterrows():
    popup = f"""
        <strong>{row['name']}</strong><br>
        <img src="{row['image_url']}" width="200"><br><br>
        <iframe width="250" height="150" src="{row['video_url']}"></iframe><br>
        <p>{row['description']}</p>
        <a href="https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={row['latitude']},{row['longitude']}" target="_blank">
        View in 360° Street View
        </a>
"""
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup = folium.Popup(popup, max_width=500),
        tooltip=row['name']
    ).add_to(m)

# ✅ Show the map in Streamlit
folium_static(m)
