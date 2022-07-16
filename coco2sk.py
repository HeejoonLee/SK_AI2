# Script to convert YOLO output to SK format
# SK format:
# [image file] [class index] [confidence] [x1] [y1] [x2] [y2]
# img_pred_0001.jpg 2 0.9888 0.084 0.294 0.23 0.44

import os
import sys

if len(sys.argv) < 2:
    print("Usage: python3 coco2sk.py input_folder output_csv_file")
    exit()

COCO_OUTPUT_PATH = sys.argv[1]
SK_CSV_PATH = sys.argv[2]

YOLO_TO_SK = {
    "0": "2",
    "1": "3",
    "2": "4",
    "3": "5",
    "4": "6"
}

if not os.path.exists(COCO_OUTPUT_PATH):
    print("Error: YOLO output does not exist")
    exit()

image_list = [f for f in os.listdir(COCO_OUTPUT_PATH) if f.endswith(".jpg")]
image_list.sort()

with open(SK_CSV_PATH, "w") as f:
    f.write("img_id,class_id,score,x1,y1,x2,y2\n")

    for image in image_list:
        text_file_name = image.split(".")[0] + ".txt"
        if not os.path.exists(os.path.join(COCO_OUTPUT_PATH, text_file_name)):
            # No detection found
            f.write(f"{image},0,0,0,0,0,0\n")
            continue

        with open(os.path.join(COCO_OUTPUT_PATH, text_file_name), "r") as r:
            detections = r.readlines()
            for detection in detections:
                yolo_class, confidence, x_center, y_center, width, height = detection.split()
                x_center = float(x_center)
                y_center = float(y_center)
                width = float(width)
                height = float(height)

                # Convert YOLO class index to SK index(discard all invalid indices)
                if yolo_class not in YOLO_TO_SK.keys():
                    continue
                sk_class = YOLO_TO_SK[yolo_class]

                # Convert x_center, y_center, width, height to x1, y1, x2, y2
                x1 = x_center - width / 2
                y1 = y_center - height / 2
                x2 = x_center + width / 2
                y2 = y_center + height / 2

                f.write(f"{image},{sk_class},{confidence},{x1},{y1},{x2},{y2}\n")
