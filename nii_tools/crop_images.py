'''
Description: The file will be used to crop nii and seg mask files.
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-03-28 07:36:18
LastEditors: ShuaiLei
LastEditTime: 2024-06-17 11:25:18
'''
import os
import sys
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from io_tools.file_management import get_sub_folder_paths, join, get_subfiles, load_json_file, save_json_file
import SimpleITK as sitk
import itk
import numpy as np
from collections import defaultdict
from nii_tools.verse_separate_mask import VerseCategoriesFormat
from nii_tools.reoriented_images import reorient_to_rai


def crop_nii_according_vertebrae_label(input_folder, vertebrae_label_list, verbose=True, is_crop_pelvis=True):
    """
    The function will be used to crop nii file.
    param: input_folder: The ct dataset input root folder.
    param: output_folder: The cropped ct dataset output root folder.
    param: vertebrae_label_list: The vertebrae label in ct after cropped. 
    """
    catid2catname = VerseCategoriesFormat().get_catid2catname()
    sub_folder_paths = get_sub_folder_paths(input_folder)
    need_to_crop_ct_path_dict = defaultdict(list)
    # 获得需要裁剪的CT列表
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
        print("orientation:", orientation)
        # 找到裁剪的上下坐标位置
        crop_top_z = 0
        crop_bottom_z = 0
        for point_data in json_data:
            # from T9 crop 
            if "label" in point_data and catid2catname[point_data["label"]] == vertebrae_label_list[0]:
                crop_top_z = int(point_data["Z"] / 1)
                print("X=",point_data["X"] / spacing[1], "Y=" , point_data["Y"] / spacing[2], "Z=",  point_data["Z"] / spacing[0])
        # from pelvis crop 如果L5或者L6存在，且还存在很长的骨盆，则根据是否选择裁剪骨盆裁剪
        if catid2catname[json_data[-1]["label"]] == "L5" or catid2catname[json_data[-1]["label"]] == "L6":
            if json_data[-1]["Z"] / (json_data[-2]["Z"] - json_data[-1]["Z"]) > 2:
                crop_bottom_z = int(json_data[-1]["Z"] - (json_data[-2]["Z"] - json_data[-1]["Z"]) * 2) 
                crop_bottom_z = crop_bottom_z if crop_bottom_z > 0 else 0
            
        if not is_crop_pelvis:
            crop_bottom_z = 0
        else:
            # 如果裁剪了骨盆则需要修改中心点坐标，因为重定向后坐标会被修改
            modify_points_center_json(json_data, crop_bottom_z, vertebrae_label_list, catid2catname, json_path)
                
        if orientation != ['L', 'P', 'S']:
            raise ValueError("orientation != ['L', 'P', 'S'], please check {}".format(json_path))
        else:
            image_bottom = image_total[:, :, crop_bottom_z:crop_top_z]
            mask_bottom = mask_total[:, :, crop_bottom_z:crop_top_z]
            basename_wo_ext = os.path.basename(need_to_crop_ct_path).split(".")[0]
            bottom_image_path = join(os.path.dirname(need_to_crop_ct_path), basename_wo_ext + "bottom.nii.gz")
            bottom_mask_path = join(os.path.dirname(need_to_crop_ct_path), basename_wo_ext + "bottom_seg.nii.gz")
            print(bottom_image_path, "save successfully!")
            print(bottom_mask_path, "save successfully!")
            # save cropped image and mask
            sitk.WriteImage(image_bottom, bottom_image_path)
            sitk.WriteImage(mask_bottom, bottom_mask_path)
            # if is_crop_pelvis 如果裁剪了骨盆，需要重新定向，让CT还在坐标原点
            if is_crop_pelvis:
                reorient_to_origin(bottom_image_path)
                reorient_to_origin(bottom_mask_path)
                
        if verbose:
            print("need_to_crop_ct_path: ", need_to_crop_ct_path)
            print("not_need_cat_name_list: ", not_need_cat_name_list)
            print("size: ", size)
            print("spacing: ", spacing)
            print("\n")


def modify_points_center_json(json_data, crop_bottom_z, vertebrae_label_list, catid2catname, json_path):
    """
    这个文件用来裁剪骨盆后用于重新修改json_data坐标
    """
    bottom_json_data = [json_data[0]]
    for point_data in json_data:
        if "label" in point_data and catid2catname[point_data["label"]] in vertebrae_label_list:
            point_data["Z"] -= crop_bottom_z
            bottom_json_data.append(point_data)
    basename_wo_ext = os.path.basename(json_path).split(".")[0] + "bottom.json"
    bottom_json_path = join(os.path.dirname(json_path), basename_wo_ext)
    save_json_file(bottom_json_data, bottom_json_path)


def reorient_to_origin(image_path):
    """
    裁剪了骨盆就需要重新定向到原点
    """
    ImageType = itk.Image[itk.SS, 3] 
    reader = itk.ImageFileReader[ImageType].New()
    reader.SetFileName(image_path)
    image = reader.GetOutput() 
    reoriented = reorient_to_rai(image)
    reoriented.SetOrigin([0, 0, 0])
    m = itk.GetMatrixFromArray(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], np.float64))
    reoriented.SetDirection(m)
    reoriented.Update()
    itk.imwrite(reoriented, image_path)


if __name__ == "__main__":
    crop_nii_according_vertebrae_label("data/verse2020_fracture",["T9", "T10", "T11", "T12", "L1", "L2", "L3", "L4", "L5", "L6"], is_crop_pelvis=True)
    # image = sitk.ReadImage("data/verse2019/sub-verse009bottom/sub-verse009bottom.nii.gz")
    # mask = sitk.ReadImage("data/verse2019/sub-verse009bottom/L1_seg.nii.gz")
    # print(image.GetSize())
    # print(image.GetSpacing())
    # print(mask.GetSize())
    