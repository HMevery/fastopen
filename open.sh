#!/bin/bash

FILE=/home/test/ssd/open/open.txt

echo $(pwd) > $FILE
for i in "$@"; do
    echo $i >> $FILE
done
sync

