import os
import sys
import numpy as np

###
# Static Evaluation Parameters
###
TOP_STATS = 0
# easy, moderate and hard evaluation level
DIFFICULTY = {'easy':0, 'moderate':1, 'hard':2}
# evaluation parameter
MIN_HEIGHT = (40, 25, 25)
MAX_OCCLUSION = (0, 1, 2)
MAX_TRUNCATION = (0.15, 0.3, 0.5)
# evaluated object class
#CLASSES = {'car':0, 'pedestrian':1, 'cyclist':2}
CLASSES = {'bus':0, 'car':1, 'person':2}
# no. of recall steps that should be evaluated (discretized)
N_SAMPLE_PTS = 41

# parameters varying per class
#CLASS_NAMES = ['car','pedestrian','cyclist']
CLASS_NAMES = ['bus','car','person']
# min overlap required for evaluation
min_overlap = (0.7,0.7,0.5)


### 
# Date Types For Evaluation
###
class PrData:
    """holding data needed for precision-recall and precision-aos"""
    def __init__(self):
        self.v = [] # detection score for computing score thresholds
        self.similarity=0 # orientation similarity
        self.tp=0 # true positives
        self.fp=0 # false positives
        self.fn=0 # false negatives

class Box:
    """holding bounding boxes for ground truth and detction"""
    def __init__(self):
        self.type # object type
        self.x1 # left corner
        self.y1 # top corner
        self.x2 # right corner
        self.y2 # bottom corner
        self.alpha # image orientation

class GroundTruth:
    """holding ground truth data"""
    def __init__(self):
        self.box
        self.truncation
        self.occlusion

class Detection:
    """holding detection data"""
    def __init__(self):
        self.box
        self.thresh # detection score


###
# Function To Load Detection And Ground Truth Data
###
def get_ground_truth(line):
    ground_truth = GroundTruth()
    ls = list(line.strip().split())
    if 5 == len(ls):
        ground_truth.box.type = ls[0]
        ground_truth.box.x1 = ls[1]
        ground_truth.box.y1 = ls[2]
        ground_truth.box.x2 = ls[3]
        ground_truth.box.y2 = ls[4]
        ground_truth.box.alpha = 0
        ground_truth.truncation = 0.15
        ground_truth.occlusion = 0
    else:
        return ()

def get_detection_result(line):
    """type,x,y,w,h,score"""
    ls = list(line.strip().split())
    if 6 == len(ls):
        return (ls[0],ls[1],ls[2],ls[3],ls[4],ls[5])
    else:
        return ()

def load_ground_truth(file_path):
    total_ground_truth = []
    with open(file_path, 'r') as fp:
        for line in iter(fp.readline, ''):
            ground_truth = get_ground_truth(line)
            if 0 != len(ground_truth):
                total_ground_truth.append(ground_truth)
    return total_ground_truth

def load_detection_result(file_path):
    total_detection_result = []
    with open(file_path, 'r') as fp:
        for line in iter(fp.readline, ''):
            detection_result = get_detection_result(line)
            if 0 != len(detection_result):
                total_detection_result.append(detection_result)
    return total_detection_result


def box_overlap(box1, box2, criterion=-1):
    """
    overlap is computed with respect to both areas(ground truth and detection)
    or with respect to box a or b(detection and "dontcare" areas)
    """
    # overlap is invalid in the beginning
    ol = -1
    # get overlapping area
    x1 = max(box1[1]-box1[3]/2,box2[1]-box2[3]/2)
    y1 = max(box1[2]-box1[4]/2,box2[2]-box2[4]/2)
    x2 = min(box1[1]+box1[3]/2,box2[1]+box2[3]/2)
    y2 = min(box1[2]+box1[4]/2,box2[2]+box2[4]/2)
    # compute width and height of overlapping area
    w = x2-x1
    h = y2-y1
    # set invalid entries to o overlap
    if(w<=0 or h<=0):
        return 0
    # get overlapping areas
    inter = w*h
    box1_area = box1[3]*box1[4]
    box2_area = box2[3]*box2[4]
    # intersection over union overlap depending on users choice
    if(-1 == criterion):
        ol = inter/(box1_area+box2_area-inter)
    elif(0 == criterion):
        ol = inter/box1_area
    elif(1 == criterion):
        ol = inter/box2_area
    # overlap
    return ol


def eval(total_ground_truth, total_detection_result):
    """
    evaluation with iou thresh, box iou > thresh: label=1, else label=-1
    """
    for ground_truth in total_ground_truth:
        print ground_truth
    return (-1,-1,1,1), (0.1,0.4,0.35,0.8)


# run evaluation
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


# compute N_SAMPLE_PTS recall values
def get_thresholds(val, n_ground_truth):
    # holds score needed to compute N_SAMPLE_PTS recall values
    t = []
    return t


def clean_data():
    print "clean data"

