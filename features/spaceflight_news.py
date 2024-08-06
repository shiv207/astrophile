import streamlit as st
import requests
from datetime import datetime

# Spaceflight News API URL (v4)
SPACEFLIGHT_NEWS_URL = "https://api.spaceflightnewsapi.net/v4/articles"

# Fetch latest space news
def fetch_space_news():
    try:
        response = requests.get(SPACEFLIGHT_NEWS_URL)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        news_data = response.json()
        return news_data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching space news: {e}")
        return []

def display_spaceflight_news():
    st.title("Latest Spaceflight News")
    news_data = fetch_space_news()

    if news_data:
        for article in news_data["results"]:
            title = article.get("title", "No Title")
            summary = article.get("summary", "No summary available.")
            url = article.get("url", "#")
            image_url = article.get("image_url", "")
            published_at = article.get("published_at", "")
            
            if published_at:
                try:
                    published_at = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    published_at = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')
            
            st.subheader(title)
            st.write(f"**Published on:** {published_at}")
            st.write(summary)
            if image_url:
                st.image(image_url, width=300, caption=title)
            st.markdown(f"[Read more]({url})", unsafe_allow_html=True)
    else:
        st.write("Space news data could not be loaded.")