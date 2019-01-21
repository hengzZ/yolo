#!/usr/bin/python

import xml.etree.ElementTree as ET
import pickle
import os
import errno
import shutil
import sys
from os import getcwd
from os.path import join
import argparse

import numpy as np
import cv2 as cv


# root to save selected data
dst_dir = "./preview"
# xml suffix
xmlextension = ".xml"
# global variable for image file suffix
imgextension = ".png"


def my_makedirs(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def boxs(annot_name):
    tree = ET.parse(annot_name)
    root = tree.getroot()
    for obj in root.findall("object"):
        obj_name = str(obj.find("name").text)
        bndbox = obj.find("bndbox")
        obj_xmin = int(bndbox.find("xmin").text)
        obj_ymin = int(bndbox.find("ymin").text)
        obj_xmax = int(bndbox.find("xmax").text)
        obj_ymax = int(bndbox.find("ymax").text)
        yield [obj_name, obj_xmin, obj_ymin, obj_xmax, obj_ymax]


def draw_result(window_name,image_name,annot_name):
    image = cv.imread(image_name)
    for box in boxs(annot_name):
        if "car" == box[0]:
            color = (0,0,255)
        elif "person" == box[0]:
            color = (0,255,0)
        elif "bus" == box[0]:
            color = (255,0,0)
        else:
            color = (0,255,0)
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(image, box[0], (box[1],box[2]), font, 1, color, 1, cv.LINE_AA)
        cv.rectangle(image, (box[1],box[2]), (box[3],box[4]), color, 1)
    cv.imshow(window_name,image)
    keyval = cv.waitKey(0)&0xFF
    return keyval


def preview(index_file,jpeg_dir,annotation_dir):
    with open(index_file) as file:
        window_name = "demo"
        cv.namedWindow(window_name,cv.WINDOW_AUTOSIZE)
        for line in file:
            image_name = join(jpeg_dir, line.strip()+imgextension)
            annot_name = join(annotation_dir, line.strip()+xmlextension)
            ret = draw_result(window_name,image_name,annot_name)
            if 27 == ret:   break
            elif ord('y') == ret:
                # Copy target image and annotation to destination folder
                shutil.copy(image_name, join(dst_dir, "JPEGImages/"+line.strip()+imgextension)) 
                shutil.copy(annot_name, join(dst_dir, "Annotations/"+line.strip()+xmlextension))
        cv.destroyAllWindows()

def parse_args():
    parser = argparse.ArgumentParser('preview annotation in VOC format.')
    parser.add_argument('--dataset_dir', dest='dataset_directory', help='dataset such as: VOCdevkit/VOC2007')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    # Get Database
    args = parse_args()
    filedir = args.dataset_directory
    if not os.path.exists(filedir):
        print "directory %s not exist" % (filedir)
        sys.exit(2)
    if not os.path.exists(join(filedir,"Annotations")):
        print "directory %s not exist" % (join(filedir,"Annotations"))
        sys.exit(2)
    if not os.path.exists(join(filedir,"ImageSets")):
        print "directory %s not exist" % (join(filedir,"ImageSets/Main"))
        sys.exit(2)
    if not os.path.exists(join(filedir,"JPEGImages")):
        print "directory %s not exist" % (join(filedir,"JPEGImages"))
        sys.exit(2)
    # Make destination folder (Implement of make -p)
    my_makedirs(join(dst_dir, "Annotations"))
    my_makedirs(join(dst_dir, "JPEGImages"))
    my_makedirs(join(dst_dir, "ImageSets/Main"))
    # Get image index
    imagesets_dir = join(filedir,"ImageSets/Main")
    print "Directory %s contains %s" % (imagesets_dir, os.listdir(imagesets_dir))
    idx_file_name = raw_input("Please enter the file name for preview: \n$ ")
    print "You Selected %s for preview" % (join(imagesets_dir,idx_file_name))
    # Preview ImageSets
    preview(join(imagesets_dir,idx_file_name),join(filedir,"JPEGImages"),join(filedir,"Annotations"))

