# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-11 17:46:17
# @Last Modified time: 2019-02-11 19:00:41

import requests
import json
import time
from mail import qq_mail
from config import logger


def get_cookie():
    cookie = {}
    with open("cookie.txt", 'r') as f:
        ress = json.load(f)
        for res in ress:
            cookie[res['name']] = res['value']
    return cookie


def send_mail(type, message, av):
    message = (str)(message)
    send_message = {}
    if type == 1:
        send_message['title'] = "av{}: 发送评论成功".format(av)
        logger.info("av{}: 发送评论成功".format(av))
        send_message['content'] = message
    else:
        send_message['title'] = "av{}: 发送评论失败".format(av)
        logger.info("av{}: 发送评论失败".format(av))
        send_message['content'] = message
    qq_mail.send_email(send_message)


def send_comment(av, comment):
    cookie = get_cookie()

    url = "https://api.bilibili.com/x/v2/reply/add"
    data = {'oid': av, 'type': 1, 'message': comment,
            'plat': 1, 'jsonp': 'jsonp', 'csrf': cookie['bili_jct']}
    try:
        response = requests.post(url, data=data, cookies=cookie)
        response = json.loads(response.text)
        if response['code'] == 0:
            send_mail(1, response, av)
        else:
            send_mail(0, response, av)
    except Exception as e:
        logger.error(e)


def get_content(info):  # 自定义需要回复的评论
    return "我住在b站了"


def new_post(mid):
    # 根据mid获取最新的投稿
    url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&page=1&pagesize=1".format(
        mid)
    try:
        response = requests.get(url)
        result = {}
        res = json.loads(response.text)['data']['vlist'][0]
        result['mid'] = res.get('mid', 0)
        result['created_time'] = res.get('created', 0)
        result['description'] = res.get('description', 'null')
        result['title'] = res.get('title', 'null')
        result['aid'] = res.get('aid', 0)

        if int(time.time()) - result['created_time'] < 30:  # 在1min之内证明是最新投稿
            return result
        else:
            return None
    except Exception as e:
        logger.error(e)


def get_attentions(mid):  # 获取关注者的mid
    url = "https://api.bilibili.com/x/relation/followings?vmid={}".format(mid)
    try:
        response = requests.get(url)
        content = response.content.decode('utf-8')

        res = json.loads(content)
        data = res.get('data').get('list')
        attentions = [d.get('mid') for d in data]
        return attentions
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    send_comment(32781021, 'good')
