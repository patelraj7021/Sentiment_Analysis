# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 17:35:52 2024

@author: patel
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sys


def crawl_ticker(ticker):
    # call spider and save files in article_temp_files

    # call spider
    yahoo_finance_url = 'https://finance.yahoo.com/quote/'
    process = CrawlerProcess(get_project_settings())   
    process.crawl('article_text', 
                  url_in=yahoo_finance_url + ticker.upper() + '/')       
    process.start(install_signal_handlers=False)

    return 


if __name__ == '__main__':
    # the scrapy crawlers need to be called this way to work around
    # twisted reactor limitations
    # get parameter from command line input
    function = getattr(sys.modules[__name__], sys.argv[1])
    ticker = sys.argv[2]
    crawl_ticker(ticker)