'''
Description: 
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-03-28 07:39:57
LastEditors: ShuaiLei
LastEditTime: 2024-03-28 07:44:28
'''
import os
import sys
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import SimpleITK as sitk
from nii_tools.verse_format_conver import VerseCategoriesFormat


def sitk_merge_masks(mask_path_list, merged_mask_nii_path):
    """
    Using sitk.
    The function will used to merge seg mask.
    param: mask_path_list: The seg mask file path list.
    param: merged_mask_nii_path: The merged seg file save path.
    """
    image = sitk.ReadImage("data/verse2019/sub-verse009/sub-verse009bottom.nii.gz")
    first_mask = sitk.ReadImage(mask_path_list[0])
    first_mask_array = sitk.GetArrayFromImage(first_mask)
    catname = os.path.basename(mask_path_list[0]).split("_")[0]
    catname2catid = VerseCategoriesFormat().get_catname2catid() 
    first_mask_array[first_mask_array==1] = catname2catid[catname]
    first_mask = sitk.GetImageFromArray(first_mask_array)
    merged_mask = first_mask
    for mask_path in mask_path_list[1: ]:
        mask = sitk.ReadImage(mask_path)
        mask_array = sitk.GetArrayFromImage(mask)
        catname = os.path.basename(mask_path).split("_")[0]
        catname2catid = VerseCategoriesFormat().get_catname2catid() 
        mask_array[mask_array==1] = catname2catid[catname]
        mask = sitk.GetImageFromArray(mask_array)
        merged_mask += mask
    # merged_mask.SetOrigin(first_mask.GetOrigin())
    # merged_mask.SetDirection(first_mask.GetDirection())
    # merged_mask.SetSpacing(first_mask.GetSpacing())
    merged_mask.SetOrigin(image.GetOrigin())
    merged_mask.SetDirection(image.GetDirection())
    merged_mask.SetSpacing(image.GetSpacing())
    # merged_mask_array = sitk.GetArrayFromImage(merged_mask)
    # labels = set(merged_mask_array.flatten())
    # print(labels)
    sitk.WriteImage(merged_mask, merged_mask_nii_path)
    

    
def nibabel_merge_masks(seg_mask_path_list, merge_seg_nii_path):
    """
    Using nibabel.

    """


if __name__ == "__main__":
    sitk_merge_masks(["data/verse2019/sub-verse009/T10_seg.nii.gz",
                      "data/verse2019/sub-verse009/T11_seg.nii.gz",
                      "data/verse2019/sub-verse009/T12_seg.nii.gz",
                      "data/verse2019/sub-verse009/L1_seg.nii.gz",
                      "data/verse2019/sub-verse009/L2_seg.nii.gz",
                      "data/verse2019/sub-verse009/L3_seg.nii.gz",
                      "data/verse2019/sub-verse009/L4_seg.nii.gz",
                      "data/verse2019/sub-verse009/L5_seg.nii.gz"], "data/verse2019/sub-verse009/sub-verse009bottom_seg.nii.gz")