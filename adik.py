import cv2
from pytube import YouTube
import speech_recognition as sr
from transformers import pipeline
from PIL import Image, ImageDraw, ImageFont
import tempfile
import os

# Function to download YouTube video and return the video path
def download_youtube_video(url):
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension="mp4", res="360p").first()
    video_path = stream.download(filename="temp_video.mp4")
    return video_path

# Function to extract audio and perform speech-to-text
def get_video_transcript(video_path):
    recognizer = sr.Recognizer()
    temp_audio_path = "temp_audio.wav"

    # Extract audio from video
    os.system(f"ffmpeg -i {video_path} -ab 160k -ac 2 -ar 44100 -vn {temp_audio_path}")
    
    # Convert audio to text
    with sr.AudioFile(temp_audio_path) as source:
        audio_data = recognizer.record(source)
        transcript = recognizer.recognize_google(audio_data)
    
    os.remove(temp_audio_path)
    return transcript

# Function to extract frames and match to transcript
def find_best_frame(video_path, transcript, title):
    # Initialize OpenCV to capture frames from the video
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Initialize NLP model for semantic similarity
    similarity_model = pipeline("zero-shot-classification")

    best_frame = None
    highest_score = 0

    # Loop through frames at intervals (e.g., every 5 seconds)
    for i in range(0, frame_count, fps * 5):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            break

        # Check if this part of the transcript matches the title best
        segment = transcript[i:i+300]  # Use a segment of the transcript for matching
        result = similarity_model(segment, candidate_labels=[title])
        score = result["scores"][0]

        # Keep track of the best-matching frame
        if score > highest_score:
            highest_score = score
            best_frame = frame

    cap.release()
    return best_frame

# Function to save the thumbnail with title overlay as JPEG
def save_thumbnail_with_text(frame, title, output_path="thumbnail.jpg"):
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 40)
    
    # Position the text
    text_width, text_height = draw.textsize(title, font=font)
    width, height = image.size
    text_position = ((width - text_width) // 2, height - text_height - 20)
    
    # Draw text on image
    draw.text(text_position, title, font=font, fill="yellow")
    
    # Convert image to RGB and save as JPEG
    rgb_image = image.convert("RGB")
    rgb_image.save(output_path, "JPEG")
    print(f"Thumbnail saved as {output_path}")

# Main function to put it all together
def generate_youtube_thumbnail(video_url, title):
    video_path = download_youtube_video(video_url)
    transcript = get_video_transcript(video_path)
    best_frame = find_best_frame(video_path, transcript, title)
    
    if best_frame is not None:
        save_thumbnail_with_text(best_frame, title)
    else:
        print("No suitable frame found.")
    
    os.remove(video_path)  # Cleanup downloaded video

# Example usage
video_url = "https://www.youtube.com/watch?v=aw-XYrMFb0A"
title = "How Mozilla lost the Internet (& what's next)"
generate_youtube_thumbnail(video_url, title)
