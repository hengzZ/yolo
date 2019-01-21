#!/usr/bin/python

import os
import sys
import errno
import shutil
import argparse

import xml.etree.ElementTree as ET
import numpy as np
import cv2 as cv


# Global variencies
ANNO_SUFFIX='.xml'
IMAGE_SUFFIX='.png'
DEST_ROOT_DIR='./voc_pure'

######## xml helper functions #########
def create_xml_tree(image_name):
    root = ET.Element('annotation')
    
    folder = ET.SubElement(root,'folder')
    filename = ET.SubElement(root,'filename')
    
    source = ET.SubElement(root,'source')
    srdatabase = ET.SubElement(source,'database')
    srannotation = ET.SubElement(source,'annotation')
    srimage = ET.SubElement(source,'image')
    
    segmented = ET.SubElement(root,'segmented')
    
    folder.text = "VOC"
    filename.text = image_name
    srdatabase.text = "VOC"
    srannotation.text = "VOC"
    srimage.text = "VOC"
    segmented.text = "0"
    
    tplttree = ET.ElementTree(root)
    return tplttree
    
def add_image_size(tree,image_size):
    root = tree.getroot()
    size = ET.SubElement(root,'size')
    szwidth = ET.SubElement(size,'width')
    szheight = ET.SubElement(size,'height')
    szdepth = ET.SubElement(size,'depth')
    
    szheight.text = str(image_size[0])
    szwidth.text = str(image_size[1])
    szdepth.text = str(image_size[2])

def add_object(tree,obj):
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

# Directory Creation helper function
def mkdirs(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

# Box Extraction helper function
def boxes(anno_file):
    tree = ET.parse(anno_file)
    root = tree.getroot()
    for obj in root.findall("object"):
        obj_name = str(obj.find("name").text)
        bndbox = obj.find("bndbox")
        obj_xmin = int(bndbox.find("xmin").text)
        obj_ymin = int(bndbox.find("ymin").text)
        obj_xmax = int(bndbox.find("xmax").text)
        obj_ymax = int(bndbox.find("ymax").text)
        yield [obj_name, obj_xmin, obj_ymin, obj_xmax, obj_ymax]

# Display Boxes helper function
def display_boxes(window_name, image_file, anno_file):
    image = cv.imread(image_file)
    for box in boxes(anno_file):
        if "Car" == box[0]:
            color = (0,0,255)
        elif "Pedestrian" == box[0]:
            color = (0,255,0)
        elif "Cyclist" == box[0]:
            color = (255,0,0)
        else:
            color = (0,255,255)
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(image, box[0], (box[1],box[2]), font, 1, color, 1, cv.LINE_AA)
        cv.rectangle(image, (box[1],box[2]), (box[3], box[4]), color, 1)
    cv.imshow(window_name, image)
    keyval = cv.waitKey(0)&0xFF
    return keyval

# Pure Annotation helper function
def pure_anno(root_path, image_set):
    global DEST_ROOT_DIR, ANNO_SUFFIX, IMAGE_SUFFIX
    # Check Original folder
    root_anno = os.path.join(root_path,'Annotations')
    root_sets = os.path.join(root_path,'ImageSets/Main')
    root_imgs = os.path.join(root_path,'JPEGImages')
    if not os.path.exists(root_anno) or not os.path.exists(root_sets) or not os.path.exists(root_imgs):
        return 1
    # Create Destination folder
    dest_anno = os.path.join(DEST_ROOT_DIR,'Annotations')
    dest_sets = os.path.join(DEST_ROOT_DIR,'ImageSets/Main')
    dest_imgs = os.path.join(DEST_ROOT_DIR,'JPEGImages')
    mkdirs(dest_anno)
    mkdirs(dest_sets)
    mkdirs(dest_imgs)
    ### Specific labels ###
    labels = ['Car', 'Pedestrian', 'Cyclist', 'background']
    #######################
    with open(os.path.join(root_sets,image_set)) as fp:
        for line in fp:
            image_id = str(line).strip()
            org_anno = os.path.join(root_anno, image_id+ANNO_SUFFIX)
            org_image = os.path.join(root_imgs, image_id+IMAGE_SUFFIX)
            dst_anno = os.path.join(dest_anno, image_id+ANNO_SUFFIX)
            dst_image = os.path.join(dest_imgs, image_id+IMAGE_SUFFIX)
            dst_set = os.path.join(dest_sets, 'train.txt')
            # create destination annotation
            xml_tree = create_xml_tree(image_id)
            image = cv.imread(org_image)
            add_image_size(xml_tree, image.shape)
            # filter
            for box in boxes(org_anno):
                label = box[0]
                # merge labels
                if "DontCare" == label or "Misc" == label:
                    label = "background"
                elif "person" == label:
                    label = "Pedestrian"
                elif "car" == label:
                    label = "Car"
                # 
                if label not in labels:
                    continue
                add_object(xml_tree, [label,box[1],box[2],box[3],box[4]])
            if 0 == len(xml_tree.findall("object")):
                continue
            print org_image
            xml_tree.write(dst_anno)
            shutil.copy(org_image, dst_image)
            set_file = open(dst_set, 'a+')
            set_file.write(image_id+'\n')
            set_file.close()

    return 0


# Console arguments parse helper function
def parse_args():
    parser = argparse.ArgumentParser(description='pure annotation with specific classes.')
    parser.add_argument('--path',dest='dataset',help='root path of dataset in voc format.')
    args = parser.parse_args()
    return args

# Main
def main(args):
    # Check 
    root_path = args.dataset
    root_sets = os.path.join(root_path,'ImageSets/Main')
    if not os.path.exists(root_path) or not os.path.exists(root_sets):
        print "some folder not exist."
        return 2
    # Get orignal Image Sets
    image_sets = os.listdir(root_sets)
    print "orignal dataset {} contains {}".format(root_sets,image_sets)
    image_set = raw_input("Please enter the target set: \n$ ")
    print "You selected {}.".format(image_set)
    # Pure the annotations
    ret = pure_anno(root_path, image_set)

    if 0 != ret : return 1
    return 0


if __name__ == "__main__":
    args = parse_args()
    sys.exit(main(args))

