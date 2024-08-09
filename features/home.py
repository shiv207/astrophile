import streamlit as st

def display_home():
    # Adding responsive CSS with media queries
    st.markdown(
        """
        <style>
        .main-content {
            width: 100%;
            padding: 10px;
            box-sizing: border-box;
        }
        
        .welcome-section h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }

        .welcome-section p {
            font-size: 1.2em;
        }

        /* Media query for screens smaller than 768px (smartphone screens) */
        @media only screen and (max-width: 768px) {
            .welcome-section h1 {
                font-size: 1.5em;
                text-align: center;
            }

            .welcome-section p {
                font-size: 1em;
                text-align: center;
            }

            .main-content {
                padding: 5px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
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
