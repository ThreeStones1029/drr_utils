'''
Description: The file will be used to check the download verse dataset.
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-03-29 08:26:20
LastEditors: ShuaiLei
LastEditTime: 2024-03-29 12:16:11
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
    Check the verse dataset and delete the folder if there is no ct.
    dataset format before check example:
        verse2020
            ├── GL003
            └── GL018
                ├── GL018-GL016.nii.gz
                ├── GL018-GL016-w.png
                ├── GL018-GL016_iso-ctd.json
                └── GL018-GL016_seg.nii.gz
                ├── GL018-GL017.nii.gz
                ├── GL018-GL017-w.png
                ├── GL018-GL017_iso-ctd.json
                └── GL018-GL017_seg.nii.gz
            └── GL020
                ├── GL020-w.png
                ├── GL020_iso-ctd.json
                └── GL020_seg.nii.gz
            └── GL025
                ├── GL025.nii.gz
                ├── GL025-w.png
                ├── GL025_iso-ctd.json
                └── GL025_seg.nii.gz
    param: root_path: the verse datset path.
    Example of manually modified dataset format based on code run results:
        verse2020
            └── GL016
                ├── GL016.nii.gz
                ├── GL016-w.png
                ├── GL016_iso-ctd.json
                └── GL016_seg.nii.gz
            └── GL017
                ├── GL017.nii.gz
                ├── GL017-w.png
                ├── GL017_iso-ctd.json
                └── GL017_seg.nii.gz
            └── GL025
                ├── GL025.nii.gz
                ├── GL025-w.png
                ├── GL025_iso-ctd.json
                └── GL025_seg.nii.gz
    """
    sub_folder_paths = get_sub_folder_paths(root_path) 
    for sub_folder_path in tqdm(sub_folder_paths, desc="checking sub folder"):
        nii_file_paths = get_subfiles(sub_folder_path, ".nii.gz")
        if len(nii_file_paths) == 0:
            print(sub_folder_path, "don't exist ct")
        if len(nii_file_paths) == 1:
            print(sub_folder_path, "only one nii.gz file, please delete the subfolder")
        if len(nii_file_paths) > 2:
            print(sub_folder_path, "have multi nii.gz file, please repartition and ensure that each subfolder has only one nii.gz and one seg.nii.gz.")


def split_sub_folder(sub_folder_path):
    """
    Some sub-folders are stored in the same person's CT, need to separate the ct separately.
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
    check_root_folder("data/verse2019_test1")