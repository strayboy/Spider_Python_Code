#coding=utf-8
import urllib2,urllib

url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action'

headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}

formdata ={
    'start':'0',
    'limit':'20'
}
data = urllib.urlencode(formdata)
req = urllib2.Request(url,data=data,headers=headers)
response = urllib2.urlopen(req)
print response.read()
