# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 17:35:52 2024

@author: patel
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import shutil
import os


def crawl_ticker(ticker):
    # call spider and return filepath where article text is stored
    
    # delete log folder from previous code executions
    # create folder
    data_filepath = os.path.join(os.getcwd(), 'article_temp_files')
    if os.path.exists(data_filepath):
        shutil.rmtree(data_filepath)
    os.makedirs(data_filepath)

    # call spider
    yahoo_finance_url = 'https://finance.yahoo.com/quote/'
    process = CrawlerProcess(get_project_settings())   
    process.crawl('article_text', 
                  url_in=yahoo_finance_url + ticker.upper() + '/')       
    process.start()

    return data_filepath