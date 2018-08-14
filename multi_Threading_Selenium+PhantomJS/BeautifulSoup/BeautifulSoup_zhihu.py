# coding=utf-8
from bs4 import BeautifulSoup
import requests
import time

def captcha(captcha_data):
    with open("captcha.jpg","wb") as f:
        f.write(captcha_data)
    text = raw_input("请输入验证码：")
    return text

def zhihulogin():

    # 构建一个Session对象，可以保存Cookie
    session = requests.Session()

    user_headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}

    # 首先获取登录页面，找到需要post的数据（_xsrf）,同事会记录当前网页的Cookie值
    html = session.get("https://www.zhihu.com/#signin",headers=user_headers).text

    # 调用lxml解析库
    bs = BeautifulSoup(html,"lxml")

    # 获取之前get的页面里的_xsfr值
    _xsrf = bs.find("input",attrs={"name":"_xsrf"}).get("value")
    # _xsrf作用是防止csrf攻击（夸张请求伪造），跨域攻击，是一种利用网站对用户的信任机制来做攻击
    # 跨域攻击通常通过伪造成网站信任的用户请求（利用Cookie值），盗取用户信息，欺骗网络服务器

    # print _xsrf

    captcha_url = "https://www.zhihu.com/captcha.gif?r=%d&type=login&lang=cn"%(time.time()*1000)
    # 发送图片的请求，获取图片数据流
    captcha_data = session.get(captcha_url,headers = user_headers).content
    # 获取验证码里的文字，需要手动输入
    text = captcha(captcha_data)
    data = {
        "_xsrf":_xsrf,
        "email":"*****",
        "passworld":"*****",
        "captcha":text
    }

    response = session.post("https://www.zhihu.com/login/email", data=data, headers=user_headers)
    # print response

    res = session.get("https://www.zhihu.com/people/zui-bai-cai/activities",headers = user_headers)
    # print res.text
    with open("zhihulogin.html","w") as f:
        f.write(res.text.encode("utf-8"))


if __name__ == "__main__":
    zhihulogin()