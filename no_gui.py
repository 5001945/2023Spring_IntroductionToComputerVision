import time
import argparse
import shutil

import cv2

from core import *


parser = argparse.ArgumentParser()
parser.add_argument("-i", dest="in_file")
parser.add_argument("-o", dest="out_file")
args = parser.parse_args()

start = time.time()

img = cv2.imread(args.in_file)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

a4 = get_a4(img, get_quadrilateral(img))
results = get_ocr_results(a4)
each_fonts = get_corresponding_fonts(a4, results)

temp_filename = get_pdf(results, each_fonts)
shutil.move(temp_filename, args.out_file)

print(f"Running time: {time.time() - start} seconds")
