'''
Descripttion: this file will be used to gen cut segmentation dataset
version: 
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-12-08 20:24:16
LastEditors: ShuaiLei
LastEditTime: 2024-01-15 15:24:24
'''
from segmentation_tools.init_segmentation_json import InitSegmentationDatasetJsonTools
from segmentation_tools.cut_segmentation_json import CutSegmentationDatasetJson
from detection_tools.detection_result_json import coco_annotations
from drr_tools.drr_image_postprocess import compute_min_bbox_coverage_mask
from io_tools.file_management import join
import numpy as np
import cv2
import os
from tqdm import tqdm


class GenCutSegmentationDrrDataset:
    def __init__(self,
                 detection_result=None, 
                 init_dataset_json_path=None, 
                 init_drrs_path=None, 
                 init_masks_path=None, 
                 cut_dataset_json_path=None, 
                 cut_drrs_save_path=None, 
                 cut_masks_save_path=None, 
                 cut_parameter=None):
        """
        self.detection_result: 检测结果
        self.init_dataset_json_path: 初始数据集json文件
        self.init_drrs_path: 初始数据集drrs文件夹
        self.init_masks_path: 初始数据集masks文件夹
        self.cut_dataset_json_path: 裁剪数据集json文件
        self.cut_drrs_save_path: 裁剪数据集drrs文件夹
        self.cut_masks_save_path: 裁剪数据集masks文件夹
        self.cut_parameter: 裁剪参数
        """
        self.detection_result = detection_result
        self.detection_predict = coco_annotations(self.detection_result)
        self.init_dataset_json_path = init_dataset_json_path
        self.init_drrs_path = init_drrs_path
        self.init_masks_path = init_masks_path
        self.cut_dataset_json_path = cut_dataset_json_path
        self.cut_drrs_save_path = cut_drrs_save_path
        self.cut_masks_save_path = cut_masks_save_path
        self.cut_parameter = cut_parameter
        self.drr_cut_segmentation_dataset = CutSegmentationDatasetJson(self.cut_dataset_json_path)
        

    def cut_drrs_and_masks(self):
        '''
        description: detection bbox center cut or mask cut
        mutil process to be realized
        '''
        dataset_json_tools = InitSegmentationDatasetJsonTools(self.init_dataset_json_path)
        for image_id in tqdm(dataset_json_tools.Imageid2Masks.keys(), desc="cuting"):
            Vertebraename2Masks = dataset_json_tools.get_vertebrae_name2masks(image_id)
            drr_image_info = dataset_json_tools.Imageid2Image[image_id][0]
            drr_image_name = drr_image_info["image_name"]
            # 读取drr
            drr_image = cv2.imread(join(self.init_drrs_path, drr_image_name))
            # 添加原图信息
            # print(drr_image_name)
            self.drr_cut_segmentation_dataset.add_image(drr_image_name, drr_image_info["width"], drr_image_info["height"])
            for cat_name, mask_info in Vertebraename2Masks.items():
                # 得到需要裁剪的bbox最小最大坐标
                bbox = self.get_bbox(drr_image_name, mask_info)
                cut_bbox_coordinate = self.get_cut_bbox_coordinate(mask_info, bbox)
                width, height = mask_info[0]["width"], mask_info[0]["height"]
                min_cut_bbox_width, min_cut_bbox_height = self.get_min_cut_bbox_width_height(width, height)
                cut_bbox_in_edge = self.is_edge_cut_bbox(cut_bbox_coordinate, width, height)
                if cut_bbox_in_edge:
                    if cut_bbox_coordinate[2] - cut_bbox_coordinate[0] >= min_cut_bbox_width and cut_bbox_coordinate[3] - cut_bbox_coordinate[1] >= min_cut_bbox_height:
                        # 边缘的bbox判断是否大于指定的大小
                        # 裁剪drr
                        self.cut_drr(drr_image, drr_image_name, cat_name, cut_bbox_coordinate)
                        # 裁剪mask
                        self.cut_masks(mask_info, cat_name, cut_bbox_coordinate)
                else:
                    # 裁剪drr
                    self.cut_drr(drr_image, drr_image_name, cat_name, cut_bbox_coordinate)
                    # 裁剪mask
                    self.cut_masks(mask_info, cat_name, cut_bbox_coordinate)
        self.drr_cut_segmentation_dataset.to_json()


    def cut_drrs(self):
        """
        no masks to cut
        """
        for image_id, anns in tqdm(self.detection_predict.imgToAnns.items(), desc="cuting"):
            drr_image_name = anns[0]["file_name"]
            # 读取drr
            drr_image = cv2.imread(join(self.init_drrs_path, drr_image_name))
            # 添加原图信息
            # print(drr_image_name)
            width, height =  drr_image.shape[0], drr_image.shape[1]
            self.drr_cut_segmentation_dataset.add_image(drr_image_name, width, height)
            for ann in anns:
                # 得到需要裁剪的bbox最小最大坐标
                bbox, cat_name = ann["bbox"], ann["category_name"]
                cut_bbox_coordinate = self.get_cut_bbox(bbox, width, height, 1.9)
                min_cut_bbox_width, min_cut_bbox_height = self.get_min_cut_bbox_width_height(width, height)
                cut_bbox_in_edge = self.is_edge_cut_bbox(cut_bbox_coordinate, width, height)
                if cut_bbox_in_edge:
                    if cut_bbox_coordinate[2] - cut_bbox_coordinate[0] >= min_cut_bbox_width and cut_bbox_coordinate[3] - cut_bbox_coordinate[1] >= min_cut_bbox_height:
                        # 边缘的bbox判断是否大于指定的大小
                        # 裁剪drr
                        self.cut_drr(drr_image, drr_image_name, cat_name, cut_bbox_coordinate)
                else:
                    # 裁剪drr
                    self.cut_drr(drr_image, drr_image_name, cat_name, cut_bbox_coordinate)
        self.drr_cut_segmentation_dataset.to_json()


    def get_bbox(self, drr_image_name, mask_info):
        if self.cut_parameter["cut_mode"] == "mask_center":
            bbox = self.mask_bbox(mask_info)
        if self.cut_parameter["cut_mode"] == "detection_bbox_center":
            bbox = self.detection_bbox(drr_image_name, mask_info)
        return bbox


    def mask_bbox(self, mask_info):
        # 根据mask求裁剪框
        all_mask = cv2.imread(join(self.init_masks_path, mask_info[0]["mask_name"]), cv2.IMREAD_GRAYSCALE)
        for i in range(1, len(mask_info)):
            mask = cv2.imread(join(self.init_masks_path, mask_info[i]["mask_name"]), cv2.IMREAD_GRAYSCALE)
            all_mask = all_mask + mask
        # 确保叠加后还是0, 255
        all_mask = np.clip(all_mask, 0, 255)
        bbox = compute_min_bbox_coverage_mask(image=all_mask)
        return bbox


    def detection_bbox(self, drr_image_name, mask_info):
        # 根据检测的预测结果框裁剪
        img_id = self.detection_predict.FilenameToimg_id[drr_image_name]
        predict_anns = self.detection_predict.imgToAnns[img_id]
        vertebrae_category_name2ann = self.detection_predict.cat_name2ann(predict_anns)
        vertebrae_category_name = mask_info[0]["vertebrae_category_name"]
        if vertebrae_category_name in vertebrae_category_name2ann.keys():
            bbox = vertebrae_category_name2ann[vertebrae_category_name][0]["bbox"]
        else:
            bbox = [0, 0, 0, 0]
        return bbox


    def get_cut_drr_image_name(self, drr_image_name, cat_name):
        if "_" in drr_image_name:
            separate_name_list = drr_image_name.split("_")
            cut_drr_image_name = ""
            for i in range(len(separate_name_list) - 1):
                if i == 0:
                    cut_drr_image_name = cut_drr_image_name + separate_name_list[i]
                else:
                    cut_drr_image_name = cut_drr_image_name + "_" + separate_name_list[i]
            cut_drr_image_name = cut_drr_image_name + "_" + cat_name + "_" + separate_name_list[-1]
        else:
            drr_image_name_no_ext = drr_image_name.split(".")[0]
            ext = "." + drr_image_name.split(".")[1]
            cut_drr_image_name = drr_image_name_no_ext + "_" + cat_name + ext
        return cut_drr_image_name


    def get_cut_bbox_coordinate(self, mask_info, bbox):
        # 扩大了适当倍 侧位设置为1.3,正位为1.9倍
        width, height = mask_info[0]["width"], mask_info[0]["height"]
        if mask_info[0]["AP_or_LA"] == "LA":
            cut_bbox_coordinate = self.get_cut_bbox(bbox, width, height, self.cut_parameter["LA_expand_coefficient"])
        if mask_info[0]["AP_or_LA"] == "AP":
            cut_bbox_coordinate = self.get_cut_bbox(bbox, width, height, self.cut_parameter["AP_expand_coefficient"])
        return cut_bbox_coordinate


    def get_cut_bbox(self, bbox, width, height, expand_coefficient):
        # 根据bbox计算最大最小坐标
        x, y, w, h = bbox
        center_x, center_y = x + w/2, y + h/2
        expand_w = expand_coefficient * w
        expand_h = expand_coefficient * h
        new_min_x = center_x - expand_w / 2 if center_x - expand_w / 2 > 0 else 0
        new_min_y = center_y - expand_h / 2 if center_y - expand_h / 2 > 0 else 0
        new_max_x = center_x + expand_w / 2 if center_x + expand_w / 2 < width else width
        new_max_y = center_y + expand_h / 2 if center_y + expand_h / 2 < height else height
        return [int(new_min_x), int(new_min_y), int(new_max_x), int(new_max_y)]
    

    def is_edge_cut_bbox(self, cut_bbox_coordinate, width, height):
        # 判断是否为边缘框
        if cut_bbox_coordinate[0] == 0 or cut_bbox_coordinate[1] == 0 or cut_bbox_coordinate[2] == width or cut_bbox_coordinate[3] == height:
            return True
        else:
            return False
    

    def get_min_cut_bbox_width_height(self, width, height):
        # 计算最小的bbox宽度和高度
        min_cut_bbox_width = self.cut_parameter["Minimum_width_relative_to_the_image"] * width
        min_cut_bbox_height = self.cut_parameter["Minimum_height_relative_to_the_image"] * height
        return min_cut_bbox_width, min_cut_bbox_height
    

    def cut_drr(self, drr_image, drr_image_name, cat_name, cut_bbox_coordinate):
        # 裁剪后的drr名字
        cut_drr_image_name = self.get_cut_drr_image_name(drr_image_name, cat_name)
        # 裁剪drr图像
        cut_drr_image = drr_image[cut_bbox_coordinate[1]: cut_bbox_coordinate[3], cut_bbox_coordinate[0]: cut_bbox_coordinate[2]]
        cv2.imwrite(join(self.cut_drrs_save_path, cut_drr_image_name), cut_drr_image)
        # 添加裁剪后的信息
        self.drr_cut_segmentation_dataset.add_cut_image(cut_drr_image_name, cut_bbox_coordinate, cat_name)
        # print("cut", join(self.cut_drrs_save_path, cut_drr_image_name), "save successfully")


    def cut_masks(self, mask_info, cat_name, cut_bbox_coordinate):
        for i in range(len(mask_info)):
            mask = cv2.imread(join(self.init_masks_path, mask_info[i]["mask_name"]), cv2.IMREAD_GRAYSCALE)
            cut_mask = mask[cut_bbox_coordinate[1]: cut_bbox_coordinate[3], cut_bbox_coordinate[0]: cut_bbox_coordinate[2]]
            cv2.imwrite(join(self.cut_masks_save_path, mask_info[i]["mask_name"]), cut_mask)
            self.drr_cut_segmentation_dataset.add_cut_mask(mask_info[i]["mask_name"], cut_bbox_coordinate, cat_name, mask_info[i]["mask_category_name"])
            # print("cut", join(self.cut_masks_save_path, mask_info[i]["mask_name"]), "save successfully")  


if __name__ == "__main":
    cut_dataset = GenCutSegmentationDrrDataset()