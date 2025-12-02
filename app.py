import streamlit as st
import requests

st.set_page_config(page_title="Mars Rover Photos", layout="wide")
st.title("🚀 Mars Rover Image Viewer")
st.markdown("Explore real images taken by **Curiosity rover**, filtered by Sol (Martian day) and camera.")

API_KEY = "DEMO_KEY"

with st.container():
    col1, col2 = st.columns([1, 1])
    with col1:
        sol = st.slider("🔢 Select a Sol (Martian Day)", min_value=100, max_value=4300, value=2012, step=1)

@st.cache_data(show_spinner=True)
def fetch_photos(sol):
    url = "https://rovers.nebulum.one/api/v1/rovers/Curiosity/photos"
    params = {"sol": sol}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        st.error(f"API Error {response.status_code}")
        return []
    elif "application/json" not in response.headers.get("Content-Type", ""):
        st.error("Received non-JSON response from API")
        return []
    data = response.json()
    return data.get("photos", [])

photos = fetch_photos(sol)

if not photos:
    st.warning("😕 No photos found for this Sol. Try another.")
    selected_camera = None
else:
    available_cameras = sorted(set(photo["camera"]["full_name"] for photo in photos))
    with col2:
        selected_camera = st.selectbox("📷 Filter by Camera", options=available_cameras)

if photos and selected_camera:
    filtered_photos = [photo for photo in photos if photo["camera"]["full_name"] == selected_camera]
    st.success(f"Showing {min(len(filtered_photos), 3)} photo(s) from '{selected_camera}' on Sol {sol}")

    num_images = min(3, len(filtered_photos))
    columns = st.columns(num_images if num_images < 3 else 3)

    for i in range(num_images):
        photo = filtered_photos[i]
        with columns[i]:
            st.markdown(
                f"""
                <div style="height: 300px; overflow: hidden; display: flex; align-items: center; justify-content: center;
                            background: #111; border-radius: 8px; margin-bottom: 0.5rem;">
                    <img src="{photo['img_src']}" style="height: 100%; object-fit: cover;" />
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(f"**📅 Earth Date:** {photo['earth_date']}")
            st.markdown(f"**📷 Camera:** {photo['camera']['full_name']} (`{photo['camera']['name']}`)")
            st.markdown(f"**🛰️ Rover:** {photo['rover']['name']}")
            st.markdown(f"**🚦 Status:** `{photo['rover']['status']}`")
            st.markdown(
                f'<a href="{photo["img_src"]}" target="_blank">'
                f'<button style="width:100%;background-color:maroon">🔍 View Fullscreen</button></a>',
                unsafe_allow_html=True
            )