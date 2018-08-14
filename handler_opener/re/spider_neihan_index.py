#coding=utf-8
import urllib2
import re

class Spider():
    def __init__(self):
        # 初始化起始页位置
        self.page = 1
        # 爬去开关，如果为TRUE继续爬取
        self.switch = True



    def loadPage(self):
        '''
            下载页面
        :return:
        '''
        print "下载ing。。"
        if self.page == 1:
            url = "http://www.neihan8.com/article/index.html"
        else:
            url = "http://www.neihan8.com/article/index_" + str(self.page) + ".html"
        ua_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko'
        }
        request = urllib2.Request(url,headers=ua_header)
        response = urllib2.urlopen(request)
        # 获取每一页的html源码字符串
        html = response.read()

        # 创建正则表达式规则对象，匹配每页里的段子内容，re.S 表示匹配全部字符串内容
        pattern = re.compile('<div class="desc">(.*?)</div>',re.S)
        # 将正则匹配对象应用到源码字符串，返回页面里所有段子列表
        content_list = pattern.findall(html)
        # for content in content_list:
        #     print content.decode('utf-8')
        # 调用dealPage()处理
        self.dealPage(content_list)

    def dealPage(self,content_list):
        '''
            处理每页的段子,替换的方法replace，sub
        :return:
        '''
        for content in content_list:
            self.writePage(content)

    def writePage(self,content):
        '''
            把每条段子逐个写入文件
        :return:
        '''
        print "正在写入。。。"
        with open("duanzi.txt","a+") as f:
            f.write(content+"\n\r")


    def startWork(self):
        '''
            控制爬虫运行
        :return:
        '''
        self.loadPage()
        while self.switch:
            commond = raw_input("继续请按回车，退出输入quit:")
            if commond == "quit":
                self.switch = False
            self.page += 1
        print "thx for using"


if __name__ == "__main__":
    duanziSpider = Spider()
    # duanziSpider.loadPage()
    duanziSpider.startWork()

