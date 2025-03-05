import streamlit as st
import requests

API_URL = "https://api.thecatapi.com/v1/images/search"
BREEDS_URL = "https://api.thecatapi.com/v1/breeds"

st.title("🐱 Random Cat Images Gallery")


@st.cache_data
def get_breeds():
    response = requests.get(BREEDS_URL)
    if response.status_code == 200:
        breeds = response.json()
        return {breed["name"]: breed["id"] for breed in breeds}
    return {}


def fetch_cat_images(limit=9, breed_id=None):
    params = {"limit": limit}
    if breed_id:
        params["breed_ids"] = breed_id
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return [img["url"] for img in response.json()]
    return []

breeds = get_breeds()
selected_breed = st.selectbox("Filter by breed:", ["All"] + list(breeds.keys()))

if "images" not in st.session_state:
    breed_id = breeds.get(selected_breed) if selected_breed != "All" else None
    st.session_state.images = fetch_cat_images(breed_id=breed_id)

cols = st.columns(3)
for index, image in enumerate(st.session_state.images):
    with cols[index % 3]:
        st.image(image, use_container_width=True)  

if st.button("Load More"):
    breed_id = breeds.get(selected_breed) if selected_breed != "All" else None
    st.session_state.images = fetch_cat_images(breed_id=breed_id)
    st.rerun() 
