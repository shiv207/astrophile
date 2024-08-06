import requests
import streamlit as st
import plotly.graph_objects as go

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-title {
        font-size: 8rem;  /* Increased font size for main title */
        color: #FFD700;
        text-align: center;
        margin-bottom: 20px;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.8); /* Glowing effect */
    }
    .tracking-text {
        font-size: 4rem;  /* Increased font size for tracking text */
        color: #00BFFF;
        text-align: center;
        margin-top: 10px;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        text-shadow: 0 0 12px rgba(0, 191, 255, 0.7); /* Glowing effect */
    }
    .section-title {
        font-size: 2.5rem;
        color: #00BFFF;
        text-align: center;
        margin-top: 20px;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        text-shadow: 0 0 8px rgba(0, 191, 255, 0.5); /* Glowing effect */
    }
    .info-box {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        color: #FFF;
        font-size: 1.5rem;
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

def fetch_iss_location():
    """Fetch the current location of the ISS."""
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['message'] == 'success':
            lat = float(data['iss_position']['latitude'])
            lon = float(data['iss_position']['longitude'])
            return lat, lon
    return None, None

def fetch_iss_info():
    """Fetch the number of astronauts and spacecrafts docked to the ISS."""
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        astronauts = [person for person in data['people'] if person['craft'] == 'ISS']
        num_astronauts = len(astronauts)
        spacecrafts = list(set([person['craft'] for person in data['people'] if person['craft'] != 'ISS']))
        return num_astronauts, spacecrafts
    return None, None

def display_iss_location():
    """Display the live location of the ISS on a Plotly map with Streamlit."""
    st.title("Live ISS Tracker 🛰️")
    st.write("Tracking the ISS in real-time...")

    fig = go.Figure(go.Scattergeo())
    fig.update_geos(
        visible=True,
        showcountries=False,
        showland=True,
        landcolor="lightgray",
        oceancolor="rgb(5, 15, 27)",
        showocean=True,
        showcoastlines=False,
        projection_type="orthographic",
        projection_rotation=dict(lon=0, lat=0, roll=0),
        lataxis_showgrid=False,
        lonaxis_showgrid=False,
        bgcolor="black",
    )

    lat, lon = fetch_iss_location()
    if lat is not None and lon is not None:
        fig.data = []  # Clear previous traces
        fig.add_trace(go.Scattergeo(
            lon=[lon],
            lat=[lat],
            mode='markers',
            marker=dict(size=10, color='rgb(0, 255, 255)', symbol='circle'),
            name='ISS'
        ))
        fig.update_layout(
            title=f"Current ISS Location: Latitude {lat:.2f}, Longitude {lon:.2f}",
            margin=dict(l=0, r=0, t=50, b=0),
            paper_bgcolor="rgba(0, 0, 0, 0.6)",
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='orthographic',
                bgcolor="rgba(20, 20, 20, 0.6)",
            )
        )
        st.plotly_chart(fig, use_container_width=True)

        num_astronauts, spacecrafts = fetch_iss_info()
        if num_astronauts is not None:
            st.markdown('<div class="section-title">👩‍🚀 Current Astronauts on the ISS</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-box">Number of astronauts: {num_astronauts}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">Could not retrieve ISS information.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">Could not retrieve ISS location.</div>', unsafe_allow_html=True)
