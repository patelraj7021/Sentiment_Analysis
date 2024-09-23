# Stock Sentiment Analysis

### Objective
It is commonly believed that a key driver for future variations in stock value for a publicly traded company is investor sentiment.
Share prices will increase if investors have optimistic outlooks about a company, and decrease if their sentiment is more pessimistic.  
With a wealth of news articles available for frequently traded stocks though, it is time consuming and monotonous for a typical retail investor to track the sentiment of industry professionals on a regular basis.

This project aims to address this issue by automating the market research and analysis pipeline for retail investors.
Advances in large language model (LLM) architectures in recent years have enabled precise and context-informed quantifications of text, allowing for the sentiment of an article to be well understood by a machine.
Thanks to the availability of pretrained transformer models, 

### Methodology
Note: this project is still under development and the sections below are only a short summary. 
Further details will be included as development continues.

#### Web Scraping
Yahoo Finance provides news aggregation for a given stock, making it a readily accessible source of articles to use for sentiment analysis.
This project uses the Python web scraping framework Scrapy to extract article text from the "Recent News" section of a stock page on Yahoo Finance.
The text is processed and separated into sentence-long context windows for the sentiment analysis itself.

#### Transformed-Powered Sentiment Analysis
HuggingFace offers many pretrained LLMs designed to serve different applications.
This project uses a version of the DistilBERT model, a transformer-based model designed for use in sequence classification, making it an excellent fit for this task.
Sentences are embedded in a vector space where vectors (i.e., words or sentences) of a similar nature occupy the same localized region of the vector space.
A dot product between two vectors quantifies how similar they are, and so taking the dot product of a sentence and a predefined ''positive'' (or negative) word, like ''optimistic'', returns a scalar value that measures how ''optimistic'' that sentence is.

#### Database
Django includes a relational database framework, which is used for this project to store analyses for tracked tickers for each update.

#### Web App
Django and React are used for the back and front end of the web app.
Users can input a ticker, which will prompt the system to run the analysis for that day (if it does not exist in the database) and display aggregate sentiments for that stock, along with historical data (if available).

#### Deployment
To be developed...