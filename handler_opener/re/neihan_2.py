#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib2
import re

class Spider:
    def __init__(self):
        # 初始化起始页位置
        self.page = 1
        # 爬取开关，如果为True继续爬取
        self.switch = True

    def loadPage(self):
        """
            作用：下载页面
        """
        print "正在下载数据...."
        if self.page == 1:
            url = "http://www.neihan8.com/article/"
        else:
            url = "http://www.neihan8.com/article/index_" + str(self.page) + ".html"
        headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        request = urllib2.Request(url, headers = headers)
        response = urllib2.urlopen(request)

        # 获取每页的HTML源码字符串
        html = response.read()
        #print html

        # 创建正则表达式规则对象，匹配每页里的段子内容，re.S 表示匹配全部字符串内容
        pattern = re.compile('<a href="/article/(\d+).html"', re.S)

        # 将正则匹配对象应用到html源码字符串里，返回这个页面里的所有段子的列表
        page_list = pattern.findall(html)
        page_list = page_list[:20]

        # for content in page_list:测试
        #     print content

        # 拼接新的url地址
        newUrl_list = []
        for page in page_list:
            newUrl_list.append("http://www.neihan8.com/article/" + page + ".html")
        print newUrl_list

        # 调用dealPage() 处理新地址
        self.dealPage(newUrl_list)

    def dealPage(self, newUrl_list):
        """
            处理新地址
            newUrl_list : 每页的段子列表
        """
        ua_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko'
        }
        for item in newUrl_list:
            request = urllib2.Request(url=item, headers=ua_header)
            response = urllib2.urlopen(request)
            # 获取每一页的html源码字符串
            item_html = response.read()

            # 正则提取处理数据
            pattern = re.compile('<p>(.*?)</p>', re.S)
            item_content_list = pattern.findall(item_html)
            content_list = []
            for content in item_content_list:
                item_content = content.replace("请文明发言，严禁散播谣言和诽谤他人~","").replace('Copyright 2005-2015 Neihan8.com <a href="/" target="_blank" title="内涵吧">内涵吧</a> 版权所有 <span style="color: #333333; font-size: 12px; line-height: 16px;">沪ICP备14040517号-1</span> <div style="display:none;"><script language="javascript" src="/js/stats.js?fee3fv"></script></div>',"")
                # 处理完后调用writePage() 将每个段子写入文件内
                self.writePage(item_content)

    def writePage(self, item_content):
        """
            把每条段子逐个写入文件里
            item: 处理后的每条段子
        """
        # 写入文件内
        print "正在写入数据...."
        with open("duanzi.txt", "a") as f:
            f.write(item_content)

    def startWork(self):
        """
            控制爬虫运行
        """
        # 循环执行，直到 self.switch == False
        while self.switch:
            # 用户确定爬取的次数
            self.loadPage()
            command = raw_input("如果继续爬取，请按回车（退出输入quit)")
            if command == "quit":
                # 如果停止爬取，则输入 quit
                self.switch = False
            # 每次循环，page页码自增1
            self.page += 1
        print "谢谢使用！"


if __name__ == "__main__":
    duanziSpider = Spider()
    # duanziSpider.loadPage()
    duanziSpider.startWork()

