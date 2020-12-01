## Evaluating the Business Impact of COVID-19 using Natural Language Processing

The project aims to use ***Natural Language Processing*** (NLP) to quantitatively analyze the business effect of COVID-19 on companies and industries. This blog will walk you through the techniques used for web scraping, data preprocessing, and sentiment analysis. The program language in use is based on Python 3.

### Content
- [Web Scraping and Data Preprocessing](#web-scraping-and-data-preprocessing)
- [Sentiment Analysis](#sentiment-analysis)

### Web Scraping and Data Preprocessing
#### 1. Data and Data source
The data used for NLP analysis are ***earnings call transcripts***, ***quarterly reports(10-Q)***, and ***annual reports (10-K)*** filed between Jan-10-2020 and Nov-10-2020. All the documents are available from Capital IQ.

We will take Tesla,Inc. (NasdaqGS:TSLA) as an example to illustrate. The following images show the target earnings call transcripts and financial reports to be used for analysis.

<img width="946" alt="earnings transcript_TSLA" src="https://user-images.githubusercontent.com/62812841/100451812-fb397e00-30f2-11eb-8fc9-be7efdcdfd33.png">
Image1.1


<img width="940" alt="report" src="https://user-images.githubusercontent.com/62812841/100451885-12786b80-30f3-11eb-8f5a-a7c06e4f86f8.png">
Image1.2

#### 2. Web Scraping
In order to extract the target documents from Capital IQ through web scraping, we use ***Selenium*** with Python. For example, a task is to download the financial reports of Tesla shown in Image1.2.

First, create a Chrome driver and use driver.get method to navigate to the page of Filing Annual Report website given by the URL.

    driver = webdriver.Chrome(executable_path="...", chrome_options=options) #...input the local directory of Chrome driver 
    driver.implicitly_wait(finish_time) #finish_time is the maximum waiting time set by yourself
    driver.delete_all_cookies()
    driver.get("https://www.capitaliq.com/CIQDotNet/Filings/FilingsAnnualReports.aspx")

Since the Capital IQ requires login information to access the website, you need to input the username and password, and click "Login" button. 

    driver.find_element(By.ID, "password").send_keys("...") #...input password
    driver.find_element(By.ID, "username").click()
    driver.find_element(By.ID, "username").send_keys("...") #... input username
    driver.find_element(By.ID, "myLoginButton").click()

Next, type in the Ticker of the company to search.

    driver.find_element(By.ID, "dspCustomView_Toggle_myCompanySearch_myInnerDS_myTickerBox").click()
    driver.find_element(By.ID, "dspCustomView_Toggle_myCompanySearch_myInnerDS_myTickerBox").send_keys("TSLA") #TSLA is the ticker of Tesla, it can be replaced by other company's Ticker

Next step is to set the search criteria, including ***Date Range***, ***Form Types***, ***Company Countries***. In our case, date range should be from 01/20/2020 to 11/20/2020. Form types include 10Q and 10K. Company countries should be the United States.

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
    
After following the steps above, the driver will lead you to the page shown in Image1.2, click the button with a doc icon and quit the driver. 

    element = driver.find_element(By.CSS_SELECTOR, "body")
    driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .binderIcoSprite_doctype_word_img").click()
    driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) .binderIcoSprite_doctype_word_img").click()
    driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) .binderIcoSprite_doctype_word_img").click()
    driver.find_element(By.CSS_SELECTOR, "tr:nth-child(4) > td > div > a > .binderIcoSprite_doctype_word_img").click()
    time.sleep(120)
    driver.quit()

In our case, we choose to download the files in ***doc*** format for further processing in the following stages. You may also choose PDF files, which may be more convenient to read for Python.

#### 3. Data preprocessing
Since Python 3 does not support reading doc files, we first convert all doc files to ***docx*** files.

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

For the purpose of the following analysis, all the texts are converted back to sentence and stored in txt file as cleaned data.

### Sentiment Analysis

We introduce three sentiment analysis methods used in our proect: 
* [TextBlob](#TextBlob)
* [NLTK Vader](#NLTK-Vader)
* [FinBert](#FinBert)

Suppose we have the following three sentences containing the word ***"COVID-19"***. Intuitively, the first sentence is negative, the second one is the neutral, and the last one is positive.

    s1 = "The COVID-19 pandemic has seriously disrupted the global automotive industry and customer sales, production volumes."
    s2 = "We are continuing to monitor the impact of COVID-19 on financial condition and cash flows."
    s3 = "We are confident that the COVID-19 pandemic will not cause any disruptions to the supply of our medicine."

#### 1. TextBlob
TextBlob package is a simple way to conduct sentiment analysis. Its sentiment property can return the ***polarity score*** of a sentence. The score is a float within the range [-1.0, 1.0], where -1.0 is very negative and 1.0 is very positive.

    # first, we import TextBlob package
    from textblob import TextBlob

    # then, we create a TextBlob objective based on s1
    s1_tb = TextBlob(s1)

    # then, we can calculate the polarity score of this TextBlob objective
    s1_tb.sentiment.polarity

The above code will return the polarity score of s1: -0.16666666666666666.  
We can calculate the scores for these three sentences:

    print("s1 polarity score:", TextBlob(s1).sentiment.polarity)
    print("s2 polarity score:", TextBlob(s2).sentiment.polarity)
    print("s3 polarity score:", TextBlob(s3).sentiment.polarity)

The results are: 

    s1 polarity score: -0.16666666666666666
    s2 polarity score: 0.0
    s3 polarity score: 0.5

#### 2. NLTK Vader

NLTK Vader is another convenient package for sentiment analysis. Its result also ranges from -1 (very negative) to 1 (very positive)

    # first, we import the related package
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    # next, we create the analyzer
    analyzer = SentimentIntensityAnalyzer()

    # then, we calculate the polarity scores of these three sentences
    print("s1 polarity score:", analyzer.polarity_scores(s1)['compound'])
    print("s2 polarity score:", analyzer.polarity_scores(s2)['compound'])
    print("s3 polarity score:", analyzer.polarity_scores(s3)['compound'])


The results are: 

    s1 polarity score: -0.1779
    s2 polarity score: 0.0
    s3 polarity score: 0.6412

#### 3. FinBert
FinBERT is a BERT model pre-trained on financial communication text, including Corporate Reports 10-K & 10-Q, Earnings Call Transcripts and Analyst Report. It has the state-of-the-art performance on financial sentiment classification task.  
Their paper is: *Yi Yang, Mark Christopher Siy UY, & Allen Huang. (2020). FinBERT: A Pretrained Language Model for Financial Communications.*
You can find more information on their official [GitHub repo](https://github.com/yya518/FinBERT)  
We use the fine-tuned model provided by the authors and change its last layer to output the sentiment score. In this setting, the score also ranges from -1 (very negative) to 1 (very positive).  
You can also fine-tune the model on your text data first, and then use it for the following task.

The requirements of FinBert model are:

    pytorch-pretrained-bert==0.6.2
    torch==1.2.0
    torchvision==0.4.0
    CUDA==10.1
    
First, we import the required packages:

    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.optim import lr_scheduler
    from torch.utils.data import Dataset, DataLoader
    from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM, BertConfig
    from bertModel import BertClassification, dense_opt # This is from the official GitHub of FinBert
    from datasets import text_dataset, financialPhraseBankDataset # This is from the official GitHub of FinBert

Then, please set the parameters and weight path following the instruction in the [link](https://github.com/yya518/FinBERT/blob/master/README.md)

    labels = {0:'neutral', 1:'positive',2:'negative'}
    num_labels = 3
    vocab = "finance-uncased"
    vocab_path = 'vocab'
    pretrained_weights_path = "pretrained_weights" # this is pre-trained FinBERT weights
    fine_tuned_weight_path = "fine_tuned.pth"      # this is fine-tuned FinBERT weights
    max_seq_length = 256
    device = 'cuda:0'
    tokenizer = BertTokenizer(vocab_file = vocab_path, do_lower_case = True, do_basic_tokenize = True)

Next, we load the fine-tuned model:

    model = BertClassification(weight_path= pretrained_weights_path, num_labels=num_labels, vocab=vocab)
    model.load_state_dict(torch.load(fine_tuned_weight_path, map_location = "cuda:0"))
    model.to(device)
    
Now, we can use the FinBert model on our three sentences:
    
    sentences = [s1, s2, s3]
    model.eval()
    for sent, index in zip(sentences, range(0,3)):
        tokenized_sent = tokenizer.tokenize(sent)
        if len(tokenized_sent) > max_seq_length:
            tokenized_sent = tokenized_sent[:max_seq_length]

        ids_review  = tokenizer.convert_tokens_to_ids(tokenized_sent)
        mask_input = [1]*len(ids_review)        
        padding = [0] * (max_seq_length - len(ids_review))
        ids_review += padding
        mask_input += padding
        input_type = [0]*max_seq_length

        input_ids = torch.tensor(ids_review).to(device).reshape(-1, 256)
        attention_mask =  torch.tensor(mask_input).to(device).reshape(-1, 256)
        token_type_ids = torch.tensor(input_type).to(device).reshape(-1, 256)

        with torch.set_grad_enabled(False):
            outputs = model(input_ids, token_type_ids, attention_mask)
            outputs = F.softmax(outputs,dim=1)
            print("s" + str(i), 'FinBert score: ', labels[torch.argmax(outputs).item()])
     
The results are:
 
    s1 FinBert score:  -0.2335
    s2 FinBert score:  0.0003
    s3 FinBert score:  0.3602

### Conclusion
What has been mentioned above is the methods we use to conduct sentiment analysis on finanical reports and earnings call transcripts. If your want to know more about our further analysis on company level, industry level, and geographic level through statistics models and data visualization, please check our official repo [here](https://github.com/cuicorey/FINA4350-GroupProject).
