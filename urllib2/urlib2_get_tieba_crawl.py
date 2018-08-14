# coding= utf-8
import urllib2,urllib

def loadPage(url,filename):
    '''根据url发送请求，获取服务器响应文件
        url:需要爬取的URL地址
        filename: 处理的文件名
    '''
    print "正在下载" + filename
    ua_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko'}

    req = urllib2.Request(url,headers = ua_header)
    response = urllib2.urlopen(req)
    return response.read()

def writePage(html, filename):
    '''
    将html内容写入到本地
    :param html:服务器相应文件内容
    :return:
    '''
    print "正在保存" + filename
    # 文件写入
    with open(filename.decode('utf-8'), "w+") as f:
        f.write(html)
    print "-"*30

def tiebaSpider(url, beginPage, endPage):
    '''
    贴吧作用调度器，负责组合处理每个页面的url
    :return:
    '''
    for page in range(beginPage,endPage+1):
        pn = (page - 1) * 50
        filename = "第" + str(page) + "页.html"
        fullurl = url + "&pn=" + str(pn)
        # print fullurl
        html = loadPage(fullurl,filename)
        # print html
        writePage(html,filename)



if __name__ == "__main__":
    kw = raw_input("请输入贴吧名字：")
    beginPage = int(raw_input("请输入起始页："))
    endPage = int(raw_input("请输入结束页："))

    url = 'http://tieba.baidu.com/f?'
    key = urllib.urlencode({'kw':kw})
    fullurl = url + key
    tiebaSpider(fullurl, beginPage, endPage)
    print '#'*30
    print "thx for using!"
