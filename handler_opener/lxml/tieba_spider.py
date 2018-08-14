# coding= utf-8
import urllib2,urllib
from lxml import etree

def loadPage(url):
    '''根据url发送请求，获取服务器响应文件
        url:需要爬取的URL地址
    '''
    # print "正在下载"
    ua_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko'}

    req = urllib2.Request(url,headers = ua_header)
    html = urllib2.urlopen(req).read()
    # 解析html文档为html_dom模型
    content = etree.HTML(html)
    # 返回所有匹配成功的列表集合
    link_list = content.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
    for link in link_list:
        fulllink = "http://tieba.baidu.com" + link
        loadImage(fulllink)

# 取出每个帖子里的图片链接
def loadImage(link):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko'
               }
    request = urllib2.Request(link,headers=headers)
    html = urllib2.urlopen(request).read()
    content = etree.HTML(html)
    # 返回帖子里所有图片链接的列表集合
    link_list = content.xpath('//img[@class="BDE_Image"]/@src')
    for link in link_list:
        # print link
        writeImage(link)


def writeImage(link):
    '''
    将link内容写入到本地
    :param link:每层图片链接地址
    :return:
    '''
    # tieba图片写入
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko'
        }
    request = urllib2.Request(url=link, headers=headers)
    image = urllib2.urlopen(request).read()
    filename = link[-10:]
    with open(filename, "wb") as f:
        f.write(image)
    print "succeed  downloading"

def tiebaSpider(url, beginPage, endPage):
    '''
    贴吧作用调度器，负责组合处理每个页面的url
    :return:
    '''
    for page in range(beginPage,endPage+1):
        pn = (page - 1) * 50

        fullurl = url + "&pn=" + str(pn)

        html = loadPage(fullurl)




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
