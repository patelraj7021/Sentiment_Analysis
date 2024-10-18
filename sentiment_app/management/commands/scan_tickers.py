from django.core.management.base import BaseCommand
from sentiment_app.models import Articles
from analysis_module import crawling_wrapper, analyze_article
import os
from random import choice, randint
from time import sleep


class Command(BaseCommand):
    help = 'Scrapes and analyzes articles for the predefined list of tickers to update everyday'
    
    def handle(self, *args, **kwargs):
        
        tickers_all_file = 'sp500_tickers.csv'
        tickers_completed_file = 'completed_tickers.log'
        
        with open(tickers_all_file, 'r') as file:
            tickers_all = file.read().split('\n')
        with open(tickers_completed_file, 'r') as file:
            tickers_completed = file.read().split('\n')
        tickers_queue = list(set(tickers_all) - set(tickers_completed))
        print(str(len(tickers_queue)) + ' tickers added to queue')
        while len(tickers_queue) > 0:
            # sleep a random amount of time before each ticker is processed
            wait_time = randint(1, 30)
            print('Waiting for ' + str(wait_time) + ' seconds...')
            sleep(wait_time)
            # pick a random ticker from the queue
            ticker = choice(tickers_queue)
            # crawl articles
            print('Scraping for ' + ticker + '...')
            data_filepath = crawling_wrapper(ticker)
            print('Finished scraping')
            num_articles = len(os.listdir(data_filepath))
            if num_articles == 0:
                # scraping has failed - do not continue with rest of code
                # keep the ticker in the queue so scraping can try again
                print('Scraping failed: no articles found')
                print('Continuing to next ticker...')
                continue 
            print('Saving data for ' + str(num_articles) + ' articles for ' + ticker + '...')
            active_article_num = 1
            # get text from each article and run analysis
            for article_file in os.listdir(data_filepath):
                with open(os.path.join(data_filepath, article_file), 'r') as file:
                    data_input = file.read().split('\n')
                # get link from article data file
                article_link = data_input[1]
                # search if article already exists in database
                # from previous analysis runs
                query = Articles.objects.filter(link=article_link, ticker=ticker)
                if not query.exists():                   
                    # only run analysis and add article if it doesn't
                    article_analysis = analyze_article(data_input, ticker)
                    if article_analysis is not None:
                        new_record = Articles(ticker=ticker, 
                                                title=article_analysis.title,
                                                date=article_analysis.date,
                                                link=article_analysis.link,
                                                pos_score=article_analysis.pos_score,
                                                neg_score=article_analysis.neg_score,
                                                overall_rating=article_analysis.overall_rating)
                        new_record.save()
                    print('Article '+ str(active_article_num) + '/' + str(num_articles) + ' saved')
                else:
                    print('Article '+ str(active_article_num) + '/' + str(num_articles) + ' already exists')
                active_article_num = active_article_num + 1
            with open(tickers_completed_file, 'a') as file:
                print('Finished scrape and data save for ' + ticker)
                file.write(ticker + '\n')
            tickers_queue.remove(ticker)
        # clear completed tickers log file when all tickers have been analyzed
        with open(tickers_completed_file, 'w') as file:
            file.write('')