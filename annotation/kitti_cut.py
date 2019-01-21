#!/usr/bin/python

import os
import sys
import argparse

import xml.etree.ElementTree as ET
import shutil
import errno

import numpy as np
import cv2 as cv


def create_xml_tree(img_id):
    root = ET.Element('annotation')
    
    folder = ET.SubElement(root,'folder')
    filename = ET.SubElement(root,'filename')
    
    source = ET.SubElement(root,'source')
    srdatabase = ET.SubElement(source,'database')
    srannotation = ET.SubElement(source,'annotation')
    srimage = ET.SubElement(source,'image')
    
    segmented = ET.SubElement(root,'segmented')
    
    folder.text = "VOC"
    filename.text = img_id + '.jpg'
    srdatabase.text = "Intel Database"
    srannotation.text = "Intel"
    srimage.text = "CP"
    segmented.text = "0"
    
    tplttree = ET.ElementTree(root)
    return tplttree


def add_image_size(tree, img_size):
    root = tree.getroot()
    size = ET.SubElement(root,'size')
    szwidth = ET.SubElement(size,'width')
    szheight = ET.SubElement(size,'height')
    szdepth = ET.SubElement(size,'depth')
    
    szheight.text = str(img_size[0])
    szwidth.text = str(img_size[1])
    szdepth.text = str(img_size[2])


def add_object(tree, obj):
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


def image_size(anno_file_path):
    tree = ET.parse(anno_file_path)
    root = tree.getroot()
    img_size = root.find("size")
    img_width = int(img_size.find("width").text)
    img_height = int(img_size.find("height").text)
    img_depth = int(img_size.find("depth").text)
    return [img_width, img_height, img_depth]


def image_ids(sets_file_path):
    with open(sets_file_path) as file:
        for line in file:
            yield line.strip()


def resize_image(org_img_file_path, dst_img_file_path, img_size, x_offset):
    org_img = cv.imread(org_img_file_path)
    xmin = 0 + int(x_offset)
    xmax = int(img_size[0]) + int(x_offset)
    ymin = 0
    ymax = int(img_size[1])
    dst_img = org_img[ymin:ymax, xmin:xmax]
    cv.imwrite(dst_img_file_path, dst_img)


def cut_image(org_dir_tree, dst_dir_tree, old_img_id, new_img_id, img_size, x_offset):
    org_img_file_path = os.path.join(org_dir_tree["jpgs_dir"], old_img_id+'.jpg')
    org_anno_file_path = os.path.join(org_dir_tree["anno_dir"], old_img_id+'.xml')
    dst_img_file_path = os.path.join(dst_dir_tree["jpgs_dir"], new_img_id+'.jpg')
    dst_anno_file_path = os.path.join(dst_dir_tree["anno_dir"], new_img_id+'.xml')
    xml_tree = create_xml_tree(new_img_id)
    add_image_size(xml_tree, img_size)
    num = 0
    for obj in boxes(org_anno_file_path):
        if obj[1] < (0 + int(x_offset)) or obj[1] > (int(img_size[0]) + int(x_offset)):
            continue
        elif obj[3] < (0 + int(x_offset)) or obj[3] > (int(img_size[0]) + int(x_offset)):
            continue
        elif obj[2] < 0 or obj[2] > img_size[1]:
            continue
        elif obj[4] < 0 or obj[4] > img_size[1]:
            continue
        dst_name = str(obj[0])
        dst_xmin = int(obj[1]) - int(x_offset)
        dst_ymin = int(obj[2])
        dst_xmax = int(obj[3]) - int(x_offset)
        dst_ymax = int(obj[4])
        dst_obj = [dst_name, dst_xmin, dst_ymin, dst_xmax, dst_ymax]
        add_object(xml_tree, dst_obj)
        num += 1
    if num > 0:
        xml_tree.write(dst_anno_file_path)
        resize_image(org_img_file_path, dst_img_file_path, img_size, x_offset)


def tailor_image(org_dir_tree, dst_dir_tree, img_id):
    org_anno_file_path = os.path.join(org_dir_tree["anno_dir"], img_id+'.xml')
    org_img_size = image_size(org_anno_file_path)
    # resize the image
    dst_width = int(org_img_size[1])*16/9
    dst_height = int(org_img_size[1])
    dst_depth = int(org_img_size[2])
    dst_img_size = [dst_width, dst_height, dst_depth]
    x_offset = int(org_img_size[0]) - dst_width
    #print dst_img_size
    # left part
    new_img_id = str(img_id) + '0'
    cut_image(org_dir_tree, dst_dir_tree, img_id, new_img_id, dst_img_size, 0)
    # right part
    new_img_id = str(img_id) + '1'
    cut_image(org_dir_tree, dst_dir_tree, img_id, new_img_id, dst_img_size, x_offset)


def create_dir_tree(path):
    root_dir = path;
    anno_dir = os.path.join(path, "Annotations")
    sets_dir = os.path.join(path, "ImageSets/Main")
    jpgs_dir = os.path.join(path, "JPEGImages")
    dir_tree = {"root_dir": root_dir, "anno_dir": anno_dir, "sets_dir": sets_dir, "jpgs_dir": jpgs_dir}
    return dir_tree


def my_makedirs(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


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
    dst_tree = create_dir_tree("./dest_kitti")
    for key,val in dst_tree.items():
        my_makedirs(val)
    print "Directory %s contains %s" % (org_tree["sets_dir"], os.listdir(org_tree["sets_dir"]))
    sets_file_name = raw_input("Please select one file: \n$")
    sets_file_path = os.path.join(org_tree["sets_dir"], sets_file_name)
    print "You selected %s" % sets_file_path
    for img_id in image_ids(sets_file_path):
        tailor_image(org_tree, dst_tree, img_id)


if __name__ == "__main__":
    args = parse_args()
    sys.exit(main(args))

