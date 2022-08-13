import sys
import os
import pandas as pd
import argparse

from ensemble_boxes import weighted_boxes_fusion

parser = argparse.ArgumentParser()
parser.add_argument("--detections", nargs="+", type=str, default="", help=".csv file paths")
parser.add_argument("--weights", nargs="+", type=int, help="Specify a weight for each csv file")
parser.add_argument("--iou_threshold", type=float, default=0.5)

args = parser.parse_args()
print(args)

if len(args.detections) < 2:
    print("At least two .csv file are required for ensemble")
    exit()

if len(args.weights) != len(args.detections):
    print("The same number of weights and detections is required")
    exit()

boxes = []
scores = []
labels = []
weights = args.weights

iou_threshold = args.iou_threshold
skip_box_threshold = 0.0001

for detection in args.detections:
    if not os.path.exists(detection):
        print(f"File {detection} does not exist")
        continue

    df = pd.read_csv(detection)
    df_coordinates = df[["x1", "y1", "x2", "y2"]]
    
    boxes_list = df_coordinates.values.tolist()
    score_list = df["score"].to_list()
    labels_list = df["class_id"].to_list()

    scores.append(score_list)
    labels.append(labels_list)
    boxes.append(boxes_list)
    
    print(len(score_list))
    print(len(boxes_list))
    print(len(labels_list))
    
