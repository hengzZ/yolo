#!/usr/bin/python

import os
import sys
import errno
import argparse

import cv2 as cv
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser("Convert image format to jpg.")
    parser.add_argument('--path', dest='image_dir', help='Directory contains images.')
    args = parser.parse_args()
    return args


def main(args):
    path = args.image_dir
    if not os.path.exists(path):
        return -1
    # make correspond Directory for images with jpg format 
    dest_path = "dest_jpgs"
    try:
        os.makedirs(dest_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dest_path):
            pass
        else:
            raise
    # convert
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        dest_file_path = os.path.join(dest_path, str(file).strip().split('.')[0]+'.jpg')
        img = cv.imread(file_path)
        cv.imwrite(dest_file_path, img)


if __name__ == "__main__":
    args = parse_args()
    sys.exit(main(args))
