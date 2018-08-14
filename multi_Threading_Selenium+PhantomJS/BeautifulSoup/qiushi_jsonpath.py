#coding=utf-8
import urllib2
from lxml import etree
import json


url = "https://www.qiushibaike.com/8hr/page/3/"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}

request = urllib2.Request(url, headers=headers)

html = urllib2.urlopen(request).read()

# 响应返回的是字符串，解析为HTML_DOM模式
text = etree.HTML(html)

# 根节点//div[contains(@id, "qiushi_tag")]
# 返回所有段子的节点位置，contains（）模糊查询方法，第一个参数是匹配的标签，第二个部分是标签名部分参数内容
node_list = text.xpath('//div[contains(@id, "qiushi_tag")]')

items = {}

for node in node_list:
    # 用户名
    username = node.xpath('./div/a/@title')[0]

    # 图片链接
    image = node.xpath(".//div[@class='thumb']//@src") # [0]

    # 段子内容
    content = node.xpath(".//div[@class='content']/span")[0].text

    # 点赞
    content_vote = node.xpath(".//i")[0].text

    # 评论
    comment = node.xpath(".//i")[1].text

    items = {
        "username" : username,
        "image" : image,
        "content" : content,
        "zan" : content_vote,
        "comment" : comment,
    }

    with open("qiushi.json","a") as f:
        f.write(json.dumps(items, ensure_ascii=False).encode("utf-8") + "\n")