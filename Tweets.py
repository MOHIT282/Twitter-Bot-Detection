import requests
import Database
class FetchTweets:

    def __init__(self,api):
        self.api_key = api
        self.db = Database.DB()

    def getUserDetails(self, username):

        url = "https://twitter154.p.rapidapi.com/user/details"
        querystring = {"username":username}
        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "twitter154.p.rapidapi.com"
        }
        # response = requests.get(url, headers=headers, params=querystring)
        # user_data = response.json()
        user_data = self.db.fetchUserData(username)
        return user_data

    def getUserTweets(self, username):
        url = "https://twitter154.p.rapidapi.com/user/tweets"
        querystring = {"username":username,"limit":"100","include_replies":"false","include_pinned":"true"}
        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "twitter154.p.rapidapi.com"
        }
        # response = requests.get(url, headers=headers, params=querystring)
        # res = response.json()
        tweets = self.db.fetchUserTweets(username)
        return tweets