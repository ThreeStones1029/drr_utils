'''
Description: The file will be used to check the download verse dataset.
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-03-29 08:26:20
LastEditors: ShuaiLei
LastEditTime: 2024-03-29 08:27:59
'''
import os
import sys
import json
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import SimpleITK as sitk
from tqdm import tqdm
import numpy as np
import shutil
from io_tools.file_management import get_sub_folder_paths, get_subfiles, load_json_file, join, create_folder, save_json_file


def check_root_folder(root_path):
    """
    整理verse2020数据集,对于子文件夹多个ct需要拆出来, 没有ct则删除该文件夹
    """
    sub_folder_paths = get_sub_folder_paths(root_path) 
    for sub_folder_path in tqdm(sub_folder_paths, desc="checking"):
        nii_file_paths = get_subfiles(sub_folder_path, ".nii.gz")
        if len(nii_file_paths) > 2:
            print(sub_folder_path, "exist multi cts")
            split_sub_folder(sub_folder_path)


def check_none_folder(root_path):
    sub_folder_paths = get_sub_folder_paths(root_path) 
    for sub_folder_path in tqdm(sub_folder_paths, desc="checking None folder"):
        nii_file_paths = get_subfiles(sub_folder_path, ".nii.gz")
        if len(nii_file_paths) == 0:
            print(sub_folder_path, "don't exist ct")
        if len(nii_file_paths) == 1:
            print("please check", sub_folder_path)