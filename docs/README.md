# Investigating Business Impact of COVID-19 through Nature Language Processing of Financial Reports and Earning Conference Call Transcripts

The project aims to use **Natural Language Processing** (NLP) quantitatively analyze the effect of COVID-19 on some companies and industries. This blog will walk you through the techniques used for web scraping and data preprocessing and introduce the packages for sentiment analysis. The program language in theis project is based on Python 3.0.

## Content
- [Web Scraping and Data Preprocessing](#web-scraping-and-data-preprocessing)
- [Sentiment Analysis](#sentiment-analysis)

## Web Scraping and Data Preprocessing
### 1. Data and Data source
The data used for NLP analysis are **earnings call transcripts**, **quarterly reports(10-Q)**, **annual reports (10-K)** filed between Jan-10-2020, when WHO issued technical briefings warning about urging precautions of COVID-19, and Nov-10-2020. All the documents are downloaded from Capital IQ.

Take Tesla,Inc.(NasdaqGS:TSLA) as an example. These are the target earnings call transcripts and financial reports.

<img width="946" alt="earnings transcript_TSLA" src="https://user-images.githubusercontent.com/62812841/100451812-fb397e00-30f2-11eb-8fc9-be7efdcdfd33.png">

<img width="940" alt="report" src="https://user-images.githubusercontent.com/62812841/100451885-12786b80-30f3-11eb-8f5a-a7c06e4f86f8.png">

### 2. Web Scraping
