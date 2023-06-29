#!/bin/bash
FILE=$(pwd)/$2
if [ d = $1 ];then
    python3 /home/username/ssd/Snail/server.py -c d -f $FILE   
fi
if [ f = $1 ];then
    python3 /home/username/ssd/Snail/server.py -c f -f $FILE   
fi
if [ vs = $1 ];then
    python3 /home/username/ssd/Snail/server.py -c vs -f $FILE   
fi
if [ services = $1 ];then
    python3 /home/username/ssd/Snail/server.py -c services   
fi
if [ selinux = $1 ];then
    python3 /home/username/ssd/Snail/server.py -c selinux   
fi
if [ apush = $1 ];then
    python3 /home/username/ssd/Snail/server.py -c apush -f $FILE  -p  $3 $4 $5 $6 
fi
if [ areboot = $1 ];then
    python3 /home/username/ssd/Snail/server.py -c areboot   
fi
if [ adb = $1 ];then
    python3 /home/username/ssd/Snail/server.py -c adb  -p $2 $3 $4 $5 $6 
fi
