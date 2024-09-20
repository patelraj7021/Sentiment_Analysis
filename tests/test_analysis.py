# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 18:53:41 2024

@author: patel
"""

import sys
import os
import pytest
sys.path.append(os.path.dirname(os.getcwd()))
from sentiment_analysis import analysis_script as a_s
import torch as pt
import numpy as np



@pytest.fixture
def create_pos_word_embeddings():
    # bag of positive sentiment words to compare against
    pos_words = ['positive',
                 'optimistic',
                 'hopeful'
                 ]
    pos_sequences, pos_model, pos_embeddings = a_s.embed_sequences(pos_words)
    
    return pos_sequences, pos_model, pos_embeddings


@pytest.fixture
def create_neg_word_embeddings():
    # bag of negative sentiment words
    neg_words = ['negative',  
                 'pessimistic',
                 'cautious']
    neg_sequences, neg_model, neg_embeddings = a_s.embed_sequences(neg_words)
    
    return neg_sequences, neg_model, neg_embeddings


def dot_product_identity_comparison(embeddings):
    # helper func for test_identity_correlation
    result = True
    num_words = embeddings.shape[0]
    for i in range(num_words):
        prods_list = []
        for j in range(num_words):
            prod = pt.dot(embeddings[i, 0, :], embeddings[j, 0, :]).item()
            prods_list.append(prod)
        if np.argmax(prods_list) != i:
            result = False
    return result


def dot_product_differing_comparision(embeddings_same, embeddings_different):
    # helper func for test_differing_correlation
    result = True
    num_words = embeddings_same.shape[0]
    for i in range(num_words):
        pos_prods = []
        neg_prods = []
        for j in range(num_words):
            neg_prod = pt.dot(embeddings_same[i, 0, :], embeddings_different[j, 0, :]).item()
            pos_prod = pt.dot(embeddings_same[i, 0, :], embeddings_same[j, 0, :]).item()
            pos_prods.append(pos_prod)
            neg_prods.append(neg_prod)
        if max(neg_prods) >= min(pos_prods):
            result = False
    return result
    

class TestTokenComparison:
    
    def test_identity_correlation(self, create_pos_word_embeddings,
                                 create_neg_word_embeddings):
        # dot product value should be highest when
        # a vector is compared to itself
        pos_sequences, pos_model, pos_embeddings = create_pos_word_embeddings
        neg_sequences, neg_model, neg_embeddings = create_neg_word_embeddings
        
        pos_result = dot_product_identity_comparison(pos_embeddings)
        neg_result = dot_product_identity_comparison(neg_embeddings)
        
        assert pos_result and neg_result
        
    def test_differing_correlation(self, create_pos_word_embeddings,
                                   create_neg_word_embeddings):
        # dot product values should be lower for vectors
        # belonging to the opposite class of sentiment
        # min(same class prod) > max(opposite class prod)
        pos_sequences, pos_model, pos_embeddings = create_pos_word_embeddings
        neg_sequences, neg_model, neg_embeddings = create_neg_word_embeddings
        
        pos_test = dot_product_differing_comparision(pos_embeddings, neg_embeddings)
        neg_test = dot_product_differing_comparision(neg_embeddings, pos_embeddings)
        
        assert pos_test and neg_test
    
    