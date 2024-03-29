'''
Description: this file will be used to rename verse datset ct mask png and json.
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-03-29 09:01:25
LastEditors: ShuaiLei
LastEditTime: 2024-03-29 09:03:29
'''
import os
import sys
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from tqdm import tqdm
from io_tools.file_management import get_sub_folder_paths, join


def rename_cts(root_path):
    """
    重新命名文件名字,让ct名字与子文件名字一样,方便生成数据
    """
    sub_folder_paths = get_sub_folder_paths(root_path) 
    for sub_folder_path in tqdm(sub_folder_paths, desc="renaming"):
        ct_folder_name = os.path.basename(sub_folder_path)
        for file in os.listdir(sub_folder_path):
            if file.endswith("seg.nii.gz"):
                new_file = ct_folder_name + "_seg.nii.gz"
            if file.endswith(".nii.gz") and "seg" not in file:
                new_file = ct_folder_name + ".nii.gz"
            if file.endswith(".png"):
                new_file = ct_folder_name + ".png"
            if file.endswith("w.png"):
                new_file = ct_folder_name + "_w.png"
            if file.endswith(".json"):
                new_file = ct_folder_name + ".json"
            os.rename(join(sub_folder_path, file), join(sub_folder_path, new_file))


def rename_verse2019_cts(root_path):
    """
    The function will used to rename verse2019 ct mask png json.
    """
    sub_folder_paths = get_sub_folder_paths(root_path) 
    for sub_folder_path in tqdm(sub_folder_paths, desc="renaming"):
        ct_folder_name = os.path.basename(sub_folder_path)
        for file in os.listdir(sub_folder_path):
            if file.endswith("ct.nii.gz"):
                new_file = ct_folder_name + ".nii.gz"
            if file.endswith("msk.nii.gz"):
                new_file = ct_folder_name + "_seg.nii.gz"
            if file.endswith(".png"):
                new_file = ct_folder_name + ".png"
            if file.endswith("w.png"):
                new_file = ct_folder_name + "_w.png"
            if file.endswith("ctd.json"):
                new_file = ct_folder_name + ".json"
            os.rename(join(sub_folder_path, file), join(sub_folder_path, new_file))


if __name__ == "__main__":
    rename_verse2019_cts("data/verse2019")