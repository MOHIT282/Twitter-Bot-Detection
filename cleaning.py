import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class CleanDataset():
    
    def clean(self,file):
        #reading the dataset
        df = pd.read_csv(file)
        
        df = df[['UserId','Tweets','Likes','Comments','Retweets','Tweet_Url']]
     
        # removing null values from the datasets
        df = df.dropna() 
        
        df = df.reset_index(drop=True)
        # converting the columns datatype into string datatype
        df.Tweets = df.Tweets.astype('str')
        df.Likes = df.Likes.astype('str')
        df.Retweets = df.Retweets.astype('str')
        df.Tweet_Url = df.Tweet_Url.astype('str')
    
        return df
    

def cleanFile(file):
    
    obj = CleanDataset()
    
    return obj.clean(file)