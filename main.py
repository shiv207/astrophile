# main.py
import streamlit as st
import os
import base64
import requests
from features import home, spaceflight_news, picture_of_the_day, next_launch, iss_location, percy_data, night_sky_map

# Set up the Streamlit page configuration
st.set_page_config(page_title="Astrophile", layout="wide", page_icon="🌌")

# CSS for background images and styling
def get_img_as_base64(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    else:
        return base64.b64encode(requests.get("https://via.placeholder.com/600x400").content).decode()

bg_img = get_img_as_base64("Images/stars.jpg")
sidebar_img = get_img_as_base64("Images/Angular_gradient.png")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/png;base64,{bg_img}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
[data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/png;base64,{sidebar_img}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(5px);
    z-index: -1;
}}
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
    right: 2rem;
}}
.sidebar-title {{
    display: flex;
    align-items: center;
    font-size: 1.5rem;
    color: white;
}}
.sidebar-title i {{
    margin-right: 10px;
    font-size: 1.5rem;
    color: white;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Load Font Awesome CSS
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
""", unsafe_allow_html=True)

# Inline critical CSS
st.markdown("""
<style>
    body {{ font-family: 'Poppins', sans-serif; }}
    .main {{ background-color: #111; color: #ddd; }}
</style>
""", unsafe_allow_html=True)

# Function to load and cache CSS
@st.cache_data
def load_css(file_name):
    with open(file_name) as f:
        return f.read()

css_version = int(os.path.getmtime("style.css"))
css_content = load_css("style.css")
st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown('<div class="sidebar-title"><i class="fa-solid fa-compass"></i> Navigation</div>', unsafe_allow_html=True)

# Define a session state variable to manage page selection
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

def set_page(page):
    st.session_state.page = page

# Create sidebar buttons to switch between pages
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.button('Home', on_click=set_page, args=('Home',))
st.sidebar.button('Spaceflight News', on_click=set_page, args=('Spaceflight News',))
st.sidebar.button('Picture of the Day', on_click=set_page, args=('Picture of the Day',))
st.sidebar.button('Latest Launch', on_click=set_page, args=('Latest Launch',))
st.sidebar.button('ISS Location', on_click=set_page, args=('ISS Location',))
st.sidebar.button('Perseverance Rover', on_click=set_page, args=('Perseverance Rover',))
st.sidebar.button('Curiosity Data', on_click=set_page, args=('Curiosity Data',))
st.sidebar.button('Night sky', on_click=set_page, args=('Night sky',))
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Main page logic
def main():
    if st.session_state.page == 'Home':
        home.display_home()
    elif st.session_state.page == 'Spaceflight News':
        spaceflight_news.display_spaceflight_news()
    elif st.session_state.page == 'Picture of the Day':
        picture_of_the_day.display_picture_of_the_day()
    elif st.session_state.page == 'Latest Launch':
        next_launch.display_launch_schedule()
    elif st.session_state.page == 'ISS Location':
        iss_location.display_iss_location()
    elif st.session_state.page == 'Perseverance Rover':
        percy_data.display_perseverance_data()
    elif st.session_state.page == 'Curiosity Data':
        percy_data.display_curiosity_data()
    elif st.session_state.page == 'Night sky':
        night_sky_map.display_night_sky_map()

if __name__ == "__main__":
    main()
