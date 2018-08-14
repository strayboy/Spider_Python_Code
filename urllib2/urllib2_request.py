#coding=utf-8
# User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36
import urllib2

ua_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
req = urllib2.Request('http://www.baidu.com/', headers = ua_headers)
response = urllib2.urlopen(req)
html = response.read()
# 打印所有内容
print html

# 返回HTTP的响应码
# print response.getcode()

# 返回实际数据的URL，防止重定向
# print response.geturl()

# 返回服务器响应的http报头
# print response.info()