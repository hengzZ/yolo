#!/usr/bin/python

import xml.etree.ElementTree as ET
import pickle
import os,shutil
from os import getcwd
from os.path import join
import argparse

import numpy as np
import cv2 as cv

xmlextension = '.xml'
imgextension = '.jpg'
txtextension = '.txt'


######## xml helper functions #########
def createXMLTree(imagename):
    root = ET.Element('annotation')
    
    folder = ET.SubElement(root,'folder')
    filename = ET.SubElement(root,'filename')
    
    source = ET.SubElement(root,'source')
    srdatabase = ET.SubElement(source,'database')
    srannotation = ET.SubElement(source,'annotation')
    srimage = ET.SubElement(source,'image')
    
    segmented = ET.SubElement(root,'segmented')
    
    folder.text = "VOC"
    filename.text = imagename
    srdatabase.text = "VOC"
    srannotation.text = "VOC"
    srimage.text = "VOC"
    segmented.text = "0"
    
    tplttree = ET.ElementTree(root)
    return tplttree
    
def addImageSize(tree,imagesize):
    root = tree.getroot()
    size = ET.SubElement(root,'size')
    szwidth = ET.SubElement(size,'width')
    szheight = ET.SubElement(size,'height')
    szdepth = ET.SubElement(size,'depth')
    
    szheight.text = str(imagesize[0])
    szwidth.text = str(imagesize[1])
    szdepth.text = str(imagesize[2])

def addObject(tree,obj):
    root = tree.getroot()
    anobject = ET.SubElement(root,'object')
    obname = ET.SubElement(anobject,'name')
    obpose = ET.SubElement(anobject,'pose')
    obtruncated = ET.SubElement(anobject,'truncated')
    obdifficult = ET.SubElement(anobject,'difficult')
    obbndbox = ET.SubElement(anobject,'bndbox')
    
    boxxmin = ET.SubElement(obbndbox,'xmin')
    boxymin = ET.SubElement(obbndbox,'ymin')
    boxxmax = ET.SubElement(obbndbox,'xmax')
    boxymax = ET.SubElement(obbndbox,'ymax')

    obname.text = str(obj[0])
    obpose.text = "Unspecified"
    obtruncated.text = "0"
    obdifficult.text = "0"
    boxxmin.text = str(obj[1])
    boxymin.text = str(obj[2])
    boxxmax.text = str(obj[3])
    boxymax.text = str(obj[4])    
    
    
######## annotation helper functions ##########
drawing=False
minx,miny=10,10
curx,cury=30,30
font=cv.FONT_HERSHEY_SIMPLEX
# callback founction for drawing
def drawRectangle(event,x,y,flags,param):
    global drawing,minx,miny,curx,cury
    if event==cv.EVENT_LBUTTONDOWN:
        drawing=True
        minx,miny=x,y
        curx,cury=x,y
    elif event==cv.EVENT_MOUSEMOVE:
        if drawing==True:
            curx,cury=x,y
    elif event==cv.EVENT_LBUTTONUP:
        drawing=False
        
def getObject(image):
    global minx,miny,curx,cury
    cv.namedWindow("Image",cv.WINDOW_AUTOSIZE)
    cv.setMouseCallback("Image",drawRectangle)
    while(1):
        imgtmp = image.copy()
        cv.rectangle(imgtmp,(minx,miny),(curx,cury),(0,255,0),1)
        cv.imshow("Image",imgtmp)
        
        # Label
        keyval = cv.waitKey(1)&0xFF
        if keyval == ord('c'):
            cv.destroyAllWindows()
            return ("car",minx,miny,curx,cury)
        elif keyval == ord('b'):
            cv.destroyAllWindows()
            return ("bus",minx,miny,curx,cury) 
        elif keyval == ord('t'):
            cv.destroyAllWindows()
            return ("truck",minx,miny,curx,cury) 
        elif keyval == ord('p'):
            cv.destroyAllWindows()
            return ("pedestrian",minx,miny,curx,cury) 
        elif keyval == ord('s'):
            cv.destroyAllWindows()
            return ("cyclist",minx,miny,curx,cury) 
        elif keyval == 32: # Space
            cv.destroyAllWindows()
            return 0 # save and goto next image
        elif keyval == 8: # BackSpace
            cv.destroyAllWindows()
            return -1 # discard and goto next image
        elif keyval == 27: # ESC
            cv.destroyAllWindows()
            return -2 # exit
            
def getAnnoFromImage(tree,image):
    global minx,miny,curx,cury
    num = 0
    while(1):
        # Get object
        anobject = getObject(image)
        if anobject == -2: # exit
           return -2 
        elif anobject == -1: # discard and goto next image
            return -1
        elif anobject == 0: # save and goto next image
            return num
        else :
            # Update labeled objects of current image
            addObject(tree,anobject)
            num=num+1
            cv.rectangle(image,(anobject[1],anobject[2]),(anobject[3],anobject[4]),(0,0,255),1)
            cv.putText(image,str(anobject[0]),(anobject[1],anobject[2]),font,1,(0,0,255),2)
            #
            minx,miny,curx,cury=10,10,30,30

# parse console arguments
def parse_args():
    parser = argparse.ArgumentParser(description='annotate images in voc format.')
    parser.add_argument('--path',dest='dir_path',help='directory contains original images')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    # Check the destination directories
    if not os.path.exists('VOC/'):
        os.makedirs('VOC/VOC2016/Annotations/')
        os.makedirs('VOC/VOC2016/ImageSets/Main/')
        os.makedirs('VOC/VOC2016/JPEGImages/')
    if not os.path.exists('VOC/VOC2016/Annotations/'):
        os.makedirs('VOC/VOC2016/Annotations/')
    if not os.path.exists('VOC/VOC2016/ImageSets/Main/'):
        os.makedirs('VOC/VOC2016/ImageSets/Main/')
    if not os.path.exists('VOC/VOC2016/JPEGImages/'):
        os.makedirs('VOC/VOC2016/JPEGImages/')
    # Get original images directory
    args = parse_args()
    dir_path = args.dir_path

    # Traverse all images
    if os.path.exists(dir_path):        
        for file in os.listdir(dir_path):
            imagename = file
            # Create xml tree
            xmltree = createXMLTree(imagename)
            image = cv.imread(join(dir_path,file),cv.IMREAD_COLOR)
            imagesize = image.shape
            addImageSize(xmltree,imagesize)
            # Get labeled objects of current image
            nums= getAnnoFromImage(xmltree,image)
            
            # Save xml or not
            if nums > 0:
                xmltree.write('VOC/VOC2016/Annotations/'+imagename.split('.')[0]+xmlextension);
                shutil.move(join(dir_path,file),'VOC/VOC2016/JPEGImages/'+file)
                listFile = open('VOC/VOC2016/ImageSets/Main/'+'train.txt','a+')
                listFile.write(imagename.split('.')[0]+'\n')
                listFile.close()
            elif nums == -2:
                break
    else:
            print 'Note: directory- %s not exists!'%(dir_path)

