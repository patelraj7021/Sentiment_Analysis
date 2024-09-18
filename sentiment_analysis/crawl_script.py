# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 17:35:52 2024

@author: patel
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.article_text_spider import ArticleTextSpider
import shutil
import os



# delete log files from previous code executions
# temp_filepath = os.path.join(os.getcwd(), 'article_temp_files')
# shutil.rmtree(temp_filepath, ignore_errors=True) # pass if folder not present


process = CrawlerProcess(get_project_settings())

process.crawl('article_text', url_in='https://finance.yahoo.com/quote/TSLA/')
   
process.start()
    