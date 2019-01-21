#!/usr/bin/python

import os
import sys
import argparse

import xml.etree.ElementTree as ET
import shutil
import errno

import numpy as np
import cv2 as cv


def boxes(anno_file_path):
    tree = ET.parse(anno_file_path)
    root = tree.getroot()
    for obj in root.findall("object"):
        obj_name = str(obj.find("name").text)
        bndbox = obj.find("bndbox")
        obj_xmin = int(bndbox.find("xmin").text)
        obj_ymin = int(bndbox.find("ymin").text)
        obj_xmax = int(bndbox.find("xmax").text)
        obj_ymax = int(bndbox.find("ymax").text)
        yield [obj_name, obj_xmin, obj_ymin, obj_xmax, obj_ymax]
        

def image_ids(sets_file_path):
    with open(sets_file_path) as file:
        for line in file:
            yield line.strip()


def filter_image(org_dir_tree, img_id, empty_ids):
    org_anno_file_path = os.path.join(org_dir_tree["anno_dir"], img_id+'.xml')
    # labels for filter
    labels = ['Car', 'Van', 'Truck', 'Pedestrian', 'Person_sitting', 'Cyclist', 'bus', 'car', 'person']
    num = 0
    for obj in boxes(org_anno_file_path):
        if str(obj[0]) in labels:
            num +=1
    if num == 0:
        empty_ids.append(img_id)
        print "error: %s contains empty object." % org_anno_file_path


def delete_img_id(org_dir_tree, img_id):
    org_anno_file_path = os.path.join(org_dir_tree["anno_dir"], img_id+'.xml')
    org_img_file_path = os.path.join(org_dir_tree["jpgs_dir"], img_id+'.jpg')
    os.remove(org_anno_file_path)
    os.remove(org_img_file_path)
    print "delete %s." % org_anno_file_path


def create_dir_tree(path):
    root_dir = path;
    anno_dir = os.path.join(path, "Annotations")
    sets_dir = os.path.join(path, "ImageSets/Main")
    jpgs_dir = os.path.join(path, "JPEGImages")
    dir_tree = {"root_dir": root_dir, "anno_dir": anno_dir, "sets_dir": sets_dir, "jpgs_dir": jpgs_dir}
    return dir_tree


def parse_args():
    parser = argparse.ArgumentParser(description='Tailor the kitti_on_voc to the target size.')
    parser.add_argument('--root_dir', dest='root_directory', help='the root directory of dataset kitti on voc format.')
    args = parser.parse_args()
    return args


def main(args):
    org_tree = create_dir_tree(args.root_directory)
    for key,val in org_tree.items():
        if not os.path.exists(val):
            print "%s does not exist." % val
            return 2
    print "Directory %s contains %s" % (org_tree["sets_dir"], os.listdir(org_tree["sets_dir"]))
    sets_file_name = raw_input("Please select one file: \n$")
    sets_file_path = os.path.join(org_tree["sets_dir"], sets_file_name)
    print "You selected %s" % sets_file_path
    empty_ids = []
    for img_id in image_ids(sets_file_path):
        filter_image(org_tree, img_id, empty_ids)
    for img_id in empty_ids:
        delete_img_id(org_tree, img_id)


if __name__ == "__main__":
    args = parse_args()
    sys.exit(main(args))

