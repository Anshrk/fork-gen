import streamlit as st
from PIL import Image, ImageOps
import io

def create_sticker(image, size=(512, 512), border_size=10):
    """
    Generates a sticker from a given image with a specified size and optional border.

    Parameters:
    - image (PIL Image): The input image.
    - size (tuple): The target size of the sticker.
    - border_size (int): Thickness of the border (optional).
    
    Returns:
    - PIL Image: The sticker image.
    """
    # Convert image to RGBA (supports transparency)
    img = image.convert("RGBA")
    
    # Make the image square by padding it with transparent borders if needed
    img = ImageOps.pad(img, size, color=(255, 255, 255, 0))  # Transparent background
    
    # Optionally, add a white border to the image
    if border_size > 0:
        img = ImageOps.expand(img, border=border_size, fill=(255, 255, 255, 255))
    
    return img

# Streamlit UI
st.title("Sticker Generator")

# Image upload
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Sticker settings
sticker_size = st.slider("Sticker Size", min_value=128, max_value=1024, value=512, step=64)
border_size = st.slider("Border Size", min_value=0, max_value=50, value=10)

if uploaded_file is not None:
    # Load the image
    image = Image.open(uploaded_file)
    
    # Generate the sticker
    sticker = create_sticker(image, size=(sticker_size, sticker_size), border_size=border_size)
    
    # Display the result
    st.image(sticker, caption="Generated Sticker", use_column_width=True)
    
    # Download button
    img_byte_arr = io.BytesIO()
    sticker.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    st.download_button(
        label="Download Sticker",
        data=img_byte_arr,
        file_name="sticker.png",
        mime="image/png"
    )
