# Extract objects from images given a label and a bounding box

# Label format:
# [image file],[class],[x1],[y1],[x2],[y2]
# (x1, y1) is the coordinate of the top-left corner of the box
# (x2, y2) is the coordinate of the bottom-right corner of the box

# Output file hierarchy
# labels.csv
# images
# - all
# - - 000000.jpg
# - - 000001.jpg
# - - ...
# - [class 1]
# - [class 2]
# ...

import sys
import os
import cv2

if len(sys.argv) < 4:
	print("Usage: python3 extract_objects.py /path/to/images /path/to/labels.csv /path/to/output")
	exit()

PATH_IMAGES = sys.argv[1]
PATH_LABELS_CSV = sys.argv[2]
PATH_OUTPUT = sys.argv[3]
CLASS_NAMES = {
	0: "none",
	2: "normal",
	3: "unscrewed_red",
	4: "rusty_yellow",
	5: "rusty_red",
	6: "unscrewed_yellow",
}

if not os.path.exists(PATH_IMAGES):
	print("Invalid image path")
	exit()

if not os.path.exists(PATH_LABELS_CSV):
	print("Invalid label csv file path")
	exit()

if not os.path.exists(PATH_OUTPUT):
	print(f"Output dir {PATH_OUTPUT} does not exist. Creating {PATH_OUTPUT}...")
	os.makedirs(PATH_OUTPUT)

if not os.path.exists(os.path.join(PATH_OUTPUT, "images")):
	os.makedirs(os.path.join(PATH_OUTPUT, "images"))

if not os.path.exists(os.path.join(PATH_OUTPUT, "images", "all")):
	os.makedirs(os.path.join(PATH_OUTPUT, "images", "all"))

print(f"Loading images from: {PATH_IMAGES}")
print(f"Loading labels from:  {PATH_LABELS_CSV}")
print(f"Saving output to:    {PATH_OUTPUT}")

with open(PATH_LABELS_CSV, "r") as f:
	labels = f.readlines()
	labels = [label.strip() for label in labels]

labels = labels[1:]  # Delete the first row(header labels)
print(f"Found {len(labels)} objects")

with open(os.path.join(PATH_OUTPUT, "labels.csv"), "a+") as f:
	f.write(f"image,class_index,class_name,origin_image\n")

for index, label in enumerate(labels):
	image_file_name, class_index, x1_rel, y1_rel, x2_rel, y2_rel = label.split(",")

	try:
		x1_rel, y1_rel, x2_rel, y2_rel = [float(s) for s in [x1_rel, y1_rel, x2_rel, y2_rel]]
		class_index = int(class_index)
	except:
		print("Invalid csv format")
		exit()
	
	if class_index == 0:  # No detection
		continue
	
	if not os.path.exists(os.path.join(PATH_IMAGES, image_file_name)):
		print(f"Image {image_file_name} does not exist")
		exit()
	
	img = cv2.imread(os.path.join(PATH_IMAGES, image_file_name))
	img_h, img_w = img.shape[:2]

	x1_abs, x2_abs = [int(img_w * rel) for rel in [x1_rel, x2_rel]]
	y1_abs, y2_abs = [int(img_h * rel) for rel in [y1_rel, y2_rel]]

	obj_img = img[y1_abs:y2_abs, x1_abs:x2_abs].copy()
	cv2.imwrite(os.path.join(PATH_OUTPUT, "images", "all", f"{index + 1:06}.jpg"), obj_img)

	class_folder_path = os.path.join(PATH_OUTPUT, "images", CLASS_NAMES[class_index])
	if not os.path.exists(class_folder_path):
		os.makedirs(class_folder_path)
	
	cv2.imwrite(os.path.join(class_folder_path, f"{index + 1:06}.jpg"), obj_img)
	
	with open(os.path.join(PATH_OUTPUT, "labels.csv"), "a+") as f:
		f.write(f"{index + 1:06}.jpg,{class_index},{CLASS_NAMES[class_index]},{image_file_name}\n")

	print(f"                                                                                               \r", end="")
	print(f"   Processed {index + 1} / {len(labels)} labels  (class: {CLASS_NAMES[class_index]})\r", end="")

print()
print("Done")
