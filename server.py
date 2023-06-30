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
import test
import adbcommend


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

def usage():
    #print ('***********************')

    config = parseConfig()
    config.parse_cmd_config()
    commend = config.get_cmd_name_all()

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

def callback(client,topic,data):
    print(data)
    client.disconnect()
    

def send_commend(commend,data):
    send_str = data
    print("send string: "+commend)
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
    rcv = mqtt_connect()
    status = rcv.subscribe(config.get_mqtt_server(),
                            config.get_mqtt_port(),
                            config.get_mqtt_keepalive_sec(),
                            config.get_mqtt_client_id(),
                            config.get_mqtt_topic()+'local',
                            callback)    
    return




def path_back_previous(path):
    data = path

    tmp = path.split('/')
    #print(tmp)
    for i in range(tmp.count('..')):
        index = tmp.index('..')
        tmp.pop(index)
        tmp.pop(index-1)
    #print(tmp)
    data = '/'.join(tmp) 
    return data

def server_path_to_local(path):
    parse_config = parseConfig()
    parse_config.parse_server_config()

    index = 0
    data = path
    while True:
        server_path = parse_config.get_server_path(index)
        local_path = parse_config.get_local_path(index)
        #print(f"path = {data},server path = {server_path},local path = {local_path}")
        if local_path == None or server_path == None:
            break
        index = index +1
        if path.find(server_path) != -1:
            data = path.replace(server_path,local_path)     
            break 
    return data

'''def execute_path_replace(path):
    
    #path = path_back_previous(path)
    #将目录替换为目标目录
    p = server_path_to_local(path)
    return p '''   
    
    
def format_execute(args,indata):
    inparam = ''
    if args.param != None:
        inparam = " ".join(args.param)
    file_path = args.file_path  

    indata = indata.format(file = file_path,param = inparam)  
    
    if os.getenv('OUT') != None:
        indata = indata.replace("TARGET_OUT",os.getenv('OUT'))
    
    #处理路径中的返回上层符号
    path = path_back_previous(indata)
    #print(path)
    if path.find('adb push') != -1:
            path = adbcommend.push(path)

    #将目录替换为目标目录
    path = server_path_to_local(path)
    
    #print(f"in param = {inparam}")
    '''print(args.file_path)
    #处理路径中的返回上层符号
    file_path = path_back_previous(args.file_path)
    #将目录替换为目标目录
    file_path = server_path_to_local(file_path)
    #格式化命令
    indata = indata.replace("TARGET_OUT",os.getenv('OUT'))
    data = indata.format(file = file_path,param = inparam)'''

    #print(data)
    #data = execute_path_replace(cmd)
    '''if path != None:
        #给adb push 增加参数
        if args.param == None and path.find('adb push') != -1:
        #print("param:",data)  
            path = adbcommend.push(path)'''
    return path

def commend_encode(commend_name,args):
    parse_config = parseConfig()
    parse_config.parse_cmd_config()
    local = parse_config.get_cmd_execute(commend_name)
    #print("local cmd = ",local)
    if local == None:
        print('commed is must:',parse_config.get_cmd_name_all())
        sys.exit(2)

    #将要发送的数据拼装成json格式
    json_array = []
    if str(type(local)).find("list") != -1:
        count = 0
        for l in local:
            data = format_execute(args,l)
            #d = dict()
            #d[count] = data
            json_array.append(data)
            count = count + 1  
    else:
        data = format_execute(args,local)
        #d = dict()
        #d[0] = data
        json_array.append(data)

    tmp_json = {"commend":commend_name}    
    tmp_json["execute"] = json_array    
    data_json=json.dumps(tmp_json,sort_keys=True,indent=4)
    #print(data_json)
    return data_json



def main(argv):
    #test.main()
    args = usage()
    commend_name = args.commend
    if commend_name == 'ServerInstall':
        server_install()
        sys.exit(2)

    send_str = commend_encode(commend_name,args)
    #print(send_str)
    send_commend(commend_name,send_str)

if __name__ == "__main__":
    main(sys.argv[1:])



 
            
            