import streamlit as st
from PIL import Image, ImageFilter, ImageOps
import cv2
import numpy as np
from io import BytesIO

def simplify_image(image, color_count=8):
    # Convert the image to RGB and OpenCV format
    image = image.convert('RGB')
    open_cv_image = np.array(image)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

    # Resize the image to reduce detail
    width, height = 300, int(300 * open_cv_image.shape[0] / open_cv_image.shape[1])
    open_cv_image = cv2.resize(open_cv_image, (width, height), interpolation=cv2.INTER_LINEAR)

    # Convert to LAB color space for color reduction
    lab_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2LAB)
    lab_image_flat = lab_image.reshape((-1, 3))
    lab_image_flat = np.float32(lab_image_flat)

    # K-means clustering for color reduction
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(lab_image_flat, color_count, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Reconstruct the image
    centers = np.uint8(centers)
    simplified_lab_image = centers[labels.flatten()].reshape(lab_image.shape)
    simplified_image = cv2.cvtColor(simplified_lab_image, cv2.COLOR_LAB2RGB)

    # Convert back to a PIL Image for additional filtering
    pil_image = Image.fromarray(simplified_image)

    # Apply edge enhancement for a minimalistic effect
    pil_image = pil_image.filter(ImageFilter.EDGE_ENHANCE)

    # Apply contrast adjustment for a more striking look
    pil_image = ImageOps.autocontrast(pil_image, cutoff=5)

    return pil_image

def main():
    st.title("Minimalistic Image Generator")
    st.write("Upload an image to transform it into a minimalistic style.")

    # File uploader for image input
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Open the uploaded image file
        input_image = Image.open(uploaded_file)

        # Display the original image
        st.image(input_image, caption="Original Image", use_column_width=True)

        # Slider for selecting the number of colors
        color_count = st.slider("Select Number of Colors", min_value=2, max_value=20, value=8)

        # Generate the minimalistic image
        minimalistic_image = simplify_image(input_image, color_count=color_count)

        # Display the simplified image
        st.image(minimalistic_image, caption="Minimalistic Image", use_column_width=True)

        # Provide a download button for the processed image
        buffer = BytesIO()
        minimalistic_image.save(buffer, format="JPEG")
        st.download_button(
            label="Download Minimalistic Image",
            data=buffer,
            file_name="minimalistic_image.jpg",
            mime="image/jpeg"
        )

if __name__ == "__main__":
    main()
