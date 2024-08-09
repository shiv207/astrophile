import requests
import os
from dotenv import load_dotenv
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
import time
import numpy as np
from PIL import Image
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Get NASA API key from environment variables
NASA_API_KEY = os.getenv("NASA_API_KEY")

# API URLs
PERSEVERANCE_PHOTOS_URL = f"https://api.nasa.gov/mars-photos/api/v1/rovers/perseverance/photos?sol=1000&api_key={NASA_API_KEY}"
CURIOSITY_PHOTOS_URL = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={NASA_API_KEY}"

# Placeholder coordinates for rovers (replace with actual data if available)
ROVER_LOCATIONS = {
    'Perseverance': {'lat': 6.0913, 'lon': 77.0589},  # Example coordinates
    'Curiosity': {'lat': -4.5895, 'lon': 137.4417}  # Example coordinates
}

# Local Mars map image path
MARS_MAP_IMAGE_PATH = 'Images/mars_map.jpg'  # Ensure this file exists

# Wikipedia-style information for the rovers
ROVER_INFO = {
    'Perseverance': (
        "Perseverance is a car-sized rover designed to explore the surface of Mars. "
        "It was launched by NASA on July 30, 2020, and landed on Mars on February 18, 2021. "
        "Its mission is to search for signs of ancient life and collect Martian soil and rock samples."
    ),
    'Curiosity': (
        "Curiosity is a car-sized rover designed to explore the surface of Mars. "
        "It was launched by NASA on November 26, 2011, and landed on Mars on August 6, 2012. "
        "Its mission is to investigate the Martian climate and geology and assess whether the Red Planet has ever offered environmental conditions favorable for microbial life."
    )
}

def fetch_data(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(2)  # Wait before retrying
            else:
                st.error(f"Error fetching data: {e}")
                st.write(f"Debug info: {e}")  # Provide additional debug information
                return None

def display_rover_image():
    image_url = "https://upload.wikimedia.org/wikipedia/commons/a/a4/Perseverance-Selfie-at-Rochette-Horizontal-V2.gif"  # Example direct image URL

    # Fetch the image
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        # Check if the content type is an image
        if 'image' in response.headers['Content-Type']:
            image = Image.open(BytesIO(response.content))
            st.image(image, caption="Perseverance Rover", use_column_width=True)
        else:
            st.error(f"URL did not return an image. Content-Type: {response.headers['Content-Type']}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching image: {e}")

    except UnidentifiedImageError:
        st.error("The image could not be identified or is not a valid image format.")

def display_curious_image():
    curious_url = "https://upload.wikimedia.org/wikipedia/commons/f/f3/Curiosity_Self-Portrait_at_%27Big_Sky%27_Drilling_Site.jpg"  # Updated example URL

    # Fetch the image
    try:
        response = requests.get(curious_url)
        response.raise_for_status()
        
        # Verify content type to ensure it's an image
        if 'image' in response.headers['Content-Type']:
            image = Image.open(BytesIO(response.content))
            st.image(image, caption="Curiosity Rover", use_column_width=True)
        else:
            st.error(f"URL did not return an image. Content-Type: {response.headers['Content-Type']}")
            
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching image: {e}")

def fetch_image(image_path):
    try:
        img = Image.open(image_path)
        return img
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

def display_photos(url, title):
    data = fetch_data(url)
    if data:
        photos = data.get("photos", [])
        if photos:
            st.write(f"### {title} Photos")
            for photo in photos[:5]:  # Show only the first 5 photos for brevity
                img_url = photo.get("img_src", "")
                earth_date = photo.get("earth_date", "Unknown Date")
                camera_name = photo.get("camera", {}).get("full_name", "Unknown Camera")

                st.image(img_url, caption=f"{camera_name} - {earth_date}", use_column_width=True)
        else:
            st.write("No photos available.")
    else:
        st.write(f"Unable to fetch {title} photos.")

def display_rover_map():
    st.write("# Mars Rover Locations")

    # Load Mars map image
    img = fetch_image(MARS_MAP_IMAGE_PATH)
    if img:
        fig, ax = plt.subplots(figsize=(10, 8))

        # Display Mars map
        ax.imshow(img, extent=[-180, 180, -90, 90])  # Adjust extent to match image coordinates

        # Create a DataFrame with rover locations
        rover_data = pd.DataFrame(ROVER_LOCATIONS).T
        rover_data.reset_index(inplace=True)
        rover_data.columns = ['Rover', 'Latitude', 'Longitude']

        # Convert rover coordinates to image coordinates
        for index, row in rover_data.iterrows():
            lon, lat = row['Longitude'], row['Latitude']
            ax.plot(lon, lat, 'o', markersize=10, label=row['Rover'])

        # Add labels and legend
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title('Rover Locations on Mars')
        ax.legend()
        plt.gca().invert_yaxis()  # Invert y-axis to match image coordinates

        # Show plot in Streamlit
        st.pyplot(fig)
    else:
        st.write("Unable to fetch Mars map image.")

def display_rover_info(rover_name):
    st.write(f"### {rover_name} Rover Information")
    info = ROVER_INFO.get(rover_name, "No information available.")
    st.write(info)

def display_perseverance_data():
    st.write("# Perseverance Rover Data")
    display_photos(PERSEVERANCE_PHOTOS_URL, "Perseverance Rover")
    st.write("---")
    display_rover_map()

    if st.button("More about Perseverance Rover", key="perseverance_info"):
        display_rover_image()
        display_rover_info("Perseverance")
        

def display_curiosity_data():
    st.write("# Curiosity Rover Data")
    display_photos(CURIOSITY_PHOTOS_URL, "Curiosity Rover")
    st.write("---")
    display_rover_map()

    if st.button("More about Curiosity Rover", key="curiosity_info"):
        display_curious_image()
        display_rover_info("Curiosity")
