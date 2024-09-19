# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 23:07:07 2024

@author: patel
"""

from transformers import AutoTokenizer, TFBertModel
import pandas as pd
import tensorflow as tf
from sklearn.decomposition import PCA
import os

    
def preprocess_article_text(text):
    
    
    return
    

if __name__ == '__main__':
    
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
    model = TFBertModel.from_pretrained('bert-base-cased')

    test_file = os.listdir('article_temp_files')[0]
    with open(os.path.join('article_temp_files', test_file), 'r') as file:
        text = file.read().split('.')
        
    sequences = tokenizer(text, padding='longest', truncation=True,
                          return_tensors='tf')
    output = model(sequences)
    embeddings = output.last_hidden_state
    # reduced_embeddings = PCA(n_components=10)
    # reduced_embeddings.fit(embeddings)
    # print(reduced_embeddings.explained_variance_ratio)
    