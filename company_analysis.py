import pandas as pd

result = pd.read_excel(r'company.xlsx')
data1 = {}
data2 = {}
data1['Consumer services'] = pd.read_excel(r'record.xlsx',sheet_name = "Consumer services")
data1['Healthcare'] = pd.read_excel(r'record.xlsx',sheet_name = "Healthcare")
data1['Retailing'] = pd.read_excel(r'record.xlsx',sheet_name = "Retailing")
data1['Automobiles and components'] = pd.read_excel(r'record.xlsx',sheet_name = "Automobiles and components")
data1['Transportation'] = pd.read_excel(r'record.xlsx',sheet_name = "Transportation")
data2['Consumer services'] = pd.read_excel(r'ML_SentScore.xlsx',sheet_name = "Consumer services")
data2['Healthcare'] = pd.read_excel(r'ML_SentScore.xlsx',sheet_name = "Healthcare")
data2['Retailing'] = pd.read_excel(r'ML_SentScore.xlsx',sheet_name = "Retailing")
data2['Automobiles and components'] = pd.read_excel(r'ML_SentScore.xlsx',sheet_name = "Automobiles and components")
data2['Transportation'] = pd.read_excel(r'ML_SentScore.xlsx',sheet_name = "Transportation")

x = -1
for industry in ['Consumer services','Healthcare','Retailing','Automobiles and components','Transportation']:
    df1 = data1[industry]
    df2 = data2[industry]
    for i in range(len(df1)):
        ticker = df1.iloc[i,0]
        for j in [2,6,10,14,18,22,26,30]:
            date = df1.iloc[i,j]
            print(ticker,date)
            if pd.isnull(date):
                continue
            else:
                if j in [2,6,10,14]:
                    month = date.split('-')[0]
                    day = date.split('-')[1]
                    year = date.split('-')[2]
                    date = year+'-'+month+'-'+day
                covid_exposure = df1.iloc[i,j+1]
                if covid_exposure == 0:
                    continue
                else:
                    risk_exposure = df1.iloc[i,j+2]
                    sentiment_score = df1.iloc[i,j+3]
                    tb = df2.iloc[i,j+1]
                    vd = df2.iloc[i,j+2]
                    finbert = df2.iloc[i,j+3]
                    x += 1
                    result.iloc[x,0] = ticker
                    result.iloc[x,1] = date
                    result.iloc[x,2] = covid_exposure
                    result.iloc[x,3] = risk_exposure
                    result.iloc[x,4] = sentiment_score
                    result.iloc[x,5] = tb
                    result.iloc[x,6] = vd
                    result.iloc[x,7] = finbert
result.to_excel("company_result.xlsx")
