#coding=utf-8
import urllib2

# 代理开关，表示是否启用的代理
proxyswitch = True

# 构建一个proxyHandler处理器对象，参数是一个字典类型，协议类型：IP+port
httpproxy_handler = urllib2.ProxyHandler({"http":"124.88.67.54:80"})

# 构建无代理的处理器对象
nullproxy_httphandler = urllib2.ProxyHandler({})

if proxyswitch:
    opener = urllib2.build_opener(httpproxy_handler)
else:
    opener = urllib2.build_opener(nullproxy_httphandler)

# 构建一个全局的operner,之后所有的请求都可以用urlopen()方式去发送，也附带Handler的功能
urllib2.install_opener(opener)

request = urllib2.Request("http://www.baidu.com/")
response = urllib2.urlopen(request)

print response.read()