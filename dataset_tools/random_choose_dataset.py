'''
Description: 
version: 
Author: ThreeStones1029 221620010039@qq.com
Date: 2024-01-23 20:11:03
LastEditors: ShuaiLei
LastEditTime: 2024-04-07 07:55:10
'''
import os
import sys
sys.path.insert(0, sys.path.append(os.path.dirname(sys.path[0])))
import numpy as np
import shutil
from collections import defaultdict
from io_tools.file_management import join, save_json_file
from segmentation_tools.init_segmentation_json import InitSegmentationDatasetJsonTools


def random_choose_images(images_folder, target_folder, random_numbers):
    """
    每一例CT随机筛选图片
    """
    os.makedirs(target_folder, exist_ok=True)
    for file_name in os.listdir(images_folder):
        file_name_no_ext = os.path.splitext(file_name)[0]
        number = file_name_no_ext.split("_")[-1]
        if int(number) in random_numbers:
            shutil.copy(join(images_folder, file_name), join(target_folder, file_name))

    
if __name__ == "__main__":
    random_choose_images("data/segmentation_dataset/LA512/masks", 
                         "data/segmentation_dataset/all512/masks",
                         random_numbers=[1, 3, 5, 8, 10, 13, 15, 20, 17, 19])
