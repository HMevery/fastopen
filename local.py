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


def send_result(data):
    send_str = data
    config = parseConfig()
    config.get_mqtt_config()

    send = mqtt_connect()
    status = send.publish(config.get_mqtt_server(),
                          config.get_mqtt_port(),
                          config.get_mqtt_keepalive_sec(),
                          config.get_mqtt_client_id(),
                          config.get_mqtt_topic()+'local',
                          send_str)
    if status != 0:
        print("send error")
    return


def callback(client,topic,data):
    print(data)
    json_data = json.loads(data)
    commend = json_data["commend"]
    execute = json_data["execute"]

    if str(type(execute)).find("list") != -1:    
        for exe in execute:
            if exe[:4].find('adb')!= -1:
                #os.system(f"start cmd /k \"{exe}\"")
                result = os.system(exe)
                if result != 0:
                    t = "error,"+exe
                    send_result(t)
                    break
            else:
                os.system(exe.replace('/','\\'))
    send_result("success")

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



 
            
            