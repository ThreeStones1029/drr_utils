'''
Description: this file will be used to rename verse datset ct mask png and json.
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-03-29 09:01:25
LastEditors: ShuaiLei
LastEditTime: 2024-06-17 06:21:14
'''
import os
import sys
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from tqdm import tqdm
from io_tools.file_management import get_sub_folder_paths, join


def rename_verse2020_cts(root_path):
    """
    VerSe 2020(MICCAI2020 challenge data stracture)
    the ct sub folder directly put in verse2020 don't need training test valiadtion folder.
    example:
        verse2020
        ├── GL003
        │   ├── GL003.nii.gz
        │   ├── GL003-w.png
        │   ├── GL003_iso-ctd.json
        │   └── GL003_seg.nii.gz
        └── sub-verse013
            ├── GL016.nii.gz
            ├── GL016-w.png
            ├── GL016_iso-ctd.json
            └── GL016_seg.nii.gz
    Rename the file name so that the ct name is the same as the subfile name to facilitate data generation.
    param: root_path: the verse 2020 dataset folder.
    """
    sub_folder_paths = get_sub_folder_paths(root_path) 
    for sub_folder_path in tqdm(sub_folder_paths, desc="renaming"):
        ct_folder_name = os.path.basename(sub_folder_path)
        for file in os.listdir(sub_folder_path):
            if file.endswith("seg.nii.gz"):
                new_file = ct_folder_name + "_seg.nii.gz"
            if file.endswith("ct.nii.gz"):
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
    Verse 2019(subject based data stracture)
    the ct sub folder directly put in verse2020 don't need training test valiadtion folder.
    example: 
        verse2019
        ├── sub-verse012
        │   ├── sub-verse012_ct.nii.gz
        │   ├── sub-verse012_seg-subreg_ctd.json
        │   ├── sub-verse012_seg-vert_msk.nii.gz
        │   └── sub-verse012_seg-vert_snp.png
        └── sub-verse013
            ├── sub-verse013_ct.nii.gz
            ├── sub-verse013_seg-subreg_ctd.json
            ├── sub-verse013_seg-vert_msk.nii.gz
            └── sub-verse013_seg-vert_snp.png

    Rename the file name so that the ct name is the same as the subfile name to facilitate data generation.
    param: root_path: the verse 2019 dataset folder.
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
    rename_verse2020_cts("data/verse2020_fracture")