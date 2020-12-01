import pandas as pd
import numpy as np

data = pd.read_excel(r'company_result.xlsx')
price = pd.read_excel(r'bbg_price.xlsx',sheet_name = "price")

for i in range(len(data)):
    ticker = data.iloc[i,0]
    date = data.iloc[i,1]
    print(ticker,date)
    x = -1
    y = -1
    for j in range(len(price)):
        if x != -1:
            break
        if price.iloc[j,0] == date:
            for k in range(len(price.columns)):
                if price.columns[k].split(' ')[0] == ticker:
                    x = j
                    y = k
                    break
    if x == -1:
        continue

    past = []
    for j in range(x-1,-1,-1):
        if np.isnan(price.iloc[j,y]) == False:
            past.append(price.iloc[j,y])
        if len(past) == 3:
            break
    if len(past) != 3:
        continue

    future = []
    for j in range(x,len(price)):
        if np.isnan(price.iloc[j,y]) == False:
            future.append(price.iloc[j,y])
        if len(future) == 3:
            break
    if len(future) != 3:
        continue

    aver1 = sum(past) / 3
    aver2 = sum(future) / 3
    data.iloc[i,8] = (aver2 - aver1) / aver1

data.to_excel("company_price_result.xlsx")
