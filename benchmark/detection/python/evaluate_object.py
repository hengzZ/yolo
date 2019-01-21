import os
import sys
import numpy as np


top_stats = 0
# easy, moderate and hard evaluation level
difficulty = {'easy':0, 'moderate':1, 'hard':2}
# evaluation parameter
min_height = (40, 25, 25)
max_occlusion = (0, 1, 2)
max_truncation = (0.15, 0.3, 0.5)
# evaluated object class
classes = {'bus':0, 'car':1, 'person':2}
# min overlap: bus,car,person
min_overlap = (0.7,0.7,0.5)


def get_ground_truth(line):
    ls = list(line.strip().split())
    if 5 == len(ls):
        return (ls[0],ls[1],ls[2],ls[3],ls[4])
    else:
        return ()

def get_detection_result(line):
    ls = list(line.strip().split())
    if 6 == len(ls):
        return (ls[0],ls[1],ls[2],ls[3],ls[4],ls[5])
    else:
        return ()

def load_ground_truth(file_path):
    """type,x,y,w,h"""
    total_ground_truth = []
    with open(file_path, 'r') as fp:
        for line in iter(fp.readline, ''):
            ground_truth = get_ground_truth(line)
            if 5 == len(ground_truth):
                total_ground_truth.append(ground_truth)
    #print total_ground_truth
    return total_ground_truth

def load_detection_result(file_path):
    """type,x,y,w,h,score"""
    total_detection_result = []
    with open(file_path, 'r') as fp:
        for line in iter(fp.readline, ''):
            detection_result = get_detection_result(line)
            if 6 == len(detection_result):
                total_detection_result.append(detection_result)
    #print total_detection_result
    return total_detection_result

def eval(total_ground_truth, total_detection_result):
    """
    evaluation with iou thresh, box iou > thresh: label=1, else label=-1
    """
    return (-1,-1,1,1), (0.1,0.4,0.35,0.8)


def evaluate_object(result_dir, truth_dir):
    """run evaluation"""
    if not os.path.exists(result_dir) or not os.path.exists(truth_dir):
        print "error: non-exist directory"
        os.exit(1)
    y_labels = []
    y_scores = []
    for file in os.listdir(truth_dir):
        image_id = str(file).strip().split('.')[0]
        truth_file = os.path.join(truth_dir, image_id+'.txt')
        result_file = os.path.join(result_dir, image_id+'.txt')
        # get total ground truth and detection result about image_id
        total_ground_truth = load_ground_truth(truth_file)
        total_detection_result = load_detection_result(result_file)
        # box iou evaluation
        labels, scores = eval(total_ground_truth, total_detection_result)
        y_labels.extend(list(labels))
        y_scores.extend(list(scores))
    return y_labels, y_scores

