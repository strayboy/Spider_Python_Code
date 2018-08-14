#coding=utf-8
import urllib2,urllib

url = 'http://www.renren.com/287807015/profile'

ua_header = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Content-Type":"application/x-www-form-urlencoded",
    "Accept":"*/*",
    "Cookie":"anonymid=j4sekxo8-2yvowr; depovince=BJ; jebecookies=f1031552-95d4-41ac-a5d8-59adcbb17f74|||||; _r01_=1; JSESSIONID=abcYOuScJScEDb1vQ2x0v; ick_login=5f78e0e8-c597-4b2f-ac8f-31661fb3f08f; _de=7C6278BA56CF8ABC72FFEFECAA50653A696BF75400CE19CC; p=aa5f19c91385ccbf1846f1c9c73a19db5; first_login_flag=1; ln_uact=910916988@qq.com; ln_hurl=http://hdn.xnimg.cn/photos/hdn521/20140116/1955/h_main_fkx1_034600029b1a111a.jpg; t=95629b9820a9e3347fa9681e21f0f96a5; societyguester=95629b9820a9e3347fa9681e21f0f96a5; id=328199985; xnsid=e81860de; jebe_key=bd0cfac7-eb88-4b1b-8688-721723420511%7C3c77173ca9369463804c3d104af61d80%7C1499344645466%7C1%7C1499344642935; ver=7.0; loginfrom=null; XNESSESSIONID=542b0b9a2395; wp=0; wp_fold=0",
}

request = urllib2.Request(url,headers=ua_header)
response = urllib2.urlopen(request)
print response.read()