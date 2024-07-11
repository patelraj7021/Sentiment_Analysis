# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 20:10:38 2024

@author: patel
"""

import scrapy
from pathlib import Path


class ArticleSpider(scrapy.Spider):
    name = 'articles'
    
    start_urls = ['https://ca.finance.yahoo.com/quote/NVDA/']
        
        
    def parse(self, response):
        page_name = response.url.split("/")[-2]
        filename = f"quotes-{page_name}.html"
        Path(filename).write_bytes(response.body)