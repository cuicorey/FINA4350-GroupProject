from nltk import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
import os
import re
from tqdm import tqdm

def load_txt (load_path, file_name):
    file = load_path + "/" + file_name
    print(file)
    f = open(file, 'rt',encoding='utf-8')
    text = f.readlines()
    endline = 0
    cc = 0
    for i in text:
        cc = cc+1
        if i.lower().strip().startswith("copyright") and i.lower().strip().endswith("all rights reserved."):
            endline = cc
        if i.lower().strip().startswith("these materials have been prepared solely for information purposes"):
            break
    text_true = ""
    cc = 0
    st = False
    page = False
    checkst = False
    for i in text:
        cc = cc+1
        if i.lower().strip() == "presentation":
            checkst = True
        if checkst == True and i.strip() == "":
            checkst = False
            st = True
        if i.lower().strip().startswith("copyright") and i.lower().strip().endswith("all rights reserved."):
            page = True
        if page == True and i.strip() == "":
            page = False
        if cc == endline:
            break
        if st == True and page == False:
            text_true = text_true + i

    f.close()
    return text_true

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
    f = open(save_path + "/" + save_name, 'wt',encoding='utf-8')
    for sentence in sentence_list:
        f.write(sentence)
        f.write("\n")
    f.close()

def process (load_path, save_path):
    try:
        with tqdm (os.listdir(load_path), desc = "preprocess files", ncols=80) as t:
                for i in t:
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
    except KeyboardInterrupt:
        t.close()
        raise
    t.close()

if __name__ == "__main__":
    process(r"/Users/cky/Desktop/NLP/raw_transcript_txt",r"/Users/cky/Desktop/NLP/preprocessed_transcript_txt")
