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
        if os.path.isdir(p):
            t = src.rfind("/")
            dest = src[index:t+1]
        else:    
            dest = src[index:]
        data = f"{src} {dest}"
    return data