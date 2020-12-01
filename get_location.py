import requests
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd

df=pd.read_excel("D://FINA4350//_sentiment_score//average_sent_score.xlsx", sheet_name='Sheet1')
df['Office']=''
df['Name']=''
for i in range(df.shape[0]):
    try:
        ticker=df['Ticker'][i]
        r = \
        requests.get(
            'https://finance.yahoo.com/quote/{}/profile?p={}'.format(ticker,ticker),
            timeout=3)
        s = BeautifulSoup(r.text, 'lxml')
        df['Name'][i]=s.title.text
        df['Office'][i]=s.find_all('p')[0].text.split(',')[1].strip().split(' ')[0]
        print(df['Name'][i],df['Office'][i])
    except:
        print('fail to find',ticker) 

df.to_csv('D://FINA4350//_sentiment_score//location.csv')
    