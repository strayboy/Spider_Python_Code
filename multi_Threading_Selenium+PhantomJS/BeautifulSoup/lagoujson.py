#coding=utf-8
import urllib2
# json解析库，对应到lxml
import json
# json的解析语法，对应到xpath
import jsonpath

url = "http://www.lagou.com/lbs/getAllCitySearchLabels.json"
user_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
request = urllib2.Request(url,headers=user_headers)
response = urllib2.urlopen(request).read()
# print response
# 把json格式的字符串转换为python格式Unicode字符串
unicodestr = json.loads(response)
# python形式的列表
city_list = jsonpath.jsonpath(unicodestr, "$..name")
# for item in city_list:
#     print item

# 禁用ascii编码，返回的是Unicode字符串，dumps()默认中文为ascii编码
array = json.dumps(city_list, ensure_ascii=False)
# array = json.dumps(cite_list)

with open("lagoucity.json","w") as f:
    f.write(array.encode("utf-8"))