import streamlit as st
from anime import anime_page
from image_gen import image_gen_page
from object_detect import object_detect_page
from spanish_translator import spanish_translator_page
from speech_recog import speech_recog_page

# Define the main function
def main():
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        [
            "Home",
            "Anime",
            "Image Generation",
            "Object Detection",
            "Spanish Translator",
            "Speech Recognition"
        ]
    )

    # Adding custom CSS for styling
    st.markdown("""
        <style>
            .big-font {
                font-size: 3rem;
                color: #3498db;
                font-weight: bold;
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

    # Page routing logic
    if page == "Home":
        st.markdown('<h1 class="big-font">Welcome to the Home Page</h1>', unsafe_allow_html=True)

    elif page == "Anime":
        st.markdown('<h1 class="big-font">Anime Page</h1>', unsafe_allow_html=True)
        anime_page()

    elif page == "Image Generation":
        st.markdown('<h1 class="big-font">Image Generation Page</h1>', unsafe_allow_html=True)
        image_gen_page()

    elif page == "Object Detection":
        st.markdown('<h1 class="big-font">Object Detection Page</h1>', unsafe_allow_html=True)
        object_detect_page()

    elif page == "Spanish Translator":
        st.markdown('<h1 class="big-font">Spanish Translator Page</h1>', unsafe_allow_html=True)
        spanish_translator_page()

    elif page == "Speech Recognition":
        st.markdown('<h1 class="big-font">Speech Recognition Page</h1>', unsafe_allow_html=True)
        speech_recog_page()

# Entry point of the application
if __name__ == "__main__":
    main()
