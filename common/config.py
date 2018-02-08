# coding: utf-8
import os
import sys
import json
import re


def open_accordant_config(config_name):
    '''
    调用配置文件
    '''
    config_file = sys.path[0]+os.path.sep+config_name
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            print("[INFO] Load config file from {}".format(config_file))
            return json.load(f)
    else:
        print("[ERROR] Fail to load config file from {}".format(config_file))

