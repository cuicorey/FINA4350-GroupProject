import pandas as pd
import numpy as np

data = pd.read_excel(r'company_price_clean.xlsx')

data1 = {}
data2 = {}
data1['Consumer services'] = pd.read_excel(r'record.xlsx',sheet_name = "Consumer services")
data1['Healthcare'] = pd.read_excel(r'record.xlsx',sheet_name = "Healthcare")
data1['Retailing'] = pd.read_excel(r'record.xlsx',sheet_name = "Retailing")
data1['Automobiles and components'] = pd.read_excel(r'record.xlsx',sheet_name = "Automobiles and components")
data1['Transportation'] = pd.read_excel(r'record.xlsx',sheet_name = "Transportation")
data2['Consumer services'] = pd.read_excel(r'industry.xlsx',sheet_name = "Consumer services")
data2['Healthcare'] = pd.read_excel(r'industry.xlsx',sheet_name = "Healthcare")
data2['Retailing'] = pd.read_excel(r'industry.xlsx',sheet_name = "Retailing")
data2['Automobiles and components'] = pd.read_excel(r'industry.xlsx',sheet_name = "Automobiles and components")
data2['Transportation'] = pd.read_excel(r'industry.xlsx',sheet_name = "Transportation")

for industry in ['Consumer services','Healthcare','Retailing','Automobiles and components','Transportation']:
    ticker_list = []
    x = -1
    namelist = data1[industry]
    result = data2[industry]
    for i in range(len(namelist)):
        ticker_list.append(namelist.iloc[i,0])
    for i in range(len(data)):
        ticker = data.iloc[i,0]
        if ticker in ticker_list:
            x += 1
            for j in range(9):
                result.iloc[x,j] = data.iloc[i,j]
    result.to_excel(industry+".xlsx")
