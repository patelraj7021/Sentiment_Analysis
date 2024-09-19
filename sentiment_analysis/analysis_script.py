# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 23:07:07 2024

@author: patel
"""

from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import os
import torch as pt

    
def embed_sequences(input_seqs, pretrained_name):
    # initialize transformer
    tokenizer = DistilBertTokenizer.from_pretrained(pretrained_name)
    model = DistilBertForSequenceClassification.from_pretrained(
        pretrained_name, output_hidden_states=True)
    # tokenize
    sequences = tokenizer(input_seqs, padding='longest', truncation=True,
                       return_tensors = 'pt')
    # embed
    model_out = model(**sequences)
    embeddings = model_out.hidden_states[-1]
    
    return sequences, model_out, embeddings
    

if __name__ == '__main__':
    
    pretrained = "distilbert-base-uncased-finetuned-sst-2-english"
    
    test_file = os.listdir('article_temp_files')[0]
    with open(os.path.join('article_temp_files', test_file), 'r') as file:
        text = file.read().split('.')
        
        
    sequences, model_output, embeddings = embed_sequences(text, pretrained) 

    # use CLS of each sequence as a summary of the sentiment of that sentence
    
    
    # bag of positive sentiment words to compare against
    pos_words = ['I have positive feelings about this.',
                 'I am optimistic.',
                 'I suggest this.', 
                 'This is a good idea.',
                 'The bird flew over the tree.']
    pos_sequences, pos_model, pos_embeddings = embed_sequences(pos_words,
                                                               pretrained)
    
    # bag of negative sentiment words
    neg_words = ['I have negative feelings about this.',  
                 'I am pessimistic.',
                 'Do not do this.',
                 'This is a bad idea.',
                 'Do you want to do this?']
    neg_sequenecs, neg_model, neg_embeddings = embed_sequences(neg_words,
                                                               pretrained)
    

    for i in range(len(pos_words)):
        print(pt.dot(pos_embeddings[0, 0, :], pos_embeddings[i, 0, :]))
        
    for i in range(len(pos_words)):
        print(pt.dot(pos_embeddings[0, 0, :], neg_embeddings[i, 0, :]))
