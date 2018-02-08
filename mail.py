# -*- coding: utf-8 -*-
from aifc import Error
from email.mime.text import MIMEText
from email.header import Header
from smtplib import *
from common import Global
Global.__init__()
def SendEmail(content):
    # qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    # pwd为qq邮箱的授权码
    pwd = Global.get_value('pwd')
    # 发件人的邮箱
    sender_qq_mail = Global.get_value('sender')
    # 收件人邮箱
    receiver = Global.get_value('recipient')
    # 邮件的正文内容
    mail_content = content['content']

    # 邮件标题
    mail_title = content['title']

    # ssl登录

    try:
        smtp = SMTP_SSL(host_server)
        smtp.login(Global.get_value('qq'), pwd)
        msg = MIMEText(mail_content, "plain", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = sender_qq_mail
        msg["To"] = receiver
        smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
        smtp.quit()
    except Error as e:
        print(e)