#coding=utf-8
import urllib2

# 构建一个HTTPHandler处理器对象，支持处理HTTP请求
http_handler = urllib2.HTTPHandler()

# 调用build_opener()方法构建一个自定义的operner对象，参数是构建的处理器对象
opener = urllib2.build_opener(http_handler)

req = urllib2.Request("http://www.baidu.com/")

res = opener.open(req)

print res.read()