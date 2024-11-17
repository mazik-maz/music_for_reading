import streamlit as st
from PIL import Image
import requests
from get_features_from_text import get_features_from_text
from closest_track import find_closest_track
from chunking import split_text_by_context
from extract_text import (
    # extract_text_from_pdf,
    # extract_text_from_epub,
    # extract_text_from_fb2,
    extract_text_from_txt,
)
import json

# Load track database
with open("data.json", "r") as file:
    track_database = json.load(file)

@st.cache_data
def search_deezer(track_name):
    try:
        query = track_name.replace(' ', '+')
        url = f"https://api.deezer.com/search?q={query}&limit=5"
        response = requests.get(url)
        data = response.json()

        for track_info in data.get('data', []):
            preview_url = track_info['preview']
            if preview_url:
                track_title = track_info['title']
                artist_name = track_info['artist']['name']
                album_cover = track_info['album']['cover_medium']
                full_track_name = f"{artist_name} - {track_title}"
                return preview_url, full_track_name, album_cover
        return None, None, None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, None, None

def main():
    st.title("Text to Music Matcher")

    uploaded_file = st.file_uploader("Upload a text file", type=["pdf", "txt", "epub", "fb2"])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension == 'txt':
            text = extract_text_from_txt(uploaded_file)
        # elif file_extension == 'pdf':
        #     text = extract_text_from_pdf(uploaded_file)
        # elif file_extension == 'epub':
        #     text = extract_text_from_epub(uploaded_file)
        # elif file_extension == 'fb2':
        #     text = extract_text_from_fb2(uploaded_file)
        else:
            st.error("Unsupported file type.")
            return

        # Display the extracted text (optional)
        st.subheader("Extracted Text")
        st.write(text)

        # Process the text
        sections = split_text_by_context(text)
        section_features = [get_features_from_text(section) for section in sections]
        tracks = [find_closest_track(features, track_database) for features in section_features]

        # Display results
        for i, track in enumerate(tracks):
            st.subheader(f"Section {i+1}")
            st.write(sections[i])

            st.write(f"Matched Track: {track['name']}")

            preview_url, full_track_name, album_cover = search_deezer(track['name'])
            if preview_url:
                st.write(f"Playing Preview: {full_track_name}")
                st.image(album_cover, width=300)
                st.audio(preview_url)
            else:
                st.write("No preview available for this track.")

if __name__ == "__main__":
    main()
