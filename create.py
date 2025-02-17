"""
This script serves to extract a small dataset (ca. 55 MB) out of the large original dataset (3.4 GB).
This small dataset is used for unittests.

The original dataset is assumed to be located in `../atsds_large`.
"""

import os
import glob
import collections
import shutil
from ipydex import IPS


# number of images per class which should be considered
limit = 2


src_path = os.path.abspath("../atsds_large")
work_path = os.path.abspath(os.getcwd())
target_ds_name = "atsds_demo"


png_list = glob.glob(f"{src_path}/*/*/*.png")
png_list.sort()

processed_files = collections.Counter()


for png_path in png_list:
    rel_path = png_path.replace(src_path, "")[1:]
    dir_path, fname = os.path.split(rel_path)
    if processed_files[dir_path] >= limit:
        continue
    if processed_files[dir_path] == 0:
        os.makedirs(os.path.join(target_ds_name, dir_path))
        os.makedirs(os.path.join(f"{target_ds_name}_background", dir_path))
        os.makedirs(os.path.join(f"{target_ds_name}_mask", dir_path))

    processed_files[dir_path] += 1

    # main image
    target_path = png_path.replace(src_path, os.path.join(work_path, target_ds_name))
    shutil.copy(png_path, target_path)

    # background
    target_path = png_path.replace(src_path, os.path.join(work_path, f"{target_ds_name}_background"))
    png_path_background = png_path.replace(src_path, f"{src_path}_background")
    shutil.copy(png_path_background, target_path)

    # mask
    target_path = png_path.replace(src_path, os.path.join(work_path, f"{target_ds_name}_mask"))
    png_path_mask = png_path.replace(src_path, f"{src_path}_mask")
    shutil.copy(png_path_mask, target_path)

    print(target_path)


print("done.")
