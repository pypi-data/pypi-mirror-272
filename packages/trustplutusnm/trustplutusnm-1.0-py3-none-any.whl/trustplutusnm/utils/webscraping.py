import json
import random
import time
import email.utils
import requests
import iso639
from langdetect import detect
from bs4 import BeautifulSoup
# from fastapi.security import http
from gnews import GNews
from trustplutusmr.utils.logs import loga
import trustplutusmr.config.constants as ct
import lxml
from newspaper import Article, Config
from datetime import datetime
from nlpretext import Preprocessor
from trustplutusmr.utils.helpers import SentimentAnalysis, clean_text, TextChunk
from pydantic import BaseModel, Field
# from utils.secretStore import SecretStore
from trafilatura import fetch_url, extract

class GoogleNews(BaseModel):
    # Max number is 100. Getting more than 100 results increases chance of getting blocked
    max_results: int = Field(100, lt=101)

    # Format for period field
    # hours (eg: 1h), day (eg:2d), months (eg: 1m), years (eg:1y)
    period: str = None

    # Format for start and end date : Tuple(dd,mm,yyyy)
    end_date: datetime = None
    start_date: datetime = None

    language: str = "en"
    country: str = "IN"

    # store = SecretStore()
    # secrets: dict = store.decrypt(secret_keys=["ScrapperAPI"])

    @staticmethod
    def get_article(link):
        article = Article(link)
        article.download()
        article.parse()
        article.nlp()
        return article

    @staticmethod
    def extract_article_html(url):
        config = Config()
        config.fetch_images = True
        config.request_timeout = 30
        config.keep_article_html = True
        article = Article(url, config=config)

        article.download()
        article.parse()

        article_html = article.article_html

        html = lxml.html.fromstring(article_html)
        for tag in html.xpath('//*[@class]'):
            tag.attrib.pop('class')

        return lxml.html.tostring(html).decode('utf-8')

    # @loga
    def get_news(self, query, sentiment: bool = False, start_date: tuple = None,
                 end_date: tuple = None, country: str = None, period: str = None,
                 max_results: int = None):

        google_news = GNews()
        google_news.language = self.language
        google_news.period = self.period if period is None else period
        google_news.max_results = self.max_results if max_results is None else max_results
        google_news.country = self.country if country is None else country
        google_news.start_date = self.start_date if start_date is None else start_date
        google_news.end_date = self.end_date if end_date is None else end_date

        query_news = google_news.get_news(query)
        print("Finished scraping Google News")
        import pickle
        file = open('dump.txt', 'wb')
        pickle.dump(query_news, file)
        file.close()
        print("Processing articles...")
        processed_feed = []
        preprocessor = Preprocessor()
        for i in query_news:
            article_dict = {"title": i["title"], "date": i["published date"]}
            try:
                article = self.get_article(i["url"])
                article_dict["url"] = url = dict(article.meta_data)["og"]["url"]
                article_dict["summary"] = preprocessor.run(article.summary)
                document = fetch_url(url)
                text = extract(document)
                article_dict["text"] = preprocessor.run(text)
                processed_feed.append(article_dict)
            except Exception as e:
                print("Newspaper3k error: {0}, skipping article.".format(e.__class__.__name__))
                print("Exception details: ", e)
        print("Done")

        feed_with_sentiment = []
        if sentiment:
            print("Analyzing Sentiment...")
            for i in processed_feed:
                text = clean_text(i["title"])
                result = detect(text)
                lang_name = iso639.Language.from_part1(result).name
                if lang_name == 'English':
                    sa = SentimentAnalysis()
                    sa.get_sentiment(text)
                    i["sentiment"] = sa.label
                    print("Overall Sentiment: ", i["sentiment"])
                    feed_with_sentiment.append(i)
                    article_html = ''
                    try:
                        article_html = self.extract_article_html(i["url"])
                    except Exception as e:
                                print("Newspaper3k error: {0}, skipping article.".format(e.__class__.__name__))
                                print("Exception details: ", e)
                    i["articleHtml"] = '<div> <center> <h2>'+ i["title"] +' </h2> <center> <h4>Date: '+ i["date"] +'</h4><h4>Sentiment: '+str(i["sentiment"])+'</h4> </div><a></a><hr>' + article_html +"<hr><hr>"
                else:
                    continue
                # time.sleep(random.uniform(1.5, 5.5))
            print("Done")
            return feed_with_sentiment
        return processed_feed


    # def get_gserp(self,query):
    #     # Scarper API
    #     payload = {
    #         'api_key': self.secrets["SrcrapperAPI"],
    #         'country': 'in',
    #         'query': query
    #     }
    #     response = requests.get(
    #         'https://api.scraperapi.com/structured/google/search', params=payload)
    #     response_dict = json.loads(response.text)
    #
    #     result = []
    #     for i in response_dict["organic_results"]:
    #         print("Snippet: ",i["snippet"])
    #         page = http.request("GET",i["link"])
    #         print("Link: ",i["link"])
    #         soup = BeautifulSoup(page.data)
    #         try:
    #             text = soup.body.get_text(strip=True)
    #         except:
    #             pass
    #         else:
    #             print("-----------------")
