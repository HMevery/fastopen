#!/usr/bin/env python3
#coding=utf-8

import json
import random
import sys

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
        return f'mqtt-{random.randint(0, 1000)}' 

    '''读取服务器和win路径配置'''
    __server_path = {}
    __local_path = {}
    def get_server_path_config(self):
        with open(self.__config_path,'r') as f:
            param = json.load(f)

            #服务器路径和映射到windows的路径
            keys = param["server path"].keys()
            for i in range(len(keys)):
                self.__server_path[f"server{i}"] = param["server path"][list(keys)[i]]["server"]
                self.__local_path[f"local{i}"] = param["server path"][list(keys)[i]]["local"]
        #print(self.__server_path)
        #return self.__server_path
            
    def get_server_path(self,index):        
        if len(self.__server_path) != 0 and len(self.__server_path) > index :
            return self.__server_path[f"server{index}"]
        return None
    def get_local_path(self,index):        
        if len(self.__local_path) != 0 and len(self.__local_path) > index :
            return self.__local_path[f"local{index}"]
        return None   

    '''获取命令配置'''
    __first_cmd = []
    __local_cmd = []
    def parse_cmd_config(self):
        with open(self.__config_path,'r') as f:
            param = json.load(f)
            #print(list(param))
            self.__first_cmd.clear()
            #命令
            cmd = param["command"].keys()
            #print(cmd)
            for i in range(len(cmd)):
                #self.__first_path[f"first{i}"] = list(cmd)[i][4:]
                self.__first_cmd.append(list(cmd)[i][4:])
                #self.__command_path[f"short{i}"] = param["command"][list(cmd)[i]]["short"]
                #self.__local_cmd[f"cmd{i}"] = param["command"][list(cmd)[i]]["local cmd"]
                self.__local_cmd.append(param["command"][list(cmd)[i]]["local cmd"])

    def get_all_cmd(self):  
        str = ''
        for i in range(len(self.__first_cmd)):
            str = str + self.__first_cmd[i]+","
        return str

    def get_first_cmd_from_index(self,index):        
        if len(self.__first_cmd) != 0 and len(self.__first_cmd) > index :
            return self.__first_cmd[index]
        return None

    def get_first_cmd_index(self,cmd):  
        for i in range(len(self.__first_cmd)):
            if cmd == self.__first_cmd[i]:
                return i
        return None

    '''def get_cmd_local(self,index):   
        if index == None:
            return None     
        if len(self.__local_cmd) != 0 and len(self.__local_cmd) > index :
            return self.__local_cmd[index]
        return None'''  
    def get_local_cmd(self,cmd):  
        index = self.get_first_cmd_index(cmd) 
        if index == None:
            return None     
        if len(self.__local_cmd) != 0 and len(self.__local_cmd) > index :
            return self.__local_cmd[index]
        return None          