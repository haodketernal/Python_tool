##Author: HaoPV
import feedparser
import urllib3
import csv
from bs4 import BeautifulSoup
from datetime import datetime
from elasticsearch import Elasticsearch
import json

es = Elasticsearch("http://10.6.156.22:9200", http_auth=('elastic','hpt@123'))

#['summary_detail', 'published_parsed', 'links', 'title', 'author', 'slash_comments', 'comments', 'summary', #'guidislink', 'title_detail', 'link', 'authors', 'post-id', 'author_detail', 'wfw_commentrss', 'id', 'tags', 'published']
#Create CSV and Columns


filename = datetime.now().strftime('hotnews-%Y-%m-%d-%H-%M.csv')
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['ID', 'Source', 'Title', 'Tags', 'Detail', 'Link', 'Public date'])
#ID now static for once round of running code, in the future ID is Dynamic and not duplicate for Identity
#end create 

## RSS GBhackers
NewsFeedGbh = feedparser.parse("http://feeds.feedburner.com/Gbhackers")
x=0
#y is from 0 to end of list feed
for x in range(0,10): 
 entry = NewsFeedGbh.entries[x]
 detail = entry.summary_detail.value
 soup = BeautifulSoup(detail)
 print(soup.get_text())
#put to elasticsearch
 es.index(index="hpt-news-v1", id = entry.id, body={ "timestamp": datetime.utcnow(), "news.date": entry.published, "news.source": 'HPT-News-GBH', "news.title": entry.title, "tags": entry.tags, "author": entry.author, "news.detail": soup.get_text(), "reference": entry.link})
# print detail
#write csv
# with open(filename, 'a', newline='') as file:
#    writer = csv.writer(file)
#    writer.writerow([(x+1), 'GBHackers', entry.title,"tags", soup.get_text(), entry.link, entry.published])
#
 x=x+1

##FEED RSS thehackernews###
#['summary_detail', 'published_parsed', 'links', 'author', 'feedburner_origlink', 'title', 'media_thumbnail', 'summary', #'guidislink', 'title_detail', 'href', 'link', 'authors', 'author_detail', 'id', 'published']
print(" The Hacker news feed: \n")
NewsFeedThkn = feedparser.parse("http://feeds.feedburner.com/TheHackersNews")
y=0#y is from 0 to end of list feed
for y in range(0,49): 
 entry2 = NewsFeedThkn.entries[y]
 print(entry2.keys())
# entry = NewsFeedThkn.entries
 print('Number of RSS posts :'), len(NewsFeedThkn.entries)
 print (y+1,'.')
 detail2 = entry2.summary_detail.value ##encode HTML to text
 soup2 = BeautifulSoup(detail2)
 print(soup2.get_text())
# put to elasticsearch
 es.index(index="hpt-news-v1",id = entry2.id, body={ "timestamp": datetime.utcnow(), "news.date": entry2.published, "news.source": 'HPT-News-THN', "news.title": entry2.title, "tags": {"term": "TheHackersNews"}, "author": entry2.author, "news.detail": soup2.get_text(),  "reference": entry2.link}) 
##write csv
#
# with open(filename, 'a', newline='') as file:
#    writer = csv.writer(file)
#    writer.writerow([(y+1), 'The Hacker News', entry2.title,'Tags: THKN', soup2.get_text(), entry2.link, entry2.published.encode('utf8')])
 y=y+1

##FEED Cyber-security http://feeds.feedburner.com/Cyber-security
#print("Cyber-security news feed \n")
#NewsFeedCs = feedparser.parse("\nhttp://feeds.feedburner.com/Cyber-security")
##z=0
#for z in range(0,0): 
# entry3 = NewsFeedCs.entries[z]
# #print(entry3.keys())
# print('Number of CS-RSS posts :', len(NewsFeedCs.entries))
# print (z+1,'.')
# detail3 = entry3.summary_detail.value ##encode HTML to text
# soup3 = BeautifulSoup(detail3)
# print(soup3.get_text())
##write csv
# with open(filename, 'a', newline='') as file:
#    writer = csv.writer(file)
#    writer.writerow([(y+1), 'Cyber', entry3.title,entry3.source, soup3.get_text(), entry3.link, entry3.published.encode('utf8')])
# z=z+1