#4travel import
from urllib.request import urlopen
import urllib.request
import urllib.parse
import urllib
import lxml.html
import re
import requests
import pandas as pd
#mongodb import
import pymongo
from pymongo import MongoClient
from datetime import datetime


#4travel
inputspot='国内'
inputkeyword='大仏'
spot = urllib.parse.quote(inputspot)
keyword=urllib.parse.quote(inputkeyword)
page=100

url_list=[]
for i in range(page): #1ページで10タイトル
    bodyRes1 = urllib.request.urlopen(f'https://4travel.jp/search/travelogue/dm?order=desc&page={i+1}&sa={spot}&sk={keyword}&sort=vote_count')
    bodyHtml1 = bodyRes1.read()
    root1 = lxml.html.fromstring(bodyHtml1.decode('utf-8',errors='replace'))
    url_path = root1.xpath('//a[@class="ico_travelogue"]')
    for k in url_path:
        url=k.get('href')
        url_list.append(url)


article=[]
for j in range(len(url_list)):
    bodyRes2 = urllib.request.urlopen(f'{url_list[j]}')
    bodyHtml2 = bodyRes2.read()
    root2 = lxml.html.fromstring(bodyHtml2.decode('utf-8',errors='replace'))

    title_path=root2.xpath('//h1[@class="headingText"]')
    date_path=root2.xpath('//p[@class="day"]')
    count_path=root2.xpath('//span[@class="count"]')
    area_path=root2.xpath('//div[@class="travelInfoBlock is_areaPath"]/a')
    intro_path=root2.xpath('//p[@class="outlineTextBlock"]')
    body_path=root2.xpath('//p[@class="contentsDescription"]')
    photo_path=root2.xpath('//a[@class="swipebox"]')

    title=title_path[0].text_content()
    date=date_path[0].text_content().replace("\n      ", "").strip()
    count=count_path[0].text_content().replace("いいね！", "").strip()
    area=area_path[0].text_content().replace("エリア", "").strip()
    intro=intro_path[0].text_content().replace("\u3000", "").strip()

    sections=[]
    for p,b in zip(photo_path,body_path):
        photo=p.get('href')
        body=b.text_content().replace("\u3000", "").strip()
        section={'photo':photo,'body':body}
        sections.append(section)
        
    data={
        'title':title,
        'date':date,
        'count':count,
        'area':area,
        'intro':intro,
        'sections':sections
    }  
    
    article.append(data)



'''
article=[{
        'title':title,
        'date':date,
        'count':count,
        'area':area,
        'intro':intro,
        'sections':[{
                    'photo':photo
                    'body':body
                    .......
                    }]
    }]
'''

#mongodb
client = pymongo.MongoClient("mongodb://localhost:27017/")
db_name = "travel"
db = client[db_name]
collection_name = "travel_daibutsu"
collection = db[collection_name]
insert_result = collection.insert_many(article)


