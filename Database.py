import mysql.connector as connector
import pandas as pd
class DB:
    def __init__(self):
        self.conn = connector.connect(host='localhost',
                                    password='MyDatabase24', 
                                    user='root',
                                    port='3306',
                                    database='twitter_dataset')
    
    def fetchUserData(self,UserId):
        query = f'select * from twitter_accounts where UserId = "@{UserId}"'
        cursor = self.conn.cursor()
        cursor.execute(query)
        # print("fetching results")
        data = cursor.fetchall()
        if(data == []):
            # print(data)
            return None
        else:
            # print(data)
            columns = ['Name','UserId','Followers','Following','Joined Date','Verified','UserId Url','Image']
            df = pd.DataFrame(data=data, columns=columns)
            # print(df)
            return df
          
              
    def fetchUserTweets(self, UserId):
        # print(UserId)
        try:
            query = f'select * from {UserId}'
            cursor = self.conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            
            if(data == []):
                # print(data)
                return None
            else:
                columns = ['UserId','Tweets','Likes','Comments','Retweets','Tweet_Url']
                df = pd.DataFrame(data=data, columns=columns)
                # print('data coming from mysql->',df)
                return df
        except:
            return pd.read_csv(f'datasets/cleaned_data/{UserId}.csv')


def FetchData(UserId):
    
    db = DB()
    return db.fetchUserData(UserId)
    # print(data['UserId'])
    # db.fetchUserTweets(UserId.lower())
    

def fetchTweets(UserId):
    
    db = DB()
    return db.fetchUserTweets(UserId.lower())
    
    # if data == None:
         # print('User not present')
    # return data

# fetchTweets('AndroidPolice')
