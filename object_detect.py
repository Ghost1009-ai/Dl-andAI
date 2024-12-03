import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import numpy as np

# Hugging Face DETR model API details
API_URL = ""
headers = {"Authorization": "Bearer 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"}  # Replace with your token

import os
import requests
import streamlit as st
from dotenv import load_dotenv
from PIL import Image, ImageDraw

# Load environment variables
load_dotenv()

api_url = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"

# Hugging Face API query function
def hf_api(image_file):
    headers = {"Authorization": "Bearer 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"}

    response = requests.post(api_url, headers=headers, data=image_file.read())
    return response.json()

# Function to process and format the API results
def prettier(results):
    formatted_results = []
    for item in results:
        score = round(item['score'], 3)
        label = item['label']
        location = [round(value, 2) for value in item['box'].values()]
        formatted_results.append({"label": label, "score": score, "box": location})
    return formatted_results

# Function to draw bounding boxes on the image
def draw_boxes(image, results):
    draw = ImageDraw.Draw(image)
    for item in results:
        box = item['box']
        label = item['label']
        score = item['score']
        # Draw the bounding box
        draw.rectangle(box, outline="red", width=3)
        # Add label and confidence score
        draw.text((box[0], box[1] - 10), f"{label}: {score:.2f}", fill="red")
    return image

# Streamlit app
def main():
    st.title("Object Detection with Hugging Face API")
    st.write("Upload an image to detect objects using the Hugging Face model.")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image",  use_container_width=True)

        st.write("Detecting objects...")
        with st.spinner("Processing..."):
            uploaded_file.seek(0)  # Reset file pointer for re-reading
            raw_results = hf_api(uploaded_file)

        # Format and process results
        formatted_results = prettier(raw_results)

        # Draw bounding boxes on the image
        image_with_boxes = draw_boxes(image.copy(), formatted_results)

        # Display results
        st.image(image_with_boxes, caption="Image with Detected Objects", use_container_width=True)

        st.success("Detection complete!")
        st.write("Detailed Results:")
        for result in formatted_results:
            st.write(f"**{result['label']}** - Confidence: {result['score']} - Location: {result['box']}")

if __name__ == "__main__":
    main()