import os
import copy
import numpy as np
import pandas as pd
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import lr_scheduler
from torch.utils.data import Dataset, DataLoader
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM, BertConfig
from bertModel import BertClassification, dense_opt
from datasets import text_dataset, financialPhraseBankDataset
#import argparse
#from sklearn.metrics import f1_score
from tqdm import tqdm

def covid_in(covid_list, token_sentence):
    for i in token_sentence:
        if i in covid_list:
            return True
    return False

def analyze_txt (file_path, covid_list):
    score_list = []
    with open(file_path,'r',encoding='utf-8') as f:
        line = f.readline().strip("\n")
        while line:
            token_sentence = tokenizer.tokenize(line)
            if covid_in(covid_list, token_sentence):
                score_list.append(bert_score(token_sentence, max_seq_length, tokenizer))                 
            line = f.readline().strip("\n") 
    f.close()
    if len(score_list) == 0:
        return 0, 0
    return len(score_list), sum(score_list) / len(score_list) 

def bert_score(token_sentence, max_seq_length, tokenizer):
    if len(token_sentence) > max_seq_length:
        token_sentence = token_sentence[:max_seq_length]
    ids_review  = tokenizer.convert_tokens_to_ids(token_sentence)
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
    return (outputs[0][1] - outputs[0][2]).item()

def main (out_df, column_name, covid_list, folder_path, out_path):
    with tqdm (os.listdir(folder_path), desc = "FinBert_Analysis", ncols=80) as t:
        try:
            for i in t:
                result = [i]
                covid_number, bert_score = analyze_txt(folder_path + "//" + i, covid_list)
                result.append(covid_number)
                result.append(bert_score)
                result_series = pd.Series(result, index = column_name)
                out_df.append(result_series, ignore_index = True)
        except KeyboardInterrupt:
            t.close()
            raise
    t.close()
    out_df.to_csv(out_path, index = False)
    
if __name__ == "__main__":
    
    labels = {0:'neutral', 1:'positive',2:'negative'}
    num_labels = len(labels)
    vocab = "finance-uncased"
    vocab_path = '/data/corey/FinBert/vocab'
    pretrained_weights_path = "/data/corey/FinBert/pretrained_weights" # this is pre-trained FinBERT weights
    fine_tuned_weight_path = "/data/corey/FinBert/fine_tuned.pth"      # this is fine-tuned FinBERT weights
    max_seq_length = 256
    device='cuda:0'
    model = BertClassification(weight_path = pretrained_weights_path, num_labels=num_labels, vocab=vocab)
    model.load_state_dict(torch.load(fine_tuned_weight_path, map_location = "cuda:0"))
    model.to(device)
    model.eval()
    tokenizer = BertTokenizer(vocab_file = vocab_path, do_lower_case = True, do_basic_tokenize = True)
    column_name = ['file_name', "COVID_number", "FinBert_score"]
    out_df = pd.DataFrame(columns = column_name)
    covid_list=['covid','sarscov','coronavirus','ncov']
    
    main(out_df, column_name, covid_list, "trans1", "trans1.csv")
