from nltk.tokenize import word_tokenize, sent_tokenize
import os
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from statistics import mean
#import nltk
#nltk.download('vader_lexicon')
import pandas as pd
from tqdm import tqdm

industries=['Retailing',"Transportation","Automobiles and components","Consumer services","Healthcare"]
dict={'Jan':"01","Feb":"02","Mar":"03","Apr":"04","May":"05",\
     "Jun":"06","Jul":"07","Aug":'08','Sep':'09','Oct':'10','Nov':'11'}
covid_list=['covid','sarscov','coronavirus','ncov']

def Textblob_score(i,sentences):
    try:
        sent_before=TextBlob(sentences[i-1]).sentiment.polarity
        sent=TextBlob(sentences[i]).sentiment.polarity
        sent_after=TextBlob(sentences[i+1]).sentiment.polarity
        average=(sent_before + sent + sent_after)/3     
    except:
        average=0
    return average

def Vader_score(i,sentences):
    sid=SentimentIntensityAnalyzer()
    try:
        sent_before=sid.polarity_scores(sentences[i-1])['compound']
        sent=sid.polarity_scores(sentences[i])['compound']
        sent_after=sid.polarity_scores(sentences[i+1])['compound']
        average=(sent_before + sent + sent_after)/3
    except:
        average=0
    return average

def sentiment_analysis(file_path):
    with open(file_path,'r',encoding='utf-8') as f:
        text=f.read()
        sentences=sent_tokenize(text)
        Textblob_sentscore=[]
        Vader_sentscore=[]
        for i in range(len(sentences)):
            [Textblob_sentscore.append(Textblob_score(i,sentences)) for word in word_tokenize(sentences[i]) if word in covid_list]
            [Vader_sentscore.append(Vader_score(i,sentences)) for word in word_tokenize(sentences[i]) if word in covid_list]

        if len(Textblob_sentscore) != 0:
            file_textsent_score=mean(Textblob_sentscore)
            file_vadersent_score=mean(Vader_sentscore)
        else:
            file_textsent_score=0
            file_vadersent_score=0

        return [file_textsent_score, file_vadersent_score]

#transcript
industries=['consumer','healthcare','retailing','transportation','automobile']

for industry in industries:
    print (industry)
    df=pd.read_excel("D:\\FINA4350\\preprocessed_transcript_txt\\record.xls",sheet_name=industry)  #directory should be changed accordingly
    with tqdm (range(df.shape[0]), desc = "sentiment analysis", ncols=80) as t:
        for i in t:
                for file in os.listdir('D:\\FINA4350\\preprocessed_transcript_txt\\preprocessed_transcript_txt'):
                    if file.split(',')[0]==df['Company'][i]:
                        print(file)
                        date='-'.join([file.split('.')[-2].split(',')[-1].strip(),\
                                       dict[file.split('.')[-2].split(',')[-2].split(' ')[-2]],\
                                       file.split('.')[-2].split(',')[-2].split(' ')[-1]])
                        file_path='D:\\FINA4350\\preprocessed_transcript_txt\\preprocessed_transcript_txt\\'+file
                        textblob=sentiment_analysis(file_path)[0]
                        vader=sentiment_analysis(file_path)[1]
                        
                        for j in range(1,5):
                            if date==str(df['transcript{}'.format(j)][i]).split(' ')[0]:
                                df['TB_score_tran_{}'.format(j)][i]=textblob
                                df['VD_score_tran_{}'.format(j)][i]=vader
                                #print(textblob,vader)
                                print (date,\
                                       df['TB_score_tran_{}'.format(j)][i],\
                                       df['VD_score_tran_{}'.format(j)][i])
                                break


    df.to_csv("D://FINA4350//{}_transcript.csv".format(industry),index=False)

#report
industries=['Retailing',"Transportation","Automobiles and components","Consumer services","Healthcare"]

for industry in industries:
    df=pd.read_excel("D:\\FINA4350\\5_industry_report(1).xlsx",sheet_name=industry,index_col=0)
    with tqdm (os.listdir('D:\\FINA4350\\'+industry), desc = "sentiment analysis", ncols=80) as t:
        for company in t:
            print (company)
            try:
                for file in os.listdir('D:\\FINA4350\\'+industry+'\\'+company+'\\'+'clean'):
                        date='-'.join([dict[file.split(".")[0].split('(')[1].strip(')').split('-')[0]],\
                                       file.split(".")[0].split('(')[1].strip(')').split('-')[1],\
                                       file.split(".")[0].split('(')[1].strip(')').split('-')[2]])
                        file_path='D:\\FINA4350\\'+industry+'\\'+company+'\\'+'clean'+'\\'+file
                        textblob=sentiment_analysis(file_path)[0]
                        vader=sentiment_analysis(file_path)[1]
                        print(sentiment_analysis(file_path))
                        for j in range(1,5):
                            if date==df['report{}'.format(j)][company]:
                                df['TB_score_{}'.format(j)][company]=textblob
                                df['VD_score_{}'.format(j)][company]=vader
                                print(df['report{}'.format(j)][company],\
                                      df['TB_score_{}'.format(j)][company],\
                                      df['VD_score_{}'.format(j)][company])
                                break
            except:
                print ("Cannot find",company)
    
        df.to_excel("D:\\FINA4350\\5_industry_report(1).xlsx",sheet_name=industry)
    
    
