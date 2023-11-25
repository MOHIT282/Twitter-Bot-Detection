# import streamlit as st
# from PIL import Image
# import base64
# from pathlib import Path

# # Function to load an image
# def load_image(image_file):
#     img = Image.open(image_file)
#     return img

# # Function to convert image to base64 (for CSS embedding)
# def img_to_bytes(img_path):
#     img_bytes = Path(img_path).read_bytes()
#     encoded = base64.b64encode(img_bytes).decode()
#     return encoded

# # Function to set a background image
# def set_bg_image(image_file):
#     # Convert the image to base64 and display it using CSS
#     bin_str = img_to_bytes(image_file)
#     page_bg_img = f'''
#     <style>
#     .stApp {{
#         background-image: url("data:image/png;base64,{bin_str}");
#         background-size: cover;
#     }}
#     </style>
#     '''
#     st.markdown(page_bg_img, unsafe_allow_html=True)

# # Main function to run the app
# def main():
#     # Set the background image (replace 'path_to_your_image.jpg' with your image file)
#     set_bg_image("background.jpg")

#     # Example content
#     st.title("Welcome to My Streamlit App")
#     st.write("This is an example of Streamlit with a background image.")

# # Run the main function

# main()

# import streamlit as st 

# def clear_text():
#     st.session_state.text = ""

# def try_clean():
#     st.session_state.text = ""
    
# if 'text' not in st.session_state:
#     st.session_state['text'] = ""
    
    
# st.text_input('Enter something', key='text')
# st.text_input('again enter', value='something')

# st.button('clear output', on_click=clear_text)
# st.button('this button do nothing', on_click=try_clean)
# st.write(st.session_state)

#  Add CSS for the border
    # st.markdown(
    #     """
    #     <style>
    #     .with-border {
    #         border: 4px solid #8B4513; /* Brown border color */
    #         padding: 10px;
    #         border-radius: 10px; /* Optional: Add rounded corners */
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )

    # # Create columns
    # col1, col2 = st.columns([1, 4])

    # # Display image with a border in the first column
    # with col1:
    #     st.markdown(
    #         '<div class="with-border"><img src="https://pbs.twimg.com/profile_images/1562753500726976514/EPSUNyR3_400x400.jpg" width="400"></div>',
    #         unsafe_allow_html=True
    #     )

    # # Display text with a border in the second column
    # with col2:
    #     st.markdown(
    #         '<div class="with-border"><h2>Virat Kohli</h2></div>',
    #         unsafe_allow_html=True
    #     )


# st.sidebar.markdown(
#     """
#     <style>
#     .sidebar .center {
#         width: 150px;
#         display: flex;
#         justify-content : center;
#         align-items : center;
#         height: 100px; /* Adjust height as needed */
#     }
    
#     .center button{
#         color : aqua;
#         background-color: transparent;
#         border : 2px solid black;
#         border-radius : 8px;
#     }
    
#     </style>
#     """,
#     unsafe_allow_html=True
# ) 
    
# st.sidebar.markdown('<div class="center sidebar"><button>Centered Button</button></div>', unsafe_allow_html=True)

# code for slider component
# st.title("BOT-BUSTER")

import streamlit as st 

file = st.file_uploader('Upload your file here ', type='csv')

if file is not None:
    st.write('hello')

st.button('okay')