import streamlit as st
import subprocess
import os
from pathlib import Path
from PIL import Image

def extract_keyframes_ffmpeg(video_path, output_dir, threshold=0.3):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # FFmpeg command to extract key frames with scene detection
    ffmpeg_cmd = [
        'ffmpeg', 
        '-i', video_path,
        '-vf', f"select='gt(scene,{threshold})'",
        '-vsync', 'vfr',
        os.path.join(output_dir, 'keyframe_%04d.jpg')
    ]
    
    # Run the FFmpeg command
    subprocess.run(ffmpeg_cmd)
    keyframes = sorted(Path(output_dir).glob("keyframe_*.jpg"))
    return keyframes

# Streamlit UI
st.title("Keyframe Extraction App")

st.write("Upload a video, and this app will extract keyframes using FFmpeg's scene detection.")

# Upload video
video_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])

# Set a scene detection threshold
threshold = st.slider("Scene Change Threshold", min_value=0.1, max_value=1.0, value=0.3, step=0.1,
                      help="Lower values detect minor changes; higher values detect only major scene changes.")

if video_file:
    # Save the uploaded video to a temporary file
    temp_video_path = f"temp_{video_file.name}"
    with open(temp_video_path, "wb") as f:
        f.write(video_file.read())
    
    # Output directory for keyframes
    output_dir = "keyframes_output"
    
    # Extract keyframes
    st.write("Extracting keyframes...")
    keyframes = extract_keyframes_ffmpeg(temp_video_path, output_dir, threshold)
    
    # Display keyframes
    st.write("Extracted Keyframes:")
    if keyframes:
        for keyframe in keyframes:
            image = Image.open(keyframe)
            st.image(image, caption=f"{keyframe.name}", use_column_width=True)
    else:
        st.write("No keyframes detected. Try lowering the threshold.")
    
    # Cleanup temporary files
    if st.button("Clear Output"):
        for keyframe in keyframes:
            os.remove(keyframe)
        os.remove(temp_video_path)
        st.write("Temporary files cleared.")
