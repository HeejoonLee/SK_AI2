# Script to split the given dataset into three sets(training, validation and test) such that they have similar distribution of classes

import os
import sys
import random

# 1. Split randomly
# 2. Evaluate distribution for each set
# 3. Measure the distribution difference
# 4. Continue 1-3 until there is enough data
# 5. Choose the data with the smallest difference

# Usage: python3 stratified_split.py 80

if len(sys.argv) < 2:
    print("Usage: python3 stratified_split.py [training set proportion]")
    exit()

# TODO
