#-*- coding:utf-8 -*-
import scrapy
from selenium import webdriver
import os
import datetime
import re
import pymssql
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')


monthToNum={'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
def strToDateTime(l):
	if l[0].lower() in monthToNum:
		l[0]=monthToNum[l[0].lower()]
	ans=datetime.date(int(l[2]),int(l[0]),int(l[1]))
	return ans
l=['DEC', '30', '2010']


print strToDateTime(l)

class usda_refresh():
	name='usda_refrseh'
	start_urls=["https://www.ams.usda.gov/market-news/national-grain-reports"]
	filename=""
	conn=pymssql.connect(host='.',port='5889',user='Data@Ngoic.org',password='58891135@#*Ngoic',database='NgoicDataAutoCollection',charset='utf8')
	cur=conn.cursor()
	
	def parse(self):
		sql="select * from SYS_GlabFlag where Module='出口检验'"
		self.cur.execute(sql)
		a=self.cur.fetchone()
		description=a[5]
		if(a[3]==1):
			self.filename=description.split(";")[-2]
			self.parse_txt()
			
		
	def parse_txt(self):
		f=open(self.filename,"rU")
		table=0
		unit=""
		end=0
		head=[]
		sign=[]
		date=[]
		grainsone=[]
		grainstwo=[]
		cur_portarea=''
		table2_lines=[]
		wheat=0
		grainportarea=0
		graincountry=0
		dateOfTable6=""
		last5=""
		public_date=''
		publish_date=datetime.date(2016,1,1)
		region=""
		port=""
		print f.name
		rc=[]
		updatetime=datetime.datetime(int(f.name[8:12]),int(f.name[12:14]),int(f.name[14:-4]))
		for line in f:
			if line=="\n":
				continue
			
			if table==0:
				if 'GRAINS INSPECTED AND/OR WEIGHED FOR EXPORT' == line.strip():
					print line
					table=1
					index=1
					continue
				
				elif 'SOYBEANS INSPECTED AND/OR WEIGHED FOR EXPORT' in line:
					print line
					table=0
					index=1
					continue
			
				elif 'WHEAT INSPECTED AND/OR WEIGHED FOR EXPORT BY CLASS, REGION AND PORT AREA' in line:
					print line
					table=0
					index=1
					continue
				
				elif 'GRAINS INSPECTED AND/OR WEIGHED FOR EXPORT BY REGION AND PORT AREA' in line:
					print line
					table=0
					index=1
					continue
			
				elif 'GRAINS INSPECTED AND/OR WEIGHED FOR EXPORT BY REGION AND COUNTRY OF DESTINATION' in line:
					print line
					table=0
					index=1
					continue
				
				elif 'CORRECTIONS TO PREVIOUS PUBLICATIONS' in line:
					print line
					table=0
					index=1
					continue
			
			
			elif table==1:
				try:
					if index==1:
						date=line.strip().split()
						date=date[4:]
						date[1]=date[1][:-1]
						print date
						publish_date=strToDateTime(date)
						index=index+1
					
					elif re.match('^--.+?--$',line.strip()) and ('-----------------------------------' not in line):
						print line.strip()
						unit=line.strip()
						index=2
					
					elif index==3:
						sign=line.split()
						print sign
						index=index+1
					
					elif "GRAIN" in line:
						head=line.strip().split()
						head=head[:-4]
						head.append(sign[0]+" MARKET YEAR TO DATE")
						head.append(sign[1]+" MARKET YEAR TO DATE")
						print head
						index=index+1
					
					elif '-----------------------------' in line:
						end=end+1
						if end==1:
							index=3
						
						if end==2:
							table=0
							index=0
							end=0
							continue
					
				
					elif index>4 and line!="\n":
						data=line.strip().split()
						for i in range(len(data[1:])):
							print date
							record=(data[0].strip(),publish_date,head[1:][i].strip(),unit,int(data[1:][i].strip().replace(',',"")),updatetime)
							print record
							index=index+1
							rc.append(record)
							
						
				except:
					sql="select * from SYS_GlabFlag where Module='出口检验'"
					self.cur.execute(sql)
					description=self.cur.fetchone()[5]
					if(str(description)==None):
						description="Weekly error;"+self.filename+";"
					else:
						description=str(description)+"Weekly error;"+self.filename+";"
					
					python_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
					sql="update SYS_GlabFlag set PythonTime = %s,Description = %s,PythonFlag = %s where Module = '出口检验'"
					self.cur.execute(sql,(python_time_str,description,0))
					try:
						self.conn.commit()
					except:
						self.conn.rollback()
						
					break
				
			elif table==2:
				index+=1
				#print index
				#print line 
				#print index
				if ' REPORTED IN WEEK ENDING' in line:
					print line 
					reg=r'[a-zA-Z]+\s*\d+\s*\,\s*\d+'
					public_date=re.findall(reg,line)[0]
					print 'public_date:'+public_date
					date=public_date.split()
					date[1]=date[1][:-1]
					publish_date=strToDateTime(date)
				elif index==4:
					reg=r'\-[a-zA-Z\d\,\s]+\-'
					unit=re.findall(reg,line)[0][1:-1]
					print 'unit:'+unit
				elif '-------------------------------------------' not in line:
					reg_pair='[a-zA-Z\.\s]+[\d\,]+'
					result=re.findall(reg_pair,line)
					if len(result)==0:
						reg_curport=r'[a-zA-Z\s\.]+'
						cur_portarea=re.findall(reg_curport,line)[0]
						if '\n' in cur_portarea:
							cur_portarea=cur_portarea[:-1]
					else:
						print result
						for pair in result:
							reg1=r'[a-zA-Z\s\.]+'
							reg2=r'[\d\,]+'
							area=re.findall(reg1,pair)[0]
							value=re.findall(reg2,pair)[0]
							table2_lines.append((publish_date,cur_portarea.strip(),area.strip(),unit.strip(),value.strip(),updatetime))
				elif '-------------------------------------------' in line:
					end=end+1
					index=index+1
					if end==2:
						for line in table2_lines:
							print line
							
						conn=pymssql.connect(host='.',port='5889',user='Data@Ngoic.org',password='58891135@#*Ngoic',database='NgoicDataAutoCollection',charset='utf8')
						cur=conn.cursor()
						sql="insert AMS_Inspected_Soybeans values(%s,%s,%s,%s,%s,%s)"
						cur.executemany(sql,table2_lines)
						try:
							conn.commit()
						except:
							conn.rollback()
							
						table=0
						index=0
						end=0
						continue              
					
					
				
			elif table==3:
				if index==1:
					date=line.strip().split()
					date=date[4:]
					date[1]=date[1][:-1]
					print date
					publish_date=strToDateTime(date)
					index=index+1
				
				elif index==2:
					unit=line.strip()
					print unit
					index=index+1
			
				elif "----------------------------------------------" in line:
					end=end+1
					index=index+1
					if end==2:
						table=0
						index=0
						end=0
						continue
					
				
				elif index==4:
					grainsone=line.strip().split('  ')
					while '' in grainsone:
						grainsone.remove('')
				
					for i in range(len(grainsone)):
						grainsone[i]=grainsone[i].strip()
					
					print grainsone
					index=index+1
				
				elif index==5:
					if 'REGION/PORT' not in line:
						wheat=1
						
					grainstwo=line.strip().split()
					if wheat==0:
						grainstwo=grainstwo[2:]
					else:
						grainstwo=grainstwo[3:]
						
					print grainstwo
					head=[]
					for i in range(len(grainstwo)):
						if i < len(grainsone):
							head.append(grainsone[i]+" "+grainstwo[i])
						else:
							head.append(grainstwo[i])
					
							
					print head
					index=index+1 
				
				elif line[0]!=' ' and line[:5]!='TOTAL' and line!="\n":
					if wheat==0:
						region=line.strip()
						print region
						index=index+1
					else:
						mid=line.strip().split('  ')
						while '' in mid:
							mid.remove('')
						
						region=mid[0]
						print region
						a=mid[1:]
						for i in range(len(a[1:])):
							record=(publish_date,head[i],region,a[0],None,unit,int(a[1:][i].strip().replace(",","")),updatetime)
							conn=pymssql.connect(host='.',port='5889',user='Data@Ngoic.org',password='58891135@#*Ngoic',database='NgoicDataAutoCollection',charset='utf8')
							cur=conn.cursor()
							sql="insert into AMS_Inspected_Wheat values(%s,%s,%s,%s,%s,%s,%s,%s)"
							cur.execute(sql,record)
							try:
								conn.commit()
							except:
								conn.rollback()
						
						
						
				elif line.strip()[:5]=='TOTAL':
					region='TOTAL'
					a=line.strip().split()
					print a
					for i in range(len(a[1:])):
						record=(publish_date,head[i],region,a[0],None,unit,int(a[1:][i].strip().replace(",","")),updatetime)
						conn=pymssql.connect(host='.',port='5889',user='Data@Ngoic.org',password='58891135@#*Ngoic',database='NgoicDataAutoCollection',charset='utf8')
						cur=conn.cursor()
						sql="insert into AMS_Inspected_Wheat values(%s,%s,%s,%s,%s,%s,%s,%s)"
						cur.execute(sql,record)
						try:
							conn.commit()
						except:
							conn.rollback()
						
						
					end=0
					table=0
					index=0
					continue
					
				elif line!="\n":
					a=line.strip().split('  ')
					while '' in a:
						a.remove('')
					
					print a
					for i in range(len(a[1:])):
						record=(publish_date,head[i],region,a[0],None,unit,int(a[1:][i].strip().replace(",","")),updatetime)
						conn=pymssql.connect(host='.',port='5889',user='Data@Ngoic.org',password='58891135@#*Ngoic',database='NgoicDataAutoCollection',charset='utf8')
						cur=conn.cursor()
						sql="insert into AMS_Inspected_Wheat values(%s,%s,%s,%s,%s,%s,%s,%s)"
						cur.execute(sql,record)
						try:
							conn.commit()
						except:
							conn.rollback()
						
						
					index=index+1
				
				else:
					index=index+1
						
			elif table==4:
				if index==1:
					date=line.strip().split()
					date=date[4:]
					date[1]=date[1][:-1]
					print date
					publish_date=strToDateTime(date)
					index=index+1
				
				elif index==2:
					unit=line.strip()
					print unit
					index=index+1
			
				elif "-------------------------------------------------------------" in line:
					end=end+1
					index=index+1
					if end==2:
						table=0
						index=0
						end=0
						continue
					
				
				elif index==4:
					grainsone=line.strip().split('   ')
					while '' in grainsone:
						grainsone.remove('')
				
					for i in range(len(grainsone)):
						grainsone[i]=grainsone[i].strip()
					
					print grainsone
					index=index+1
				
				elif index==5:
					grainstwo=line.strip().split()
					print grainstwo
					if 'REGION/PORT' not in line:
						grainportarea=1
						
					head=[]
					if grainportarea==1:
						grainstwo=grainstwo[1:]
						
					for i in range(len(grainstwo)):
						head.append(grainstwo[i])
					
					for i in range(len(head)):
						if head[i]=='YELLOW' or head[i]=='WHITE':
							head[i]=head[i]+" CORN"
						elif head[i]=='SEED':
							head[i]='FLAX-'+head[i]

						
					print head
					index=index+1 
				
				elif line[0]!=' ' and line[:5]!='TOTAL' and line!="\n":
					if grainportarea==0:
						region=line.strip()
						print region
					else:
						a=line.strip().split('  ')
						
						while '' in a:
							a.remove('')
							
						region=a[0]
						print region
						a=a[1:]
						print a
						for i in range(len(a[1:])):
							record=(head[2:][i],publish_date,region,a[0],unit,int(a[1:][i].strip().replace(",","")),updatetime)
							conn=pymssql.connect(host='.',port='5889',user='Data@Ngoic.org',password='58891135@#*Ngoic',database='NgoicDataAutoCollection',charset='utf8')
							cur=conn.cursor()
							sql="insert into AMS_Inspected_Grains_ByRegionAndPortArea values(%s,%s,%s,%s,%s,%s,%s)"
							cur.execute(sql,record)
							try:
								conn.commit()
							except:
								conn.rollback()
								
							
							
					index=index+1
				
				elif line[:5]=='TOTAL':
					region='TOTAL'
					a=line.strip().split()
					print a
					for i in range(len(a[1:])):
						record=(head[2:][i],publish_date,region,a[0],unit,int(a[1:][i].strip().replace(",","")),updatetime)
						conn=pymssql.connect(host='.',port='5889',user='Data@Ngoic.org',password='58891135@#*Ngoic',database='NgoicDataAutoCollection',charset='utf8')
						cur=conn.cursor()
						sql="insert into AMS_Inspected_Grains_ByRegionAndPortArea values(%s,%s,%s,%s,%s,%s,%s)"
						cur.execute(sql,record)
						try:
							conn.commit()
						except:
							conn.rollback()
					
					
					end=0
					table=0
					index=0
					continue
					
				elif line!="\n":
					a=line.strip().split('  ')
					while '' in a:
						a.remove('')
					
					print a
					for i in range(len(a[1:])):
						record=(head[2:][i],publish_date,region,a[0],unit,int(a[1:][i].strip().replace(",","")),updatetime)
						conn=pymssql.connect(host='.',port='5889',user='Data@Ngoic.org',password='58891135@#*Ngoic',database='NgoicDataAutoCollection',charset='utf8')
						cur=conn.cursor()
						sql="insert into AMS_Inspected_Grains_ByRegionAndPortArea values(%s,%s,%s,%s,%s,%s,%s)"
						cur.execute(sql,record)
						try:
							conn.commit()
						except:
							conn.rollback()
						
						
					index=index+1
				
				else:
					index=index+1
						
			elif table==5:
				rc=[]
				sql="insert into AMS_Inspected_Grains_ByRegionAndCountryOfDestination values(%s,%s,%s,%s,%s,%s,%s)"
				if index==1:
					date=line.strip().split()
					date=date[4:]
					date[1]=date[1][:-1]
					print date
					publish_date=strToDateTime(date)
					index=index+1
				
				elif index==2:
					unit=line.strip()
					print unit
					index=index+1
			
				elif "-----------------------------------------------------------" in line:
					end=end+1
					index=index+1
					if end==2:
						table=0
						index=0
						end=0
						continue
					
				
				elif index==4:
					grainsone=line.strip().split('   ')
					while '' in grainsone:
						grainsone.remove('')
				
					for i in range(len(grainsone)):
						grainsone[i]=grainsone[i].strip()
					
					print grainsone
					index=index+1
				
				elif index==5:
					if 'REGION/COUNTRY' not in line:
						graincountry=1
					
					grainstwo=line.strip().split()
					print grainstwo
					head=[]
					for i in range(len(grainstwo)):
						head.append(grainstwo[i])
					
					for i in range(len(head)):
						if head[i]=='YELLOW' or head[i]=='WHITE':
							head[i]=head[i]+" CORN"
						elif head[i]=='SEED':
							head[i]='FLAX-'+head[i]

						
					print head
					if graincountry==1:
						head=head[1:]
						
					index=index+1 
				
				elif end<2 and line[0]!=' ' and line[:5]!='TOTAL' and line!="\n":
					if graincountry==0:
						region=line.strip()
						print region
					else:
						mid=line.split('  ')
						while '' in mid:
							mid.remove('')
							
						region=mid[0].strip()
						print region
						a=mid[1:]
						for i in range(len(a[1:])):
							record=(publish_date,region,a[0],head[1:][i],unit,int(a[1:][i].strip().replace(",","")),updatetime)
							rc.append(record)
							
						
					index=index+1
					
				elif 'CORRECTIONS TO PREVIOUS PUBLICATIONS' in line:
					print line.strip()
					dateOfTable6=last5.strip().strip('***').split(' ')[1:]
					dateOfTable6[0]=dateOfTable6[0][:3]
					dateOfTable6[1]=dateOfTable6[1][:-1]
					print dateOfTable6
					publish_date=strToDateTime(dateOfTable6)
					table=6
					index=0
					end=0
					continue
				
				elif end>=2 and line!="\n":
					last5=line.strip()
				
				elif line[:5]=='TOTAL':
					region='TOTAL'
					a=line.strip().split()
					print a
					for i in range(len(a[1:])):
						record=(publish_date,region,a[0],head[1:][i],unit,int(a[1:][i].strip().replace(",","")),updatetime)
						rc.append(record)
						
					end=2
					continue
					
				elif line!="\n":
					a=line.strip().split('  ')
					while '' in a:
						a.remove('')
					
					print a
					for i in range(len(a[1:])):
						record=(publish_date,region,a[0],head[1:][i],unit,int(a[1:][i].strip().replace(",","")),updatetime)
						rc.append(record)
						
					index=index+1
				
				else:
					index=index+1
					
				cur.executemany(sql,rc)
				try:
					conn.commit()
				except:
					conn.rollback()
					
				
			elif table==6:
				rc=[]
				sql="insert into AMS_Inspected_Corrections values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				if line!='\n' and line[:6].upper()!='SOURCE':
					ans=[]
					s=line.strip().split(' ')
					while '' in s:
						s.remove('')
					i=0
					while i<len(s):
						if i<2:
							i+=1
							continue
						if i<=4:
							ans.append(s[i])
							i+=1
							continue
						if i==5:
							if(len(s[i])>=2 and s[i][1]=='.'):
								ans.append(s[i])
								ans.append(s[i+1])
								i+=2
							else:
								ans.append('')
								if s[i+1]!="FROM":
									ans.append(s[i]+' '+s[i+1])
								else:
									ans.append(s[i])
									s.insert(i,'')
									
								i+=2
							continue
						if i==8:
							l=''
							l+=s[i]+' '
							i+=1
							while i<len(s) and s[i]!='TO':
								l+=s[i]
								i+=1
							ans.append(l)
							continue
						if s[i]=='TO':
							l=''
							i+=1
							l+=s[i]
							i+=1
							while i<len(s):
								l+=' '+s[i]
								i+=1
							ans.append(l)
							break
						else:i+=1
				
					for i in range(len(ans)):
						ans[i]=ans[i].strip()
				
					ans.insert(0,publish_date)
					ans.append(updatetime)
					ans[3]=int(ans[3].strip().replace(",",""))
					if ans[4]=='':
						ans[4]=None
					
					record=tuple(ans)
					print ans
					rc.append(record)
					
				elif line[:6].upper()=='SOURCE':
					table=0	
					
				cur.executemany(sql,rc)
				try:
					conn.commit()
				except:
					conn.rollback()
					
				
			else:
				table=0
				
			
			sql="insert into AMS_Inspected_WeekEnding values(%s,%s,%s,%s,%s,%s)"
			self.cur.executemany(sql,rc)
			try:
				self.conn.commit()
			except:
				self.conn.rollback()
				sql="select * from SYS_GlabFlag where Module='出口检验'"
				self.cur.execute(sql)
				description=cur.fetchone()[5]
				if(str(description)==None):
					description="Weekly error;"+self.filename+";"
				else:
					description=str(description)+"Weekly error;"+self.filename+";"
				
				python_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				sql="update SYS_GlabFlag set PythonTime = %s,Description = %s,PythonFlag = %s where Module = '出口检验'"
				self.cur.execute(sql,(python_time_str,description,0))
				try:
					self.conn.commit()
				except:
					self.conn.rollback()
					
				
			sql="select * from SYS_GlabFlag where Module = '出口检验'"
			self.cur.execute(sql)
			cbot=self.cur.fetchone()
			description=cbot[5]
			if(str(description)==None):
				description="Weekly success;"+self.filename+";"
			else:
				description=str(description)+"Weekly success;"+self.filename+";"
			
			python_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			sql="update SYS_GlabFlag set PublishTime=%s,PythonTime = %s,Description = %s,PythonFlag = %s where Module = '出口检验'"
			self.cur.execute(sql,(publish_date,python_time_str,str(description),1))
			try:
				self.conn.commit()
			except:
				self.conn.rollback()
		
		
		
		
		self.cur.close()
		self.conn.close()
		f.close()
		
		
if __name__=='__main__':
	weekly=usda_refresh()
	weekly.parse()