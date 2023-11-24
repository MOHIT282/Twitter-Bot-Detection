import streamlit as st
from PIL import Image
import base64
from pathlib import Path

# Function to load an image
def load_image(image_file):
    img = Image.open(image_file)
    return img

# Function to convert image to base64 (for CSS embedding)
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

# Function to set a background image
def set_bg_image(image_file):
    # Convert the image to base64 and display it using CSS
    bin_str = img_to_bytes(image_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Main function to run the app
def main():
    # Set the background image (replace 'path_to_your_image.jpg' with your image file)
    set_bg_image("background.jpg")

    # Example content
    st.title("Welcome to My Streamlit App")
    st.write("This is an example of Streamlit with a background image.")

# Run the main function

main()
