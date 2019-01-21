#!/usr/bin/python

import os 
import sys 
import shutil
import argparse


IMAGE_SUFFIX = ".jpg"
LABEL_SUFFIX = ".xml"


def get_image_ids_in_anno(anno_path):
	image_ids = []
	for file_name in os.listdir(anno_path):
		image_id = str( str(file_name).strip().split('/')[-1] ).split('.')[0]
		image_ids.append(image_id)
	return image_ids


def create_train_list(image_ids,imageset_path):
		list_file_name = os.path.join(imageset_path, "train.txt")
		with open(list_file_name, 'w') as f:
			for i in range(len(image_ids)):
				image_id = "{:0>6}".format(i)
				f.write(image_id+'\n')


def serialize_image_ids(dataset_root_path):
	if not os.path.exists(dataset_root_path):
		print "dataset path {0} not exist".format(dataset_root_path)
		sys.exit(1)
	anno_path = os.path.join(dataset_root_path,"Annotations")
	images_path = os.path.join(dataset_root_path,"JPEGImages")
	imageset_path = os.path.join(dataset_root_path,"ImageSets/Main")
	image_ids = get_image_ids_in_anno(anno_path)
	#
	for image_id in image_ids:
		org_image = os.path.join(images_path,image_id+IMAGE_SUFFIX)
		org_label = os.path.join(anno_path,image_id+LABEL_SUFFIX)
		dest_image_id = "{:0>6}".format(image_ids.index(image_id))
		dest_image = os.path.join(images_path,dest_image_id+IMAGE_SUFFIX)
		dest_label = os.path.join(anno_path,dest_image_id+LABEL_SUFFIX)
		# move
		shutil.move(org_image, dest_image)
		shutil.move(org_label, dest_label)
	# create imageset list
	create_train_list(image_ids, imageset_path)


def parse_args():
	parser = argparse.ArgumentParser('serialize the image ids of dataset into continous.')
	parser.add_argument('--path', dest='dataset', help='root path of dataset, which contains Annotations, ImageSet, and JPEGImages')
	args = parser.parse_args()
	return args


def main(args):
	dataset = args.dataset
	serialize_image_ids(dataset)
	return 0


if __name__ == "__main__":
	args = parse_args()
	sys.exit(main(args))

