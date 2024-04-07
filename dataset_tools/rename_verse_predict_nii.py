'''
Description: this file will be used to rename the nii file which are predicted by [MedicalDataAugmentationTool-VerSe](https://github.com/christianpayer/MedicalDataAugmentationTool-VerSe)
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-04-07 07:56:08
LastEditors: ShuaiLei
LastEditTime: 2024-04-07 08:39:50
'''
import os 
import sys
sys.path.insert(0, sys.path.append(os.path.dirname(sys.path[0])))
from io_tools.file_management import get_sub_folder_paths, get_subfiles
from nii_tools.verse_separate_mask import VerseCategoriesFormat
import re



def rename_prediction_resampled_nii_files(data_root_folder):
    """
    The function will be used to rename predicted nii file by MedicalDataAugmentationTool-VerSe.
    param: data_root_folder: the dataset root folder.
    """
    catid2catname = VerseCategoriesFormat().get_catid2catname()
    sub_folder_paths = get_sub_folder_paths(data_root_folder)
    modified_sub_folder_path_list = []
    for sub_folder_path in sub_folder_paths:
        nii_file_paths = get_subfiles(sub_folder_path, ".nii.gz")
        for nii_file_path in nii_file_paths:
            nii_file_name = os.path.basename(nii_file_path)
            if "prediction_resampled" in nii_file_name:
                cat_id = re.findall(r'\d+', nii_file_name)
                cat_name = catid2catname[int(cat_id[0]) + 1]
                nii_new_file_name = cat_name + "_seg.nii.gz"
                print(os.path.join(sub_folder_path, nii_new_file_name))
                os.rename(os.path.join(sub_folder_path, nii_file_name), os.path.join(sub_folder_path, nii_new_file_name))
                if sub_folder_path not in modified_sub_folder_path_list:
                    modified_sub_folder_path_list.append(sub_folder_path)
    print(modified_sub_folder_path_list)

    
if __name__ == "__main__":
    rename_prediction_resampled_nii_files("data/Fracture")