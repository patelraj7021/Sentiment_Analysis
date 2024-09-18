# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 17:16:26 2024

@author: patel
"""

import scrapy
import re
import os

class ArticleSpider(scrapy.Spider):
    # crawl through articles to get text
    name = 'article'
    
    
    def __init__(self, url_in, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        self.start_url = url_in
    
    def start_requests(self):
        yield scrapy.Request(self.start_url, meta={'playwright': True})
        
    def parse(self, response):
        # get title
        title = response.xpath(
            '//h1[@data-test-locator="headline"]/text()').get()
        title = re.sub(r'\W+', '', title)
        title = re.sub('\s+', '_', title)
        # get text
        text = response.xpath(
            '//div[@class="caas-body"]//text()').extract()
        text_filepath = os.path.join('article_temp_files', title + '.log')
        with open(text_filepath, 'a') as file:
            for p in text:
                file.write(p + '\n')
            