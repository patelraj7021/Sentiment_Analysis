from django.core.management.base import BaseCommand
from query_ticker import query_ticker
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
            try:
                query_ticker(ticker)
            except:
                continue
            with open(tickers_completed_file, 'a') as file:
                print('Finished scrape and data save for ' + ticker)
                file.write(ticker + '\n')
            tickers_queue.remove(ticker)
        # clear completed tickers log file when all tickers have been analyzed
        with open(tickers_completed_file, 'w') as file:
            file.write('')