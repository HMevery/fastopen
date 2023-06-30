#!/usr/bin/env python3
#coding=utf-8

import time
import os
import json
import sys
import getopt
import argparse
from parseConfig import *
from mqtt_connect import *

def main():
    config = parseConfig()
    config.parse_cmd_config()
    #print(f'all commend:{config.get_cmd_name_all()}')
    for i in config.get_cmd_name_all():
        exe = config.get_cmd_execute(i)
        print(f"commend {i}:{exe}")
    config.parse_server_config()
    for i in  range(config.get_server_count()):
        print(f"server path:{config.get_server_path(i)},local path:{config.get_local_path(i)}")
    print('**********************************************')
    print('test over')
    print('**********************************************')