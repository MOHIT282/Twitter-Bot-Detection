import streamlit as st
import streamlit_lottie as st_lottie
import json
import pickle
import pandas as pd
import numpy as np
import time
import base64
from wordcloud import WordCloud
from customClass import CustomLinguisticFeatureTransformer
from phrases import common_words
import matplotlib.pyplot as plt
import Database 

st.set_page_config(page_title='Bot-Buster',page_icon='icon.png')

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

#load the animation on the main page
def load_lottiefile(filepath):
    with open(filepath,"r") as f:
        return json.load(f)
    

# displaying animation to the main window
def display_animation(animation):
    
    st_lottie.st_lottie(
        animation,
        speed = 0.75,
        loop = True,
        quality = 'high',
        height = 450,
        width = None,
        key = None,
    )

def display_words():
    """
    Generates a word cloud visualization based on the common words used in a user's tweets.

    Example Usage:
    ```python
    display_words()
    ```

    Inputs:
    - None

    Flow:
    1. Read the cleaned data of the user's tweets from a CSV file.
    2. Create an empty list to store the tweets.
    3. Iterate over each tweet in the DataFrame and append it to the list.
    4. Generate the common words used in the tweets using the `common_words` function.
    5. Generate a word cloud visualization using the generated words.
    6. Display the word cloud visualization using `st.pyplot`.

    Outputs:
    - None
    """
    df = pd.read_csv(f'./datasets/cleaned_data/{username}.csv')
    tweets_list = []

    df['Tweets'] = df['Tweets'].astype('str')

    for i in df['Tweets']:
        tweets_list.append(i)

    words = common_words(tweets_list)

    wordcloud = WordCloud().generate(words)
    # Display the generated image:
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(fig, use_container_width=True)



# Prediction function which usees the model to make predictions
def predict(username):
    """
    Predicts whether the tweets associated with a given username are from a human or a bot account.
    
    Args:
        username (str): The username for which the prediction is to be made.

    Returns:
        list: A list of predictions, where each prediction is either 0 (human) or 1 (bot).
    """
    
    # tweet_file = pd.read_csv(f'./datasets/cleaned_data/{username}.csv')
    tweet_file = Database.fetchTweets(username)
    model = pickle.load(open('custom1_pipe_model.pkl','rb'))
    tweets = tweet_file['Tweets']
    tweets = tweets.astype('str')
    output = model.predict(tweets)
    
    return output.tolist()


# if the UserId matches with the UserIds in the dataset, this function will run
def showData(row):
    """
    Displays the fetched data of a Twitter user, including their profile picture, username, number of followers, verification status, and join date. It also shows the progress of analyzing the user's tweets and making predictions about whether the account is a bot or not. Additionally, it displays a bar chart of the prediction results, the common words used by the user, and a table of their recent tweets.

    Args:
        row (pandas.DataFrame): A pandas DataFrame row containing the fetched data of a Twitter user.

    Returns:
        None
    """
    with st.empty():
        for i in range(1):
            st.success('Tweets fetched Successfully!', icon="✅")
            time.sleep(1)
        st.write("")
        
    col1, col2 = st.columns([3,6],gap='large')
    global danger_value
    danger_value = None
    
    with col1:
        st.image(row.iloc[0, -1],width=300, use_column_width=True)
        st.subheader(f'{row.iloc[0, 0]}')
        st.write(f'Twitter Handle : {row.iloc[0,1]}')
        st.write(f"Followers : {row.iloc[0, 2]}")
        st.write(f'Verified : {row.iloc[0, -3]}')
        st.write(f'Joined Twitter: {row.iloc[0, 4]}')
            
    with col2:
        with st.status("Analyzing Tweets...", expanded=True) as status:
            st.write("Cleaning the data...")
            time.sleep(4)
            st.write("Feeding tweets to the model...")
            time.sleep(2)
            st.write("Waiting for the response...")
            time.sleep(4)
            st.write("Prediction made Successfully...")
            time.sleep(2)
            status.update(label="Displaying the Prediction!", state="complete", expanded=False)

        output = predict(username)
            
        zeros = output.count(0)
        ones = output.count(1)
        danger_value = zeros - ones
        st.write("## Predictions   ")
        chart_data = pd.DataFrame([[zeros,ones]], columns=["Human", "Bot"])
        st.bar_chart(chart_data, use_container_width=True)
        
    if(danger_value is not None and danger_value < 10):
        # print(danger_value)
        st.warning('This Account may have supspicious activities', icon='⚠️')
    
    st.write(f"### Common words used by {username}")
    display_words()
    df = Database.fetchTweets(username)
    # print('data reaching at streamlit to load-->',df)------
    if df is not None:
        st.write(f"### Recent tweets from {username}")
        st.dataframe(data=df[['Tweets','Likes','Comments','Retweets','Tweet_Url']])


# main display that will render after user inputs some value
def display_window():
    """
    Display information based on a given username.

    If the username is not empty, fetch tweets from a dataset, show a progress bar, and retrieve data for the given username.
    If the data is found, call the `showData` function. Otherwise, display an error message.
    If the username is empty, display a description of a Twitter Bot account detection model and an animation.

    Inputs:
    - None

    Outputs:
    - None
    """
    if username != "":
    
        df = pd.read_csv('data.csv') # reading the dataset
        progress_text = f"#### Fetching tweets of {username} from the dataset. Please wait."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.05)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()
        
        # row = df[df.UserId == username] # finding the username
        row = Database.FetchData(username)
        # print(row)
        
        if(row is not None):
            showData(row)
        else:
            st.error('## Invalid username or no details found in the fetched data.\n ## Please recheck the entered Twitter Handle or hashtag')

    
    else:
        st.write('This is a Twitter Bot account Detection Model having Machine Learning Capabilites to predicts the chances of a twitter account to be a bot account or not by analyzing various parameters of a tweet done by any user like common words, phrases and sentences etc.')
        
        animation = load_lottiefile("animation.json")
        display_animation(animation)
        
    

# Add CSS for the border
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
heading, logo = st.columns([1,1])

with heading:
    st.title('BOT-BUSTER')

# with logo:
#     st.image('logo-hd.png', width=200)
st.sidebar.write("# Enter the Credentials here...")
username = st.sidebar.text_input(label='Enter the **Twitter Handle**...', placeholder='For eg. elonmusk')
st.sidebar.write('# OR')
hashtag = st.sidebar.text_input(label='Enter the **Hashtag**...', placeholder='For eg. #WorldCup2k23',disabled=True)

st.sidebar.button('Analyze Tweets', type='secondary')

display_window()


    