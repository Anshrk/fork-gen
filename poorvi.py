import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# Function to add text overlay to an image
def add_text_overlay(image, text, position=(50, 50), font_size=36, color=(255, 255, 255)):
    draw = ImageDraw.Draw(image)
    # Load a default font (or specify a path to a .ttf font file)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Add text to the image
    draw.text(position, text, font=font, fill=color)
    return image

# Function to add a logo overlay to an image
def add_logo_overlay(image, logo_url, position="bottom-right", logo_size=(100, 100)):
    # Fetch the logo image from the URL
    response = requests.get(logo_url)
    logo = Image.open(BytesIO(response.content))

    # Resize logo to desired size
    logo = logo.resize(logo_size)

    # Determine position for the logo
    if position == "top-left":
        logo_position = (10, 10)
    elif position == "top-right":
        logo_position = (image.width - logo.width - 10, 10)
    elif position == "bottom-left":
        logo_position = (10, image.height - logo.height - 10)
    else:  # bottom-right
        logo_position = (image.width - logo.width - 10, image.height - logo.height - 10)

    # Paste the logo onto the image (using alpha for transparency if logo has it)
    image.paste(logo, logo_position, logo if logo.mode == "RGBA" else None)
    return image

# Main function to perform text overlay and autobranding
def create_branded_image(image, logo_url, text="Your Brand Name", text_position=(50, 50), font_size=36, color=(255, 255, 255), logo_position="bottom-right", logo_size=(100, 100)):
    # Add text overlay to the main image
    image = add_text_overlay(image, text, position=text_position, font_size=font_size, color=color)

    # Add logo overlay to the main image
    image = add_logo_overlay(image, logo_url, position=logo_position, logo_size=logo_size)

    return image

# Streamlit UI
st.title("Image Branding Tool")

# Upload main image
uploaded_image = st.file_uploader("Upload the main image", type=["jpg", "jpeg", "png"])

# Input fields for branding text and logo URL
logo_url = st.text_input("Enter the URL of the logo image")
text_overlay = st.text_input("Enter text to overlay on the image", "Your Brand Name")
font_size = st.slider("Font size of overlay text", min_value=10, max_value=100, value=36)
color = st.color_picker("Pick text color", "#FFFFFF")

# Text position
text_x = st.number_input("Text X Position", min_value=0, max_value=1000, value=50)
text_y = st.number_input("Text Y Position", min_value=0, max_value=1000, value=50)
text_position = (text_x, text_y)

# Logo position and size
logo_position = st.selectbox("Choose logo position", ["top-left", "top-right", "bottom-left", "bottom-right"])
logo_width = st.number_input("Logo width", min_value=10, max_value=500, value=100)
logo_height = st.number_input("Logo height", min_value=10, max_value=500, value=100)
logo_size = (logo_width, logo_height)

# Process the image if inputs are provided
if uploaded_image and logo_url:
    # Open the uploaded image
    image = Image.open(uploaded_image)

    # Create the branded image
    branded_image = create_branded_image(
        image=image,
        logo_url=logo_url,
        text=text_overlay,
        text_position=text_position,
        font_size=font_size,
        color=color,
        logo_position=logo_position,
        logo_size=logo_size
    )

    # Display the branded image
    st.image(branded_image, caption="Branded Image", use_column_width=True)

    # Provide an option to download the branded image
    buffered = BytesIO()
    branded_image.save(buffered, format="JPEG")
    st.download_button(
        label="Download Branded Image",
        data=buffered.getvalue(),
        file_name="branded_image.jpg",
        mime="image/jpeg"
    )
