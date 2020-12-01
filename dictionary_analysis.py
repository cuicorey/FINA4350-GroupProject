import pandas as pd
import numpy as np
import os

record = {}
data = pd.read_excel(r'Transcripts_data.xls',sheet_name = "summary")
record['Consumer services'] = pd.read_excel(r'record.xlsx',sheet_name = "Consumer_service")
record['Healthcare'] = pd.read_excel(r'record.xlsx',sheet_name = "Health_care")
record['Retailing'] = pd.read_excel(r'record.xlsx',sheet_name = "Retailing")
record['Automobiles and components'] = pd.read_excel(r'record.xlsx',sheet_name = "Automobiles and components")
record['Transportation'] = pd.read_excel(r'record.xlsx',sheet_name = "Transportation")
risk_dictionary = pd.read_excel(r'LoughranMcDonald_SentimentWordLists_2018.xlsx',sheet_name = "Uncertainty")
pos_dictionary = pd.read_excel(r'LoughranMcDonald_SentimentWordLists_2018.xlsx',sheet_name = "Positive")
neg_dictionary = pd.read_excel(r'LoughranMcDonald_SentimentWordLists_2018.xlsx',sheet_name = "Negative")

covid_list = ['covid','sarscov','coronavirus','ncov']
risk_list = []
pos_list = []
neg_list = []
for i in range(len(risk_dictionary)):
    risk_list.append(risk_dictionary.iloc[i,0].lower())
for i in range(len(pos_dictionary)):
    pos_list.append(pos_dictionary.iloc[i,0].lower())
for i in range(len(neg_dictionary)):
    neg_list.append(neg_dictionary.iloc[i,0].lower())

for name in ['Consumer services','Healthcare','Retailing','Automobiles and components','Transportation']:
    result = record[name]
    for i in range(len(result)):
        ticker = result.iloc[i,0]
        for col in [18,22,26,30]:
            date = result.iloc[i,col]
            print(ticker,date)
            if pd.isnull(date) == False:
                covid_count = 0
                total_word_count = 0
                num = data[(data['ticker'] == ticker)&(data['date'] == date)]
                text_name = num['txt'].iloc[0]
                path = r"/Users/cky/Desktop/NLP/preprocessed_transcript_txt/"+text_name
                f = open(path)
                text = f.readlines()

                words = []
                covid_num_list = []
                hashwords = []

                for j in range(len(text)):
                    word_list = text[j].split(' ')
                    covid_flag = False
                    for k in word_list:
                        if k == ".\n":
                            continue
                        words.append(k)
                        total_word_count += 1
                        if k in covid_list:
                            covid_count += 1
                            covid_num_list.append(len(words)-1)

                risk = 0
                pos = 0
                neg = 0
                for j in range(len(words)):
                    hashwords.append(False)
                for j in range(len(covid_num_list)):
                    covid_num = covid_num_list[j]
                    for k in range(max(covid_num-10,0),min(covid_num+10,len(words)-1)+1):
                        hashwords[k] = True
                    for k in range(max(covid_num-10,0),min(covid_num+10,len(words)-1)+1):
                        if words[k] in risk_list:
                            risk += 1
                            break
                for j in range(len(words)):
                    if hashwords[j]:
                        if words[j] in pos_list:
                            pos += 1
                        if words[j] in neg_list:
                            neg += 1

                result.iloc[i,col+1] = covid_count / total_word_count
                result.iloc[i,col+2] = risk / total_word_count
                if covid_count == 0:
                    pass
                else:
                    result.iloc[i,col+3] = (pos-neg) / covid_count
        month_dict = {"01":"Jan","02":"Feb","03":"Mar","04":"Apr","05":"May","06":"Jun","07":"Jul","08":"Aug","09":"Sep","10":"Oct","11":"Nov","12":"Dec"}
        for col in [2,6,10,14]:
            date = result.iloc[i,col]
            print(ticker,date)
            if pd.isnull(date) == False:
                month = str(date).split('-')[0]
                path = r"/Users/cky/Desktop/NLP/Quarterly reports/" + name + r"/" + ticker + r"/clean"
                for file_name in os.listdir(path):
                    if file_name.find("("+month_dict[month]+"-") != -1:
                        covid_count = 0
                        total_word_count = 0
                        text_name = path+ r"/" +file_name
                        f = open(text_name)
                        text = f.readlines()

                        words = []
                        covid_num_list = []
                        hashwords = []

                        for j in range(len(text)):
                            word_list = text[j].split(' ')
                            covid_flag = False
                            for k in word_list:
                                if k == ".\n" or k.strip() == "":
                                    continue
                                words.append(k)
                                total_word_count += 1
                                if k in covid_list:
                                    covid_count += 1
                                    covid_num_list.append(len(words)-1)

                        risk = 0
                        pos = 0
                        neg = 0
                        for j in range(len(words)):
                            hashwords.append(False)
                        for j in range(len(covid_num_list)):
                            covid_num = covid_num_list[j]
                            for k in range(max(covid_num-10,0),min(covid_num+10,len(words)-1)+1):
                                hashwords[k] = True
                            for k in range(max(covid_num-10,0),min(covid_num+10,len(words)-1)+1):
                                if words[k] in risk_list:
                                    risk += 1
                                    break
                        for j in range(len(words)):
                            if hashwords[j]:
                                if words[j] in pos_list:
                                    pos += 1
                                if words[j] in neg_list:
                                    neg += 1

                        result.iloc[i,col+1] = covid_count / total_word_count
                        result.iloc[i,col+2] = risk / total_word_count
                        if covid_count == 0:
                            pass
                        else:
                            result.iloc[i,col+3] = (pos-neg) / covid_count

    result.to_excel(name+".xlsx")
