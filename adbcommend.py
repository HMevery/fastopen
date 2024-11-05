#!/usr/bin/env python3
#coding=utf-8

import os


def push(path):
    data = path
    src = path.replace('\\','/')
    index = src.rfind("/system/")
    if index == -1:
        index = src.rfind("/system_ext/")
    if index == -1:
        index = src.rfind("/vendor/")
    if index == -1:
        index = src.rfind("/product/")
    if index != -1:
        dest = ''
        p = src
        if 'adb push ' in src:
            p = src[len('adb push '):]
        if p.endswith(" "):
            p = p.rstrip()
        #print(f"p:{p}")
        #print(os.path.isdir(p))
        if os.path.isdir(p):
            tmp = src
            if tmp.endswith(" "):
                tmp = tmp.rstrip()
            if tmp.endswith("/"):
                tmp = tmp[:-1]
            #print(f"tmp:{tmp}")    
            t = tmp.rfind("/")
            dest = tmp[index:t+1]
            #print(f"dir:{dest}")
        else:    
            dest = src[index:]
            
        data = f"{src} {dest}"
    return data