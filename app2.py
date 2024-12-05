import streamlit as st
import streamlit_lottie as st_lottie
import json
import pickle
import pandas as pd
import time
import os
from wordcloud import WordCloud
from customClass import CustomLinguisticFeatureTransformer
import matplotlib.pyplot as plt
import cleaning
from Tweets import FetchTweets
from typing import List

if 'username' not in st.session_state:
    st.session_state.username = ""

if 'form_expand' not in st.session_state:
    st.session_state.form_expand = True
        
if 'file' not in st.session_state:
    st.session_state.file = None

def close_form():
    st.session_state.form_expand = False

import os
import streamlit as st

class Config:
    """Application configuration and constants"""
    PAGE_TITLE = 'Bot-Buster'
    
    # Dynamically resolve paths
    # Full paths for Streamlit Cloud
    PAGE_ICON = '/mount/src/twitter-bot-detection/images/icon.png'
    LOGO_PATH = '/mount/src/twitter-bot-detection/images/canva-logo.png'
    ANIMATION_PATH = '/mount/src/twitter-bot-detection/animations/animation4.json'
    MODEL_PATH = '/mount/src/twitter-bot-detection/models/custom1_pipe_model.pkl'
class RenderUI:
    @staticmethod
    def showLogo() -> None:
        __,logo, heading,_ = st.columns([1,0.5,2,1])

        with logo:
            st.image(Config.PAGE_ICON, width=65)
        with heading:
            # st.title(':blue[BOT-BUSTER]')
            st.image(Config.LOGO_PATH, width=360)

    @staticmethod
    def displayAnimation(animation):
        """
        Display an animation using the `st_lottie` library in Streamlit.

        Parameters:
        animation (JSON): The animation file to be displayed.

        Returns:
        None. The function only displays the animation on the Streamlit app.
        """
        st_lottie.st_lottie(
            animation,
            speed=2,
            loop=True,
            quality='high',
            height=350,
            width=None,
            key=None
        )
    
    @staticmethod
    def loadSidebar():
        st.sidebar.write("# :orange[Enter Credentials here...]")
        st.sidebar.text_input(label='Enter the :blue[**Twitter Handle**...]', placeholder='For eg. elonmusk',key='username')
        st.sidebar.write('OR')
        st.sidebar.text_input(label='Enter the :blue[**Hashtag**...]', placeholder='For eg. #WorldCup2k23',disabled=True )

        tweet_button = st.sidebar.button('Analyze Tweets', type='secondary')
        st.sidebar.write('---')
        st.sidebar.write('# :orange[Analyze data...]')
        st.session_state.file = st.sidebar.file_uploader('Make Predictions on your :blue[**own dataset**?]', type=['csv'],disabled=True)
        
    
    @staticmethod
    def loadMainWindow():
        
        st.markdown("""

        Unmask the :orange[bots] with **Machine Learning**! This model predicts the likelihood of a Twitter account being a bot by analyzing key tweet characteristics.  

        ## :blue[Key Features] 🔍
        - **Common Words & Phrases**: Identifies repetitive or bot-like text.  
        - **Sentence Structures**: Detects unnatural tweet compositions.   

        Built with cutting-edge technology, this tool ensures a more authentic Twitter experience by shining a light on automation. Say goodbye to bots and hello to transparency!  
        """)

        file = open(Config.ANIMATION_PATH,'r')
        animation = json.load(file)
        file.close()
        RenderUI.displayAnimation(animation)
    
    @staticmethod
    def loadWaitingWindow():
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
        progress_text = f"#### Looking for Twitter handle :orange[{st.session_state.username}] in the dataset. Please wait..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.05)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()

    @staticmethod
    def loadPredictionWindow():
        pass
            
class FetchData:
    
    def __init__(self) -> None:
        self.tweet = FetchTweets()

    def userDetails(self,username) -> List:
        return self.tweet.getUserDetails(username=username)

    def userTweets(self,username) :
        return self.tweet.getUserTweets(username=username)
    

class BotPrediction():
    
    @staticmethod
    def wordCloud(dataset) -> None:
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

        dataset['Tweets'] = dataset['Tweets'].astype('str')

        tweets_list = ' '.join(dataset['Tweets'])

        words = tweets_list

        wordcloud = WordCloud().generate(words)
        # Display the generated image:
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.imshow(wordcloud)
        plt.axis("off")
        st.pyplot(fig, use_container_width=True)

    @staticmethod
    def classifyBot(danger_value) -> None:
        
        """
        Display the results of the prediction made about whether a Twitter account is a bot or not.

        Args:
            danger_value (int): The danger value calculated for the Twitter account.

        Returns:
            None

        Summary:
            The `show_results` function is responsible for displaying the results of the prediction made about whether a Twitter account is a bot or not. It provides different messages and icons based on the danger value calculated.

        Flow:
            1. If the danger value is between 10 and 50, a warning message with an exclamation icon is displayed, indicating that the account may have suspicious activities.
            2. If the danger value is less than 10, an error message with a stop sign icon is displayed, indicating that the account has a high chance of being a bot. A link to report the account is also provided.
            3. If the danger value is greater than 50, a success message with a checkmark icon is displayed, indicating that the account does not appear to be a bot.
        """
        if(danger_value > 10 and danger_value < 50):
            # print(danger_value)
            st.warning(' This Account may have supspicious activities', icon='⚠️')
                    
        elif(danger_value < 10):
            st.error('The twitter account has high chances to be a bot account', icon='⛔')
            st.write(":red[You can report this account here] : <a href='https://help.twitter.com/en/rules-and-policies/x-report-violation' style='text-decoration: none;'>Twitter Help</a>", unsafe_allow_html=True)
                        
        elif(danger_value > 50):
            st.success(icon='✅',body=' The twitter account doesn\'t appers to be a bot account')

    @staticmethod
    def showData(dataset) -> None:
        """
        Displays the fetched data of a Twitter user, including their profile picture, username, number of followers, verification status, and join date. It also shows the progress of analyzing the user's tweets and making predictions about whether the account is a bot or not. Additionally, it displays a bar chart of the prediction results, the common words used by the user, and a table of their recent tweets.

        Args:
            dataset (pandas.DataFrame): A pandas DataFrame dataset containing the fetched data of a Twitter user.

        Returns:
            None
        """
        with st.empty(): 
            for i in range(1):
                st.success('Tweets fetched Successfully!', icon="✅")
                time.sleep(1)
            st.write("")
            
        col1, col2 = st.columns([1,1],gap='medium')
        global danger_value
        danger_value = None
        
        with col1:
            st.image(dataset['profile_pic'],width=300, use_column_width=True)
            with st.expander(label=f"### :orange[{dataset['name']}]", expanded=True):
                st.write(f"Twitter Descrtiption : :blue[{dataset['description']}]")
                st.write(f"Twitter Handle : <a href='https://www.twitter.com/{st.session_state.username}' style='text-decoration: none;'>{dataset['username']}</a>", unsafe_allow_html=True)
                st.write(f"Followings : :blue[{dataset['following_count']}]")
                st.write(f"Followers : :blue[{dataset['follower_count']}]")
                st.write(f"Verified : :blue[{dataset['is_blue_verified']}]")
                st.write(f"Joined Twitter : :blue[{dataset['creation_date']}]")
                
        with col2:
            danger_value = BotPrediction.predict(st.session_state.tweets)
            
        BotPrediction.classifyBot(danger_value)
        
        st.write('---')
        st.write(f"### Common words used by :blue[{st.session_state.username}]")
        BotPrediction.wordCloud(st.session_state.tweets)
        
        # print('data reaching at streamlit to load-->',df)------
        if dataset is not None:
            st.write('---')
            st.write(f"### Recent tweets from :blue[{st.session_state.username}]")
            st.dataframe(data=st.session_state.tweets[['Tweets','Views','Likes','Comments','Retweets','Timestamp']].iloc[1:])

    @staticmethod
    def predict(dataset) -> int:

        """
        Predicts whether the tweets associated with a given username are from a human or a bot account.
        
        Args:
            username (str): The username for which the prediction is to be made.

        Returns:
            list: A list of predictions, where each prediction is either 0 (human) or 1 (bot).
        """
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

        model = pickle.load(open(Config.MODEL_PATH,'rb'))
        tweets = dataset['Tweets']
        tweets = dataset['Tweets'].astype('str')
        prediction = model.predict(tweets)
        
        output = prediction.tolist()
        
        zeros = output.count(0)
        ones = output.count(1)
        danger_value = (ones//(zeros+ones))*100
            
        # Create pie chart
        labels = ['Bot', 'Human']
        sizes = [zeros, ones]  # Data for pie chart
        colors = ['lightblue', 'orange']  # Optional color scheme

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

        # Display the pie chart
        st.pyplot(fig)
        
        return danger_value

    @staticmethod
    def analyzeUserFile(file):
        
        """
        Analyzes user data from a CSV file and displays various details about the user.
        
        Args:
            file (str): The path to the CSV file containing user data.
            
        Returns:
            None
        """
        temp_df = pd.read_csv(file)
        # print(temp_df)
        if not all(col in temp_df.columns for col in ['UserId','Tweets','Likes','Retweets','Comments','Tweet_Url']):
                st.error("#### csv file must have the following columns :orange[UserId, Tweets, Likes, Retweets, Comments, Tweet_Url]")
        else:
            button = None
            form_complete = False
            with st.expander(label="### :orange[Enter User Details]",expanded=st.session_state.form_expand):
                
                col1, col2 = st.columns([1,1])
                with col1:
                    name = st.text_input('Twitter Handle of the User',value=temp_df.UserId[0][1:])
                    Following = st.number_input('Twitter Following',help='Enter the no. of followings', min_value=0)
                
                with col2:
                    followers = st.number_input('Number of Twitter followers',min_value=0)
                    verified = st.radio('Verified on Twitter',['Yes','No'], horizontal=True)
                    
                form_complete = name and verified
                
                if(form_complete):
                    button = st.button('Submit Now', on_click=close_form)
            
            if button and form_complete :
            
                col1, col2 = st.columns([1,1])
                
                with col1:
                    st.write(f"#### Twitter Handle : <a href='https://www.twitter.com/{name}' style='text-decoration: none;' id='my-link'>{name}</a>", unsafe_allow_html=True)
                    st.write(f'#### Following : :blue[{Following}]')
                
                with col2:
                    st.write(f'#### Followers : :blue[{followers}]')
                    st.write(f'#### Verified : :blue[{verified}]')
            
                df = temp_df.copy()
                df = cleaning.clean(df)
                # st.write(file)
                # st.header('Your data will be evaluated here')
                danger_value = BotPrediction.predict(df)
                    
                BotPrediction.classifyBot(danger_value)
                    
                st.write(':red[Note:] The predictions accuracy is based on how clean and formated the tweets are.')
                        
                st.write('---')
                st.write(f'### Common words used by :blue[{name}]')
                BotPrediction.wordCloud(df)
                st.write('---')
                st.write(f'### Recent Tweets of :blue[{name}]')
                df = st.dataframe(df[['Tweets','Likes','Comments','Retweets','Tweet_Url']].iloc[1:])


class MainApp():

    def __init__(self) -> None:
        st.set_page_config(page_title=Config.PAGE_TITLE,page_icon=Config.PAGE_ICON)

    def run(self):
        RenderUI.showLogo()
        RenderUI.loadSidebar()
        if st.session_state.username == "":
            RenderUI.loadMainWindow()
        
        # elif st.session_state.file != None:
        #     st.write('file selected')
        #     BotPrediction.analyzeUserFile(st.session_state.file)

        else:
            RenderUI.loadWaitingWindow()
            data = FetchData()
            userDetails = data.userDetails(st.session_state.username)
            if len(userDetails) > 1:
                st.session_state.tweets = data.userTweets(st.session_state.username)
                data = data.userTweets(st.session_state.username)
                BotPrediction.showData(userDetails)
            
            else:
                st.error(body='## :orange[Invalid username] or no details found in the fetched data.\n ## Please recheck the entered :orange[Twitter Handle]')
                

if __name__ == "__main__":
    app = MainApp()
    app.run()