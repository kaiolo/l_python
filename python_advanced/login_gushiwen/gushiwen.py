import requests
from lxml import html
email="3425503053@qq.com"
pwd="gushiwen"
url="https://www.gushiwen.cn/user/login.aspx?tab=account&from=%2Fuser%2Fwode.aspx"

headers={
"referer":"https://www.gushiwen.cn/user/login.aspx?tab=account&from=%2Fuser%2Fwode.aspx",
"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36 Edg/156.0.0.0"
}


session=requests.session()
response=session.get(url)
etree=html.fromstring(response.text)

src=etree.xpath('//*[@id="imgCode"]/@src')[0]
token=etree.xpath("//*[@id='panelAccount']/form/input[1]/@value")[0]

print(token)
img_url="https://www.gushiwen.cn"+src
content=session.get(img_url).content
with open ('./python_advanced/login_gushiwen/captcha.png','wb') as f:
    f.write(content)

code=input('输入验证码')
data={
    "__RequestVerificationToken":token,
    "from":"/user/wode.aspx",
    "email":email,
    "pwd":pwd,
    "code":code
}

page=session.post(url=url , data=data , headers=headers).text

with open ("./python_advanced/login_gushiwen/page.html","w",encoding='utf-8') as f:
    f.write(page)
