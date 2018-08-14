#coding=utf-8

# 使用了进程
import threading
# 队列
from Queue import Queue
# 解析库
from lxml import etree
# 请求处理
import requests
# json处理
import json

import time

class ThreadCrawl(threading.Thread):
    def __init__(self, threadName, pageQueue,dataQueue):
        # threading.Thread.__init__(self)
        # 调用父类初始化方法
        super(ThreadCrawl,self).__init__()
        # 线程名
        self.threadName = threadName
        # 页码队列
        self.pageQueue = pageQueue
        # 数据队列
        self.dataQueue = dataQueue
        # 请求报头
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}


    def run(self):
        print "启动" + self.threadName
        while not CRAWL_EXIT:
            try:
                # 取出一个数字
                # 可选参数block，默认值为TRUE
                # 如果队列为空，block=true，不会结束，就会进入阻塞状态，直到队列有新的的数据
                # 如果队列为空，block=false，就会弹出一个Queue.empty()的异常
                page = self.pageQueue.get(False)
                url = "https://www.qiushibaike.com/8hr/page/" + str(page) + "/"
                content = requests.get(url,headers=self.headers).text
                time.sleep(1)
                self.dataQueue.put(content)
                # print len(content)
            except:
                pass
        print "结束" + self.threadName


class ThreadParse(threading.Thread):
    def __init__(self, threadName, dataQueue, fileStream, lock):
        super(ThreadParse,self).__init__()
        # 线程名
        self.threadName = threadName
        # 数据队列
        self.dataQueue = dataQueue
        # 保存解析后数据的文件名
        self.fileStream = fileStream
        # 锁
        self.lock = lock

    def run(self):
        print "启动" + self.threadName
        while not PARSE_EXIT:
            try:
                html = self.dataQueue.get(False)
                self.parse(html)

            except:
                pass
        print "结束" + self.threadName
    def parse(self, html):
        html = etree.HTML(html)
        node_list = html.xpath('//div[contains(@id, "qiushi_tag")]')

        for node in node_list:
            # 用户名
            username = node.xpath('./div/a/@title')[0]

            # 图片链接
            image = node.xpath(".//div[@class='thumb']//@src")  # [0]

            # 段子内容
            content = node.xpath(".//div[@class='content']/span")[0].text

            # 点赞
            content_vote = node.xpath(".//i")[0].text

            # 评论
            comment = node.xpath(".//i")[1].text

            items = {
                "username": username,
                "image": image,
                "content": content,
                "zan": content_vote,
                "comment": comment,
            }
            # with后面有两个必须执行的操作：__enter__和__exit__
            # 不管里面的操作结果如何， 都会执行打开、关闭
            # 打开锁、处理内容、释放锁
            with self.lock:
                # 写入存储的解析后的数据
                self.fileStream.write(json.dumps(items, ensure_ascii=False).encode("utf-8") + "\n")

CRAWL_EXIT = False
PARSE_EXIT = False

def main():

    # 页码的队列，表示存储20个页面
    pageQueue = Queue(20)
    # 放入1-10的数字，先进先出
    for i in range(1,21):
        pageQueue.put(i)

    # 采集结果的数据队列，参数为空时表示不限制大小
    dataQueue = Queue()
    # 创建文件流
    fileStream = open("duanzi.json","a")
    # 创建锁
    lock = threading.Lock()

    # 三个采集线程的名字
    crawllist = ["采集线程1号","采集线程2号","采集线程3号"]

    # 存储三个采集线程列表集合
    threadcrawl = []
    for threadName in crawllist:
        thread = ThreadCrawl(threadName, pageQueue, dataQueue)
        thread.start()
        threadcrawl.append(thread)

    # 三个解析线程的名字
    parselist = ["解析线程1号", "解析线程2号", "解析线程3号"]

    # 存储三个解析线程
    threadparse = []
    for threadName in parselist:
        thread = ThreadParse(threadName, dataQueue, fileStream, lock)
        thread.start()
        threadparse.append(thread)

    # 等待pageQueue队列为空，也就是等待之前的操作执行完毕
    while not pageQueue.empty():
        pass

    # 如果pageQueue为空，采集线程退出循环
    global CRAWL_EXIT
    CRAWL_EXIT = True

    print "pageQueue为空"

    for thread in threadcrawl:
        thread.join()
        print "1"

    # 解析线程
    while not dataQueue.empty():
        pass

    global PARSE_EXIT
    PARSE_EXIT = True

    for thread in threadparse:
        thread.join()
        print "2"

    with lock:
        # 关闭文件
        fileStream.close()


if __name__ == "__main__":
    main()