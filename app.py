import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import folium
from streamlit_folium import st_folium

# ========== LOAD DATA ==========
df = pd.read_csv("district6_sites_with_walks.csv")
walk1_pins = pd.read_csv("walk1_custom_pins.csv")  # Custom data for Walk 1

# ========== STREAMLIT UI ==========
st.set_page_config(layout="wide")
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
        return " ".join(p.text for p in paragraphs)
    except Exception as e:
        return f"Error fetching info: {e}"

# ========== SIMPLE LOCAL CHATBOT ==========
def simple_local_response(question):
    q = question.lower()

    if "district six" in q:
        return "District Six was a vibrant community forcibly removed under apartheid. The museum preserves their stories."
    elif "why was it destroyed" in q or "what happened" in q:
        return "District Six was declared a 'whites-only' area under apartheid in 1966, and over 60,000 residents were forcibly removed."
    elif "museum" in q:
        return "The District Six Museum educates visitors about the history of the community and the injustices they faced."
    elif "how many people" in q:
        return "More than 60,000 people were displaced from District Six during the apartheid era."
    elif "can i visit" in q or "how to visit" in q:
        return "Yes! You can visit the District Six Museum in Cape Town. They also offer walking tours."
    elif "walking tour" in q or "site" in q:
        return "The walking tours highlight key sites in District Six, telling the stories of families and landmarks that once thrived there."
    else:
        return "I’m not sure how to answer that, but you can learn more at https://www.districtsix.co.za"

# ========== MAIN WALK LOOP ==========
for i, (walk_name, tab) in enumerate(zip(walks, tabs)):
    with tab:
        st.subheader(f"{walk_name}: Interactive Map")

        # Use custom Walk 1 pins, or default for others
        if walk_name == "Walk 1":
            walk_df = walk1_pins.copy()
        else:
            walk_df = df[df["walk_group"] == walk_name]

        if not walk_df.empty:
            lat_center = walk_df["latitude"].mean()
            lon_center = walk_df["longitude"].mean()

            m = folium.Map(location=[lat_center, lon_center], zoom_start=17)

            for _, row in walk_df.iterrows():
                popup_html = f"""
                    <strong>{row['current_name']}</strong><br/>
                    <em>{row['historic_name']}</em><br/>
                    <p style='max-width: 250px;'>{row.get('description', '')}</p>
                """
                folium.Marker(
                    location=[row["latitude"], row["longitude"]],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=row["current_name"],
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(m)

            st_data = st_folium(m, width=1000, height=500)

        # 🤖 Offline Chat Interface
        st.subheader("Ask about this walk")
        user_input = st.chat_input("Ask a question about District Six Museum...", key=f"chat_input_{i}")

        if user_input:
            st.chat_message("user").write(user_input)
            ai_response = simple_local_response(user_input)
            st.chat_message("assistant").write(ai_response)
