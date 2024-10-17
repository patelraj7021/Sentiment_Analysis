


class ArticleRecord:
    def __init__(self, ticker, title, date, link, pos_score, neg_score, overall_rating):
        self.ticker = ticker
        self.title = title
        self.date = date
        self.link = link
        self.pos_score = pos_score
        self.neg_score = neg_score
        self.overall_rating = overall_rating