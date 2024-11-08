import streamlit as st
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from PIL import Image, ImageDraw, ImageFont
import random
import requests
from io import BytesIO

# DALL-E or similar image generation function (mocked here for example)
def generate_image_from_keywords(keywords):
    # Example: send a request to an image generation API with keywords
    prompt = " ".join(keywords)
    
    # Mockup for DALL-E style image generation
    # Replace with actual API calls as needed
    url = f"https://dummyimage.com/600x400/000/fff.png&text={'+'.join(keywords)}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        return None

# Extract keywords from title and description
def extract_keywords(title, description):
    text = title + " " + description
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    words = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    return list(set(keywords))

# Overlay title text on image
def add_text_to_image(image, text, output_path="thumbnail.jpg"):
    draw = ImageDraw.Draw(image)
    font_size = int(image.width * 0.1)
    
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
        
    # Text position and color
    text_position = (10, 10)
    text_color = "white"

    # Draw text with shadow for better contrast
    shadow_offset = (2, 2)
    shadow_color = "black"
    
    # Shadow text
    draw.text((text_position[0] + shadow_offset[0], text_position[1] + shadow_offset[1]), text, font=font, fill=shadow_color)
    # Main text
    draw.text(text_position, text, font=font, fill=text_color)
    
    image.save(output_path)
    return image

# Streamlit UI for video thumbnail generation
st.title("Random Thumbnail Generator for Video")

title = st.text_input("Enter Video Title")
description = st.text_area("Enter Video Description")

if st.button("Generate Thumbnail"):
    if title and description:
        # Step 1: Extract Keywords
        keywords = extract_keywords(title, description)
        st.write("Extracted Keywords:", keywords)
        
        # Step 2: Generate Image based on Keywords
        image = generate_image_from_keywords(keywords)
        
        if image:
            # Step 3: Overlay Title on Thumbnail
            thumbnail = add_text_to_image(image, title)
            st.image(thumbnail, caption="Generated Thumbnail", use_column_width=True)
        else:
            st.write("Error: Could not generate thumbnail image.")
    else:
        st.write("Please enter both title and description.")
