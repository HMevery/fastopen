
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

    __event = Event()  
    __connect_status = 0  
    def connect(self,server,port,keepalive,id):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:#响应状态码为0表示连接成功
                #print("Connected to MQTT OK!")
                self.__connect_status = 1
                #self.__event.set()
            else:
                print("Failed to connect, return code %d\n", rc)

        '''print(f"server:{server}")
        print(f"port:{port}")
        print(f"keepalive:{keepalive}")'''
        client = mqtt_client.Client(id)
        client.on_connect = on_connect
        client.connect(server, port, keepalive)
        return client

    def publish(self,server,port,keepalive,id,topic,param):
        if len(param) == 0:
            return
        client = self.connect(server,port,keepalive,id)
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
        #client.disconnect()
        return 0

    def subscribe(self,server,port,keepalive,id,topic,callback):
        def on_message(client, userdata, msg):
            #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            callback(topic,msg.payload.decode())

        client = self.connect(server,port,keepalive,id)
        #client.loop_start()
        client.subscribe(topic)
        client.on_message = on_message
        client.loop_forever()
        client.disconnect() 


