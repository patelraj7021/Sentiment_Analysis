# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 23:07:07 2024

@author: patel
"""

from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import os

    
def embed_sequences(input_seqs):
    
    # initialize transformer
    pretrained_name = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = DistilBertTokenizer.from_pretrained(pretrained_name,
                                                    clean_up_tokenization_spaces=True)
    model = DistilBertForSequenceClassification.from_pretrained(pretrained_name, 
                                                                output_hidden_states=True)
    
    # tokenize
    sequences = tokenizer(input_seqs, padding='longest', truncation=True,
                          return_tensors = 'pt')
    
    # embed
    model_out = model(**sequences)
    embeddings = model_out.hidden_states[-1]
    
    return sequences, model_out, embeddings
    

if __name__ == '__main__':
    
    
    
    test_file = os.listdir('article_temp_files')[0]
    with open(os.path.join('article_temp_files', test_file), 'r') as file:
        text = file.read().split('.')
        
        
    sequences, model_output, embeddings = embed_sequences(text) 
    
    
    # bag of positive sentiment words to compare against
    pos_words = ['positive',
                 'optimistic',
                 'hopeful'
                 ]
    pos_sequences, pos_model, pos_embeddings = embed_sequences(pos_words)
    
    # bag of negative sentiment words
    neg_words = ['negative',  
                 'pessimistic',
                 'cautious']
    neg_sequences, neg_model, neg_embeddings = embed_sequences(neg_words)
