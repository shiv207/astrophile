import streamlit as st
from googleapiclient.discovery import build

API_KEY = 'AIzaSyAVcloXaiimUXaUPAOJ6967K5p_Kafg2v0'
CHANNEL_IDS = {
    "Everyday Astronaut": "UC6uKrU_WqJ1R2HMTY3LIx5Q",
    "Scott Manley": "UCxzC4EngIsMrPmbm6Nxvb-A",
    "Matt Lowne": "UC4UeJHfJlRRJusn9GV5vqrg",
    "BPS.space": "UCeQw1Wczg3b1c-mhwxeGG2w",
    "NASA": "UCLA_DiR1FfKNvjuUpBHmylQ",
    "ISRO": "UCcU9yR_dVa1QbKO1l221pMQ",
    "ESA": "UCIBaDdAbGlFDeS33shmlD0A",
    "SpaceX": "UCtI0Hodo5o5dUb67FeUjDeA",
    "NASASpaceflight": "UCSUu1lih2RifWkKtDOJdsBA"
}

def get_latest_video(channel_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=1,
        order="date"
    )
    response = request.execute()
    if 'items' in response and response['items']:
        video_id = response['items'][0]['id']['videoId']
        video_title = response['items'][0]['snippet']['title']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_title, video_url, video_id
    else:
        return None, None, None

def display_latest_videos():
    st.header("Latest Videos from Space Nerds")
    
    # Apply custom CSS for rounded corners and edge blur
    st.markdown("""
    <style>
    .blurred-video iframe {
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.7);
    }
    </style>
    """, unsafe_allow_html=True)
    
    for channel_name, channel_id in CHANNEL_IDS.items():
        video_title, video_url, video_id = get_latest_video(channel_id)
        if video_title and video_url:
            st.markdown(f"### {channel_name}")
            st.markdown(f'<div class="blurred-video">{st.video(video_url)}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"**{channel_name}**: No recent videos found.")
        
