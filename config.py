# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-11 17:06:22
# @Last Modified time: 2019-02-11 18:57:04
import logging
import logging.config
import json
import os


# read conf for log
os.makedirs('log', exist_ok=True)
logging.config.fileConfig("log.conf")
logger = logging.getLogger()
logger.info('Finish loading config for logging')


class MailConf():

    def __init__(self):
        # read conf for mail
        mail_conf = 'mail.conf'
        if os.path.exists(mail_conf):
            with open(mail_conf, 'r') as f:
                self.conf = json.load(f)
                logger.info("Finish loading config for mail")
        else:
            logger.error("Fail to load config from {}".format(mail_conf))

    def get_value(self, key, defValue=None):
        try:
            return self.conf[key]
        except KeyError:
            return defValue

mail_conf = MailConf()
