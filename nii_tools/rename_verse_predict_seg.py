'''
Description: 这个文件用于重命名verse2020代码预测的seg文件
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-06-21 06:10:05
LastEditors: ShuaiLei
LastEditTime: 2024-06-21 06:33:02
'''
import sys
import os
import itk
sys.path.insert(0, sys.path.append(os.path.dirname(sys.path[0])))
from tqdm import tqdm
from io_tools.file_management import get_sub_folder_paths, create_folder, join, get_subfiles, load_json_file, save_json_file
from nii_tools.verse_separate_mask import VerseCategoriesFormat


def rename_predict_seg_file(input_folder, output_folder):
    """
    param: input_folder: seg files which will be rename to vertebrae labels.
    """
    sub_folder_paths = get_sub_folder_paths(input_folder)
    catid2catname = VerseCategoriesFormat().get_catid2catname()
    for sub_folder_path in tqdm(sub_folder_paths, desc="renameing"):
        sub_folder_name = os.path.basename(sub_folder_path)
        sub_output_folder = create_folder(join(output_folder, sub_folder_name))
        for file_name in os.listdir(sub_folder_path):
            if file_name.endswith("resampled.nii.gz"):
                vertebrae_id = int(file_name.split("_")[-3])
                label = catid2catname[vertebrae_id + 1]
                new_file_name = label + "_seg.nii.gz"
                os.rename(os.path.join(sub_folder_path, file_name), os.path.join(sub_output_folder, new_file_name))
                

if __name__ == "__main__":
    rename_predict_seg_file("data/TD_fracture", "data/TD_fracture")