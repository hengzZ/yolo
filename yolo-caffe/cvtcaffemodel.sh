#!/bin/bash
# File Name: cvtcaffemodel.sh
# Author: 
# Mail: 
# Created Time: 2017年03月16日 星期四 10时08分04秒

python create_yolo_caffemodel.py -m $1 -w $2 -o $3
