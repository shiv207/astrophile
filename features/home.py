import streamlit as st

def display_home():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="welcome-section">
            <h1>Welcome to Astrophyile!</h1>
            <p>
                <strong>Astrophyile</strong> is your go-to source for space-related content. 
                Discover fascinating facts about the universe, explore spaceflight news, 
                and immerse yourself in the beauty of our cosmos through stunning visuals.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)