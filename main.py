from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json

from chunking import split_text_by_context
from get_features_from_text import get_features_from_text
from closest_track import find_closest_track

# Load the track database
with open("data.json", "r") as file:
    track_database = json.load(file)

# Initialize FastAPI
app = FastAPI()

class TextInput(BaseModel):
    text: str
    similarity_threshold: float = 0.5
    max_sentences_per_section: int = 5
    min_sentences_per_section: int = 2

@app.post("/split-text/")
def split_text(input_data: TextInput):
    """
    Split text into chunks based on context.
    """
    try:
        sections = split_text_by_context(
            text=input_data.text,
            similarity_threshold=input_data.similarity_threshold,
            max_sentences_per_section=input_data.max_sentences_per_section,
            min_sentences_per_section=input_data.min_sentences_per_section
        )
        return {"sections": sections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get-features/")
def get_features(input_data: TextInput):
    """
    Get features for a given text chunk.
    """
    try:
        features = get_features_from_text(input_data.text)
        return {"features": {"tempo": features[0], "energy": features[1], "valence": features[2]}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class FeatureInput(BaseModel):
    tempo: float
    energy: float
    valence: float

@app.post("/find-closest-track/")
def find_track(features: FeatureInput):
    """
    Find the closest track based on features.
    """
    try:
        closest_track = find_closest_track(
            target_features=(features.tempo, features.energy, features.valence),
            track_database=track_database
        )
        return {"closest_track": closest_track}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-text/")
def process_text(input_data: TextInput):
    """
    Complete pipeline: split text -> extract features -> find closest track.
    """
    try:
        sections = split_text_by_context(
            text=input_data.text,
            similarity_threshold=input_data.similarity_threshold,
            max_sentences_per_section=input_data.max_sentences_per_section,
            min_sentences_per_section=input_data.min_sentences_per_section
        )
        section_features = [get_features_from_text(section) for section in sections]
        tracks = [find_closest_track(features, track_database) for features in section_features]
        return {"sections": sections, "tracks": tracks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
