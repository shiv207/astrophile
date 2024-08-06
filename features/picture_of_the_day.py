import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get NASA API key from environment variables
NASA_API_KEY = os.getenv("NASA_API_KEY")
NASA_APOD_URL = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"

# Fetch NASA's Astronomy Picture of the Day (APOD)
def fetch_nasa_apod():
    try:
        response = requests.get(NASA_APOD_URL)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching NASA APOD: {e}")
        return None

def display_picture_of_the_day():
    nasa_data = fetch_nasa_apod()

    if nasa_data:
        url = nasa_data.get("url", "")
        title = nasa_data.get("title", "No Title")
        date = nasa_data.get("date", "Unknown Date")
        explanation = nasa_data.get("explanation", "No explanation available.")

        if url:
            # Set APOD image as the background
            st.markdown(f"""
            <style>
            [data-testid="stAppViewContainer"] > .main {{
                background-image: url("{url}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                min-height: 100vh;
            }}
            [data-testid="stAppViewContainer"]::before {{
              content: "";
              position: absolute;
              top: 0;
              left: 0;
              width: 100%;
              height: 100%;
              background: rgba(0, 0, 0, 0.6); /* Dark overlay for readability */
              backdrop-filter: blur(5px); /* Blur effect */
              z-index: -1;
            }}
            .headline {{
                text-align: center;
                font-size: 3rem;
                text-shadow: 0 0 5px #0ff, 0 0 10px #0ff, 0 0 15px #0ff, 0 0 20px #0ff, 0 0 25px #0ff;
                font-weight: bold;
                color: #ffffff;
                text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.8);
                margin-top: 20px;
            }}
            .info-section {{
                font-size: 1.5rem;
                line-height: 1.7;
                color: #ffffff;
                text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.8);
                margin-bottom: 50px;
                padding: 0 20px;
                text-align: center;
                position: absolute;
                bottom: -650px;
                width: 100%;
            }}
            </style>
            """, unsafe_allow_html=True)

            # Display headline and picture title at the top
            st.markdown(f'<div class="headline">{title}</div>', unsafe_allow_html=True)

            # Display additional information at the bottom
            st.markdown(f"""
            <div class="info-section">
                <p><strong>Date:</strong> {date}</p>
                <p><strong>Explanation:</strong> {explanation}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("NASA APOD data could not be loaded.")
