
import csv
import urllib.request
import urllib.parse
import urllib
import lxml.html
import time
import pymongo
	


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["fortravelDB2024"]
reviews_collection = db['fortravel_reviews']

keyword=input('input keyword')
key_w = urllib.parse.quote(keyword)

page=0
review_scraped=[]


while True:

    

    page = page +1
    time.sleep(1)
    print(page)
   
    html = urllib.request.urlopen('https://4travel.jp/search/review/dm?order=desc&page={0}&sa={1}&sort=visited_at'.format(page,key_w)).read() 
     
    root = lxml.html.fromstring(html.decode('utf-8',errors='replace'))
    
    
    if page % 10 ==0:
        print(review_scraped)
        reviews_collection.insert_many(review_scraped)
        review_scraped=[]
       
    
    #review_list = root.xpath("//p[@class='summary_ttl']/a") <li class="">	
    review_list = root.xpath('//li[@class=""]')	
    for review in review_list:	

        review_dic={}
        
        t_path = review.xpath(".//p[@class='summary_ttl']/a")
        if len(t_path)!=0:
            title =t_path[0].text_content().replace('\r\n','').replace('\n','').replace('<br />','').replace(' ','')
            review_dic['title'] = title
            
        b_path = review.xpath(".//p[@class='tips_txt']")
        if len(b_path)!=0:
            body =b_path[0].text_content().replace('\r\n','').replace('\n','').replace('<br />','').replace(' ','').replace('...\xa0続きを読む','').replace('\xa0閉じる','')
            review_dic['body'] = body
        #<p class="date">
        d_path = review.xpath(".//p[@class='date']")
        if len(d_path)!=0:
            date =d_path[0].text_content().replace('\r\n','').replace('\n','').replace('<br />','').replace(' ','')
            review_dic['date'] = date
            
        # <p class="info">
        e_path = review.xpath(".//p[@class='info']")
        if len(e_path) !=0:
            evals = e_path[0].text_content().replace('\r\n','').replace('\n','').replace('<br />','').replace(' ','')
            review_dic['eval'] = evals
        '''
        <div class="spot_box">
              <p class="spot_name spot_hotel_m">
                <a href="https://4travel.jp/dm_hotel-11994549">アパホテル 京都五条大宮</a>
              </p>
              <p class="spot_info">
                エリア：京都駅周辺 (京都)

            <br>
                カテゴリー：
                  宿・ホテル
                  
        '''
        
        if len(review_dic)!=0:
            spot_path = review.xpath(".//div[@class='spot_box']/p/a")
            if len(spot_path)!=0:
                spot_name = spot_path[0].text_content()                
                spot_link = spot_path[0].get('href')
                review_dic['spot_name']=spot_name
                review_dic['spot_link']=spot_link
            
            spot_info_path = review.xpath(".//p[@class='spot_info']")
            if len(spot_info_path)!=0:
                spot_info = spot_info_path[0].text_content().replace('\r\n','').replace('\n','').replace('<br />','').replace(' ','')
                review_dic['spot_info']=spot_info
                
            review_dic['pref']=keyword

        #print(review_dic)
        #input()
        review_scraped.append(review_dic)
        