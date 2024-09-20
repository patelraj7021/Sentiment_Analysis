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
    
    # delete log folder from previous code executions
    # create folder
    temp_filepath = os.path.join(os.getcwd(), 'article_temp_files')
    if os.path.exists(temp_filepath):
        shutil.rmtree(temp_filepath)
    os.makedirs(temp_filepath)

    process = CrawlerProcess(get_project_settings())   
    process.crawl('article_text', 
                  url_in='https://finance.yahoo.com/quote/' + \
                      ticker.upper() + '/')       
    process.start()
    return 
    

