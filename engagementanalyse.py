import os
import cv2
import numpy as np
import requests
import streamlit as st
from pytube import YouTube
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image

# Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Function to get video statistics
def get_video_data(video_url):
    # Extract video ID
    video_id = video_url.split("v=")[-1].split("&")[0]
    api_url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id={video_id}&key={YOUTUBE_API_KEY}'
    response = requests.get(api_url)
    data = response.json()
    
    if 'items' in data and len(data['items']) > 0:
        video_info = data['items'][0]
        snippet = video_info['snippet']
        statistics = video_info['statistics']
        
        return {
            "title": snippet.get('title', 'N/A'),
            "description": snippet.get('description', 'N/A'),
            "channelTitle": snippet.get('channelTitle', 'N/A'),
            "publishedAt": snippet.get('publishedAt', 'N/A'),
            "viewCount": statistics.get('viewCount', 'N/A'),
            "likeCount": statistics.get('likeCount', 'N/A'),
            "dislikeCount": statistics.get('dislikeCount', 'N/A'),
            "commentCount": statistics.get('commentCount', 'N/A')
        }
    else:
        return None

# Function to extract frames for thumbnails
def extract_thumbnails(video_url, timestamps):
    video = YouTube(video_url)
    stream = video.streams.filter(file_extension="mp4").first()
    video_path = stream.download(filename="temp_video.mp4")
    
    cap = cv2.VideoCapture(video_path)
    thumbnails = []

    for timestamp in timestamps:
        cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)  # Set timestamp in milliseconds
        success, frame = cap.read()
        
        if success:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            thumbnails.append(image)
    
    cap.release()
    os.remove(video_path)  # Clean up downloaded video
    return thumbnails

# Streamlit App
st.title("YouTube Video Analysis and Thumbnail Generator")

video_url = st.text_input("Enter YouTube Video URL")

if video_url:
    # Fetch video data
    video_data = get_video_data(video_url)
    
    if video_data:
        # Display engagement metrics
        st.subheader("Engagement Metrics")
        st.write(f"**Title:** {video_data['title']}")
        st.write(f"**Channel:** {video_data['channelTitle']}")
        st.write(f"**Views:** {video_data['viewCount']}")
        st.write(f"**Likes:** {video_data['likeCount']}")
        st.write(f"**Dislikes:** {video_data['dislikeCount']}")
        st.write(f"**Comments:** {video_data['commentCount']}")
        
        # Generate potential thumbnails
        st.subheader("Generated Thumbnails")
        timestamps = [10, 30, 60, 120]  # Sample timestamps in seconds for thumbnails
        thumbnails = extract_thumbnails(video_url, timestamps)
        
        for idx, thumbnail in enumerate(thumbnails):
            st.image(thumbnail, caption=f"Thumbnail {idx+1}")
            buffer = BytesIO()
            thumbnail.save(buffer, format="JPEG")
            st.download_button(
                label=f"Download Thumbnail {idx+1}",
                data=buffer.getvalue(),
                file_name=f"thumbnail_{idx+1}.jpg",
                mime="image/jpeg"
            )
    else:
        st.error("Could not retrieve video data. Please check the URL or try again.")
