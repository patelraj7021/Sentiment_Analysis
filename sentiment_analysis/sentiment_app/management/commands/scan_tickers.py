from django.core.management.base import BaseCommand
from sentiment_app.models import Articles
from analysis_module import crawling_wrapper, analyze_article
import os

class Command(BaseCommand):
    help = 'Scrapes and analyzes articles for the predefined list of tickers to update everyday'
    
    def handle(self, *args, **kwargs):
        with open('sp500_tickers.csv', 'r') as file:
            tickers = file.read().split('\n')
        with open('completed_tickers.log', 'w') as file:
            file.write('Scanning list...')
        for ticker in tickers:
            # crawl articles
            print('Scraping for ' + ticker + '...')
            data_filepath = crawling_wrapper(ticker)
            print('Finished scraping')
            num_articles = len(os.listdir(data_filepath))
            print('Saving data for ' + str(num_articles) + ' articles for ' + ticker + '...')
            active_article_num = 1
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
                print('Article '+ str(active_article_num) + '/' + str(num_articles) + ' completed')
                active_article_num = active_article_num + 1
            with open('completed_tickers.log', 'a') as file:
                print('Finished scrape and data save for ' + ticker)
                file.write(ticker + '\n')