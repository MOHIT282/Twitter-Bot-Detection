import pandas as pd
from sqlalchemy import create_engine
import os

folder_path = 'D:\Twitter Bot Detection\datasets\cleaned_data'
for file in os.listdir(folder_path):
    
    file_path = os.path.join(folder_path,file)
    df = pd.read_csv(file_path)
    
    db_engine = create_engine('mysql+pymysql://root:Mohit$282@localhost/twitter_database')
    
    df.to_sql(name= file.split('.')[0],if_exists='replace',index=False,con=db_engine)
    
    