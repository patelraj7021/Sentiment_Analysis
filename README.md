# Sentiment Analysis of Articles for a Stock

### Project Reflection
After several months of development, I've decided to discontinue this stock sentiment analysis project due to significant technical challenges around autonomous web scraping. 
Yahoo Finance was chosen as a single, consistent data source, however it proved difficult to reliably extract article content at scale.
In particular, Yahoo Finance's HTML structure changes periodically, breaking scrapers and requiring constant maintenance. 

Despite these roadblocks, I achieved my primary objective: expanding my technical skillset.
I gained hands-on expertise with Django server design, building REST APIs, creating dynamic frontend interfaces with React, and AWS deployment using EC2 instances and RDS databases. 
While I'm shelving this project, the technical skills and architectural knowledge I've developed will stay with me and position me to succeed in future projects.

---

### Objective

Public opinion plays a key role in stock pricing.
Therefore, assessing the market's sentiment about a given stock is a fundamental step an informed investor must make through manual effort before making investment decisions.
News articles from industry professionals are well-established and credible sources of information for investors.
With a wealth of articles available for frequently traded stocks though, it is time-consuming and monotonous for a retail investor to track the sentiment of industry professionals on a regular basis.

This project aims to address this issue by automating the market research and analysis pipeline for retail investors.
Advances in large language model (LLM) architectures in recent years have enabled precise and context-informed quantifications of text, allowing for the sentiment of an article to be understood by a machine.
By leveraging a LLM, the overall sentiment of a stock can be assessed and delivered to users, as well as links to the most positive/negative articles and the sentiment trend over a period of time.
To facilitate ease of use, the analyzer is deployed as a web app accessible through a browser.

This project does not aim to explicitly quantify the correlation between public opinion and stock prices, or to predict price variations in any way.
It is a tool for investors to use to quickly assess sentiment for a stock and to discover relevant articles for informed decision-making.

[1] Yaya Su, Yi Qu, Yuxuan Kang. Online public opinion and asset prices: a literature review. Data Science in Finance and Economics, 2021, 1(1): 60-76. doi: 10.3934/DSFE.2021004

[2] Das N, Sadhukhan B, Chatterjee T, Chakrabarti S. Effect of public sentiment on stock market movement prediction during the COVID-19 outbreak. Soc Netw Anal Min, 2022, 12(1):92. doi:10.1007/s13278-022-00919-3

[3] Yin Ni, Zeyu Su, Weiran Wang, Yuhang Ying. A novel stock evaluation index based on public opinion analysis. Procedia Computer Science, 2019, 147: 581-587. doi: doi.org/10.1016/j.procs.2019.01.212.

[4] Chen Meilan , Guo Zhiying , Abbass Kashif , Huang Wenfeng. Analysis of the impact of investor sentiment on stock price using the latent dirichlet allocation topic model. Frontiers in Environmental Science, 2022(10). doi: 10.3389/fenvs.2022.1068398

### Components

#### Web Scraping / Data Collection

Yahoo Finance provides news aggregation for a given stock, making it a readily accessible source of articles to use for sentiment analysis.
This project uses the Python web scraping framework Scrapy to extract article text from the "Recent News" section of a stock page on Yahoo Finance.
The text is processed and separated into sentence-long sequences for the sentiment analysis itself.

#### Transformed-Powered Sentiment Analysis

HuggingFace offers many pretrained LLMs designed to serve different applications.
This project uses a version of the DistilBERT model, a transformer-based model designed for use in sequence classification, making it an excellent fit for this task.
Sentences are embedded in a vector space where vectors (i.e., words or sentences) of a similar nature point in the same direction.
A (normalized) dot product between two vectors quantifies how similar they are, and so taking the dot product between a sentence embedding and a predefined ''positive'' (or negative) word embedding, like ''optimistic'', returns a scalar value that measures how ''optimistic'' that sentence is.

#### Database

Automated scans of tickers are performed daily, and sentiment analysis results are stored in a database on AWS's RDS.

#### Web App

Django and React are used for the back and front end of the web app.
The server runs on an AWS EC2 instance.
The public web page has been taken offline, see "Project Reflection" section above.
Users can input a ticker, which will prompt the system to run the analysis for that day (if it does not already exist in the database) and display aggregate sentiments for that stock, along with historical data (if available).
