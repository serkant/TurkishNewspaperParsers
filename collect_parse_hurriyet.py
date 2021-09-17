"""
Author: Fatih Serkant Adiguzel
This script collects URLs from a specified day using
Hurriyet's digital archive. It uses newspaper3k library to
parse maintext and title. However, we need a custom function to parse the newspaper article's publish date.
"""

from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
from datetime import timedelta, date
from newspaper import Article
import newspaper
import pandas as pd
import time
import random
import dateparser
import os


hdr = {'User-Agent': 'Mozilla/5.0'} #header settings


##Date range function
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

##Date range set. 
start_date = date(2012, 2, 1)
end_date = date(2012, 2, 2)
extra = "&r=tarih&p="

whole_links = []

#iterates over the defined date range and collects all links in these days.
for single_date in daterange(start_date, end_date):
    base = "https://www.hurriyet.com.tr/haberleri/?d="
    date = base + single_date.strftime("%Y%m%d")
    print('Getting articles with the following date:', date)
    main_page = date + extra
    # news ranked in the first 5 pages.
    for page_no in range(5):
        url = main_page + str(page_no+1)

        page = requests.get(url)
        wait_time = random.uniform(1, 5)
        time.sleep(1*wait_time)   

        data = page.text
        soup = BeautifulSoup(data)

        links= []
        for link in soup.find_all('a'):
            link_captured = link.get('href')
            links.append(link_captured)
        whole_links = whole_links + links
       

#Among all links, let's just get gundem (politics) and ekonomi (economy).

selected_links = list(filter(lambda x: x and x.startswith(("/gundem", "/ekonomi")), whole_links))


links3k = []
for index, haber in enumerate(selected_links):
    link3k = "http://www.hurriyet.com.tr" + haber
    links3k.append(link3k)

#removing duplicate links.
links3k_unique = list(set(links3k)) 

#A custom date extractor since newspaper3k did not work for dates.
def date_extract(html):
    hold_dict = {}
    soup = BeautifulSoup(html, "lxml")
    date = soup.find("span", {"class": "rhd-time-box-text"}).text
    pattern_date = r'.*?:(.*)-.*'
    match = re.search(pattern_date, date)
    parsed = match.group(1)
    hold_dict['date'] = parsed
    return hold_dict


main_texts = []
titles = []
images = []
extracted_dates = []
links_gathered = []

#downloading links and parsing them using newspaper3k and a custom date extractor.
for index, link3k in enumerate(links3k_unique):
    link3k = link3k.strip()
    print("Downloading:", index/len(links3k_unique), "--url:", link3k)
    article = Article(link3k)

    article.download()

    try:    
        article.parse()
    except newspaper.article.ArticleException:
        continue

    try:
        response = requests.get(link3k, headers=hdr)
    except requests.exceptions.ConnectionError:
        continue

    main_text = article.text
    main_texts.append(main_text)

    article_title = article.title
    titles.append(article_title)

    image = article.top_image
    images.append(image)

    
    
    content = response.content

    try:
        extracted_date = date_extract(content)
        date_news  = extracted_date["date"]
    except:    
        date_news = None
    
    links_gathered.append(link3k)

    extracted_dates.append(date_news)

    wait_rnd = random.uniform(1, 2)
    time.sleep(wait_rnd*1)
    

d = pd.DataFrame()
d["article_text"] = main_texts
d["article_title"] = titles
d["article_image"] = images
d["article_url"]  = links_gathered   
d["article_date"] = extracted_dates


name_d = f"{start_date}_to_{end_date}.xlsx"

d.to_excel(name_d)





