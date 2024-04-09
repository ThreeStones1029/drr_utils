'''
Description: 
version: 
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-12-07 21:28:15
LastEditors: ShuaiLei
LastEditTime: 2024-04-09 07:35:41
'''
import os
import sys
# sys.path.insert(0, os.path.dirname(sys.path[0]))
from io_tools.file_management import load_json_file, save_json_file
from datetime import datetime
from collections import defaultdict
import cv2
import numpy as np


class InitSegmentationDatasetJson:
    def __init__(self, projection_parameter, rotations_and_translations, init_dataset_json_path):
        '''
        description: 
        self.info 初始数据集基本信息
        self.images 初始数据集drr
        self.masks 初始数据集mask
        self.masks_categories 初始数据集类别
        self.cts 投影使用的ct信息
        self.images_num 记录drr数量
        self.masks_num 记录masks数量
        self.catname2catid mask类别名字到类别id映射
        self.catid2catname mask类别id到类别名字映射
        self.projection_parameter 投影参数
        self.rotations_and_translations 生成的随机角度与随机移动列表
        self.init_dataset_json_path 生成的json文件保存路径
        return {*}
        '''
        self.info = dict()
        self.images = []
        self.masks = []
        self.masks_categories = []
        self.cts = []
        self.cts_num = 0
        self.images_num = 0
        self.masks_num = 0
        self.exist_ct_nii_names = {"AP": [], "LA": []}
        self.catname2catid = dict()
        self.catid2catname = dict()
        self.projection_parameter = projection_parameter
        self.rotations_and_translations = rotations_and_translations
        self.init_dataset_json_path = init_dataset_json_path
        self.InitJson()


    def InitJson(self):
        """
        初始化json文件
        """
        self.add_info()
        self.add_masks_categories()


    def gen_init_dataset_json(self):
        """生成json文件"""
        segmentation_data = {
                            "info": self.info,
                            "images": self.images,
                            "masks": self.masks,
                            "masks_categories": self.masks_categories,
                            "cts": self.cts
                            }
        save_json_file(segmentation_data, self.init_dataset_json_path)


    def add_info(self):
        self.info["dataset_info"] = {"description": "drrs and masks dataset",
                                     "version": "1.0",
                                     "Author": "ThreeStones1029",
                                     "Date": datetime.today().strftime('%Y-%m-%d')}
        self.info["projection_parameter"] = self.projection_parameter
        self.info["rotations_and_translations"] = self.rotations_and_translations
        
    def add_image(self, image_name,ct_name, AP_or_LA, width, height, rotation, translation):
        image_info = {}
        self.images_num  = self.images_num + 1
        image_info["id"] = self.images_num
        image_info["image_name"] = image_name
        image_info["ct_id"] = self.cts_num
        image_info["ct_name"] = ct_name + ".nii.gz"
        image_info["AP_or_LA"] = AP_or_LA
        image_info["width"] = width
        image_info["height"] = height
        image_info["rotation"] = rotation
        image_info["translation"] = translation
        self.images.append(image_info)


    def add_mask(self, mask_name, AP_or_LA, width, height, rotation, translation):
        mask_info = {}
        self.masks_num = self.masks_num + 1
        mask_info["id"] = self.masks_num
        mask_info["mask_name"] = mask_name
        mask_info["image_id"] = self.images_num 
        basename = os.path.basename(mask_name)
        mask_category_name = basename.split("_")[-2]
        mask_info["mask_category_name"] = mask_category_name
        mask_info["mask_category_id"] = self.catname2catid[mask_category_name]
        mask_info["vertebrae_category_name"] = basename.split("_")[-3]
        mask_info["AP_or_LA"] = AP_or_LA
        mask_info["width"] = width
        mask_info["height"] = height
        mask_info["rotation"] = rotation
        mask_info["translation"] = translation
        self.masks.append(mask_info)


    def add_ct(self, ct_name, AP_or_LA):
        ct_info = {}
        self.cts_num = self.cts_num + 1
        ct_info["id"] = self.cts_num
        ct_info["ct_name"] = ct_name + ".nii.gz"
        ct_info["AP_or_LA"] = AP_or_LA
        ct_info["vertebrae_categoties"] = []
        self.cts.append(ct_info)


    def add_ct_vertebrae_categoties(self, mask_name):
        vertebrae_category_name = os.path.basename(mask_name).split("_")[-3]
        if vertebrae_category_name not in self.cts[self.cts_num - 1]["vertebrae_categoties"]:
            self.cts[self.cts_num - 1]["vertebrae_categoties"].append(vertebrae_category_name)

        
    def add_masks_categories(self):
        self.masks_categories = [
                                {"id": 1,
                                "name": "body",
                                "supercategory": "vertebrae"},
                                {"id": 2,
                                "name": "pedicle",
                                "supercategory": "vertebrae"},
                                {"id": 3,
                                "name": "other",
                                "supercategory": "vertebrae"},
                                {"id": 4,
                                 "name": "whole",
                                 "supercategory": "vertebrae"}
                                ]
        
        for category in self.masks_categories:
            self.catid2catname[category["id"]] = category["name"]
            self.catname2catid[category["name"]] = category["id"]
            

    def load_json(self, json_file):
        """
        加载json文件
        """
        data = load_json_file(json_file)
        self.info = data["info"]
        self.images = data["images"]
        self.masks = data["masks"]
        self.cts = data["cts"]
        self.masks_categories = data["masks_categories"]
        self.images_num = len(self.images)
        self.masks_num = len(self.masks)
        self.cts_num = len(self.cts)
        for ct_info in self.cts:
            if ct_info["AP_or_LA"] == "AP" and ct_info["ct_name"] not in self.exist_ct_nii_names["AP"]:
                self.exist_ct_nii_names["AP"].append(ct_info["ct_name"])
            if ct_info["AP_or_LA"] == "LA" and ct_info["ct_name"] not in self.exist_ct_nii_names["LA"]:
                self.exist_ct_nii_names["LA"].append(ct_info["ct_name"])
        


class InitSegmentationDatasetJsonTools:
    """
    初始json的工具类
    param dataset_file: 初始json文件
    """
    def __init__(self, dataset_file):
        self.Imageid2Masks = defaultdict(list)
        self.Imageid2Image = defaultdict(list)
        self.Ctid2Ct = defaultdict(list)
        if type(dataset_file) is str:
            self.dataset = load_json_file(dataset_file)
        else:
            print("please check if " , dataset_file, " is path")
        self.gen_Imageid2Image()
        self.gen_Imageid2Masks()
        self.gen_Ctname2Ct()

    
    def gen_Imageid2Image(self):
        for image in self.dataset["images"]:
            self.Imageid2Image[image["id"]].append(image)
        

    def gen_Imageid2Masks(self):
        """
        this function will be used to gen mapping which image id to masks
        """
        for mask in self.dataset["masks"]:
            self.Imageid2Masks[mask["image_id"]].append(mask)


    def gen_Ctname2Ct(self):
        """
        this function will be used to gen mapping which ct_name to ct
        """
        for ct in self.dataset["cts"]:
            self.Ctid2Ct[ct["id"]].append(ct)


    def get_vertebrae_name2masks(self, image_id):
        Vertebraename2Masks = defaultdict(list)
        for mask_info in self.Imageid2Masks[image_id]:
            Vertebraename2Masks[mask_info["vertebrae_category_name"]].append(mask_info)
        return Vertebraename2Masks


def merge_init_jsons(init_json_path1, init_json_path2, save_json_path):
    """
    合并正位侧位init_json文件
    param init_json_path1:初始json路径1
    param init_json_path2:初始json路径2
    param save_json_path: 合并后的json保存路径
    """
    init1_json = InitSegmentationDatasetJsonTools(init_json_path1)
    init2_json = InitSegmentationDatasetJsonTools(init_json_path2)
    init_dataset1 = init1_json.dataset
    init_dataset2 = init2_json.dataset
    merge_dataset = init_dataset1
    # 获取第一个json的字典值的长度
    images_num = len(init_dataset1["images"])
    masks_num = len(init_dataset1["masks"])
    cts_num = len(init_dataset1["cts"])
    # 混合ct信息
    for ct in init_dataset2["cts"]:
        cts_num += 1
        ct["id"] = cts_num
        merge_dataset["cts"].append(ct)

    # 得到正位以及侧位所用的ct名字与id的对应字典
    AP_exist_ct_name2ct_id = {}
    LA_exist_ct_name2ct_id = {}
    for ct in merge_dataset["cts"]:
        if ct["AP_or_LA"] == "AP":
            AP_exist_ct_name2ct_id[ct["ct_name"]] = ct["id"]
        if ct["AP_or_LA"] == "LA":
            LA_exist_ct_name2ct_id[ct["ct_name"]] = ct["id"]
    
    for image in init_dataset2["images"]:
        images_num += 1
        # 获取当前图片对应的masks
        masks = init2_json.Imageid2Masks[image["id"]]
        # 修改image的id
        image["id"] = images_num
        # 修改ct的id
        if image["AP_or_LA"] == "AP":
            image["ct_id"] = AP_exist_ct_name2ct_id[image["ct_name"]]
        if image["AP_or_LA"] == "LA":
            image["ct_id"] = LA_exist_ct_name2ct_id[image["ct_name"]]
        # 添加image
        merge_dataset["images"].append(image)
        # 添加mask
        for mask in masks:
            masks_num += 1
            mask["id"] = masks_num
            mask["image_id"] = images_num
            merge_dataset["masks"].append(mask)
    save_json_file(merge_dataset, save_json_path)


def extract_init_json(init_json_path, images_folder, save_json_path):
    """
    提取init_json_path中有关images_folder的对应的信息
    param init_json_path: 原始初始数据集json
    param image_folder: 选取的数据集image图片
    param save_json_path: 提取后的数据集json
    """
    images_file_name_list = os.listdir(images_folder)
    init_json = InitSegmentationDatasetJsonTools(init_json_path)
    init_dataset = init_json.dataset
    extract_dataset = {"info": init_dataset["info"],
                       "masks_categories": init_dataset["masks_categories"],
                       "images": [],
                       "masks": [],
                       "cts": []}
    exist_ct_ids = []
    for image in init_dataset["images"]:
        if image["image_name"] in images_file_name_list:
            extract_dataset["images"].append(image)
            if image["ct_id"] not in exist_ct_ids:
                exist_ct_ids.append(image["ct_id"])
                extract_dataset["cts"].append(init_json.Ctid2Ct[image["ct_id"]][0])
            masks = init_json.Imageid2Masks[image["id"]]
            for mask in masks:
                extract_dataset["masks"].append(mask)
    save_json_file(extract_dataset, save_json_path)


def modify_width_and_height_in_init_json(init_json_path, resize_w_h):
    """
    对于做了数据增强,resize后需要修改init_json
    param init_json_path: 初始数据集json
    """
    init_dataset = load_json_file(init_json_path)
    # 修改info
    init_dataset["info"]["projection_parameter"]["height"] = resize_w_h
    for ct_name_no_ext, height in init_dataset["info"]["projection_parameter"]["specific_height_list"].items():
        init_dataset["info"]["projection_parameter"]["specific_height_list"][ct_name_no_ext] = resize_w_h
    # 修改images
    for image in init_dataset["images"]:
        image["width"] = resize_w_h
        image["height"] = resize_w_h
    # 修改masks
    for mask in init_dataset["masks"]:
        mask["width"] = resize_w_h
        mask["height"] = resize_w_h
    save_json_file(init_dataset, init_json_path)


def check_init_json(init_json_path):
    """
    检查当前init_json文件
    """
    init_dataset = load_json_file(init_json_path)
    images_num = len(init_dataset["images"])
    masks_num = len(init_dataset["masks"])
    print("images_num:", images_num,"masks_num:", masks_num)


if __name__ == "__main__":
    # modify_width_and_height_in_init_json("data/segmentation_dataset/LA512/LA512_init_dataset.json", 512)
    # merge_init_jsons("data/segmentation_dataset/AP512/AP512_init_dataset.json", 
    #                  "data/segmentation_dataset/LA512/LA512_init_dataset.json", 
    #                  "data/segmentation_dataset/all512/all512_init_dataset.json")
    # extract_init_json("data/segmentation_dataset/all512/all512_init_dataset.json",
    #                   "data/segmentation_dataset/all512/images",
    #                   "data/segmentation_dataset/all512/all512_init_dataset.json")
    check_init_json("data/segmentation_dataset/all512/all512_init_dataset.json")
    