from nltk import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
import os
import re
from tqdm import tqdm

def load_txt (load_path, file_name):
    file = load_path + "//" + file_name
    f = open(file, 'rt',encoding='utf-8')
    text = f.read()
    f.close()
    return text

def sentence_split (text):
    return sent_tokenize(text)

def word_split (text):
    return word_tokenize(text)

def remove_non_english (token):
    words = []
    for i in range(0, len(token)):
        token[i] = re.sub(r'[^A-Za-z ]+', '', token[i])
        if token[i] != "":
            words.append(token[i])
    return words

def convert_lower (token):
    return [w.lower() for w in token]

def remove_stop (token):
    words = []
    stop_words = set(stopwords.words('english'))
    for w in token:
        if w not in stop_words:
            words.append(w)
    return words

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def lemmatize (token):
    lemmatizer = WordNetLemmatizer()
    words = []
    for w in token:
        words.append(lemmatizer.lemmatize(w, get_wordnet_pos(w)))
    return words

def convert_sentence (token):
    sentence =  ' '.join(token)
    sentence = sentence + " ."
    return sentence

def save_txt(sentence_list, save_path, save_name):
    f = open(save_path + "\\" + save_name, 'wt',encoding='utf-8')
    for sentence in sentence_list:
        f.write(sentence)
        f.write("\n")
    f.close()
    
def process (load_path, save_path):
    try:
                for i in os.listdir(load_path):
                    text = load_txt (load_path, i)
                    sentence_list = sentence_split(text)
                    new_sentence_list = []
                    for sentence in sentence_list:
                        tokens = word_split(sentence)
                        tokens = remove_non_english(tokens)
                        tokens = convert_lower(tokens)
                        tokens = remove_stop(tokens)
                        tokens = lemmatize(tokens)
                        new_sentence = convert_sentence(tokens)
                        new_sentence_list.append(new_sentence)
                    save_txt(new_sentence_list, save_path, i)
                    print('finish',i)
    except KeyboardInterrupt:
        raise

path="D:\\FINA4350\\"
industries=['Retailing',"Transportation","Automobiles and components","Consumer services","Healthcare"]

for industry in industries:
        if os.path.exists(path+industry):
            with tqdm (os.listdir(path+industry), desc = "preprocess files", ncols=80) as t:            
                for i in t:
                    load_path=path+industry+'\\'+ i+'\\'+'txt'

                    if not os.path.exists(path+industry+'\\'+ i +'\\'+'clean'):
                        os.makedirs(path+industry+'\\'+ i+ "\\"+'clean')
                    save_path=path+industry+'\\'+ i+ "\\"+'clean'

                    if __name__ == "__main__":
                        process(load_path, save_path)
            t.close()