import requests
import os
from dotenv import load_dotenv
import pandas as pd
class FetchTweets:

    def __init__(self,api):
        self.api_key = api
        self.continuation_token = None
        self.df = pd.DataFrame()
        load_dotenv()

    def getUserDetails(self, username):

        url = "https://twitter154.p.rapidapi.com/user/details"
        querystring = {"username":username}
        headers = {
            "x-rapidapi-key": os.getenv('API_KEY'),
            "x-rapidapi-host": "twitter154.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        res = response.json()
        
        credentials = ['creation_date','username','name','follower_count','following_count', 'is_blue_verified','description','category']
        user_data = dict()
        for key, val in res.items():
            if key in credentials:
                user_data[key] = val

        return user_data

    def getUserTweets(self, username):
        url = "https://twitter154.p.rapidapi.com/user/tweets"
        querystring = {"username":username,"limit":"100","include_replies":"false","include_pinned":"true"}
        headers = {
            "x-rapidapi-key": "39c02cdab7msh7424bcdcee10cc5p19b56ajsn06ca92d14230",
            "x-rapidapi-host": "twitter154.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        res1 = response.json()
        
        continuation_token = res1['continuation_token']

        tweets_data = {
            'Tweets' : [],
            'Likes' : [],
            'Retweets' : [],
            'Comments' : [],
            'Views' : [],
            'Timestamp' : []
            }
        for data in res1['results']:
            tweets_data['Tweets'].append(data.get('text'))
            tweets_data['Likes'].append(data.get('favorite_count'))
            tweets_data['Retweets'].append(data.get('retweet_count'))
            tweets_data['Comments'].append(data.get('reply_count'))
            tweets_data['Views'].append(data.get('views'))
            tweets_data['Timestamp'].append(data.get('creation_date'))

        temp = pd.DataFrame(tweets_data)
        self.df = pd.concat([self.df,temp])
        for i in range(5):
            res2 = FetchTweets.get_tweets_continued('MrBeast',continuation_token)
            tweets_data = {
            'Tweets' : [],
            'Likes' : [],
            'Comments' : [],
            'Retweets' : [],
            'Views' : [],
            'Timestamp' : []
            }
            for data in res2['results']:
                tweets_data['Tweets'].append(data.get('text'))
                tweets_data['Likes'].append(data.get('favorite_count'))
                tweets_data['Retweets'].append(data.get('retweet_count'))
                tweets_data['Comments'].append(data.get('reply_count'))
                tweets_data['Views'].append(data.get('views'))
                tweets_data['Timestamp'].append(data.get('creation_date'))

            temp = pd.DataFrame(tweets_data)
            self.df = pd.concat([self.df,temp])
            self.df.reset_index(drop=True)
            continuation_token = res2['continuation_token']
        return self.df.drop(columns='Timestamp')
    
    @staticmethod
    def get_tweets_continued(username, continuation_token):
        url = "https://twitter154.p.rapidapi.com/user/tweets/continuation"
        querystring = {"username":username,"limit":"100","continuation_token":continuation_token,"include_replies":"false"}
        headers = {
            "x-rapidapi-key": "39c02cdab7msh7424bcdcee10cc5p19b56ajsn06ca92d14230",
            "x-rapidapi-host": "twitter154.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        res2 = response.json()
        return res2