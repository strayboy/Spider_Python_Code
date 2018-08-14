# -*- coding: utf-8 -*-
import zipfile
import xlrd
import scrapy
from selenium import webdriver
import time
import os
import pymssql
import datetime


class cftcSpider(scrapy.Spider):
	name="cftc"
	start_urls=["http://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm"]
	
	def parse(self,response):
		browser=webdriver.Chrome("D:/tools/chromedriver.exe")
		conn=pymssql.connect(host='.',port='5889',user='Data@Ngoic.org',password='58891135@#*Ngoic',database='NgoicDataAutoCollection',charset='utf8')
		cur=conn.cursor()
		while True:
			try:
				browser.get(response.url)
				break
			except:
				time.sleep(20)
				continue
				
			
		time.sleep(3)
		file=browser.find_element_by_xpath("//*[@id='box-text_image']/div/div/ul/li/table[7]/tbody/tr[1]/td[1]/p/a[2]")
		#file.click()
		filename=file.get_attribute('href').split("/")[-1].split(".")[-2]+time.strftime("%Y%m%d",time.localtime(time.time()))+".zip"
		os.system("powershell (new-object System.Net.WebClient).DownloadFile("+"'"+file.get_attribute('href')+"',"+"'D:/spider/cftc/"+filename+"')")
		print filename
		browser.quit()
		try:
			lexcel,sign= self.readexcel(filename)
			publish=[str(sign[:2]),str(sign[2:4]),str(sign[4:])]
			publish[0]="20"+str(publish[0])
			if(publish[1][0]=='0'):
				publish[1]=publish[1][1:]
				
			publish_time=datetime.date(int(publish[0]),int(publish[1]),int(publish[2]))
			print publish_time
			sql="select Top 1 * from Cftc_CommodityIndex where As_of_Date_In_Form_YYMMDD = "+sign
			cur.execute(sql)
			result=cur.fetchall()
			if len(result)==0:
				strl="insert into Cftc_CommodityIndex values("
				for i in range(54):
					strl=strl+"%s,"
					
				strl=strl[:-1]
				strl=strl+")"
				cur.executemany(strl,lexcel)
				
			conn.commit()
			sql="select * from SYS_GlabFlag where Module = 'CBOT持仓'"
			cur.execute(sql)
			cbot=cur.fetchone()
			description=cbot[5]
			if(str(description)==None):
				description="Cftc_CommodityIndex success;"+filename+";"
			else:
				description=str(description)+"Cftc_CommodityIndex success;"+filename+";"
				
			python_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			sql="update SYS_GlabFlag set PublishTime=%s,PythonTime = %s,Description = %s,PythonFlag = %s where Module = 'CBOT持仓'"
			cur.execute(sql,(publish_time,python_time_str,description,1))
			try:
				conn.commit()
			except:
				conn.rollback()
				
		except:
			sql="select * from SYS_GlabFlag where Module = 'CBOT持仓'"
			cur.execute(sql)
			cbot=cur.fetchone()
			description=cbot[5]
			if(str(description)==None):
				description="Cftc_CommodityIndex file error;"+filename+";"
			else:
				description=str(description)+"Cftc_CommodityIndex file error;"+filename+";"
				
			python_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			sql="update SYS_GlabFlag set PythonTime = %s,Description = %s,PythonFlag = %s where Module = 'CBOT持仓'"
			cur.execute(sql,(python_time_str,description,0))
			try:
				conn.commit()
			except:
				conn.rollback()
				
			
		cur.close()
		conn.close()
		
		
		
		
		
	def readexcel(self,filename):
		f=zipfile.ZipFile(filename,"r")
		f.extractall()
		f.close()
		data=xlrd.open_workbook('deacit.xls')
		table=data.sheets()[0]
		lexcel=[]
		sign=table.cell(1,1).value
		for i in range(table.nrows):
			if table.row_values(i)[1]==sign:
				date_format_tuple=xlrd.xldate_as_tuple(table.row_values(i)[2],0)
				date_format=datetime.date(date_format_tuple[0],date_format_tuple[1],date_format_tuple[2])
				trans=table.row_values(i)
				trans[1]=str(int(sign))
				trans[2]=date_format
				for j in range(len(trans)):
					if trans[j]=='':
						trans[j]=None
					
					
				lexcel.append(tuple(trans))
			
		if os.path.exists('deacit.xls'):
			os.remove('deacit.xls')
			
		return lexcel,str(int(sign))
	
	
 