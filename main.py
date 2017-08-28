#!/usr/bin/python
# encoding: utf-8

"""
@auth: 273327600@qq.com
@time: 2017/8/28 10:52
"""

import requests
import json
import time
import datetime

# Domain Host
host = 'https://enterbj.zhongchebaolian.com'
# 通用headers
headers = {
    'Host': 'enterbj.zhongchebaolian.com',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
    'Connection': 'keep-alive',
    'User-Agent': 'bjsgecl/201704061613 CFNetwork/811.4.18 Darwin/16.5.0',
    'X-Requested-With': 'XMLHttpRequest',
}
# 主页
page_index = '/enterbj/jsp/enterbj/index.html'
# 获取车辆列表
page_entercarlist = '/enterbj/platform/enterbj/entercarlist'
# 车辆注册
page_addcartype = '/enterbj/platform/enterbj/addcartype'
# loadotherdrivers
page_loadotherdrivers = '/enterbj-img/platform/enterbj/loadotherdrivers'
# 最后一步提交的地址
page_submitpaper = '/enterbj-img/platform/enterbj/submitpaper'

# 信息从json文件读取
def loadConfig(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

# 表单数据项
appsource = 'bjjj'
# user.json
user_info = loadConfig('user.json')
userid = user_info['userid']
appkey = user_info['appkey']
deviceid = user_info['deviceid']
timestamp = user_info['timestamp']
token = user_info['token']
sign = user_info['sign']
platform = user_info['platform']

# car.json
car_info = loadConfig('car.json')
licenseno = car_info['licenseno']
engineno = car_info['engineno']
cartypecode = car_info['cartypecode']
vehicletype = car_info['vehicletype']

carid = car_info['carid']
carmodel = car_info['carmodel']
carregtime = car_info['carregtime']

envGrade = car_info['envGrade']

# 其余无用的信息
imei = ''
imsi = ''
gpslon = ''
gpslat = ''
phoneno = ''
code = ''

def getindexdata(userid,appkey,deviceid,timestamp,token,sign,platform,appsource):
    url = host + page_entercarlist
    data = [
        ('userid', userid),
        ('appkey', appkey),
        ('deviceid', deviceid),
        ('timestamp',timestamp),
        ('token',token),
        ('sign',sign),
        ('platform',platform),
        ('appsource',appsource)
    ]
    head = headers
    head['Referer'] = host + page_index
    res = requests.post(url, data=data, headers=head, allow_redirects=False, verify=False)
    if res.status_code in [200, 201]:
        return res.status_code, res.json()
    return res.status_code,None

# 客户端运行python可以无限循环等待，直到成功
result = (0, None)
while True:
    result = getindexdata(userid,appkey,deviceid,timestamp,token,sign,platform,appsource)
    if result[1]:
        if result[1]['rescode'] == '200':
            break

    time.sleep(3)

# 数组，一辆车对应一个
datalist = result[1]['datalist']
# 这里我默认只有一辆车
carobj = datalist[0]
# 是否可以申请，carinfo下边用applyflag来判断
applyflag = carobj['applyflag']
if applyflag != '1':
    print('applyflag != 1, 无需申请')
    #exit(1)

# person.json
person_info = loadConfig('person.json')
drivingphoto = person_info['drivingphoto']
carphoto = person_info['carphoto']
drivername = person_info['drivername']
driverlicenseno = person_info['driverlicenseno']
driverphoto = person_info['driverphoto']
personphoto = person_info['personphoto']
# 进京时间选择
inbjentrancecode1 = '16'
inbjentrancecode = '13'
inbjduration = '7'
# 需要修改的字段：hiddentime，inbjtime，imageId，sign
now = time.localtime(time.time())
hiddentime = time.strftime('%Y-%m-%d %H:%M:%S', now)
# 由于是服务器自动提交，采用的签名从数据库获取，时间用特定的几个点
hiddentime = time.strftime('%Y-%m-%d 00:00:00', now)
# 进京时间，如果存在进京证，则从明天开始，否则是今日开始
inbjtime = time.strftime('%Y-%m-%d', now)
# 默认申请明天的
if True:
    today = datetime.date.today()
    today += datetime.timedelta(days=1)  # 往后加一天
    inbjtime = ('%d-%d-%d' % (today.year, today.month, today.day))

# var imageId = ("#inbjentrancecode").val()+("#inbjduration").val()+("#inbjtime").val()+("#userid").val()+("#engineno").val()+("#cartypecode").val()+("#driverlicensenow").val()+("#carid").val()+timestamp;
imageId = inbjentrancecode+inbjduration+inbjtime+userid+engineno+cartypecode+driverlicenseno+carid+hiddentime

# timestamp_sign.json
sign_info = loadConfig('timestamp_sign.json')
# sign从json中获取
sign = sign_info[hiddentime]
if not sign:
    print("缺少sign值，通知管理员更新json文件")
    exit(1)

# 客户端可以循环一直提交
form = [
('appsource',appsource),
('hiddentime',hiddentime),
('inbjentrancecode1',inbjentrancecode1),
('inbjentrancecode',inbjentrancecode),
('inbjduration',inbjduration),
('inbjtime',inbjtime),
('appkey',''),
('deviceid',''),
('token',''),
('timestamp',''),
('userid',userid),
('licenseno',licenseno),
('engineno',engineno),
('cartypecode',cartypecode),
('vehicletype',vehicletype),
('drivingphoto',drivingphoto),
('carphoto',carphoto),
('drivername',drivername),
('driverlicenseno',driverlicenseno),
('driverphoto',driverphoto),
('personphoto',personphoto),
('gpslon',gpslon),
('gpslat',gpslat),
('phoneno',phoneno),
('imei',imei),
('imsi',imsi),
('carid',carid),
('carmodel',carmodel),
('carregtime',carregtime),
('envGrade',envGrade),
('imageId',imageId),
('code',code),
('sign',sign),
('code',code),
('platform',platform)
]
# Referer
head = headers
head['Referer'] = host + page_loadotherdrivers
head['Content-Type'] = 'application/x-www-form-urlencoded'
# result
result = (0,None)
while True:
    res = requests.post(host + page_submitpaper, data=form, headers=head, allow_redirects=False, verify=False)
    if res.status_code in [200, 201]:
        result = (res.status_code, res.json())
        break

    time.sleep(30)

if result[1]:
    print(result[1]['resdes'])

    if result[1]['rescode'] == '200':
        exit(0)
    else:
        exit(1)

exit(-1)