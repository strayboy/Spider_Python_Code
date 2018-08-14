#-*- coding:utf-8 -*-
import scrapy
from selenium import webdriver
import os
import datetime
import re
import pymssql
import time



monthToNum={'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
def strToDateTime(l):
	if l[0].lower() in monthToNum:
		l[0]=monthToNum[l[0].lower()]
	ans=datetime.date(int(l[2]),int(l[0]),int(l[1]))
	return ans
l=['DEC', '30', '2010']


print strToDateTime(l)

class usda_refresh(scrapy.Spider):
	name='usda_refrseh'
	start_urls=["https://www.ams.usda.gov/market-news/national-grain-reports"]
	
	def parse(self,response):
		browser=webdriver.Chrome("D:/tools/chromedriver.exe")
		while True:
			try:
				browser.get(response.url)
				break
			except:
				time.sleep(20)
				continue
				
			
		source=browser.find_element_by_xpath('//*[@id="landingMidColWrap"]/article/div/div/div/div/ul[18]/li/a')
		yield scrapy.Request(source.get_attribute('href'),callback=self.parse_txt)
		time.sleep(3)
		browser.quit()
		
	def parse_txt(self,response):
		conn=pymssql.connect(host='.',port='5889',user='Data@Ngoic.org',password='58891135@#*Ngoic',database='NgoicDataAutoCollection',charset='utf8')
		cur=conn.cursor()
		try:
			filename=response.url.split("/")[-1].split(".")[-2]+time.strftime("%Y%m%d",time.localtime(time.time()))+".txt"
			f=open(filename,"w")
			f.write(response.body)
			f.close()
			sql="select * from SYS_GlabFlag where Module='出口检验'"
			cur.execute(sql)
			description=cur.fetchone()[5]
			if(str(description)==None):
				description=filename+";"
			else:
				description=str(description)+filename+";"
			
			python_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			sql="update SYS_GlabFlag set PythonTime = %s,Description = %s,PythonFlag = %s where Module = '出口检验'"
			cur.execute(sql,(python_time_str,str(description),1))
			try:
				conn.commit()
			except:
				conn.rollback()
				
		except:
			sql="select * from SYS_GlabFlag where Module='出口检验'"
			cur.execute(sql)
			description=cur.fetchone()[5]
			if(str(description)==None):
				description="Download error;"
			else:
				description=str(description)+"Download error;"
			
			python_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			sql="update SYS_GlabFlag set PythonTime = %s,Description = %s,PythonFlag = %s where Module = '出口检验'"
			cur.execute(sql,(python_time_str,str(description),0))
			try:
				conn.commit()
			except:
				conn.rollback()
				
			
		cur.close()
		conn.close()
		time.sleep(3)