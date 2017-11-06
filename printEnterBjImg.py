#!/usr/bin/python
# encoding: utf-8

"""
@auth: zhaopan
@time: 2017/11/6 09:41
"""

import requests

host = 'api.jinjingzheng.zhongchebaolian.com'
origin = 'http://api.jinjingzheng.zhongchebaolian.com'
# 通用headers
headers = {
    'Host': host,
    'Origin': origin,
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; E6883 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}
# 获取参数
url_getApply= 'http://api.jinjingzheng.zhongchebaolian.com/enterbj_print/filetransfer/print/getEnterBjApply'
# 生成图片
url_generate = 'http://api.jinjingzheng.zhongchebaolian.com/enterbj_print/filetransfer/print/generateEnterBjImgByApplyid'

def getEnterBjApply(flowingNo,lisenceno):
    url = url_getApply
    data = [
        ('licenseNo', lisenceno),
        ('flowingNo', flowingNo)
    ]
    head = headers
    head['Referer'] = origin + '/enterbj_print/jsp/print.jsp'
    res = requests.post(url, data=data, headers=head, allow_redirects=False, verify=False)
    if res.status_code in [200, 201]:
        return res.json()
    return None

def generateEnterBjImgByApplyid(json):
    url = url_generate
    data = [
        ('licenseno', json['licenseno']),
        ('drivername', json['drivername']),
        ('starttime', json['starttime']),
        ('endtime', json['endtime']),
        ('applyid', json['applyid']),
        ('createtime', json['createtime']),
        ('address', json['address']),
        ('paperid', json['paperid']),
        ('cartype', json['cartype'])
    ]
    head = headers
    head['Referer'] = origin + '/enterbj_print/jsp/print.jsp'
    res = requests.post(url, data=data, headers=head, allow_redirects=False, verify=False)
    if res.status_code in [200, 201]:
        return res.json()
    return None

# 进京证编号
flowingNo = ''
# 车牌号
lisenceno = ''
res = generateEnterBjImgByApplyid(getEnterBjApply(flowingNo,lisenceno))
print(res['imgPath'])
