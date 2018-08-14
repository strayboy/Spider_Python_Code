#coding=utf-8
import urllib2,urllib

url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
ua_header = {
    "Connection":"keep-alive",
    "X-Requested-With":"XMLHttpRequest",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",

}
key = raw_input("请输入需要翻译的文字：")
formdata ={
    "type":"AUTO",
    "i":key,
    "doctype":"json",
    "xmlVersion":"1.8",
    "keyfrom":"fanyi.web",
    "ue":"UTF-8",
    "action":"FY_BY_ENTER",
    "typoResult":"true"
}

data = urllib.urlencode(formdata)
req = urllib2.Request(url,data = data,headers=ua_header)
print urllib2.urlopen(req).read()
