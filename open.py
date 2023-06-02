#!/usr/bin/env python3
#coding=utf-8

from watchdog.observers import Observer
from watchdog.events import *
import time
import os
import json

def open_directory(path):
    p = path.replace('/','\\')
    os.system('start explorer '+p)
    '''if platform.system().lower() == 'windows':
        p = path.replace('/','\\')
        os.system('start explorer '+p)   '''
    #elif platform.system().lower() == 'linux':
        #print("linux")

def push(path,param):
    print("param = "+param)
    if len(param) == 0:   
        src = path.replace('\\','/')
        #print(src)
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
            #cmd = "adb remount"
            #os.system(cmd)    
            cmd = f"adb remount && adb push {src} {dest}"
            print(cmd)
            os.system("start cmd /k \""+cmd+"\"")
    else :
        src = path
        dest = param
        
        #cmd = "adb remount"
        #os.system(cmd)
        
        cmd = "adb push "+src+" "+dest
        print(cmd)
        #os.system(cmd)
        os.system("start cmd /k \""+cmd+"\"")


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path,event.dest_path))
        else:
            print("file moved from {0} to {1}".format(event.src_path,event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            print("file modified:{0}".format(event.src_path))
            start_command()


monitor_path = {}
server_path = {}
command_path = {}
def get_param():
    with open("config.json",'r') as f:
        param = json.load(f)
        #win监控的文件夹
        monitor_path["dir"] = param["monitor path"]["dir"]
        #服务器脚本写命令文件对应的win路径
        monitor_path["file"] = param["monitor path"]["file"]

        #服务器路径和映射到windows的路径
        keys = param["server path"].keys()
        for i in range(len(keys)):
            server_path[f"server{i}"] = param["server path"][list(keys)[i]]["server"]
            server_path[f"windows{i}"] = param["server path"][list(keys)[i]]["windows"]

        #命令
        cmd = param["window command"].keys()
        #print(cmd)
        for i in range(len(cmd)):
            if len(param["window command"][list(cmd)[i]]["short"]) == 0:
                if "cmd_directory" == list(cmd)[i]:
                    command_path[f"short{i}"] = "cmd_directory"
                    command_path[f"cmd{i}"] = param["window command"][list(cmd)[i]]["cmd"]
                    continue
                elif "cmd_file" == list(cmd)[i]:
                    command_path[f"short{i}"] = "cmd_file"
                    command_path[f"cmd{i}"] = param["window command"][list(cmd)[i]]["cmd"]
                    continue
            command_path[f"short{i}"] = param["window command"][list(cmd)[i]]["short"]
            command_path[f"cmd{i}"] = param["window command"][list(cmd)[i]]["cmd"]

        print(monitor_path.items())
        print(server_path.items())
        print(command_path.items())



def run_cmd(path,short,other_param):
    if path == None or short == None:
        return  
    if short == "push":
        push(path,other_param)   
        return 
    if len(short) == 0:
        if os.path.isdir(path):
            short = "cmd_directory"
            path = path.replace('/','\\')
        else:    
            short = "cmd_file"
    for i in range(len(command_path)//2):
        if short == command_path[f"short{i}"]:
            print(command_path[f"cmd{i}"]+" "+path)
            os.system(command_path[f"cmd{i}"]+" "+path)
            break




def start_command():
    cmd_file_path = monitor_path["file"]
    if not os.path.exists(cmd_file_path):
        return
    short=''
    other_param = ''
    path = ''
    with open(cmd_file_path,'r') as f:
        data = f.readline()
        for i in range(len(server_path)//2):
            if data.find(server_path[f"server{i}"]) >= 0:
                path = data[:-1].replace(server_path[f"server{i}"],server_path[f"windows{i}"])
                break
        #print(path)
        while(True):
            data = f.readline()
            #print(data)
            if not data:
                break
            if len(data) == 0:
                break
            data = data[:-1]
            if len(short) != 0:
                other_param = other_param+' '+data
                continue
            for i in range(len(command_path)//2):
                if data == command_path[f"short{i}"]:
                    short = command_path[f"short{i}"]
                    break
            if len(short) == 0:
                path = path+'/'+data
        print(f"path = {path},short cmd = {short},param = {other_param}")          
    os.remove(cmd_file_path)  
    run_cmd(path,short,other_param)
    



def main():
    get_param()
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler,monitor_path["dir"],True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



if __name__ == "__main__":
    main()



 
            
            