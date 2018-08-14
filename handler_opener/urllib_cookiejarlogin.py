#coding=utf-8

import urllib2,urllib
import cookielib

# 通过CookieJar()构建一个cookiejiar的对象，保存cookie的值
cookie = cookielib.CookieJar()

# 通过HTTPProcessor()处理器类来构建一个处理器对象，用来处理cookie
# 参数就是构建的cookiejar对象
cookie_handler = urllib2.HTTPCookieProcessor(cookie)

# 构建一个自定义的opener
opener = urllib2.build_opener(cookie_handler)

# 通过自定义的的opener的addheaders属性，添加http报头参数
opener.addheaders = [("User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")]

# renren网的登录接口
url = "http://www.renren.com/PLogin.do"

# 登录的用户名和密码
data = {"email":"", "password":""}

# 通过urlencode()编码转换
data = urllib.urlencode(data)

# 发送第一次的post请求，发送登录参数，生成登陆后的cookie（假设成功）
request = urllib2.Request(url,data=data)
response = opener.open(request)

# 第二次可以是get请求，这个请求将保存生成cookie一并发到web服务器，服务器会验证cookie通过
response_jiao = opener.open("http://www.renren.com/316175566/profile")

# 获取登录后才能访问的页面信息
print response_jiao.read()