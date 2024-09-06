# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 20:10:38 2024

@author: patel
"""

import scrapy



class LinksSpider(scrapy.Spider):
    # crawl through Yahoo main ticker page to get links for recent articles
    name = 'links'
        
    
    def __init__(self, url_in, *args, **kwargs):
        super(LinksSpider, self).__init__(*args, **kwargs)
        self.start_url = url_in
    
    def start_requests(self):
        yield scrapy.Request(self.start_url, meta={'playwright': True})
           
    def parse(self, response):
        # get links
        recent_news_links = response \
            .xpath('//section[@data-testid="storyitem"]/a/@href').getall()
        # store links
        with open('links.log', 'w') as file:
            for link in recent_news_links:
                file.write(link + '\n')