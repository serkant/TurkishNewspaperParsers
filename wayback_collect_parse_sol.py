"""
Author: Fatih Serkant Adiguzel
This script collects URLs for Sol newspaper using wayback's cdx server. 
It then uses newspaper3k to extract title and main text. Since newspaper3k cannot extract dates, I extract them using beautifulsoup.
"""
import requests as rq
from bs4 import BeautifulSoup
from time import sleep
from time import time
from random import randint
from warnings import warn
import json
import pandas as pd
from newspaper import Article
from newspaper import ArticleException
import dateparser
from random import choice
from htmldate import find_date




## Get Sol URLs captured in wayback from 2010 to 2011 in json format. 
## See details about CDX server API here: https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md
start_year = 2010
end_year = 2011
url = f'http://web.archive.org/cdx/search/cdx?url=sol.org.tr/about/&matchType=domain&output=json&from={start_year}&to={end_year}&collapse=digest'

urls = rq.get(url).text
parse_url = json.loads(urls) #parses the JSON from urls.


url_list = []
for i in range(1,len(parse_url)):
    orig_url = parse_url[i][2]
    timestamp = parse_url[i][1]
    waylink = timestamp+'/'+orig_url
    url_list.append(waylink)

## final urls we use to parse.
final_urls = []
for oneurl in url_list:
    final_url = 'https://web.archive.org/web/'+ oneurl
    final_urls.append(final_url)
print(len(final_urls))

## We do not need many of the links wayback archive (such as the main page) 
## Let's prepare a list of url patterns we want

includelist = ["medya", 'kent-gundemleri', 'haberleri', 'enternasyonal-gundem', 'elestiri-noktasi', 'ekonomi', 'dunyasoladonuyor', 'dunyadan', 'devlet_ve_siyaset', 'devlet-ve-siyaset', 'yazino', 'kentgundemleri', 'mansetler']

included = []
for url in final_urls:
    if any(x in url for x in includelist):
        included.append(url)

print('Total links:', len(included))



#this iterates over the final urls and parses them 
main_texts = []
final_dates = []
links = []
titles = []
for index, link in enumerate(included):

    print("Parsing", index, "Progress:", index/len(included), "within", index_first, "---", index_second)


    if link.endswith('.rss'):
        print('ENDS WITH .RSS, PASSS')
        continue



    article = Article(link, language="tr")
    
    article.download()

    try:    
        article.parse()
    except ArticleException:
        print('ARTICLE EXCEPTION!', link)
        continue

    
    soup = BeautifulSoup(article.html)

    main_text = article.text
    main_texts.append(main_text)

    ## sol newspaper has various date formats depending on the section, so we try every format here.
    try:
        date = soup.find('div', {'id':'yazitarih'}).text.strip()
    except AttributeError:
        try:
            date = soup.find('span', {'style': 'float: left;'}).text.strip()
        except AttributeError:
            date = find_date(link)
    try:
        date_final = dateparser.parse(date, date_formats=['%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%d %B %Y'], languages=['tr'])
    except TypeError:
        date_final = None

    
    if pd.isnull(date_final) is True:
        date_final = dateparser.parse(link, date_formats=['%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%d %B %Y'], languages=['tr'])
   



    final_dates.append(date_final)

    link_captured = link
    links.append(link_captured)

    title = article.title
    titles.append(title)
    

    

d = pd.DataFrame()
d["article_text"] = main_texts
d["article_title"] = titles
d["article_url"]  = links   
d["article_date"] = final_dates



name_d = f"wayback_sol{start_year}_to_{end_year}.xlsx"

d.to_excel(name_d)

