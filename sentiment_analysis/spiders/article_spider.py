# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 20:10:38 2024

@author: patel
"""

import scrapy
from pathlib import Path


class ArticleSpider(scrapy.Spider):
    name = 'articles'
        
    
    def start_requests(self):
        url = "https://finance.yahoo.com/quote/NVDA/"
        yield scrapy.Request(url, meta={'playwright': True})
    
        
    def parse(self, response):
        ticker_name = response.url.split("/")[-1]
        filename = f"articles-{ticker_name}.html"
        recent_news_section = response \
            .xpath('//section[@data-testid="storyitem"]/a/@href') \
                .get(default='not_found')
        print('********************')
        print('********************')
        print('********************')
        print(recent_news_section)
        print('********************')
        print('********************')
        print('********************')