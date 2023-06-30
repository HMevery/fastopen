#!/usr/bin/env python3
#coding=utf-8

import json
import random
import sys
import socket
import getpass

class parseConfig:
    def __init__(self):
        return
    
    __mqtt_config = {}
    __config_path = sys.path[0]+"/config.json"
    def get_mqtt_config(self):
        
        with open(self.__config_path,'r') as f:
            param = json.load(f)

            self.__mqtt_config["Server"] = param["MQTT config"]["Server"]
            self.__mqtt_config["Port"] = int(param["MQTT config"]["Port"])
            self.__mqtt_config["KeepAliveSeconed"] = int(param["MQTT config"]["KeepAliveSeconed"])
            self.__mqtt_config["Topic"] = param["MQTT config"]["Topic"]
        
        #return self.__mqtt_config

    def get_mqtt_server(self):
        if len(self.__mqtt_config) > 0:
            return self.__mqtt_config["Server"]
        return None
    def get_mqtt_port(self):
        if len(self.__mqtt_config) > 0:
            return self.__mqtt_config["Port"]
        return None
    def get_mqtt_keepalive_sec(self):
        if len(self.__mqtt_config) > 0:
            return self.__mqtt_config["KeepAliveSeconed"]
        return None
    def get_mqtt_topic(self):
        if len(self.__mqtt_config) > 0:
            return self.__mqtt_config["Topic"]
        return None    
    def get_mqtt_client_id(self):
        return f"mqtt-{random.randint(0, 1000)}" 

    '''读取服务器和win路径配置'''


    def get_host_ip(self):
        user_name = getpass.getuser() # 获取当前用户名
        hostname = socket.gethostname() # 获取当前主机名
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip,user_name
    __server_path = {}
    __local_path = {}
    __server_ip = ''
    __server_username = ''
    def parse_server_config(self):
        self.__server_ip,self.__server_username = self.get_host_ip()
        #print(f"server ip:{self.__server_ip},user name:{self.__server_username}")
        self.__server_path.clear()
        self.__local_path.clear()
        count = 0
        with open(self.__config_path,'r') as f:
            param = json.load(f)

            #服务器路径和映射到windows的路径
            for p in param["server config"]:
                if p["IP"] == self.__server_ip or len(p["IP"]) == 0:
                    server_path = ""
                    local_path = ""
                    if len(p["server"]) == 0:
                        server_path = f"/home/{self.__server_username}/"
                    else:
                        server_path =  p["server"] 
                    if len(p["local"]) == 0:
                        local_path = f"//{self.__server_ip}/{self.__server_username}/"
                    else:
                        local_path =  p["local"]      
                    self.__server_path[count] = server_path
                    self.__local_path[count] = local_path
                    count = count + 1
        #print(self.__server_path)
        #print(self.__local_path)

    def get_server_count(self): 
        return len(self.__server_path)       
    def get_server_path(self,index):        
        if len(self.__server_path) != 0 and len(self.__server_path) > index :
            return self.__server_path[index]
        return None
    def get_local_path(self,index):        
        if len(self.__local_path) != 0 and len(self.__local_path) > index :
            return self.__local_path[index]
        return None   

    '''获取命令配置'''
    #__cmd_name = []
    #__cmd_exe = []
    __commend = {"default":"default"}
    def parse_cmd_config(self):
        with open(self.__config_path,'r') as f:
            param = json.load(f)
            #self.__cmd_name.clear()
            #self.__cmd_exe.clear()
            self.__commend.clear()
            #命令

            #command = param["command"].keys()
            #print(command)
            '''for i in range(len(cmd)):
                #self.__first_path[f"first{i}"] = list(cmd)[i][4:]
                self.__first_cmd.append(list(cmd)[i][4:])
                #self.__command_path[f"short{i}"] = param["command"][list(cmd)[i]]["short"]
                #self.__local_cmd[f"cmd{i}"] = param["command"][list(cmd)[i]]["local cmd"]
                self.__local_cmd.append(param["command"][list(cmd)[i]]["local cmd"])'''
            for p in param["command"]:
                #self.__cmd_name.append(p["name"])
                #self.__cmd_exe.append(p["execute"])
                self.__commend[p["name"]] = p["execute"]
            #print(self.__commend.keys())    

    def get_cmd_name_all(self):  
        return list(self.__commend.keys())

    def get_cmd_execute(self,name):
        return self.__commend.pop(name)
  
        
    '''def get_first_cmd_from_index(self,index):        
        if len(self.__cmd_name) != 0 and len(self.__cmd_name) > index :
            return self.__cmd_name[index]
        return None

    def get_first_cmd_index(self,cmd):  
        for i in range(len(self.__cmd_name)):
            if cmd == self.__cmd_name[i]:
                return i
        return None'''

    '''def get_cmd_local(self,index):   
        if index == None:
            return None     
        if len(self.__cmd_exe) != 0 and len(self.__cmd_exe) > index :
            return self.__cmd_exe[index]
        return None'''  
    '''def get_local_cmd(self,cmd):  
        index = self.get_first_cmd_index(cmd) 
        if index == None:
            return None     
        if len(self.__cmd_exe) != 0 and len(self.__cmd_exe) > index :
            return self.__cmd_exe[index]
        return None'''          