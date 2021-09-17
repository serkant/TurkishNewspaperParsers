"""
Author: Fatih Serkant Adiguzel
This script collects URLs from a specified day using
Yenisafak's search function. It uses newspaper3k library to
parse maintext and title. However, we need a custom function to parse the newspaper article's publish date.
"""

import pandas as pd
from newspaper import Article
from newspaper import ArticleException
import os
from time import sleep
import time
from htmldate import find_date
from bs4 import BeautifulSoup
import requests
import sys
import re
import dateparser
from datetime import date


hdr = {'User-Agent': 'Mozilla/5.0'} #header settings



keywords = ["erdoğan", "kılıçdaroğlu", "bahçeli", "demirtaş"]


##Date range set. 
start_date = date(2012, 1, 1)
end_date = date(2012, 2, 1)


base = "https://www.yenisafak.com/arama/"


searchdate = f'start={start_date.day}.{start_date.month}.{start_date.year}&end={end_date.day}.{end_date.month}.{end_date.year}'

links_whole = []
for singlekeyword in keywords:
    keyword = singlekeyword+ "?"+ "word=" + singlekeyword

    # first generate the urls that will list the news articles with the desired keyword and within the specified time range. Note that this will only look at the first 5 pages of articles that contain the keyword within the specified time range.

    for i in range(1,5):
        link = base + keyword + "&"+ "page=" + "{}".format(i) + "&" + searchdate

        links_whole.append(link)
       

## Once we have the url for each search page, we can collect specific urls for each news story
main_texts = []
titles = []
urls = []
dates = []
for index, wholepage_link in enumerate(links_whole):

    print("Getting:", index, "Progress:", index/len(links_whole))

    try:
        wholepage = requests.get(wholepage_link, headers=hdr)
    except requests.exceptions.ConnectionError:
        print("Connection Error!")
        continue

    wholesoup = BeautifulSoup(wholepage.content)   

    ## collect each url from each search page
    articlelinks= []
    for wholepage_link in wholesoup.find_all('a', {"class": "entry"}):
        link_captured = wholepage_link.get('href')
        articlelinks.append(link_captured)
    
    articlelinks_ready = []
    for articlelink in articlelinks:
        articlelink_ready = "https://www.yenisafak.com/" + articlelink
        articlelinks_ready.append(articlelink_ready)


    ## now that we have the urls, we can parse them using newspaper3k.
    for articlelink in articlelinks_ready:

        print("Within", index, "Parsing:", articlelink)
        article = Article(articlelink, language="tr")

        try:
            article.download()
            article.parse()
        except ArticleException:
            print("ERROR!", articlelink)
            continue
        


        soup = BeautifulSoup(article.html)


        main_text = article.text
        title = article.title

        
        # since dates are not extracted properly, we need beautifulsoup to get the date.

        try:
            date = soup.find("time").text
            date_cleaner = dateparser.parse(date, languages=['tr'])
        except AttributeError:
            date_cleaner = None
        


        main_texts.append(main_text)
        titles.append(title)
        urls.append(articlelink)
        dates.append(date_cleaner)





d = pd.DataFrame()
d["article_text"] = main_texts
d["article_title"] = titles
d["article_url"]  = urls   
d["article_date"] = dates



name_d = f"yenisafak_{start_date}_to_{end_date}.xlsx"


d.to_excel(name_d)        



