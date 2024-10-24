# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 23:07:07 2024

@author: patel
"""

from transformers import DistilBertTokenizer, DistilBertForSequenceClassification 
import os
import shutil
import torch as pt
from torch.nn.functional import normalize
import numpy as np
from article_record_class import ArticleRecord
import re
import subprocess

    
def embed_sequences(input_seqs):   
    # initialize transformer and model
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
    
    return embeddings


def batched_compare_text(batched_text):
    # bag of positive sentiment words to compare against
    pos_words = ['positive',
                 'optimistic',
                 'hopeful']
    pos_embeddings = embed_sequences(pos_words)
    
    # bag of negative sentiment words, must be same num as pos_words
    neg_words = ['negative',  
                 'pessimistic',
                 'cautious']
    neg_embeddings = embed_sequences(neg_words)
    
    all_pos_scores = []
    all_neg_scores = []
    for batch in batched_text:
        embeddings = embed_sequences(batch)
        pos_scores, neg_scores = compare_text(embeddings, 
                                              pos_embeddings, neg_embeddings)
        # embeddings can take up a large amount of memory
        del embeddings 
        all_pos_scores = all_pos_scores + pos_scores
        all_neg_scores = all_neg_scores + neg_scores
    article_mean_pos_score = np.mean(all_pos_scores)
    article_mean_neg_score = np.mean(all_neg_scores)
    # embeddings can take up a large amount of memory
    del pos_embeddings
    del neg_embeddings
    return article_mean_pos_score, article_mean_neg_score


def compare_text(embeddings, pos_embeddings, neg_embeddings):

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
            norm_pos_embedding = normalize(pos_embeddings[j, 0, :], dim=0)
            norm_neg_embedding = normalize(neg_embeddings[j, 0, :], dim=0)
            norm_sent_embedding = normalize(embeddings[i, 0, :], dim=0)
            # comparison score is relative to highest possible for a word
            # highest possible is word dot product with itself, i.e., 1.0
            pos_score_sentence = pt.dot(norm_sent_embedding, norm_pos_embedding).item()
            neg_score_sentence = pt.dot(norm_sent_embedding, norm_neg_embedding).item()
            # save pos/neg scores compared to each word for sentence
            pos_scores_sentence.append(pos_score_sentence)
            neg_scores_sentence.append(neg_score_sentence)
        # save mean of sentence vs each pos/neg word
        pos_scores.append(np.mean(pos_scores_sentence))
        neg_scores.append(np.mean(neg_scores_sentence))

    # return pos and neg scores for each sentence
    return pos_scores, neg_scores


def batch_text(text, num_in_batch):
    start = 0
    end = len(text)
    step = num_in_batch
    batched_list = []
    for i in range(start, end, step):
        batched_list.append(text[i:i+step])
    return batched_list


def analyze_article(data_input, ticker):
    # get meta data from file
    article_date = data_input[0]
    article_link = data_input[1]
    article_title = data_input[2]
    # split each sentence on punctuation
    text = [article_title] + re.split(r'[!.?]\s*', data_input[3])
    if len(text) < 7:
        # some articles have a paywall that only shows first few sentences
        # don't include these in analysis
        raise RuntimeError('Skipping article: not enough data')
    # batch text
    num_in_batch = 10
    batched_text = batch_text(text, num_in_batch)
    article_pos_score, article_neg_score = batched_compare_text(batched_text)
    new_record = ArticleRecord(ticker, 
                               title=article_title, 
                               date=article_date,
                               link=article_link,
                               pos_score=article_pos_score,
                               neg_score=article_neg_score,
                               # overall_rating will be calculated in the django view later
                               # it depends on aggregrate score values that aren't accessible here
                               overall_rating=0.0) 

    return new_record


def crawling_wrapper(ticker):
    # web scraping

    # delete log folder from previous code executions
    data_filepath = os.path.join(os.getcwd(), 'article_temp_files')
    if os.path.exists(data_filepath):
        shutil.rmtree(data_filepath)
    # create folder
    os.makedirs(data_filepath)
    
    # this next line is not ideal
    # but it needs to be done in this way because scrapy's twisted reactors
    # can't be restarted after stopping
    # so users would be unable to query a different ticker after querying a first one
    # running it as a subprocess that ends after dumping crawling data in a folder works
    # since it runs under a different python process
    subprocess.run(['python', 'web_scraping/crawl_module.py', 'crawl_ticker', ticker])
    
    return data_filepath