'''
Description: this file will be used to copy body_seg.nii.gz to another folder
version: 
Author: ThreeStones1029 221620010039@qq.com
Date: 2023-12-22 21:15:44
LastEditors: ShuaiLei
LastEditTime: 2023-12-22 21:55:32
'''
from file_management import create_folder, get_sub_folder_paths, join
import os
import shutil


def copy_files(root_folder, save_folder):
    sub_folder_paths = get_sub_folder_paths(root_folder)
    
    for sub_folder_path in sub_folder_paths:
        for root, dirs, files in os.walk(sub_folder_path):
            for file in files:
                sub_folder_name = os.path.basename(root)
                create_folder(join(save_folder, sub_folder_name))
                if join(sub_folder_path, file).endswith("body_seg.nii.gz"):
                    shutil.copy(join(sub_folder_path, file), join(save_folder, sub_folder_name, file))
                    print(join(sub_folder_path, file), "copy successfully")
    

if __name__ == "__main__":
    copy_files("data/ct_mask", "data/ct_mask_body")