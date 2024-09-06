# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 17:16:26 2024

@author: patel
"""

import scrapy



class ArticleSpider(scrapy.Spider):
    # crawl through articles to get text
    name = 'article'
    
    
    def __init__(self, url_in, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        self.start_url = url_in
    
    def start_requests(self):
        yield scrapy.Request(self.start_url, meta={'playwright': True})
        
    def parse(self, response):
        # get continue reading link if it exists
        title = response \
            .xpath('//h1[@data-test-locator="headline"]/text()').getall()
        with open('debug.log', 'a') as file:
            file.write(title[0] + '\n')
        # continue_link = response. \
        #     xpath('//div[@class="caas-readmore caas-readmore-collapse"] \
        #           /a/@href').get()
        # if continue_link is not None:
        #     with open('debug.log', 'a') as file:
        #         file.write('continue_link')