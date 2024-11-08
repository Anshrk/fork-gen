# Import necessary libraries
import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
from PIL import Image, ImageEnhance
import tempfile
import os
import whisper
import subprocess
import re
import ffmpeg
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector

# Load a pre-trained Haar Cascade for detecting faces (used as a proxy for people detection)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Helper Functions
def extract_keywords(title, details):
    text = title + " " + details
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    words = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    return list(set(keywords))

def convert_video_to_audio(video_path, audio_path="audio.wav"):
    subprocess.run(['ffmpeg', '-i', video_path, '-ac', '1', '-ar', '16000', audio_path, '-y'])
    return audio_path

def transcribe_audio_with_whisper(audio_path, model_name="base"):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    return result

def extract_key_moments(transcription, keywords):
    key_moments = []
    keywords_lower = [kw.lower() for kw in keywords]
    for segment in transcription["segments"]:
        text = segment["text"].lower()
        if any(keyword in text for keyword in keywords_lower):
            key_moments.append(segment["start"])
    return key_moments

def extract_keyframes_scenedetect(video_path):
    video = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=30))
    scene_manager.detect_scenes(video)
    return [scene[0] for scene in scene_manager.get_scene_list()]

def get_frame_at_time(video_path, timestamp):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
    ret, frame = cap.read()
    if ret:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return None

def calculate_sharpness(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    return laplacian.var()

def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return len(faces)

def rank_keyframes(keyframes, video_path):
    ranked_keyframes = []
    for timestamp in keyframes:
        frame = get_frame_at_time(video_path, timestamp)
        if frame is not None:
            sharpness_score = calculate_sharpness(frame)
            people_count = detect_faces(frame)
            score = sharpness_score + (people_count * 10)
            ranked_keyframes.append((timestamp, score, frame, sharpness_score, people_count))
    ranked_keyframes.sort(key=lambda x: x[1], reverse=True)
    return ranked_keyframes[:5]

# Streamlit app
st.title("Video Keyframe Detection Tool")

# File uploader for video
uploaded_video = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi"])
keyframes = []
# Option to choose analysis type
analysis_type = st.selectbox("Choose Analysis Type", ["Emotion Detection-Based", "Subtitle Keywords-Based"])

if uploaded_video is not None:
    # Save video to temporary file
    video_path = "uploaded_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_video.getbuffer())

    if analysis_type == "Emotion Detection-Based":
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())
        cap = cv2.VideoCapture(tfile.name)
        frame_interval = 30
        frame_count = 0
        highest_emotion_frames = {emotion: {"score": 0, "timestamp": 0} for emotion in [
            "angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]}

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray_frame, 1.1, 5, minSize=(30, 30))
                if len(faces) > 0:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    try:
                        result = DeepFace.analyze(img_path=rgb_frame, actions=['emotion'], enforce_detection=False)
                        for emotion, score in result[0]["emotion"].items():
                            if score > highest_emotion_frames[emotion]["score"]:
                                highest_emotion_frames[emotion] = {"score": score, "timestamp": frame_count / cap.get(cv2.CAP_PROP_FPS)}
                    except Exception as e:
                        st.write("Error analyzing frame:", e)
            frame_count += 1
        cap.release()

        keyframes = [data["timestamp"] for data in highest_emotion_frames.values() if data["score"] > 0]
        st.write("Analyzing video for emotion-based keyframes...")

    elif analysis_type == "Subtitle Keywords-Based":
        title = st.text_input("Enter Video Title")
        details = st.text_area("Enter Video Details")
        if title and details:
            keywords = extract_keywords(title, details)
            audio_path = convert_video_to_audio(video_path)
            transcription = transcribe_audio_with_whisper(audio_path)
            keyframes = extract_key_moments(transcription, keywords)
            os.remove(audio_path)
            st.write("Extracted Keywords:", keywords)

    # Ranking and displaying keyframes
    if keyframes:
        ranked_keyframes = rank_keyframes(keyframes, video_path)
        st.write("Top 5 Ranked Keyframes:")
        for i, (timestamp, score, frame_image, sharpness_score, people_count) in enumerate(ranked_keyframes):
            st.image(frame_image, caption=f"Keyframe {i+1} - Time: {timestamp}s, Score: {score:.2f}, Sharpness: {sharpness_score:.2f}, Faces Detected: {people_count}")

    os.remove(video_path)
