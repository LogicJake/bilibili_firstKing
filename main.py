import re

import requests
import json
import time

def get_cookie():
    cookie = {}
    with open("cookie.txt", 'r') as f:
        ress = json.load(f)
        for res in ress:
            cookie[res['name']] = res['value']
    return cookie

def send_comment(av,message,cookie):
    url = "https://api.bilibili.com/x/v2/reply/add"
    data = {'oid': av, 'type' : 1, 'message':message, 'plat' : 1, 'jsonp':'jsonp','csrf': cookie['bili_jct']}
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Referer': 'https://www.bilibili.com',
        'Origin': 'https://www.bilibili.com',
        'Host':'api.bilibili.com'
    }

    response = requests.post(url,headers=headers,data=data,cookies=cookie)
    response = json.loads(response.text)
    if response['code'] == 0:
        print('发送成功')

def get_content():      #自定义需要回复的评论
    return "我住在b站了"

def new_post(mid):
    url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&page=1&pagesize=1".format(mid)     #根据mid获取最新的投稿
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Referer': 'https://www.bilibili.com',
        'Origin': 'https://www.bilibili.com',
        'Host': 'space.bilibili.com'
    }

    response = requests.get(url,headers=headers)
    result = {}
    res = json.loads(response.text)['data']['vlist'][0]
    result['created_time'] = res.get('created',0)
    result['description'] = res.get('description','null')
    result['title'] = res.get('title','null')
    result['aid'] = res.get('aid',0)
    if int(time.time())-result['created_time'] < 60:      #在1min之内证明是最新投稿
        return result
    return None

def get_name(mid):
    data = {'mid': mid, 'csrf': 'null'}
    header = {
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Content-Length': '20',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://space.bilibili.com',
        'Origin': 'https://space.bilibili.com'
    }
    try:
        proxies = {"http":"119.27.177.169:80"}
        response = requests.post('http://space.bilibili.com/ajax/member/GetInfo', headers=header, data=data,timeout=5,proxies=proxies)
        content = response.content.decode('utf-8')
        if content.find('status') != -1:
            res = json.loads(content)
            if res['status']:
                json_data = res['data']
                name = json_data['name']
                return name
    except Exception as e:
        print(e)

def get_attentions(var,type=0):        #获取关注者的mid
    '''
    :param var: mid或者姓名
    :param type: 0为姓名，1为mid
    :return: 关注者的mid列表
    '''
    name = var
    if type == 1:
        name = get_name(var)
    url = "http://interface.bilibili.com/card/{}.js".format(name)
    try:
        response = requests.get(url).content.decode('utf-8')
        pattern = re.compile(r'ShowCard\((.*)\)',re.DOTALL)
        m = pattern.match(response)
        res = json.loads(m.group(1))
        attentions = res.get('attentions')
        print(attentions)
        return attentions
    except Exception as e:
        print(e)

if __name__ == '__main__':
    cookie = get_cookie()                               #获取cookie
    attentions = get_attentions(15193611,1)             #根据mid获取关注列表
    for attention in attentions:
        flag = new_post(attention)  # 检查是否有新视频发布
        if flag != None:
            content = get_content()  # 获取评论内容
            send_comment(flag['aid'], content, cookie)  # 发表评论
