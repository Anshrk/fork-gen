
import streamlit as st
import cv2
import os
from PIL import Image
from io import BytesIO

# Function to capture frames at specific timestamps
def capture_frame(video_path, timestamp, output_folder="thumbnails"):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Capture frame at specified timestamp
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
    success, frame = cap.read()
    
    if success:
        # Save frame as an image file
        frame_path = os.path.join(output_folder, f"thumbnail_{int(timestamp)}s.jpg")
        cv2.imwrite(frame_path, frame)
        return frame_path
    else:
        return None

# Streamlit UI
st.title("Custom Thumbnail Generator from Video")

# Video file upload
uploaded_video = st.file_uploader("Upload a Video", type=["mp4", "avi", "mov"])
if uploaded_video:
    # Save uploaded video to disk
    video_path = "uploaded_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_video.read())

    # Display the video in the Streamlit app
    st.video(video_path)

    # Input for custom timestamps
    timestamps_input = st.text_input("Enter timestamps in seconds (comma-separated, e.g., 5, 10, 20):")
    
    # Generate thumbnails button
    if st.button("Generate Thumbnails"):
        if timestamps_input:
            timestamps = [float(ts.strip()) for ts in timestamps_input.split(",")]
            st.write("Selected Timestamps:", timestamps)
            
            # Generate thumbnails
            st.write("Generated Thumbnails:")
            for timestamp in timestamps:
                frame_path = capture_frame(video_path, timestamp)
                
                if frame_path:
                    # Display the thumbnail
                    image = Image.open(frame_path)
                    st.image(image, caption=f"Thumbnail at {timestamp}s")
                else:
                    st.write(f"Could not capture frame at {timestamp}s")
        else:
            st.write("Please enter at least one timestamp.")
