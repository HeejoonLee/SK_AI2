# Script to convert SK label csv file to coco label text files
# Default path:
# /home/work/sample-notebooks/data/train/train.csv
# /home/work/sample-notebooks/data/train/coco_format/labels

import os
import sys
import random
import shutil

if len(sys.argv) < 7:
    print("Usage: python3 sk2coco.py /home/work/sample-notebooks/data/train/train.csv /home/work/sample-notebooks/data/train/train /home/work/sample-notebooks/data/train/coco_format/labels 80 10 10")
    exit()

SK_LABEL_PATH = sys.argv[1]
SK_IMAGE_PATH = sys.argv[2]
COCO_LABEL_PATH = sys.argv[3]
train_set_ratio = int(sys.argv[4])
val_set_ratio = int(sys.argv[5])
test_set_ratio = int(sys.argv[6])
random.seed(0)

if not os.path.exists(SK_LABEL_PATH):
    print("Input csv file does not exist")
    exit()

# Set up output directory
if not os.path.exists(COCO_LABEL_PATH):
    print("Output path does not exist")
    print(f"Creating directory {COCO_LABEL_PATH}...")
    os.makedirs(COCO_LABEL_PATH)

os.makedirs(os.path.join(COCO_LABEL_PATH, "images/train"))
os.makedirs(os.path.join(COCO_LABEL_PATH, "images/val"))
os.makedirs(os.path.join(COCO_LABEL_PATH, "images/test"))
os.makedirs(os.path.join(COCO_LABEL_PATH, "labels/train"))
os.makedirs(os.path.join(COCO_LABEL_PATH, "labels/val"))
os.makedirs(os.path.join(COCO_LABEL_PATH, "labels/test"))

class_map = {
    "2": "0",
    "3": "1",
    "4": "2",
    "5": "3",
    "6": "4"
}

with open(SK_LABEL_PATH) as f:
    detections = f.readlines()
    detections = [x.strip() for x in detections]

for index, detection in enumerate(detections):
    # Skip the first row which contains header texts
    if index == 0:
        continue

    image_id, class_id, x1, y1, x2, y2 = detection.split(",")

    # image_tr_00001.jpg -> 00001
    image_name = image_id.split(".jpg", 1)[0]
    image_name = image_name.split("_")[-1]

    # Map class ids
    if class_id == "0":
        with open(os.path.join(COCO_LABEL_PATH, image_name + ".txt"), "a+") as f:
            f.write(f"deleteme")
        continue
    class_index = class_map[class_id]

    with open(os.path.join(COCO_LABEL_PATH, image_name + ".txt"), "a+") as f:
        f.write(f"{class_index} {x1} {y1} {x2} {y2}\n")
    
    print(f"   {index + 1} / {len(detections)} detections processed\r", end="")

# Create train, val, test sets
print("Creating train, val, and test sets...")

image_list = [f for f in os.listdir(COCO_LABEL_PATH) if f.endswith(".txt")]
train_set_count = len(image_list) * train_set_ratio // 100
val_set_count = len(image_list) * val_set_ratio // 100
test_set_count = len(image_list) - train_set_count - val_set_count

for i in range(train_set_count):
    current_draw = image_list.pop(random.randint(0, len(image_list) - 1))
    current_id = current_draw.split(".txt", 1)[0]
    shutil.move(os.path.join(COCO_LABEL_PATH, current_draw), os.path.join(COCO_LABEL_PATH, "labels", "train", current_draw))
    shutil.copy(os.path.join(SK_IMAGE_PATH, f"img_tr_{current_id}.jpg"), os.path.join(COCO_LABEL_PATH, "images", "train", f"{current_id}.jpg"))

for i in range(val_set_count):
    current_draw = image_list.pop(random.randint(0, len(image_list) - 1))
    current_id = current_draw.split(".txt", 1)[0]
    shutil.move(os.path.join(COCO_LABEL_PATH, current_draw), os.path.join(COCO_LABEL_PATH, "labels", "val", current_draw))
    shutil.copy(os.path.join(SK_IMAGE_PATH, f"img_tr_{current_id}.jpg"), os.path.join(COCO_LABEL_PATH, "images", "val", f"{current_id}.jpg"))

for i in range(test_set_count):
    current_draw = image_list.pop(random.randint(0, len(image_list) - 1))
    current_id = current_draw.split(".txt", 1)[0]
    os.remove(os.path.join(COCO_LABEL_PATH, current_draw))
    shutil.copy(os.path.join(SK_IMAGE_PATH, f"img_tr_{current_id}.jpg"), os.path.join(COCO_LABEL_PATH, "images", "test", f"{current_id}.jpg"))

print(f"Train: {train_set_count}, Val: {val_set_count}, Test: {test_set_count}")

# Create .txt files containing image paths
with open(os.path.join(COCO_LABEL_PATH, "train.txt"), "w") as f:
    image_list = [f for f in os.listdir(os.path.join(COCO_LABEL_PATH, "images", "train"))]
    image_list.sort()
    for image in image_list:
        f.write(f"./images/train/{image}\n")

with open(os.path.join(COCO_LABEL_PATH, "val.txt"), "w") as f:
    image_list = [f for f in os.listdir(os.path.join(COCO_LABEL_PATH, "images", "val"))]
    image_list.sort()
    for image in image_list:
        f.write(f"./images/val/{image}\n")

with open(os.path.join(COCO_LABEL_PATH, "test.txt"), "w") as f:
    image_list = [f for f in os.listdir(os.path.join(COCO_LABEL_PATH, "images", "test"))]
    image_list.sort()
    for image in image_list:
        f.write(f"./images/test/{image}\n")

# Clean
text_file_list = [f for f in os.listdir(os.path.join(COCO_LABEL_PATH, "labels", "train"))]
remove_list = []
for text_file in text_file_list:
    with open(os.path.join(COCO_LABEL_PATH, "labels", "train", text_file), "r") as f:
        if f.readline() == "deleteme":
            remove_list.append(text_file)

for file in remove_list:
    os.remove(os.path.join(COCO_LABEL_PATH, "labels", "train", file))

text_file_list = [f for f in os.listdir(os.path.join(COCO_LABEL_PATH, "labels", "val"))]
remove_list = []
for text_file in text_file_list:
    with open(os.path.join(COCO_LABEL_PATH, "labels", "val", text_file), "r") as f:
        if f.readline() == "deleteme":
            remove_list.append(text_file)

for file in remove_list:
    os.remove(os.path.join(COCO_LABEL_PATH, "labels", "val", file))

