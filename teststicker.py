from io import BytesIO
import streamlit as st
from PIL import Image
from rembg import remove

# Set up the Streamlit app
st.set_page_config(layout="wide", page_title="Image Background Remover")
st.title("Background Remover App")

# Upload the image
image_upload = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Function to convert image to BytesIO for download
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# Process the uploaded image
if image_upload:
    # Open the uploaded image
    image = Image.open(image_upload)
    
    # Display the original image
    st.image(image, caption="Original Image", use_column_width=True)
    
    # Remove the background
    fixed_image = remove(image)
    
    # Display the fixed image
    st.image(fixed_image, caption="Image with Background Removed", use_column_width=True)
    
    # Prepare the downloadable image
    downloadable_image = convert_image(fixed_image)
    
    # Download button for the fixed image
    st.download_button(
        "Download Fixed Image",
        downloadable_image,
        "fixed_image.png",
        "image/png"
    )