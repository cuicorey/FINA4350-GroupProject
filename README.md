# NLP Analysis: Business Impact of COVID-19 :boom:
This is the official repository of NLP Young OG's group project in FINA 4350.

## Group Members
Chen Kangyi, Kevin (3035447776)   
Cui Jinze, Corey (3035447922)  
Li Jiaying, Minnie (3035447348)    
Qu Yiyang, Yvonne (3035447623)  
Wu Shaoyi, Sophie (3035330179)   

## Code
* [scraping](https://github.com/cuicorey/FINA4350-GroupProject/tree/master/scraping) contains the code for web-scraping
  * [get_files.py](https://github.com/cuicorey/FINA4350-GroupProject/blob/master/scraping/get_files.py): download financial reports and earnings transcripts from Capital IQ 
  * [get_location.py](https://github.com/cuicorey/FINA4350-GroupProject/blob/master/scraping/get_location.py): get the location of companies from Yahoo Finance
* [preprocessing](https://github.com/cuicorey/FINA4350-GroupProject/tree/master/preprocess) contains the code for preprocessing
  * [convert_format.py](https://github.com/cuicorey/FINA4350-GroupProject/blob/master/preprocess/convert_format.py): convert the files from doc. to txt.
  * [preprocess_transcript.py](https://github.com/cuicorey/FINA4350-GroupProject/blob/master/preprocess/preprocess_transcript.py): preprocess earnings transcript
  * [preprocess_report.py](https://github.com/cuicorey/FINA4350-GroupProject/blob/master/preprocess/preprocess_report.py): preprocess financial report
* [NLP_analysis](https://github.com/cuicorey/FINA4350-GroupProject/tree/master/preprocess) contains the code for calculating the features using NLP
  * [dictionary_analysis.py](https://github.com/cuicorey/FINA4350-GroupProject/tree/master/NLP_analysis/dictionary_analysis.py): calculate the dictionary-based features
  * [textblob_vader_analysis.py](https://github.com/cuicorey/FINA4350-GroupProject/tree/master/NLP_analysis/textblob_vader_analysis.py): calculate the TB and VD scores
  * [finbert_analysis.py](https://github.com/cuicorey/FINA4350-GroupProject/tree/master/NLP_analysis/finbert_analysis.pp): calculate the FinBert score
* [result_analysis.py](https://github.com/cuicorey/FINA4350-GroupProject/tree/master/result_analysis): contains the code for analyzing the NLP results
  * [company_price.py](https://github.com/cuicorey/FINA4350-GroupProject/tree/master/result_analysis/company_price.py): process the company stock price
  * [company_analysis.py](https://github.com/cuicorey/FINA4350-GroupProject/tree/master/result_analysis/company_analysis.py): conduct the company level analysis
  * [industry_analysis.py](https://github.com/cuicorey/FINA4350-GroupProject/tree/master/result_analysis/industry_analysis.py): conduct the industry level analysis
  
 ## Blog
 * [docs](https://github.com/cuicorey/FINA4350-GroupProject/tree/master/docs): contains the files for our blog  
 You can view our blog by this [link](https://cuicorey.github.io/FINA4350-GroupProject)
  
## Data
* Google Drive [link](https://drive.google.com/drive/folders/1Ltfqh9F3jhXMVTxKootUZbzKBf59f0_P?usp=sharing) to our dataset
