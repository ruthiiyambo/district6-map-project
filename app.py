import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import folium
from streamlit_folium import st_folium

# ✅ Must be the first Streamlit command
st.set_page_config(layout="wide")

# ========== LOAD DATA ==========
df = pd.read_csv("district6_sites_with_walks.csv")
walk1_pins = pd.read_csv("walk1_custom_pins.csv")

# ========== STREAMLIT UI ==========
st.title("District Six Digital Memory Map")
st.markdown("---")

# Centered Logo (Responsive)
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/ruthiiyambo/district6-map-project/main/district6-image.png" 
             alt="District Six Museum Logo" width="300"/>
        <p style="font-size: 0.9em; color: gray;">Logo of the District Six Museum</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Museum Intro
st.markdown("""
### 🏛️ About the District Six Museum

District Six was once a vibrant, multicultural community in Cape Town until it was destroyed under apartheid. The District Six Museum works to preserve the memory, culture, and stories of those who lived there.

This digital app invites you to walk through District Six's historic sites — combining maps, media, and storytelling.

---
""")

# ========== WALK TABS ==========
walks = df["walk_group"].unique().tolist()
tabs = st.tabs(walks)

# ========== SCRAPE INFO FUNCTION ==========
def fetch_district6_info():
    url = "https://www.districtsix.co.za/walking-tours/"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        return " ".join(p.text for p
