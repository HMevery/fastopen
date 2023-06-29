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



def server_install():
    config = parseConfig()
    config.parse_cmd_config()
    shell_name = os.getcwd()+'/'+'open.sh'
    run_name = os.getcwd()+'/'+__file__
    alias = ''
    with open(shell_name,'w') as f:
        f.writelines('#!/bin/bash\n')
        f.writelines('FILE=$(pwd)/$2\n')
        index = 0
        while True:
            commend = config.get_first_cmd_from_index(index)
            index = index +1
            if commend == None:
                break
            local = config.get_local_cmd(commend)
            if local == None:
                break

            file = ''
            param = ''
            flag = '$2'
            if local.find('{file}') != -1:
                file = '-f $FILE '
                flag = ''
            if local.find('{param}') != -1:
                param = f'-p {flag} $3 $4 $5 $6'
                
            f.writelines(f'if [ {commend} = $1 ];then\n')
            f.writelines(f'    python3 {run_name} -c {commend} {file} {param} \n')    
            f.writelines(f'fi\n')

            alias = alias +f'alias {commend}=\'{shell_name} {commend} \'\n'          
    print(alias)  


def push(path):
    data = path
    src = path.replace('\\','/')
    index = src.find("/system/")
    if index == -1:
        index = src.rfind("/vendor")
    if index == -1:
        index = src.rfind("/product")
    if index != -1:
        dest = ''
        if os.path.isdir(src):
            t = src.rfind("/")
            dest = src[index:t+1]
        else:    
            dest = src[index:]

        data = f"adb remount && {src} {dest}"
    return data



def path_replace(commend,param,path):
    #处理路径中的返回上层符号
    data = path
    if path.find('../') != -1:
        tmp = path.split('/')
        d = ''
        for a in range(10):
            for i in range(len(tmp)-1):
                if tmp[i] == '..':
                    del tmp[i]
                    del tmp[i-1]
                    break
        data = ''
        for i in range(len(tmp)):   
            data = data + tmp[i]
            if i != len(tmp)-1:
                data = data + '/'
    #将目录替换为目标目录
    index = 0
    commend.get_server_path_config()
    while True:
        server_path = commend.get_server_path(index)
        if server_path == None:
            break
        local_path = commend.get_local_path(index)
        if local_path == None:
            break
        index = index +1
        if data.find(server_path) != -1:
            data = data.replace(server_path,local_path)      
    #给adb push 增加参数
    if param == None and data.find('adb push') != -1:
        #print("param:",data)  
        data = push(data)
    return data
    

def send_commend(commend,data):
    send_str = commend+','+data
    print("send string: "+send_str)
    config = parseConfig()
    config.get_mqtt_config()

    send = mqtt_connect()
    status = send.publish(config.get_mqtt_server(),
    config.get_mqtt_port(),
    config.get_mqtt_keepalive_sec(),
    config.get_mqtt_client_id(),
    config.get_mqtt_topic(),
    send_str)
    if status != 0:
        print("send error")
    return
def usage():
    #print ('***********************')

    config = parseConfig()
    config.parse_cmd_config()
    commend = config.get_all_cmd()

    if sys.argv[len(sys.argv)-1] == '-p':
        sys.argv.pop()
    parser = argparse.ArgumentParser(description='linux server to win')
    parser.add_argument('-c','--commend',dest='commend', type=str,required=True,help=f'command must be the following:ServerInstall,{commend}')
    parser.add_argument('-f', '--file',dest='file_path',type=str,help='file path')
    parser.add_argument('-p', dest='param',type=str,nargs='+',help='param')
    
    
    args = parser.parse_args()
    #print(args.commend)
    #print(args.file_path)
    #print(args.param)
    #print ('***********************')
    return args


def main(argv):
    
    args = usage()
    if args.commend == 'ServerInstall':
        server_install()
        sys.exit(2)
    #sys.exit(2)
    #options = get_option(argv)
    #print(options)
    commend = parseConfig()
    commend.parse_cmd_config()
    local = commend.get_local_cmd(args.commend)
    #print("local cmd = ",local)
    if local == None:
        print('commed is must:',commend.get_all_cmd())
        sys.exit(2)
    str = ''
    if args.param != None:
        for i in range(len(args.param)):
            str = str + args.param[i] + " "
    data = local.format(file = args.file_path,param = str)
    
    send_commend(args.commend,path_replace(commend,args.param,data))

if __name__ == "__main__":
    main(sys.argv[1:])



 
            
            