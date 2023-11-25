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

st.set_page_config(page_title='Bot-Buster',page_icon='./images/icon.png')

#creating a session state username which can retain its value even after re-rendering
if ['username','btn'] not in st.session_state:
    st.session_state.username = ""
    st.session_state.btn = ""

#load the animation on the main page
def load_lottiefile(filepath):
    with open(filepath,"r") as f:
        return json.load(f)
    

# displaying animation to the main window
def display_animation(animation):
    
    st_lottie.st_lottie(
        animation,
        speed = 1,
        loop = True,
        quality = 'high',
        height = 450,
        width = None,
        key = None,
    )
    
def clear_username():
    st.session_state.username = ""
    st.session_state.btn = ""

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
    df = pd.read_csv(f'./datasets/cleaned_data/{st.session_state.username}.csv')
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
    model = pickle.load(open('./models/custom1_pipe_model.pkl','rb'))
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
        
    col1, col2 = st.columns([1,1.5],gap='large')
    global danger_value
    danger_value = None
    
    with col1:
        st.image(row.iloc[0, -1],width=300, use_column_width=True)
        st.subheader(f'{row.iloc[0, 0]}')
        st.write(f"Twitter Handle : <a href='https://www.twitter.com/{st.session_state.username}' id='my-link'>{row.iloc[0,1][1:]}</a>", unsafe_allow_html=True)
        st.write(f"Followers : :blue[{row.iloc[0, 2]}]")
        st.write(f'Verified : :blue[{row.iloc[0, -3]}]')
        st.write(f'Joined Twitter : :blue[{row.iloc[0, 4]}]')
            
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

        output = predict(st.session_state.username)
            
        zeros = output.count(0)
        ones = output.count(1)
        danger_value = zeros - ones
        st.write("## Predictions   ")
        chart_data = pd.DataFrame([[zeros,ones]], columns=["Human", "Bot"])
        st.bar_chart(chart_data, use_container_width=True)
        
    if(danger_value is not None and danger_value < 10):
        # print(danger_value)
        st.warning('This Account may have supspicious activities', icon='⚠️')
    
    st.write('---')
    st.write(f"### Common words used by :blue[{st.session_state.username}]")
    display_words()
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
    progress_text = f"#### Fetching tweets of :orange[{st.session_state.username}] from the dataset. Please wait..."
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
        st.error(body='## :orange[Invalid username] or no details found in the fetched data.\n ## Please recheck the entered :orange[Twitter Handle] or hashtag')

# def Analyze_data(dataset):
#     with st.form("my_form"):
#         st.write("Inside the form")
#         slider_val = st.slider("Form slider")
#         checkbox_val = st.checkbox("Form checkbox")

#         # Every form must have a submit button.
#         submitted = st.form_submit_button("Submit")
#         if submitted:
#             st.write("slider", slider_val, "checkbox", checkbox_val)

def analyze_user_data(file):
    
    df = pd.read_csv(file)
    
    if not all(col in df.columns for col in ['UserId','Tweets','Likes','Retweets','Comments','Tweet_Url']):
        st.error("#### csv file must have the following columns :orange[UserId, Tweets, Likes, Retweets, Comments, Tweet_Url]")
    else:
        st.header('Your data will be evaluated here')
        st.dataframe(df)
    
    

__,logo, heading,_ = st.columns([1,0.5,2,1])

with logo:
    st.image('./images/icon.png', width=65)
with heading:
    # st.title(':blue[BOT-BUSTER]')
    st.image('./images/canva-logo.png', width=360)

st.sidebar.write("# :orange[Enter Credentials here...]")
st.sidebar.text_input(label='Enter the :blue[**Twitter Handle**...]', placeholder='For eg. elonmusk',key='username')
# st.sidebar.write('# OR')
# hashtag = st.sidebar.text_input(label='Enter the **Hashtag**...', placeholder='For eg. #WorldCup2k23',disabled=True)

tweet_button = st.sidebar.button('Analyze Tweets', type='secondary')
st.sidebar.write('---')
# file = st.sidebar.file_uploader('Make Sure your file sholud be in csv file and must have columns named as')
st.sidebar.write('# :orange[Analyze data]')
st.session_state.btn = st.sidebar.file_uploader('Make Predictions on your :blue[**own dataset**?]', type=['csv'])
# st.session_state.btn = st.sidebar.button('Load your dataset')

def run():
    if st.session_state.username != "" and tweet_button:
        st.sidebar.button('Back to Home', on_click=clear_username)
        display_window()
    
    elif st.session_state.btn:
        st.sidebar.button('Back to Home',type='secondary', on_click=clear_username)
        analyze_user_data(st.session_state.btn)
        
    else:
        st.write('##### This is a :orange[Twitter Bot account Detection] Model having Machine Learning Capabilites to predicts the chances of a twitter account to be a bot account or not by analyzing various parameters of a tweet done by any user like :orange[common words, phrases] and :orange[sentences] etc.')
        animation = load_lottiefile("./animations/animation4.json")
        display_animation(animation)
        
run()
# st.write(st.session_state)
