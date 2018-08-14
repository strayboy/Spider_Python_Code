import scrapy
from selenium import webdriver
import os
import time
import datetime
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator
import pymssql
import re
import os

class PDF_spider(scrapy.Spider):
	name="pdfspider"
	start_urls=["http://copacanada.com/copa-weekly/"]
	
	def parse(self,response):
		browser=webdriver.Chrome("D:/tools/chromedriver.exe")
		browser.get(response.url)
		time.sleep(3)
		file=browser.find_element_by_xpath('//*[@id="post-63"]/div/div[2]/div/div/div/div/div[1]/p[1]/a')
		filename=file.get_attribute('href').split('/')[-1]
		os.system("powershell (new-object System.Net.WebClient).DownloadFile("+"'"+file.get_attribute('href')+"',"+"'D:/SpiderData/Canada/"+filename+"')")
		browser.quit()
		fp=open("D:/SpiderData/Canada/"+filename,'rb')
		date=filename.split('.')[0].split('-')[2:]
		publishdate=self.strToDateTime(date)
		i=0
		parser=PDFParser(fp)
		document=PDFDocument(parser,fallback=False)
		document.__init__(parser)
		conn=pymssql.connect(host='.',port='5889',user='Data@Ngoic.org',password='58891135@#*Ngoic',database='NgoicDataAutoCollection',charset='utf8')
		cur=conn.cursor()
		if not document.is_extractable:
			raise PDFTextExtractionNotAllowed
		else:
			rsrcmgr=PDFResourceManager(caching=False)
			laparams=LAParams()
			#device=PDFDevice(rsrcmgr)
			device=PDFPageAggregator(rsrcmgr,laparams=laparams)
			interpreter=PDFPageInterpreter(rsrcmgr,device)
			table=[]
			i=0
			for page in PDFPage.create_pages(document):
				interpreter.process_page(page)
				layout=device.get_result()
				for x in layout:
					if(isinstance(x,LTTextBoxHorizontal)) and (('%' in x.get_text()) or (len(x.get_text().split('\n'))<5 and len(x.get_text().split('\n'))>3 and not re.match('^[a-zA-Z]+$',x.get_text().replace('\n','').replace(' ','')))):
						if i==0:
							table.append(("canola","tonnes","Week Ending",int(x.get_text().split('\n')[0].replace(' ','')),publishdate))
							i=i+1
						elif i==1:
							if '%' not in x.get_text().split('\n')[0]:
								table.append(("soybeans","tonnes","Week Ending",int(x.get_text().split('\n')[0].replace(' ','')),publishdate))
								i=i+1
							else:
								table.append(("canola","tonnes","Crush Capacity Utilization",float(x.get_text().split('\n')[0][:-2]),publishdate))
								i=i+1
									
						elif i==2:
							if '%' in x.get_text().split('\n')[0]:
								table.append(("canola","tonnes","Crush Capacity Utilization",float(x.get_text().split('\n')[0][:-2]),publishdate))
								i=i+1
							else:
								table.append(("soybeans","tonnes","Week Ending",int(x.get_text().split('\n')[0].replace(' ','')),publishdate))
								i=i+1
								
						elif i==3:
							table.append(("soybeans","tonnes","Crush Capacity Utilization",float(x.get_text().split('\n')[0][:-2]),publishdate))
							i=i+1
						
					
				print table
				sql="insert into COPA_Weekly values(%s,%s,%s,%s,%s)"
				cur.executemany(sql,table)
				try:
					conn.commit()
				except:
					conn.rollback()
					
				

	def strToDateTime(self,l):
		monthToNum={'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
		monthallToNum={'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,'july':7,'august':8,'september':9,'october':10,'november':11,'december':12}
		if l[0].lower() in monthToNum:
			l[0]=monthToNum[l[0].lower()]
		elif l[0].lower() in monthallToNum:
			l[0]=monthallToNum[l[0].lower()]
		
		ans=datetime.date(int(l[2]),int(l[0]),int(l[1]))
		return ans