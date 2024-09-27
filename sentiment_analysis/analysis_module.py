# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 23:07:07 2024

@author: patel
"""

from transformers import DistilBertTokenizer, DistilBertForSequenceClassification 
import os
import torch as pt
from torch.nn.functional import normalize
import numpy as np
from .crawl_module import crawl_ticker

    
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


def compare_text(embeddings):
    # bag of positive sentiment words to compare against
    pos_words = ['positive',
                 'optimistic',
                 'hopeful']
    pos_sequences, pos_model, pos_embeddings = embed_sequences(pos_words)
    
    # bag of negative sentiment words, must be same num as pos_words
    neg_words = ['negative',  
                 'pessimistic',
                 'cautious']
    neg_sequences, neg_model, neg_embeddings = embed_sequences(neg_words)

    num_sentences = embeddings.shape[0]
    num_comp_words = pos_embeddings.shape[0]

    pos_scores = []
    neg_scores = []
    # compare each sentence with each pos / neg word
    # save the mean of dot products of sentence with each pos / neg word
    for i in range(num_sentences):
        pos_scores_sentence = []
        neg_scores_sentence = []        
        for j in range(num_comp_words):
            # normalize all vectors so only direction is used for comparison
            norm_pos_embedding = normalize(pos_embeddings[j, 0, :])
            norm_neg_embedding = normalize(neg_embeddings[j, 0, :])
            norm_sent_embedding = normalize(embeddings[j, 0, :])
            # comparison score is relative to highest possible for a word
            # highest possible is word dot product with itself
            # lowest allowed score is 0
            pos_score_sentence = max(int(pt.dot(norm_sent_embedding, norm_pos_embedding).item()*100), 0)
            neg_score_sentence = max(int(pt.dot(norm_sent_embedding, norm_neg_embedding).item()*100), 0)
            # save pos/neg scores compared to each word for sentence
            pos_scores_sentence.append(pos_score_sentence)
            neg_scores_sentence.append(neg_score_sentence)
        # save mean of sentence score vs each pos/neg word
        pos_scores.append(np.mean(pos_scores_sentence))
        neg_scores.append(np.mean(neg_scores_sentence))

    # return mean of pos and neg scores for each sentence
    return np.mean(pos_scores), np.mean(neg_scores)


def analyze_ticker(data_filepath):
    ticker_pos_scores = []
    ticker_neg_scores = []
    ticker_pos_neg_fracs = []
    # analyze each article file and save its pos and neg scores
    for data_file in os.listdir(data_filepath):
        with open(os.path.join(data_filepath, data_file), 'r') as file:
            text = file.read().split('.')
            sequences, model_output, embeddings = embed_sequences(text)
            article_pos_score, article_neg_score = compare_text(embeddings)
            ticker_pos_scores.append(int(article_pos_score))
            ticker_neg_scores.append(int(article_neg_score))
            ticker_pos_neg_frac = int(article_pos_score * 100 / (article_pos_score+article_neg_score))
            ticker_pos_neg_fracs.append(ticker_pos_neg_frac)

    return ticker_pos_scores, ticker_neg_scores, ticker_pos_neg_fracs


def analysis_wrapper(ticker):
    # web scraping
    data_filepath = crawl_ticker(ticker)
    # analysis 
    result = analyze_ticker(data_filepath)
    return result