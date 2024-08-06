import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_launch_data(count=1):
    url = 'https://spaceflightnow.com/launch-schedule/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return parse_launch_data(response.text, count)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return []

def parse_launch_data(data, count):
    soup = BeautifulSoup(data, 'html.parser')
    launch_data = []

    missions = soup.select('.datename .mission')
    dates = soup.select('.datename .launchdate')
    mission_data_elements = soup.select('.missiondata')
    descriptions = soup.select('.missdescrip')

    for i in range(min(count, len(missions))):
        mission = missions[i].text
        date = dates[i].text
        missiondata = mission_data_elements[i].text.split('\n')

        if len(missiondata) < 2:
            break

        launchtime = missiondata[0][13:]
        launchsite = missiondata[1][13:]
        description = descriptions[i].text[:-9]

        launch_data.append({
            "mission": mission,
            "date": date,
            "launchtime": launchtime,
            "launchsite": launchsite,
            "description": description
        })

    return launch_data

def display_launch_schedule():
    launches = get_launch_data(count=60)
    if launches:
        for launch in launches:
            st.markdown(f"### <span style='color: #FFEB3B; text-shadow: 0px 0px 5px #FFEB3B;'>{launch['mission']}</span>", unsafe_allow_html=True)
            st.markdown(f"**Date:** {launch['date']}")
            st.markdown(f"**Launch Time:** {launch['launchtime']}")
            st.markdown(f"**Launch Site:** {launch['launchsite']}")
            st.markdown(f"**Description:** {launch['description']}")
            st.markdown("---")
    else:
        st.error("No launch data available.")

# Add custom CSS styling from a file
with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)