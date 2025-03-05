import streamlit as st
import requests

API_URL = "https://api.thecatapi.com/v1/images/search?limit=9"

def fetch_cat_images():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return [img["url"] for img in response.json()]
    return []

st.title("🐱 Random Cat Gallery")

if "images" not in st.session_state:
    st.session_state.images = fetch_cat_images()

cols = st.columns(3)
for index, image in enumerate(st.session_state.images):
    with cols[index % 3]:
        st.image(image, use_column_width=True)

if st.button("Load More"):
    st.session_state.images = fetch_cat_images()
    st.experimental_rerun()
