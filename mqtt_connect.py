
#!/usr/bin/env python
#coding:utf-8

import time
import json
import random
import sys
from paho.mqtt import client as mqtt_client
from threading import Event

class mqtt_connect:
    def __init__(self):
        return
    
    __server = 0
    __port = 0
    __keepalive = 0
    __id = 0
    __topic = 0
    __callback = 0
    __disconnect = 0
    
    __event = Event()  
    __connect_status = 0  
    def connect(self,server,port,keepalive,id):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:#响应状态码为0表示连接成功
                print("Connected to MQTT OK!")
                self.__connect_status = 1
                #self.__event.set()
            else:
                print("Failed to connect, return code %d\n", rc)
        '''def on_disconnect(client, userdata, rc):
            print("Disconnected111, trying to reconnect...")
            while True:
                try:
                    client.reconnect()
                    break
                except Exception as e:
                    print(f"Reconnection failed: {e}")
                    time.sleep(5)  # 等待5秒后重试 '''  
            #self.try_reconnect(client)
        '''print(f"server:{server}")
        print(f"port:{port}")
        print(f"keepalive:{keepalive}")'''
        client = mqtt_client.Client(id)
        #client.on_connect = on_connect
        #client.on_disconnect = on_disconnect
        client.connect(server, port, keepalive)
        return client

    def publish(self,server,port,keepalive,id,topic,param):
        if len(param) == 0:
            return
        def on_connect(client, userdata, flags, rc):
            if rc == 0:#响应状态码为0表示连接成功
                #print("Connected to MQTT OK!")
                self.__connect_status = 1
                #self.__event.set()
            else:
                print("Failed to connect, return code %d\n", rc)    
        client = self.connect(server,port,keepalive,id)
        client.on_connect = on_connect
        #client.loop_start()
        client.loop(1)
        #self.__event.wait(5)
        #self.__event.clear()
        if self.__connect_status == 0:
            print("mqtt connect error!")  
            return -1

        result = client.publish(topic,param, qos=0, retain=False)
        status = result[0]
        if status != 0:
            print(f"Failed to send message to topic {topic}")
        #print(f"Send `{param}` to topic `{topic}`")
            
           
        #client.loop_stop()      
        client.disconnect()
        return 0

    def subscribe(self,server,port,keepalive,id,topic,callback):
        def on_message(client, userdata, msg):
            #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            callback(client,topic,msg.payload.decode())
        def on_connect(client, userdata, flags, rc):
            if rc == 0:#响应状态码为0表示连接成功
                print("Connected to MQTT OK! subscribe")
                self.__connect_status = 1
                #self.__event.set()
                if self.__disconnect == 1:
                    self.__disconnect = 0
                    self.subscribe(self.__server,self.__port,self.__keepalive,self.__id,self.__topic,self.__callback)
            else:
                print("Failed to connect, return code %d\n", rc)    
        def on_disconnect(client, userdata, rc):
            print("Disconnected, trying to reconnect...")
            while True:
                try:
                    client.reconnect()
                    self.__disconnect = 1
                    break
                except Exception as e:
                    print(f"Reconnection failed: {e}")
                    time.sleep(5)  # 等待5秒后重试 '''     
        
        self.__server = server
        self.__port = port
        self.__keepalive = keepalive
        self.__id = id
        self.__topic = topic
        self.__callback = callback
    
    
        client = self.connect(server,port,keepalive,id)
        #client.loop_start()
        client.subscribe(topic)
        client.on_message = on_message
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.loop_forever()
        client.disconnect() 
        print("Connected to MQTT OK!over")
         


