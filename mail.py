# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-11 17:35:48
# @Last Modified time: 2019-02-11 18:57:40
# -*- coding: utf-8 -*-
from aifc import Error
from email.mime.text import MIMEText
from email.header import Header
from smtplib import *
from config import logger
from config import mail_conf


class QQMail():

    def __init__(self):
        # 发件人的邮箱
        self.sender = mail_conf.get_value('sender')
        # 收件人邮箱
        self.receiver = mail_conf.get_value('receiver')
        self.qq = mail_conf.get_value('qq')
        # pwd为qq邮箱的授权码
        self.pwd = mail_conf.get_value('password')

    def send_email(self, content):
        # qq邮箱smtp服务器
        host_server = 'smtp.qq.com'
        mail_content = content['content']
        # 邮件标题
        mail_title = content['title']

        # ssl登录
        try:
            smtp = SMTP_SSL(host_server)
            smtp.login(self.qq, self.pwd)
            msg = MIMEText(mail_content, "plain", 'utf-8')
            msg["Subject"] = Header(mail_title, 'utf-8')
            msg["From"] = self.sender
            msg["To"] = self.receiver
            smtp.sendmail(self.sender, self.receiver, msg.as_string())
            smtp.quit()
        except Exception as e:
            logger.error(e)

qq_mail = QQMail()

if __name__ == '__main__':
    content = {}
    content['content'] = '1'
    content['title'] = '1'
    qq_mail.send_email(content)
