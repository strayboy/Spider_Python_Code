#coding=utf-8

import urllib
import urllib2

url = 'http://www.baidu.com/s'
ua_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko'}
word = raw_input("请输入要搜索的内容：")
wd = {'wd':word}
wd = urllib.urlencode(wd)
fullurl = url + '?' + wd

req = urllib2.Request(fullurl,headers=ua_header)
response = urllib2.urlopen(req)
print response.read()