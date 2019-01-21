#!/usr/bin/python

import os
import sys
import argparse

import xml.etree.ElementTree as ET
import numpy as np
import cv2 as cv
from PIL import Image
from PIL import ImageDraw

# Global Variances
SEGMENTATION_EXTENSION = '.png'
# VOC Palette
PALETTE={'background': (0, 0, 0),
			'road':	(128, 0, 0),
			'cls02': (0, 128, 0),
			'cls03': (128, 128, 0),
			'cls04': (0, 0, 128),
			'cls05': (128, 0, 128),
			'cls06': (0, 128, 128),
			'cls07': (128, 128, 128),
			'cls08': (64, 0, 0),
			'cls09': (192, 0, 0),
			'cls10': (64, 128, 0),
			'cls11': (192, 128, 0),
			'cls12': (64, 0, 128),
			'cls13': (192, 0, 128),
			'cls14': (64, 128, 128),
			'cls15': (192, 128, 128),
			'cls16': (0, 64, 0),
			'cls17': (128, 64, 0),
			'cls18': (0, 192, 0),
			'cls19': (128, 192, 0),
			'cls20': (0, 64, 128) }


def get_image_size(anno_file):
	tree = ET.parse(anno_file)
	root = tree.getroot()
	image_size_node = root.find('imagesize')
	height = int(image_size_node.find('nrows').text)
	width = int(image_size_node.find('ncols').text)
	return [width, height]


def objects(anno_file):
	"""
	name, polygon
	"""
	tree = ET.parse(anno_file)
	root = tree.getroot()
	for obj in root.findall('object'):
		deleted = int(obj.find('deleted').text)
		if deleted: continue
		# name 
		name = obj.find('name').text
		# polygon
		polygon = []
		polygon_node = obj.find('polygon')
		for pt in polygon_node.findall('pt'):
			x = int(pt.find('x').text)
			y = int(pt.find('y').text)
			polygon.append([x,y])
		yield name,polygon


def paint_object(image, name, polygon):
	pts = np.array(polygon, np.int32)
	pts = pts.reshape((-1,1,2))
	#cv.polylines(image,[pts],True,(0,255,255))
	color = (PALETTE[name][2],PALETTE[name][1],PALETTE[name][0])
	cv.fillPoly(image,[pts],color)


def parse_args():
	parser = argparse.ArgumentParser(description='Convert annotations of LabelMe to Segmentation images.')
	parser.add_argument('--annos',dest='annos_path',help='annotations folder')
	args = parser.parse_args()
	return args


def main(args):
	annos_path = args.annos_path
	if not os.path.exists(annos_path):
		print 'path {0} not exist'.format(annos_path)
		return 1

	segmenation_path = os.path.join(annos_path, '../SegmentationLabels')
	os.makedirs(segmenation_path)

	for anno in os.listdir(annos_path):
		anno_file = os.path.join(annos_path, anno)
		segmentation_file = os.path.join(segmenation_path, str(anno).split('.')[0]+SEGMENTATION_EXTENSION)
		image_size = get_image_size(anno_file)

		img = np.zeros((image_size[1],image_size[0],3), np.uint8)

		for name, polygon in objects(anno_file):
			paint_object(img, name, polygon)
		#cv.imshow('demo',img)
		#cv.waitKey(0)
		print segmentation_file
		cv.imwrite(segmentation_file,img)
	return 0



if __name__ == '__main__':
	args = parse_args()
	sys.exit(main(args))

