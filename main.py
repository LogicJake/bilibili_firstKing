# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-11 18:07:12
# @Last Modified time: 2019-02-11 19:01:26
from functions import get_attentions, new_post, get_content, send_comment
import time


def main():
    interval = 0.2
    mid = 15193611
    attentions = get_attentions(mid)  # 根据mid获取关注列表
    while True:
        for attention in attentions:
            info = new_post(attention)  # 检查是否有新视频发布
            if info != None:
                content = get_content(flag)  # 获取评论内容
                send_comment(info['aid'], content)  # 发表评论
        time.sleep(interval * 60)  # 休眠interval*60s


if __name__ == '__main__':
    main()
