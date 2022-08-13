# Script to convert sk dataset to ImageFolder dataset
# normal, rusty_red, rusty_yellow, unscrewed_red, unscrewed_yellow

import sys
import os
import shutil

class_names = ['normal', 'rusty_red', 'rusty_yellow', 'unscrewed_red', 'unscrewed_yellow']

for class_name in class_names:
    images = os.listdir(class_name)
    total_images = len(images)
    test_images = int(total_images * 0.2)

    print(f"{class_name}: {total_images - test_images} / {test_images}")

    for i in range(test_images):
        image_name = images.pop()
        if not os.path.exists(os.path.join("test", class_name)):
            os.makedirs(os.path.join("test", class_name))
        shutil.move(os.path.join(class_name, image_name), os.path.join("test", class_name, image_name))

    for i in range(total_images - test_images):
        image_name = images.pop()
        if not os.path.exists(os.path.join("train", class_name)):
            os.makedirs(os.path.join("train", class_name))
        shutil.move(os.path.join(class_name, image_name), os.path.join("train", class_name, image_name))
        