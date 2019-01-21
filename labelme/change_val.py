#!/usr/bin/python

import os
import sys
import argparse

import numpy as np
from PIL import Image


def parse_args():
	parser = argparse.ArgumentParser('label images path.')
	parser.add_argument('--path', dest='labels_path', help='label images path')
	args = parser.parse_args()
	return args

def pixel_val(image_path,x,y):
	image = Image.open(image_path)
	val = image.getpixel((x,y))
	return val

def change_val(image_path):
	image = Image.open(image_path)
	width, height = image.size
	#for x in range(0, width):
	#	for y in range(0, height):
	#		val = image.getpixel((x,y))
	#		if 73 == val:
	#			image.putpixel([x,y],1)
	#		elif 109 == val:
	#			image.putpixel([x,y],2)
	#		elif 1 == val or 2 == val:
	#			pass
	#		else:
	#			image.putpixel([x,y],0)
	#image.save(image_path)
	#print image_path
	val = image.getpixel((1500,800))
	print val

def main(args):
	orig_path = args.labels_path
	for file in os.listdir(orig_path):
		change_val(os.path.join(orig_path,file))


if __name__ == '__main__':
	args = parse_args()
	sys.exit(main(args))

