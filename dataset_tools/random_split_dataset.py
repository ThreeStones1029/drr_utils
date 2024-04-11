'''
Description: 
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-03-31 10:02:47
LastEditors: ShuaiLei
LastEditTime: 2024-04-10 03:11:55
'''
import numpy as np
import shutil
import os
import sys
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
if project_root not in sys.path:
    sys.path.insert(0, os.path.dirname(sys.path[0]))
from io_tools.file_management import create_folder, join


def random_choose_dataset(images_folder, save_images_folder, number):
    """
    The function will be used to choose images from images_folder randomly.
    param: images_folder: The init images folder path.
    param: save_images_folder: The choosed images save folder path.
    param: number: choosed images number.
    """
    create_folder(save_images_folder)
    images_filename_list = os.listdir(images_folder)
    np.random.shuffle(images_filename_list)
    choosed_images_filename_list = images_filename_list[: number]
    for filename in choosed_images_filename_list:
        shutil.copy(join(images_folder, filename), join(save_images_folder, filename))


if __name__ == "__main__":
    random_choose_dataset("data/Fracture_dataset/all/normal_images",
                          "/home/efficientnetV2/dataset/spine_fracture/all/normal_images",
                          834)
