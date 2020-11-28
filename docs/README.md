# Investigating Business Impact of COVID-19 through Nature Language Processing of Financial Reports and Earning Conference Call Transcripts

The project aims to use ***Natural Language Processing*** (NLP) quantitatively analyze the effect of COVID-19 on some companies and industries. This blog will walk you through the techniques used for web scraping and data preprocessing and introduce the packages for sentiment analysis. The program language in theis project is based on Python 3.0.

## Content
- [Web Scraping and Data Preprocessing](#web-scraping-and-data-preprocessing)
- [Sentiment Analysis](#sentiment-analysis)

## Web Scraping and Data Preprocessing
### 1. Data and Data source
The data used for NLP analysis are ***earnings call transcripts***, ***quarterly reports(10-Q)***, ***annual reports (10-K)*** filed between Jan-10-2020, when WHO issued technical briefings warning about urging precautions of COVID-19, and Nov-10-2020. All the documents are downloaded from Capital IQ.

Take Tesla,Inc.(NasdaqGS:TSLA) as an example. The following images show the target earnings call transcripts and financial reports to be used for analysis.

<img width="946" alt="earnings transcript_TSLA" src="https://user-images.githubusercontent.com/62812841/100451812-fb397e00-30f2-11eb-8fc9-be7efdcdfd33.png">
Image1.1

<img width="940" alt="report" src="https://user-images.githubusercontent.com/62812841/100451885-12786b80-30f3-11eb-8f5a-a7c06e4f86f8.png">
Image1.2

Apart from the text documents used for NLP analysis, other types of data are also used in the analysis to determine the impact on companies. For instance, company ***stock prices*** are the indicator of financial performances, which are extracted from ***Bloomberg***. Also, company locations and COVID-19 cases are used in the geographical analysis which is supposed to find whether there is a relationship between the average sentiment score of a location and the severity of the pandemic. Information about ***company locations***, i.e. primary office address, is scraped from ***Yahoo Finance***, and the ***statistics of COVID-19*** are available on Centers for ***Disease Control and Prevention website***. 

### 2. Web Scraping
In order to web scrape the target documents from Capital IQ, we use ***Selenium*** with Python. For example, a task is to download the financial reports of Tesla in Image1.2.

First, create a Chrome driver and use driver.get method to navigate to the page of Filing Annual Report website given by the URL.

    driver = webdriver.Chrome(executable_path="...", chrome_options=options) #...input the local directory of Chrome driver 
    driver.implicitly_wait(finish_time) #finish_time is the maximum waiting time set by yourself
    driver.delete_all_cookies()
    driver.get("https://www.capitaliq.com/CIQDotNet/Filings/FilingsAnnualReports.aspx")

Since the Capital IQ requires login information to access the website, you will then input your username and password, and click "Login" button. 

    driver.find_element(By.ID, "password").send_keys("...") #...input password
    driver.find_element(By.ID, "username").click()
    driver.find_element(By.ID, "username").send_keys("...") #... input username
    driver.find_element(By.ID, "myLoginButton").click()

Now, you will type in the Ticker of the company to search.

    driver.find_element(By.ID, "dspCustomView_Toggle_myCompanySearch_myInnerDS_myTickerBox").click()
    driver.find_element(By.ID, "dspCustomView_Toggle_myCompanySearch_myInnerDS_myTickerBox").send_keys("TSLA") #TSLA is the ticker of Tesla, it can be replaced by other company's Ticker

Next step is to set the search criteria, including ***Date Range***, ***Form Types***, ***Company Countries***.

Data Range:
    
    driver.find_element(By.ID, "dspCustomView_Toggle_ddlDateType").click()
    dropdown = driver.find_element(By.ID, "dspCustomView_Toggle_ddlDateType")
    dropdown.find_element(By.XPATH, "//option[. = 'Filing Date']").click()
    driver.find_element(By.ID, "dspCustomView_Toggle_ddlDateType").click()
    driver.find_element(By.ID, "dspCustomView_Toggle_myDateRange_myFromBox").click()
    driver.find_element(By.ID, "dspCustomView_Toggle_myDateRange_myFromBox").send_keys("01/10/2020")
    driver.find_element(By.ID, "dspCustomView_Toggle_myDateRange_myToBox").send_keys('11/10/2020')

Form Types:

    driver.find_element(By.ID, "dspCustomView_Toggle_myAO_ctl03_EC").click() #Button clicked for Advanced Search
    dropdown = driver.find_element(By.ID, "dspCustomView_Toggle_myAO_Toggle_secFormTypes_optionsList")
    dropdown.find_element(By.XPATH, "//option[. = '10-Q']").click()
    dropdown.find_element(By.XPATH, "//option[. = '10-K']").click()
    driver.find_element(By.ID, "dspCustomView_Toggle_myAO_Toggle_secFormTypes_addBtn").click()

Company Countries:

    dropdown = driver.find_element(By.ID, "dspCustomView_Toggle_myAO_Toggle_countries_optionsList")
    dropdown.find_element(By.XPATH, "//option[. = 'United States']").click()
    driver.find_element(By.ID, "dspCustomView_Toggle_myAO_Toggle_countries_addBtn").click()

Then, start to search:

    driver.find_element(By.ID, "dspCustomView_Toggle__saveCancel__saveBtn").click()
    element = driver.find_element(By.ID, "dspCustomView_Toggle__saveCancel__saveBtn")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    
After the steps above, the driver will lead you to the page shown in Image1.2, click the button with a doc icon and quit the driver. 

    element = driver.find_element(By.CSS_SELECTOR, "body")
    driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .binderIcoSprite_doctype_word_img").click()
    driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) .binderIcoSprite_doctype_word_img").click()
    driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) .binderIcoSprite_doctype_word_img").click()
    driver.find_element(By.CSS_SELECTOR, "tr:nth-child(4) > td > div > a > .binderIcoSprite_doctype_word_img").click()
    time.sleep(120)
    driver.quit()

In our case, we choose to download the files in ***doc*** type for further processing in the following stages. You may also choose PDF files, which may be more convenient to read.

### 3. Data preprocessing
Since Python3 does not support reading doc files, we first convert all doc files to ***docx*** files.

    # Opening MS Word
    word = win32.gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Open(path)
    doc.Activate ()

    # Rename path with .docx
    new_file_abs = os.path.abspath(path)
    new_file_abs = re.sub(r'\.\w+$', '.docx', new_file_abs)

    if os.path.exists(new_file_abs):
        pass

    else:
        # Save and Close
        word.ActiveDocument.SaveAs(
            new_file_abs, FileFormat=constants.wdFormatXMLDocument
        )
    doc.Close()

Then read docx files and store all the content to txt files, excluding tables in financial reports (not applicable for NLP analysis).

For data cleaning, we use txt files as input, and go through the steps of ***tokenization***, ***non-English words*** and ***stop words removal***, ***lowercase conversion***, and ***lemmatization***.  These are the packages in use:

    from nltk import pos_tag
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords, wordnet
    from nltk.stem import WordNetLemmatizer
    import re
    from tqdm import tqdm

For the purpose of following analysis, all the texts are converted back to sentence and stored in txt file as cleaned data.
