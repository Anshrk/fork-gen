import streamlit as st
from rembg import remove
from PIL import Image
import numpy as np
import io

# Streamlit app UI
st.title("Sticker Maker with Background Removal")
st.write("Upload an image, and this app will remove the background to create a sticker.")

# File uploader for image input
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

# Check if an image is uploaded
if uploaded_file is not None:
    # Open the image file
    input_image = Image.open(uploaded_file)

    # Display the original image
    st.image(input_image, caption="Original Image", use_column_width=True)

    # Remove background
    with st.spinner("Removing background..."):
        # Convert image to binary for processing
        input_bytes = io.BytesIO()
        input_image.save(input_bytes, format="PNG")
        input_bytes = input_bytes.getvalue()

        # Remove background
        output_bytes = remove(input_bytes)

        # Load the result as an image with transparency
        output_image = Image.open(io.BytesIO(output_bytes))

        # Resize to a standard sticker size (optional)
        sticker_size = (512, 512)
        output_image = output_image.resize(sticker_size, Image.ANTIALIAS)

        # Display the sticker
        st.image(output_image, caption="Sticker with Transparent Background", use_column_width=True)

        # Download option for the sticker
        st.download_button(
            label="Download Sticker",
            data=output_bytes,
            file_name="sticker.png",
            mime="image/png"
        )
else:
    st.warning("Please upload an image file to proceed.")
