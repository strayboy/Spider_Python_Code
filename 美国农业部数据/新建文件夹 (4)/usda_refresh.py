import scrapy
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import xlrd
import time
import os
from stat import *
from nt import chdir
import pymssql
import datetime
import shutil


class usda_Spider(scrapy.Spider):
	name="refresh"
	start_urls=["https://apps.fas.usda.gov/esrquery/esrq.aspx"]
	def parse(self,response):
		browser=webdriver.Chrome("D:/tools/chromedriver.exe")
		browser.get(response.url)
		s1=Select(browser.find_element_by_xpath("//*[@id='ctl00_MainContent_lbCommodity']"))
		for select in s1.options:
			s1.select_by_visible_text(select.text)
			
		excel=browser.find_element_by_xpath("//*[@id='ctl00_MainContent_rblOutputType_2']")
		excel.click()
		startdate=browser.find_element_by_xpath("//*[@id='ctl00_MainContent_tbStartDate']")
		enddate=browser.find_element_by_xpath("//*[@id='ctl00_MainContent_tbEndDate']")
		chdir(os.path.dirname("D:/spider/fasusda/ExportSalesDataByCommodity.xls"))
		filetime=time.localtime(os.stat("D:/spider/fasusda/ExportSalesDataByCommodity.xls").st_ctime)
		os.remove("D:/spider/fasusda/ExportSalesDataByCommodity.xls")
		print filetime
		date=[str(filetime.tm_mon),str(filetime.tm_mday),str(filetime.tm_year)]
		date=["12","9","2016"]
		localtime=time.strftime("%Y%m%d",time.localtime(time.time()))
		if int(date[0])<10:
			date[0]='0'+date[0]
			
		if int(date[1])<10:
			date[1]='0'+date[1]
			
		print date
		startdate.clear()
		startdate.send_keys(date[0]+"/"+date[1]+"/"+date[2])
		enddate.clear()
		print localtime[4:6]+"/"+localtime[6:]+"/"+localtime[:4]
		enddate.send_keys(localtime[4:6]+"/"+localtime[6:]+"/"+localtime[:4])
		time.sleep(20)
		b=29
		if date[0]=='01' or date[0]=='03' or date[0]=='05' or date[0]=='07' or date[0]=='08' or date[0]=='10':
			if int(date[1])+7>31:
				temp=int(date[1])+7-31
				if temp<10:
					date[1]='0'+str(temp)
				else:
					date[1]=str(temp)
					
				a=int(date[0])+1
				if a<10:
					date[0]="0"+str(a)
				else:
					date[0]=str(a)	
					
			else:
				temp=int(date[1])+7
				if temp<10:
					date[1]='0'+str(temp)
				else:
					date[1]=str(temp)
				
			
		elif date[0]=='04' or date[0]=='06' or date[0]=='09' or date[0]=='11':
			if int(date[1])+7>30:
				temp=int(date[1])+7-30
				if temp<10:
					date[1]='0'+str(temp)
				else:
					date[1]=str(temp)
					
				a=int(date[0])+1
				if a<10:
					date[0]="0"+str(a)
				else:
					date[0]=str(a)
					
			else:
				temp=int(date[1])+7
				if temp<10:
					date[1]='0'+str(temp)
				else:
					date[1]=str(temp)
					
				
				
		elif date[0]=='12':
			if int(date[1])+7>31:
				temp=int(date[1])+7-31
				if temp<10:
					date[1]='0'+str(temp)
				else:
					date[1]=str(temp)
					
				a=int(date[2])+1
				date[0]='01'
				date[2]=str(a)
					
			else:
				temp=int(date[1])+7
				if temp<10:
					date[1]='0'+str(temp)
				else:
					date[1]=str(temp)
					
				
				
		elif date[0]=='02':
			year=int(date[2])
			if (year%4==0 and year%100!=0) or year%400==0:
				b=29
			else:
				b=28
					
			if int(date[1])+7>b:
				temp=int(date[1])+7-b
				if temp<10:
					date[1]='0'+str(temp)
				else:
					date[1]=str(temp)
					
				date[0]='03'
					
			else:
				temp=int(date[1])+7
				if temp<10:
					date[1]='0'+str(temp)
				else:
					date[1]=str(temp)
					
				
			
		#enddate.clear()
		#enddate.send_keys(date[0]+"/"+date[1]+"/"+date[2])
		submit=browser.find_element_by_xpath("//*[@id='ctl00_MainContent_btnSubmit']")
		submit.click()
		time.sleep(500)
		lexcel,sign=self.readexcel()
		browser.quit()
		conn=pymssql.connect(host='.',port='5889',user='Data@Ngoic.org',password='58891135@#*Ngoic',database='NgoicDataAutoCollection',charset='utf8')
		cur=conn.cursor()
		if sign!="":
			print sign
			sql="select Top 1 * from USDA_Exports_Sales where convert(varchar(10),Date,121) = "+"'"+str(sign)+"'"
			#sql="select Top 1 * from USDA_Exports_Sales"
			cur.execute(sql)
			result=cur.fetchall()
			if len(result)==0:
				sqlinsert="insert USDA_Exports_Sales values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				cur.executemany(sqlinsert,lexcel)
				try:
					conn.commit()
				except:
					conn.rollback()
					
				
		cur.close()
		conn.close()
		
		
		
		
		
	
	
	
	
	def readexcel(self):
		data=xlrd.open_workbook('C:/Users/Administrator/Downloads/ExportSalesDataByCommodity.xls')
		table=data.sheets()[0]
		signn=""
		lexcel=[]
		for i in range(table.nrows):
			if i>=7 and table.row_values(i)[2]!='':
				date_format_tuple=xlrd.xldate_as_tuple(table.row_values(i)[2],0)
				date_format=datetime.date(date_format_tuple[0],date_format_tuple[1],date_format_tuple[2])
				signn=str(date_format_tuple[0])+"-"+str(date_format_tuple[1])+"-"+str(date_format_tuple[2])
				trans=table.row_values(i)
				trans[2]=date_format
				del trans[0]
				for j in range(len(trans)):
					if trans[j]=='':
						trans[j]=None
					
					
				lexcel.append(tuple(trans))
			
		if os.path.exists('C:/Users/Administrator/Downloads/ExportSalesDataByCommodity.xls'):
			shutil.copyfile('C:/Users/Administrator/Downloads/ExportSalesDataByCommodity.xls','D:/spider/fasusda/ExportSalesDataByCommodity.xls')
			os.remove('C:/Users/Administrator/Downloads/ExportSalesDataByCommodity.xls')
			
		if len(lexcel)!=0:
			signn=lexcel[0][1]
			
		return lexcel,signn