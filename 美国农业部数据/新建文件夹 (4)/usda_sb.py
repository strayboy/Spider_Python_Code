# -*- coding: utf-8 -*-

import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import xlrd
import time
import os
import pymssql
import datetime
import shutil

# 出口销售


class UsdaSpider(scrapy.Spider):
    name = "refresh"
    start_urls = ["https://apps.fas.usda.gov/esrquery/esrq.aspx"]

    def parse(self, response):
        browser = webdriver.Chrome("D:/tools/chromedriver.exe")
        conn = pymssql.connect(host='.', port='5889', user='Data@Ngoic.org', password='58891135@#*Ngoic',
                               database='NgoicDataAutoCollection', charset='utf8')
        cur = conn.cursor()
        while True:
            try:
                browser.get(response.url)
                s1 = Select(browser.find_element_by_xpath("//*[@id='ctl00_MainContent_lbCommodity']"))
                for select in s1.options:
                    s1.select_by_visible_text(select.text)
                excel = browser.find_element_by_xpath("//*[@id='ctl00_MainContent_rblOutputType_2']")
                excel.click()
                start_date_input = browser.find_element_by_xpath("//*[@id=\"ctl00_MainContent_tbStartDate\"]")
                end_date_input = browser.find_element_by_xpath("//*[@id=\"ctl00_MainContent_tbEndDate\"]")
                cur.execute("select Top 1 Date from USDA_Exports_Sales order by Date desc")
                start_date = datetime.datetime.strptime(cur.fetchone()[0], '%Y-%m-%d') + datetime.timedelta(1)
                if start_date.date() >= datetime.date.today():
                    print ("We have fetched today's data.")
                    return
                start_date_str = start_date.strftime('%m/%d/%Y')
                start_date_input.clear()
                start_date_input.send_keys(start_date_str)
                time.sleep(20)
                end_time_str = datetime.datetime.now().strftime('%m/%d/%Y')
                end_date_input.clear()
                end_date_input.send_keys(end_time_str)
                submit = browser.find_element_by_xpath("//*[@id='ctl00_MainContent_btnSubmit']")
                submit.click()
                time.sleep(20)
                break
            except SyntaxError:
                time.sleep(20)
                continue
        l_excel, sign = self.read_excel()
        browser.quit()
        if sign != "":
            sql_insert = "insert USDA_Exports_Sales values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.executemany(sql_insert, l_excel)
            cur.execute("select Top 1 Date from USDA_Exports_Sales order by Date desc")
            publish_date_str = cur.fetchone()[0]
            cur.execute("update SYS_GlabFlag set PublishTime = %s where Module = '出口销售'", publish_date_str)
        python_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("update SYS_GlabFlag set PythonTime = %s where Module = '出口销售'", python_time_str)
        try:
            conn.commit()
        except:
            conn.rollback()
        cur.close()
        conn.close()

    def read_excel(self):
        data = xlrd.open_workbook('C:\\Users\\Administrator\\Downloads\\ExportSalesDataByCommodity.xls')
        table = data.sheets()[0]
        sign_n = ""
        l_excel = []
        print table.nrows
        for i in range(table.nrows):
            if i >= 7 and table.row_values(i)[2] != '':
                date_format_tuple = xlrd.xldate_as_tuple(table.row_values(i)[2], 0)
                date_format = datetime.date(date_format_tuple[0], date_format_tuple[1], date_format_tuple[2])
                sign_n = str(date_format_tuple[0]) + "-" + str(date_format_tuple[1]) + "-" + str(date_format_tuple[2])
                trans = table.row_values(i)
                trans[2] = date_format
                del trans[0]
                for j in range(len(trans)):
                    if trans[j] == '':
                        trans[j] = None
                l_excel.append(tuple(trans))
        if os.path.exists("C:/Users/Administrator/Downloads/ExportSalesDataByCommodity.xls"):
            if os.path.exists("D:/spider/fasusda/ExportSalesDataByCommodity.xls"):
                os.remove("D:/spider/fasusda/ExportSalesDataByCommodity.xls")
            shutil.move("C:/Users/Administrator/Downloads/ExportSalesDataByCommodity.xls",
                        "D:/spider/fasusda/ExportSalesDataByCommodity.xls")
        if len(l_excel) != 0:
            sign_n = l_excel[0][1]
        return l_excel, sign_n
