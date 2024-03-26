'''
Description: 用于保存裁剪后的信息文件方便保留裁剪信息,好可视化
version: 
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-12-29 21:58:13
LastEditors: ShuaiLei
LastEditTime: 2023-12-31 18:37:52
'''
from io_tools.file_management import save_json_file
from datetime import datetime


class CutSegmentationDatasetJson:
    def __init__(self, cut_dataset_json_path):
        self.cut_dataset_json_path = cut_dataset_json_path
        self.info = dict()
        self.images = []
        self.cut_images = []
        self.cut_masks = []
        self.cut_images_num = 0
        self.cut_masks_num = 0
        self.images_num = 0
        self.add_info()

    def add_info(self):
        self.info = {"description": "cut drrs and masks dataset",
                     "version": "1.0",
                     "Author": "ThreeStones1029",
                     "Date": datetime.today().strftime('%Y-%m-%d')}
        
    def add_image(self, image_name, width, height):
        # 添加没有裁剪的图片信息
        self.images_num += 1
        image_info = {"file_name":image_name,
                      "id": self.images_num,
                      "width": width,
                      "height": height}
        self.images.append(image_info)


    def add_cut_image(self, cut_image_name, cut_bbox_coordinate, vertebrae_category_name):
        # 添加裁剪后的图片信息
        self.cut_images_num += 1
        cut_image_info = {"file_name": cut_image_name,
                          "id": self.cut_images_num,
                          "image_id": self.images_num,
                          "width": cut_bbox_coordinate[2] - cut_bbox_coordinate[0],
                          "height": cut_bbox_coordinate[3] - cut_bbox_coordinate[1],
                          "cut_bbox_coordinate": cut_bbox_coordinate,
                          "vertebrae_category_name": vertebrae_category_name
                          }
        self.cut_images.append(cut_image_info)


    def add_cut_mask(self, cut_mask_name, cut_bbox_coordinate, vertebrae_category_name, mask_category_name):
        # 添加裁剪厚的mask信息
        self.cut_masks_num += 1
        cut_mask_info = {"file_name": cut_mask_name,
                         "id": self.cut_masks_num,
                         "image_id": self.images_num,
                         "cut_image_id": self.cut_images_num,
                         "width": cut_bbox_coordinate[2] - cut_bbox_coordinate[0],
                         "height": cut_bbox_coordinate[3] - cut_bbox_coordinate[1],
                         "cut_bbox_coordinate": cut_bbox_coordinate,
                         "vertebrae_category_name": vertebrae_category_name,
                         "mask_category_name": mask_category_name}
        self.cut_masks.append(cut_mask_info)


    def to_json(self):
        self.dataset = {"info": self.info,
                        "images": self.images,
                        "cut_images": self.cut_images,
                        "cut_masks": self.cut_masks}
        save_json_file(self.dataset, self.cut_dataset_json_path)