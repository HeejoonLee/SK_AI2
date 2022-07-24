# Script to split the given dataset into three sets(training, validation and test) such that they have similar distribution of classes

import os
import sys
import random
import shutil
from collections import defaultdict

# 1. Split randomly
# 2. Evaluate distribution for each set
# 3. Measure the distribution difference
# 4. Continue 1-3 until there is enough data
# 5. Choose the data with the smallest difference

# input csv:
# [image file name] [class index] [class name]

# Usage: python3 stratified_split.py image_dir csv_file output_dir train_proportion
# ex) python3 stratified_split.py /home/work/ /home/work/.csv /home/work/ 80

if len(sys.argv) < 4:
    print("Usage: python3 stratified_split.py /home/work/sample-notebooks/data/train/extracted42/images/all /home/work/sample-notebooks/data/train/extracted42/labels.csv output_dir 80")
    exit()

PATH_IMAGE_DIR = sys.argv[1]
PATH_CSV_FILE = sys.argv[2]
PATH_OUTPUT_DIR = sys.argv[3]
RATIO_TRAIN = (int(sys.argv[4])) / 100.0
RATIO_VAL = 1 - RATIO_TRAIN
RATIO_TEST = 1 - RATIO_TRAIN

random.seed(0)

print(f"Image path: {PATH_IMAGE_DIR}")
print(f"csv file: {PATH_CSV_FILE}")
print(f"Output path: {PATH_OUTPUT_DIR}")
print(f"train/val/test: ({RATIO_TRAIN:.2}/{RATIO_VAL:.2})/{RATIO_TEST:.2}")

# TODO
images_list = defaultdict(list)

with open(PATH_CSV_FILE, "r") as csv_f:
    for entry in csv_f:
        image_file, _, class_name, _ = entry.strip().split(",")
        if image_file == 'image':
            continue
        images_list[class_name].append(image_file)

# DEBUG
total_objects = 0
for key in images_list.keys():
    print(f"{key}: {len(images_list[key])}")
    total_objects += len(images_list[key])
print(f"Total: {total_objects}")

if not os.path.exists(PATH_OUTPUT_DIR):
    os.makedirs(PATH_OUTPUT_DIR)
    os.makedirs(os.path.join(PATH_OUTPUT_DIR, "train"))
    os.makedirs(os.path.join(PATH_OUTPUT_DIR, "val"))
    os.makedirs(os.path.join(PATH_OUTPUT_DIR, "test"))

csv_entries = {'train': [], 'val': [], 'test': []}

for key in images_list.keys():
    total_images_count = len(images_list[key])
    test_images_count = int(total_images_count * RATIO_TEST)
    val_images_count = int((total_images_count - test_images_count) * RATIO_VAL)
    train_images_count = total_images_count - test_images_count - val_images_count

    # Test set
    for i in range(test_images_count):
        index = random.randint(0, len(images_list[key]) - 1)
        image_file = images_list[key].pop(index)
        csv_entries['test'].append([image_file, key])

    # Validation set
    for i in range(val_images_count):
        index = random.randint(0, len(images_list[key]) - 1)
        image_file = images_list[key].pop(index)
        csv_entries['val'].append([image_file, key])

    # Train set
    for i in range(train_images_count):
        csv_entries['train'].append([images_list[key].pop(), key])
    
    assert(len(images_list[key]) == 0)

    print(f"{key}: {train_images_count} / {val_images_count} / {test_images_count}")

for set, images in csv_entries.items():
    with open(os.path.join(PATH_OUTPUT_DIR, f"{set}.csv"), "w") as labels:
        labels.write("image,class\n")
        for image in images:
            shutil.copy(os.path.join(PATH_IMAGE_DIR, image[0]), os.path.join(PATH_OUTPUT_DIR, set, image[0]))
            labels.write(f"{image[0]},{image[1]}\n")

    print(f"Created split for {set}. {len(csv_entries[set])} entries")

print("Done")