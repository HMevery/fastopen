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


def callback(topic,data):
    #print(data)
    cmd = data.split(',')[1]
    if cmd[:4].find('adb')!= -1:
        #os.system("start cmd /k \""+cmd+"\"")
        os.system(f"start cmd /k \"{cmd}\"")
    else:
        os.system(cmd.replace('/','\\'))

def main(argv):
    
    config = parseConfig()
    config.get_mqtt_config()
    print("local start*****")
    rcv = mqtt_connect()
    status = rcv.subscribe(config.get_mqtt_server(),
                            config.get_mqtt_port(),
                            config.get_mqtt_keepalive_sec(),
                            config.get_mqtt_client_id(),
                            config.get_mqtt_topic(),
                            callback)


    

if __name__ == "__main__":
    #main()
    main(sys.argv[1:])



 
            
            