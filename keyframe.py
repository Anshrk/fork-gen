# Install the Cloudinary Python SDK if you haven’t already
# pip install cloudinary
import streamlit as st

import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url



# Set up Cloudinary configuration
cloudinary.config(
    cloud_name="dj8np6ojh",
    api_key="254161625543897",
    api_secret="BTn-D8kOGuyWxhSZEKlQ406bDBw"
)

# Upload a video
response = cloudinary.uploader.upload("videos/zoo.mp4", resource_type="video")
video_public_id = response["public_id"]  # This will be used to access the video

# Generate a thumbnail at 5 seconds
thumbnail_url_5s, options = cloudinary_url(
    video_public_id,
    resource_type="video",
    format="jpg",
    start_offset="5"
)

# Display the generated thumbnail URL
print("Thumbnail at 5s:", thumbnail_url_5s)

# Generate a thumbnail from the first keyframe
thumbnail_url_keyframe, options = cloudinary_url(
    video_public_id,
    resource_type="video",
    format="jpg",
    flags="animated"  # Flags for automatic keyframes
)
# Generate a thumbnail every 10 seconds
thumbnail_url_interval, options = cloudinary_url(
    video_public_id,
    resource_type="video",
    format="jpg",
    start_offset="10s",
    duration="10s"
)

print("Thumbnail every 10 seconds:", thumbnail_url_interval)

print("Keyframe thumbnail:", thumbnail_url_keyframe)

st.image(thumbnail_url_5s, caption="Thumbnail at 5 seconds")
st.image(thumbnail_url_interval, caption="Thumbnail every 10 seconds")
st.image(thumbnail_url_keyframe, caption="Automatic Keyframe Thumbnail")

