# Import necessary libraries
import streamlit as st
from deepface import DeepFace
from PIL import Image
import numpy as np
import cv2
import tempfile

# Streamlit app title
st.title("Emotion Detection in Video using DeepFace")

# Load OpenCV's pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Video upload widget
uploaded_video = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi", "mkv"])

# Run emotion analysis if a video is uploaded
if uploaded_video is not None:
    # Save uploaded video to a temporary file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_video.read())

    # Load the video
    cap = cv2.VideoCapture(tfile.name)

    # Initialize a dictionary to store the highest emotion scores and their frames
    highest_emotion_frames = {
        "angry": {"score": 0, "frame": None},
        "disgust": {"score": 0, "frame": None},
        "fear": {"score": 0, "frame": None},
        "happy": {"score": 0, "frame": None},
        "sad": {"score": 0, "frame": None},
        "surprise": {"score": 0, "frame": None},
        "neutral": {"score": 0, "frame": None}
    }

    # Process frames at intervals (e.g., every 30 frames)
    frame_interval = 30
    frame_count = 0

    st.write("Analyzing video frames...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process every nth frame based on frame_interval
        if frame_count % frame_interval == 0:
            # Convert frame to grayscale for face detection
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            # Proceed only if a face is detected
            if len(faces) > 0:
                # Convert frame to RGB for emotion analysis
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Perform emotion detection
                try:
                    result = DeepFace.analyze(img_path=rgb_frame, actions=['emotion'], enforce_detection=False)
                    emotions = result[0]["emotion"]

                    # Check each emotion's score and update highest score and frame if needed
                    for emotion, score in emotions.items():
                        if score > highest_emotion_frames[emotion]["score"]:
                            highest_emotion_frames[emotion]["score"] = score
                            highest_emotion_frames[emotion]["frame"] = rgb_frame

                except Exception as e:
                    st.write("Error analyzing frame:", e)

        frame_count += 1

    cap.release()

    # Display frames with the highest score for each emotion
    st.write("Frames with the highest score for each emotion:")
    for emotion, data in highest_emotion_frames.items():
        if data["frame"] is not None:
            st.write(f"**{emotion.capitalize()}** - Score: {data['score']:.2f}")
            st.image(data["frame"], caption=f"{emotion.capitalize()} Frame", use_column_width=True)
