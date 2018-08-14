#coding=utf-8

import unittest
#  导入webdriver API对象，可以调用浏览器操作页面
from selenium import webdriver
from bs4 import BeautifulSoup as bs

class douyu(unittest.TestCase):
    # 初始化方法，必须是setUp
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.num = 0
        self.count = 0

    # 测试方法必须有test字样开头
    def testDouyu(self):
        self.driver.get("https://www.douyu.com/directory/all")
        while True:
            soup = bs(self.driver.page_source, "lxml")
            # 房间名, 返回列表
            roomnames = soup.find_all("h3", {"class":"ellipsis"})
            # 观众人数, 返回列表
            numbers = soup.find_all("span", {"class":"dy-num fr"})
            # zip(roomnames, numbers)将俩个列表合并为一个元组：[（1,2）,(3,4),...]
            for roomname, number in zip(roomnames, numbers):
                print u"观众人数:-" + number.get_text().strip() + u"-\t\t房间名：" + roomname.get_text().strip()
                self.num += 1

            # 如果在页面源码里找到“下一页”为隐藏的标签，就退出循环
            if self.driver.page_source.find("shark-pager-disable-next") != -1:
                break

            # 一直点击下一页
            self.driver.find_element_by_class_name("shark-pager-next").click()

    # 测试结束执行的方式
    def tearDown(self):
        # 退出PhantomJS（）浏览器
        print self.num

        self.driver.quit()

if __name__ == "__main__":
    # 启动测试模块
    unittest.main()