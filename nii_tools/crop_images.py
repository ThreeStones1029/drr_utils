'''
Description: The file will be used to crop nii and seg mask files.
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-03-28 07:36:18
LastEditors: ShuaiLei
LastEditTime: 2024-04-02 02:38:52
'''
import os
import sys
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from io_tools.file_management import get_sub_folder_paths, join, get_subfiles, load_json_file
import SimpleITK as sitk
from collections import defaultdict
from drr_utils.nii_tools.verse_separate_mask import VerseCategoriesFormat


def crop_nii_according_vertebrae_label(input_folder, vertebrae_label_list, verbose=True):
    """
    The function will be used to crop nii file.
    param: input_folder: The ct dataset input root folder.
    param: output_folder: The cropped ct dataset output root folder.
    param: vertebrae_label_list: The vertebrae label in ct after cropped. 
    """
    catid2catname = VerseCategoriesFormat().get_catid2catname()
    sub_folder_paths = get_sub_folder_paths(input_folder)
    need_to_crop_ct_path_dict = defaultdict(list)
    for sub_folder_path in sub_folder_paths:
        json_files = get_subfiles(sub_folder_path, ".json")
        ct_name = os.path.basename(sub_folder_path)
        json_data = load_json_file(json_files[0])
        for point_data in json_data:
            if "label" in point_data and catid2catname[point_data["label"]] not in vertebrae_label_list:
                need_to_crop_ct_path_dict[join(sub_folder_path, ct_name + ".nii.gz")].append(catid2catname[point_data["label"]])

    for need_to_crop_ct_path, not_need_cat_name_list in need_to_crop_ct_path_dict.items():
        image_total = sitk.ReadImage(need_to_crop_ct_path)
        ct_name = os.path.basename(need_to_crop_ct_path)
        mask_path = join(os.path.dirname(need_to_crop_ct_path), ct_name.split(".")[0] + "_seg.nii.gz")
        mask_total = sitk.ReadImage(mask_path)
        json_path = get_subfiles(os.path.dirname(need_to_crop_ct_path), ".json")[0]
        json_data = load_json_file(json_path)
        size = image_total.GetSize()
        spacing = image_total.GetSpacing()
        orientation = json_data[0]["direction"]
        print(orientation)
        for point_data in json_data:
            # from T9 crop
            if "label" in point_data and catid2catname[point_data["label"]] == vertebrae_label_list[0]:
                print(point_data["X"] / spacing[0], point_data["Y"] / spacing[1], point_data["Z"] / spacing[2])
                if orientation != ['L', 'P', 'S']:
                    raise ValueError("orientation != ['L', 'P', 'S'], please check {}".format(json_path))
                else:
                    crop_z = point_data["Z"] / spacing[2]
                    image_bottom = image_total[:, :, :int(crop_z)]
                    mask_bottom = mask_total[:, :, :int(crop_z)]
                    basename_wo_ext = os.path.basename(need_to_crop_ct_path).split(".")[0]
                    print(join(os.path.dirname(need_to_crop_ct_path), basename_wo_ext + "bottom.nii.gz"))
                    print(join(os.path.dirname(need_to_crop_ct_path), basename_wo_ext + "bottom_seg.nii.gz"))
                    # save cropped image and mask
                    sitk.WriteImage(image_bottom, join(os.path.dirname(need_to_crop_ct_path), basename_wo_ext + "bottom.nii.gz"))
                    sitk.WriteImage(mask_bottom, join(os.path.dirname(need_to_crop_ct_path), basename_wo_ext + "bottom_seg.nii.gz"))
        if verbose:
            print("need_to_crop_ct_path: ", need_to_crop_ct_path)
            print("not_need_cat_name_list: ", not_need_cat_name_list)
            print("size: ", size)
            print("spacing: ", spacing)
            print("\n")


def crop_images_to_fixed_size(images_folder, 
                              cropped_images_folder, 
                              fixed_size=[128, 128, 128], 
                              choosed_veterbrae_label_list=["T9", "T10", "T11", "T12", "L1", "L2", "L3", "L4", "L5", "L6"]):
    """
    The function will be used to cropped images and sef masks.
    param: images_folder: The input folder
    param: cropped_images_folder: The cropped images save folder.
    param: fixed_size: The cropped image size.
    """




if __name__ == "__main__":
    crop_nii_according_vertebrae_label("data/verse2019",["T9", "T10", "T11", "T12", "L1", "L2", "L3", "L4", "L5", "L6"])
    # image = sitk.ReadImage("data/verse2019/sub-verse009/sub-verse009bottom.nii.gz")
    # mask = sitk.ReadImage("data/verse2019/sub-verse009/sub-verse009bottom_seg.nii.gz")
    # print(image.GetSize())
    # print(image.GetSpacing())
    # print(mask.GetSize())
    