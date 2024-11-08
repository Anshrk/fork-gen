# Import necessary libraries
import streamlit as st
from deepface import DeepFace
from PIL import Image
import numpy as np

# Streamlit app title
st.title("Emotion Detection using DeepFace")

# Image upload widget
uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

# Run emotion analysis if an image is uploaded
if uploaded_image is not None:
    # Load the image
    image = Image.open(uploaded_image)
    
    # Display the uploaded image
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert image to OpenCV format
    image = image.convert("RGB")
    image = np.array(image)

    # Perform emotion detection
    try:
        result = DeepFace.analyze(img_path=image, actions=['emotion'])
        
        # Extract the emotion with the highest score
        emotions = result[0]["emotion"]
        dominant_emotion = max(emotions, key=emotions.get)
        
        # Display dominant emotion
        st.write(f"The dominant emotion is: **{dominant_emotion}**")
        
        # Display all emotion scores (optional)
        st.write("Emotion scores:", emotions)
        
    except Exception as e:
        st.write("Error:", e)