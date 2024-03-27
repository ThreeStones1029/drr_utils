'''
Descripttion: this file will be used to gen pecidle.nii.gz
version: 
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-12-05 16:24:26
LastEditors: ShuaiLei
LastEditTime: 2024-03-27 05:43:39
'''
import os
import glob
import sys
sys.path.insert(0, sys.path.append(os.path.dirname(sys.path[0])))
from io_tools.file_management import get_sub_folder_paths, join, get_subfiles, load_json_file
import nibabel as nib
import SimpleITK as sitk
import numpy as np
from tqdm import tqdm
from PIL import Image
from collections import defaultdict


class GenPedicles:
    def __init__(self):
        self.catnames = []

    def load_nii(self, nii_path):
        if os.path.exists(nii_path):
            data = nib.load(nii_path)
            return data
        else:
            print("please check ", os.path.basename(nii_path), " in ", os.path.abspath(join(nii_path, "..")))
    
    def save_nii(self, data, save_path):
        nib.save(data, save_path)
        print("data successfully save in ", save_path)

    def get_catname_list(self, vertebraes_path):
        files_path = glob.glob(join(vertebraes_path, "*seg.nii.gz"))
        for file_path in files_path:
            filename = os.path.basename(file_path)
            catname = filename.split("_")[0]
            if catname not in self.catnames:
                self.catnames.append(catname)

    def gen_pedicle(self, vertebrae_path, vertebrae_catname):
        """
        vertebrae_path: 单个椎体路径
        vertebrae_catname:椎体类别名
        """
        vertebrae = self.load_nii(join(vertebrae_path, vertebrae_catname + "_all_seg.nii.gz"))
        body = self.load_nii(join(vertebrae_path, vertebrae_catname + "_body_seg.nii.gz"))
        other = self.load_nii(join(vertebrae_path, vertebrae_catname + "_other_seg.nii.gz"))
        vertebrae_data = vertebrae.get_fdata()
        body_data = body.get_fdata()
        other_data = other.get_fdata()
        # 椎弓根 = 整体 - body - other
        pedicle_data = vertebrae_data - body_data - other_data
        # 用nii保存,同时需要拷贝原来的坐标系位置
        pedicle = nib.Nifti1Image(pedicle_data, affine=vertebrae.header.get_best_affine())
        self.save_nii(pedicle, join(vertebrae_path, vertebrae_catname + "_pedicle_seg.nii.gz"))

    def gen_pedicles(self, vertebraes_path):
        """
        vertebraes_path: 多个椎体路径
        """
        self.get_catname_list(vertebraes_path)
        print(self.catnames)
        for catname in self.catnames:
            self.gen_pedicle(vertebraes_path, catname)


class NiiTools:
    def __init__(self, ct_mask_path):
        self.ct_mask_path = ct_mask_path


    def extract_largest_volume_objects(self):
        sub_folder_paths = get_sub_folder_paths(self.ct_mask_path)
        for sub_folder_path in tqdm(sub_folder_paths, desc=f"Total progress ct mast Processing"):
            nii_paths = glob.glob(join(sub_folder_path, "*seg.nii.gz"))
            for nii_path in tqdm(nii_paths, desc=f"{sub_folder_path} Processing"):
                filename = os.path.basename(nii_path)
                if "pedicle" in filename:
                    self.extract_largest_volume_object(nii_path, num_objects_to_keep=2)
                else:
                    self.extract_largest_volume_object(nii_path, num_objects_to_keep=1)


    def extract_largest_volume_object(self, nii_path, num_objects_to_keep=2):
        """
        nii_path: 读取的nii文件
        num_objects_to_keep: 每一个nii文件中需要保留下的object个数,对于除了椎弓根外的nii文件都只保留其中最大的物体,而椎弓根因为有两部分,保留前两个最大的物体
        """
        # 读取NIfTI文件
        image = sitk.ReadImage(nii_path)

        # 使用连通区域分析提取物体
        labeled_image = sitk.ConnectedComponent(image)
        label_statistics = sitk.LabelShapeStatisticsImageFilter()
        label_statistics.Execute(labeled_image)

        # 获取所有标签及其体积
        labels = label_statistics.GetLabels()
        volumes = [label_statistics.GetPhysicalSize(label) for label in labels]

        # 找到前num_objects_to_keep个最大体积的物体标签
        max_volume_indices = np.argsort(volumes)[-num_objects_to_keep:]
        objects_to_keep_labels = [labels[i] for i in max_volume_indices]

        # 创建一个二进制掩模，只保留最大体积一个或者两个物体
        if num_objects_to_keep == 1:
            largest_volume_object_mask = labeled_image == objects_to_keep_labels[0]
        if num_objects_to_keep == 2:
            largest_volume_object_mask1 = labeled_image == objects_to_keep_labels[0]
            largest_volume_object_mask2 = labeled_image == objects_to_keep_labels[1]
            largest_volume_object_mask = largest_volume_object_mask1 + largest_volume_object_mask2

        # 应用掩模并保存结果
        result_image = sitk.Mask(image, largest_volume_object_mask)

        # 保存结果
        sitk.WriteImage(result_image, nii_path)


def crop_nii(nii_path):
    """
    param nii_path .nii.gz file path list
    """
    basename = os.path.basename(nii_path)
    basename_wo_ext = basename[:basename.find('.nii.gz')] 
    file_path = os.path.dirname(nii_path) # 获取当前文件所在的目录路径
    image_total = sitk.ReadImage(nii_path)
    size = image_total.GetSize()
    
    image_top = image_total[:, :, int(0.5 * size[2]):]
    image_bottom = image_total[:, :, :int(0.5 * size[2])]
    sitk.WriteImage(image_top, join(file_path, basename_wo_ext + "_top.nii.gz"))
    sitk.WriteImage(image_bottom, join(file_path, basename_wo_ext + "_bottom.nii.gz"))


def nii2png(nii_path, png_path):
    nii = nib.load(nii_path)
    data = nii.get_fdata()
    # data = np.rot90(data)
    min_val, max_val = data.min(), data.max()
    data = 255 * (data - min_val) / (max_val - min_val)
    data = data.astype(np.uint8)
    img = Image.fromarray(data)
    img = img.rotate(-90, expand=True)
    img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    img.save(png_path)


def png2nii(png_path, nii_path):
    img = Image.open(png_path)
    img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    img = img.rotate(-90, expand=True)
    data = np.array(img)
    data_3d = np.zeros((data.shape[0], data.shape[1], 1), dtype=np.uint8)
    data_3d[:, :, 0] = data
    nii_img = nib.Nifti1Image(data_3d, affine=np.eye(4))
    nib.save(nii_img, nii_path)


def niis2pngs(nii_folder, png_folder):
    for file_name in os.listdir(nii_folder):
        if file_name.endswith(".nii.gz"):
            basename_no_ext = file_name.split(".")[0]
            png_file_name = basename_no_ext + ".png"
            nii2png(join(nii_folder, file_name), join(png_folder, png_file_name))


def pngs2niis(png_folder, nii_folder):
    for file_name in os.listdir(png_folder):
        if file_name.endswith(".png"):
            basename_no_ext = file_name.split(".")[0]
            nii_file_name = basename_no_ext + ".nii.gz"
            png2nii(join(png_folder, file_name), join(nii_folder, nii_file_name))


def crop_nii_according_vertebrae_label(input_folder, output_folder, vertebrae_label_list, verbose=True):
    """
    The function will be used to crop nii file.
    param: input_folder: The ct dataset input root folder.
    param: output_folder: The cropped ct dataset output root folder.
    param: vertebrae_label_list: The vertebrae label in ct after cropped. 
    """
    catid2catname = {1: "C1", 2: "C2", 3: "C3", 4: "C4", 5: "C5", 6: "C6", 7: "C7",
                     8: "T1", 9: "T2", 10: "T3", 11: "T4", 12: "T5", 13: "T6", 14: "T7", 15: "T8", 16: "T9", 17: "T10", 18: "T11", 19: "T12",
                     20: "L1", 21: "L2", 22: "L3", 23: "L4", 24: "L5", 25: "L6",
                     26: "sacrum", 27: "cocygis", 28: "T13"}
    sub_folder_paths = get_sub_folder_paths(input_folder)
    need_to_crop_ct_path_dict = defaultdict(list)
    for sub_folder_path in sub_folder_paths:
        json_files = get_subfiles(sub_folder_path, ".json")
        ct_name = os.path.basename(sub_folder_path)
        vertebrae_center_label_data = load_json_file(json_files[0])
        for point_data in vertebrae_center_label_data:
            if "label" in point_data and catid2catname[point_data["label"]] not in vertebrae_label_list:
                need_to_crop_ct_path_dict[join(sub_folder_path, ct_name + ".nii.gz")].append(catid2catname[point_data["label"]])

    for need_to_crop_ct_path, not_need_cat_name_list in need_to_crop_ct_path_dict.items():
        # file_path = os.path.dirname(need_to_crop_ct_path ) # 获取当前文件所在的目录路径
        image_total = sitk.ReadImage(need_to_crop_ct_path)
        if verbose:
            print("need_to_crop_ct_path: ", need_to_crop_ct_path)
            print("not_need_cat_name_list: ", not_need_cat_name_list)
            print("size: ", image_total.GetSize())
            print("spacing: ", image_total.GetSpacing())
            print("\n")


    
if __name__ == "__main__":
    # nii_tools = NiiTools("data/ct_mask_test")
    # nii_tools.extract_largest_volume_objects()
    # nii2png("nii_tools/weng_gt_drr.nii.gz", "nii_tools/weng_gt_drr.png")
    crop_nii_according_vertebrae_label("data/verse2019", "data/verse2019", ["T9", "T10", "T11", "T12", "L1", "L2", "L3", "L4", "L5", "L6"])
