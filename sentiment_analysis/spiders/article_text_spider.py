# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 20:10:38 2024

@author: patel
"""

import scrapy
import re
import os



class ArticleTextSpider(scrapy.Spider):
    name = 'article_text'
        
    
    def __init__(self, url_in, *args, **kwargs):
        super(ArticleTextSpider, self).__init__(*args, **kwargs)
        self.start_url = url_in
    
    def start_requests(self):
        yield scrapy.Request(self.start_url, meta={'playwright': True})
           
    def parse(self, response):
        # crawl through Yahoo main ticker page to get links for recent articles
        # get links
        recent_news_links = response \
            .xpath('//section[@data-testid="storyitem"]/a/@href').getall()
        # store links
        with open('links.log', 'w') as file:
            for link in recent_news_links:
                file.write(link + '\n')
                yield scrapy.Request(link, callback=self.article_parse, 
                                     meta={'playwright': True})
                
    def article_parse(self, response):
        # crawl through article page to get text
        # get title
        raw_title = response.xpath('//h1[@data-test-locator="headline"]/text()').get()
        cleaned_title = re.sub(r'\s+', '_', raw_title)
        cleaned_title = re.sub(r'\W+', '', cleaned_title)
        # get date
        date = response.xpath('//div[@class="caas-attr-time-style"]/time/@datetime').get()
        # get text
        text = response.xpath('//div[@class="caas-body"]//text()').extract()
        text = ' '.join(text)
        text_filepath = os.path.join('article_temp_files', 
                                     cleaned_title + '.log')
        with open(text_filepath, 'w') as file:
            file.write(date  + '.\n' +
                       raw_title + '.\n' +
                       response.text)