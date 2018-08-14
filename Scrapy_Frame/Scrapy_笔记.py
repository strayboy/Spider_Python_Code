Scrapy 项目步骤：

1. 创建项目
scrapy startproject xxx

2. 编写 items.py 文件
	设置需要保存的数据字段

3. 进入xxx（项目名称）/spiders
	编写爬虫文件，文件里的name就爬虫名（不同于项目名称）

4. 运行
	scrapy crawl itcast
	scrapy crawl itcast -o csv/json/xml



##################################################################
scrapy shell "http://hr.tencent.com/position.php?&start=0#a"


response.xpath("//title")
[<Selector xpath='//title' data=u'<title>\u804c\u4f4d\u641c\u7d22 | \u793e\u4f1a\u62db\u8058 | Tencent \u817e\u8baf\u62db\u8058</title'>]

response.xpath("//title").extract()
[u'<title>\u804c\u4f4d\u641c\u7d22 | \u793e\u4f1a\u62db\u8058 | Tencent \u817e\u8baf\u62db\u8058</title>']

response.xpath("//title").extract()[0]
u'<title>\u804c\u4f4d\u641c\u7d22 | \u793e\u4f1a\u62db\u8058 | Tencent \u817e\u8baf\u62db\u8058</title>'

print response.xpath("//title").extract()[0]
<title>职位搜索 | 社会招聘 | Tencent 腾讯招聘</title>
print response.xpath("//title/text()").extract()[0]
职位搜索 | 社会招聘 | Tencent 腾讯招聘

