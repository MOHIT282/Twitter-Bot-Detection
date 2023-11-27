import streamlit as st
import streamlit_lottie as st_lottie
import json
import pickle
import pandas as pd
import time
from wordcloud import WordCloud
from customClass import CustomLinguisticFeatureTransformer
from phrases import common_words
import matplotlib.pyplot as plt
import Database 
import cleaning

st.set_page_config(page_title='Bot-Buster',page_icon='./images/icon.png')

#creating a session state username which can retain its value even after re-rendering
if 'username' not in st.session_state:
    st.session_state.username = ""

if 'form_expand' not in st.session_state:
    st.session_state.form_expand = True

def close_form():
    st.session_state.form_expand = False

def show_results(danger_value):
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

#load the animation on the main page
def load_lottiefile(filepath):
    with open(filepath,"r") as f:
        return json.load(f)
    

# displaying animation to the main window
def display_animation(animation):
    """
    Display an animation using the `st_lottie` library in Streamlit.

    Parameters:
    animation (JSON): The animation file to be displayed.

    Returns:
    None. The function only displays the animation on the Streamlit app.
    """
    st_lottie.st_lottie(
        animation,
        speed=1,
        loop=True,
        quality='high',
        height=450,
        width=None,
        key=None
    )
    
def clear_username():
    st.session_state.username = ""
    st.session_state.btn = ""

def display_words(df):
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
    # df = pd.read_csv(f'./datasets/cleaned_data/{st.session_state.username}.csv')
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
def predict(tweet_file):
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

            
    # tweet_file = pd.read_csv(f'./datasets/cleaned_data/{username}.csv')
    model = pickle.load(open('./models/custom1_pipe_model.pkl','rb'))
    tweets = tweet_file['Tweets']
    tweets = tweets.astype('str')
    prediction = model.predict(tweets)
    
    output = prediction.tolist()
    
    zeros = output.count(0)
    ones = output.count(1)
    danger_value = zeros - ones
        
    st.write("## Predictions   ")
    chart_data = pd.DataFrame([[zeros,ones]], columns=["Human", "Bot"])
    st.bar_chart(chart_data, use_container_width=True)
    
    return danger_value


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
        
    col1, col2 = st.columns([1,1.5],gap='large')
    global danger_value
    danger_value = None
    
    with col1:
        st.image(row.iloc[0, -1],width=300, use_column_width=True)
        with st.expander(label=f':orange[{row.iloc[0, 0]}]', expanded=True):
            st.write(f"Twitter Handle : <a href='https://www.twitter.com/{st.session_state.username}' style='text-decoration: none;'>{row.iloc[0,1][1:]}</a>", unsafe_allow_html=True)
            st.write(f"Followers : :blue[{row.iloc[0, 2]}]")
            st.write(f'Verified : :blue[{row.iloc[0, -3]}]')
            st.write(f'Joined Twitter : :blue[{row.iloc[0, 4]}]')
            
    with col2:
        tweet_file = Database.fetchTweets(st.session_state.username)
        danger_value = predict(tweet_file)
        
    show_results(danger_value)
    
    st.write('---')
    st.write(f"### Common words used by :blue[{st.session_state.username}]")
    dataset = Database.fetchTweets(st.session_state.username)
    display_words(dataset)
    
    df = Database.fetchTweets(st.session_state.username)
    # print('data reaching at streamlit to load-->',df)------
    if df is not None:
        st.write('---')
        st.write(f"### Recent tweets from :blue[{st.session_state.username}]")
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

    # df = pd.read_csv('data.csv') # reading the dataset
    # st.markdown("Text can be :blue[blue], but also :orange[orange]. And of course it can be :red[red]. And :green[green].")
    progress_text = f"#### Looking for Twitter handle :orange[{st.session_state.username}] in the dataset. Please wait..."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.05)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()
     
    # row = df[df.UserId == username] # finding the username
    row = Database.FetchData(st.session_state.username)
    # print(row)
        
    if(row is not None):
        showData(row)
    else:
        st.error(body='## :orange[Invalid username] or no details found in the fetched data.\n ## Please recheck the entered :orange[Twitter Handle]')

def analyze_user_data(file):
    """
    Analyzes user data from a CSV file and displays various details about the user.
    
    Args:
        file (str): The path to the CSV file containing user data.
        
    Returns:
        None
    """
    temp_df = pd.read_csv(file)
    print(temp_df)
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
            danger_value = predict(df)
                
            show_results(danger_value)
                
            st.write(':red[Note:] The predictions accuracy is based on how clean and formated the tweets are')
                    
            st.write('---')
            st.write(f'### Common words used by :blue[{name}]')
            display_words(df)
            st.write('---')
            st.write(f'### Recent Tweets of :blue[{name}]')
            df = st.dataframe(df[['Tweets','Likes','Comments','Retweets','Tweet_Url']])


__,logo, heading,_ = st.columns([1,0.5,2,1])

with logo:
    st.image('./images/icon.png', width=65)
with heading:
    # st.title(':blue[BOT-BUSTER]')
    st.image('./images/canva-logo.png', width=360)

st.sidebar.write("# :orange[Enter Credentials here...]")
st.sidebar.text_input(label='Enter the :blue[**Twitter Handle**...]', placeholder='For eg. elonmusk',key='username')
# st.sidebar.write('OR')
# st.sidebar.text_input(label='Enter the :blue[**Hashtag**...]', placeholder='For eg. #WorldCup2k23',disabled=True )

tweet_button = st.sidebar.button('Analyze Tweets', type='secondary')
st.sidebar.write('---')
st.sidebar.write('# :orange[Analyze data...]')
file = st.sidebar.file_uploader('Make Predictions on your :blue[**own dataset**?]', type=['csv'])

def run():
    if st.session_state.username != "":
            st.sidebar.button('Back to Home', on_click=clear_username)
            display_window()  
    
    elif file:
        # st.sidebar.button('Back to Home',type='secondary', on_click=clear_username)
        analyze_user_data(file)
        
    else:
        st.write('##### This is a :orange[Twitter Bot account Detection] Model having Machine Learning Capabilites to predicts the chances of a twitter account to be a bot account or not by analyzing various parameters of a tweet done by any user like :orange[common words, phrases] and :orange[sentences] etc.')
        animation = load_lottiefile("./animations/animation4.json")
        display_animation(animation)
        
run()
# st.write(st.session_state)
