#!/usr/bin/python

import os
import sys
import argparse

import numpy as np
from PIL import Image


# Image palette (an voc label image for palette imformation)
VOC_PALETTE = Image.open('palette_voc.png')
# Save path
DEST_LABELS_PATH = './SegmentationClass'


def parse_args():
	parser = argparse.ArgumentParser('label images path.')
	parser.add_argument('--path', dest='labels_path', help='label images path')
	args = parser.parse_args()
	return args

def color2palette(image):
	converted = image.quantize(palette=VOC_PALETTE)
	return converted

def main(args):
	# Create save path
	os.makedirs(DEST_LABELS_PATH)
	# Original labels path
	orig_path = args.labels_path

	# mode conversion
	for file in os.listdir(orig_path):
		label = Image.open(os.path.join(orig_path,file))
		dest_label = color2palette(label)
		dest_label.save(os.path.join(DEST_LABELS_PATH,file))
		print 'dest: ', file, 'mode: ', dest_label.mode

	return 0


if __name__ == '__main__':
	args = parse_args()
	sys.exit(main(args))
	
