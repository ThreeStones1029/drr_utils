'''
Description: The file will be used to check the download verse dataset.
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-03-29 08:26:20
LastEditors: ShuaiLei
LastEditTime: 2024-03-29 08:52:27
'''
import os
import sys
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from tqdm import tqdm
import shutil
from io_tools.file_management import get_sub_folder_paths, get_subfiles, join, create_folder


def check_root_folder(root_path):
    """
    Organize the verse dataset and delete the folder if there is no ct.
    param: root_path: 
    """
    sub_folder_paths = get_sub_folder_paths(root_path) 
    for sub_folder_path in tqdm(sub_folder_paths, desc="checking"):
        nii_file_paths = get_subfiles(sub_folder_path, ".nii.gz")
        if len(nii_file_paths) > 2:
            print(sub_folder_path, "exist multi cts")
            # split_sub_folder(sub_folder_path)


def check_none_folder(root_path):
    """
    Check the verse dataset and delete the folder if there is no ct.
    param: root_path: the verse datset path.
    """
    sub_folder_paths = get_sub_folder_paths(root_path) 
    for sub_folder_path in tqdm(sub_folder_paths, desc="checking None folder"):
        nii_file_paths = get_subfiles(sub_folder_path, ".nii.gz")
        if len(nii_file_paths) == 0:
            print(sub_folder_path, "don't exist ct")
        if len(nii_file_paths) == 1:
            print("please check", sub_folder_path)


def split_sub_folder(sub_folder_path):
    """
    verse2020数据集,有的子文件夹保存的是同一个人的CT,需要单独将ct分开
    """
    root_folder = os.path.dirname(sub_folder_path)
    print(root_folder)
    for file_name in os.listdir(sub_folder_path):
        new_sub_folder_name = file_name.split("_")[1]
        print(new_sub_folder_name)
        new_sub_folder_path = join(root_folder, new_sub_folder_name)
        create_folder(new_sub_folder_path)
        new_file_name = file_name[9:]
        os.rename(join(sub_folder_path, file_name), join(sub_folder_path, new_file_name))
        shutil.copy(join(sub_folder_path, new_file_name), join(new_sub_folder_path, new_file_name))
    shutil.rmtree(sub_folder_path)


if __name__ == "__main__":
    check_none_folder("data/verse2019_test1")