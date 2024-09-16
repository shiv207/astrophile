import streamlit as st

def display_night_sky_map():

    # Page title
    st.markdown("<h1 style='text-align: center; color: white;'>Night Sky Map ✨</h1>", unsafe_allow_html=True)

    # Location input
    st.sidebar.header("Location Settings")
    latitude = st.sidebar.number_input("Latitude", -90.0, 90.0, 37.7749, format="%.4f")
    longitude = st.sidebar.number_input("Longitude", -180.0, 180.0, -122.4194, format="%.4f")

    # Stellarium Web URL with parameters for location
    stellarium_url = f"https://stellarium-web.org/#view=sky&lat={latitude}&lng={longitude}&zoom=1"

    # Custom CSS for styling
    st.markdown("""
    <style>
        .css-18e3th9 {
            background-color: #0d0d0d;
        }
        .css-1f2v7z5 {
            background-color: #111111;
        }
        iframe {
            border: none;
        }
    </style>
    """, unsafe_allow_html=True)

    # Display the Stellarium Web map
    st.markdown(f'<iframe width="100%" height="800" src="{stellarium_url}" allowfullscreen></iframe>', unsafe_allow_html=True)
