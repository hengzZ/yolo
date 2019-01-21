#!/usr/bin/python

"""
mAp calculate and plot:
"""

import argparse
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from itertools import cycle
import numpy as np
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score

import evaluate_object as eo


# setup plot details
colors = cycle(['navy', 'turquoise', 'darkorange', 'cornflowerblue', 'teal'])
lw = 2


def get_label_and_score(args):
    return eo.evaluate_object(args.result_directory, args.truth_directory)


def parse_args():
    parser = argparse.ArgumentParser('mAP calculate')
    parser.add_argument('--result', dest='result_directory', help='directory contains files of prediction result')
    parser.add_argument('--truth', dest='truth_directory', help='directory contains files of ground truth')
    args = parser.parse_args()
    return args


def main(args):
    result_id = 'test'
    y_labels, y_scores = get_label_and_score(args)
    # Compute Precision-Recall curve
    precision, recall, thresholds = precision_recall_curve(y_labels, y_scores)
    average_precision = average_precision_score(y_labels, y_scores)
    # Echo information
    print 'Precision:', precision
    print 'Recall:', recall
    print 'Threshold:', thresholds
    # plot curve
    plt.clf()
    plt.plot(recall, precision, lw=lw, color='navy', label=result_id+'(area={0:0.2f})'.format(average_precision))
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.xlim(0.0, 1.0)
    plt.ylim(0.0, 1.05)
    #plt.title('precision-recall example: AUC={0:0.2f}'.format(average_precision))
    plt.title('precision-recall')
    plt.legend(loc='lower left')
    plt.show()
    plt.savefig(result_id+'.png')


if __name__ == '__main__':
    print(__doc__)
    args = parse_args()
    main(args)

