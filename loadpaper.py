#!/usr/bin/python
# encoding: utf-8

"""
@auth: zhaopan
@time: 2017/11/6 09:21
"""

import requests
from bs4 import BeautifulSoup

# Domain Host
host = 'https://enterbj.zhongchebaolian.com'
domain = 'enterbj.zhongchebaolian.com'
# 通用headers
headers = {
    'Host': domain,
    'Origin': host,
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; E6883 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}
# 主页
page_index = '/enterbj/jsp/enterbj/index.html'
# loadpaper
page_loadpaper = '/enterbj/platform/enterbj/loadpaper'

def loadPaper(applyid):
    url = host + page_loadpaper
    data = [
        ('applyid', applyid)
    ]
    head = headers
    head['Referer'] = host + page_index
    res = requests.post(url, data=data, headers=head, allow_redirects=False, verify=False)
    if res.status_code in [200, 201]:
        return res.content
    return None

def loadPaperFlowingNo(html):
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    tag = soup.find('p', class_='Nop')
    return tag.get_text()

applyid = ''
res = getPaperImage(loadPaperFlowingNo(applyid))
print(res)
