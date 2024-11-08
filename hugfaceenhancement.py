import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv('HUGGING_FACE_API')

# Define the URL for the ESRGAN model on Hugging Face
url = "https://api-inference.huggingface.co/qualcomm/esrgan"  # Replace with the actual model URL

# Load the image you want to enhance
image_path = "C:/Users/poorv/Downloads/shreklowqual.jpg"
with open(image_path, "rb") as image_file:
    image_data = image_file.read()

# Define the headers including the API token
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/octet-stream"
}

# Send a POST request with the image data to the ESRGAN model
response = requests.post(url, headers=headers, data=image_data)

# Check for a successful response
if response.status_code == 200:
    # Open the enhanced image
    img = Image.open(BytesIO(response.content))
    img.save("enhanced_image.jpg")
    img.show()
else:
    print(f"Error: {response.status_code} - {response.text}")

