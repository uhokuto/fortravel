from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import csv
import urllib.request
import urllib.parse
import urllib
import lxml.html
import mysql.connector
import time

try:
	page = 0
	strhtml =''	
	conn = mysql.connector.connect(user='root',password='root',host='localhost',database='travelblogDB',charset='utf8')
	cur = conn.cursor()	
	
	while (strhtml.find('条件に一致する情報は見つかりませんでした。')==-1):
	
		page = page +1
		time.sleep(1)
		print(page)
		strpage = str(page)	
		html = urllib.request.urlopen('https://4travel.jp/search/travelogue/dm?page={0}&sa=%E5%9B%BD%E5%86%85'.format(strpage)).read() 
		#html = urllib.request.urlopen('https://4travel.jp/search/travelogue/dm?page={0}&sa=%E5%9B%BD%E5%86%85&sk={1}'.format(strpage,searchWord_encode)).read() # html 取得  
		root = lxml.html.fromstring(html.decode('utf-8',errors='replace'))
		strhtml = str(html.decode('utf-8','replace'))

		
		review_list = root.xpath("//div[@class='travelogue_txt']/a")		
		for review in review_list:				
				
			
			review_pageRes = urllib.request.urlopen(review.get('href'))
			review_pageHtml = review_pageRes.read()				
			review_detail_root= lxml.html.fromstring(review_pageHtml.decode('utf-8'))
			title = review_detail_root.xpath("//div[@class='travelogue_headingBlock']/h1")
			title_text=title[0].text_content().replace('\r\n','').replace('\n','').replace('<br />','').replace(' ','')
			
			date_from_to = review_detail_root.xpath("//div[@class='dayDurationBlock']/p")
			date_txt = date_from_to[0].text_content().replace('\r\n','').replace('\n','').replace('<br />','').replace(' ','')
			
			#<li><a href="javascript:void()" class="tagInner" data-href="https://4travel.jp/dm_travelogue_list-kuchoson-aso.html?tag=413" onclick="location.href=this.dataset.href">
            #<span>#</span>ドライブ</a>              </li>
			hashTags = review_detail_root.xpath("//li/a[@class='tagInner']")
			hashTag_list = [hashTag.text_content().replace('<span>#</span>','').replace('\r\n','').replace('\n','').replace('<br />','').replace(' ','') for hashTag in hashTags]
			hashTag_str='|'.join(hashTag_list)
			
			# <p class="outlineTextBlock">
			body_outline = review_detail_root.xpath("//p[@class='outlineTextBlock']")
			body_outline_txt =body_outline[0].text_content().replace('\r\n','').replace('\n','').replace('<br />','').replace(' ','')[0:4999]
			
			#  <p class="contentsDescription">草千里展望台から見た阿蘇谷と北外輪山</p>
			pict_descriptions = review_detail_root.xpath("//p[@class='contentsDescription']")
			pict_descript_list =[pict_desc.text_content().replace('\r\n','').replace('\n','').replace('<br />','').replace(' ','') for pict_desc in pict_descriptions if pict_desc.text_content()!='']
			pict_descript_txt = '|'.join(pict_descript_list)[0:9999]
			
			print(title_text)
			try:
				cur.execute('SET NAMES utf8mb4')
				cur.execute("SET CHARACTER SET utf8mb4")
				cur.execute("SET character_set_connection=utf8mb4")
				cur.execute('INSERT INTO review_table VALUES(%s, %s, %s, %s, %s)',(title_text,date_txt,hashTag_str,body_outline_txt,pict_descript_txt))
				conn.commit()
			except:
				pass
			
	conn.close()
except HTTPError as e:
	print(e)
except URLError as e:
	print("The server could not be found.")
finally:
	pass
	print("It Worked")