import os
from sentiment_app.models import Articles
from analysis_module import analyze_article, crawling_wrapper


def query_ticker(ticker):
    # crawl articles
    print('Scraping for ' + ticker + '...')
    data_filepath = crawling_wrapper(ticker)
    print('Finished scraping')
    num_articles = len(os.listdir(data_filepath))
    if num_articles == 0:
        # scraping has failed - do not continue with rest of code
        # keep the ticker in the queue so scraping can try again
        raise RuntimeError('Scraping failed: no articles found\nContinuing to next ticker...')
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
            try:
                article_analysis = analyze_article(data_input, ticker)
            except:
                continue
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
    return