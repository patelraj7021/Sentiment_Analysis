# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 17:35:52 2024

@author: patel
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.links_spider import LinksSpider
from spiders.article_spider import ArticleSpider



process = CrawlerProcess(get_project_settings())
process.crawl('links', url_in='https://finance.yahoo.com/quote/NVDA/')
process.start()
