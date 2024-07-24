# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 17:16:26 2024

@author: patel
"""

import scrapy



class ArticleSpider(scrapy.Spider):
    name = 'article'
    
    
    def start_requests(self):
        url = "https://finance.yahoo.com/quote/NVDA/"
        yield scrapy.Request(url, meta={'playwright': True})
    
        
    def parse(self, response):
        # get continue reading link if it exists
        continue_link = response. \
            xpath('//div[@class="caas-readmore caas-readmore-collapse"] \
                  /a/@href')