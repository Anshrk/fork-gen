import streamlit as st
import whisper
import subprocess
import os
import re
import ffmpeg
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from PIL import Image
import cv2

# Function to extract keywords from title and details
def extract_keywords(title, details):
    text = title + " " + details
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    words = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    return list(set(keywords))

# Function to convert video to audio
def convert_video_to_audio(video_path, audio_path="audio.wav"):
    subprocess.run(['ffmpeg', '-i', video_path, '-ac', '1', '-ar', '16000', audio_path, '-y'])
    return audio_path

# Function to transcribe audio with Whisper
def transcribe_audio_with_whisper(audio_path, model_name="base"):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    return result

# Function to extract key moments based on keywords
def extract_key_moments(transcription, keywords):
    key_moments = []
    keywords_lower = [kw.lower() for kw in keywords]
    
    for segment in transcription["segments"]:
        text = segment["text"].lower()
        if any(keyword in text for keyword in keywords_lower):
            key_moments.append({
                "start_time": segment["start"],
                "end_time": segment["end"],
                "text": segment["text"]
            })
    
    return key_moments

# Function to generate and save keyframes from video at specified timestamps
def generate_keyframes(video_path, timestamps, output_folder="keyframes"):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    keyframes = []
    cap = cv2.VideoCapture(video_path)
    
    for i, timestamp in enumerate(timestamps):
        # Set the video position to the specified timestamp
        cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
        success, frame = cap.read()
        
        if success:
            # Save the frame as an image
            frame_path = os.path.join(output_folder, f"keyframe_{i}.jpg")
            cv2.imwrite(frame_path, frame)
            keyframes.append(frame_path)
        else:
            st.write(f"Could not extract frame at {timestamp}s")

    cap.release()
    return keyframes

# Streamlit UI
st.title("Keyframe Extraction from Video Using Important Keywords")

# Upload video file
uploaded_video = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi"])

# Input title and details
title = st.text_input("Enter Video Title")
details = st.text_area("Enter Details (e.g., topics or key points)")

if st.button("Generate Keyframes"):
    if uploaded_video and title and details:
        # Save uploaded video
        video_path = "uploaded_video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_video.read())
        
        # Step 1: Extract Keywords
        keywords = extract_keywords(title, details)
        st.write("Extracted Keywords:", keywords)

        # Step 2: Convert video to audio
        audio_path = convert_video_to_audio(video_path)

        # Step 3: Transcribe audio using Whisper
        transcription = transcribe_audio_with_whisper(audio_path)

        # Step 4: Extract key moments based on keywords
        key_moments = extract_key_moments(transcription, keywords)
        
        # Display key moments and timestamps
        if key_moments:
            st.write("Key Moments Found:")
            timestamps = []
            for moment in key_moments:
                st.write(f"{moment['text']} - Start: {moment['start_time']}s, End: {moment['end_time']}s")
                timestamps.append(moment['start_time'])

            # Step 5: Generate keyframes from timestamps
            keyframes = generate_keyframes(video_path, timestamps)
            
            # Display keyframes
            st.write("Generated Keyframes:")
            for frame_path in keyframes:
                st.image(Image.open(frame_path), caption=frame_path)
        else:
            st.write("No key moments found based on the provided keywords.")
            keyframes = []  # Initialize keyframes as an empty list if no key moments are found
        
        # Cleanup
        os.remove(video_path)
        os.remove(audio_path)
        if keyframes:  # Only attempt to delete keyframes if they were created
            for frame_path in keyframes:
                os.remove(frame_path)
            os.rmdir("keyframes")
    else:
        st.write("Please upload a video, and enter both title and details.")
