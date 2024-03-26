'''
Description: 本文件用于可视化分割mask,包括可视化到整张drr上
version: 
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-12-30 16:14:49
LastEditors: ShuaiLei
LastEditTime: 2024-01-02 19:02:49
'''
import os
from io_tools.file_management import load_json_file, join, add_whole_in_file_suffix
from visual_tools.color import Color
from collections import defaultdict
import cv2
import numpy as np
import multiprocessing
from tqdm import tqdm


class VisMask:
    def __init__(self, dataset_file):
        self.Imageid2Image = defaultdict(list)
        self.Imageid2CutMasks = defaultdict(list)
        self.Imageid2CutImage = defaultdict(list)
        self.CutImageid2CutImage = defaultdict(list)
        
        if type(dataset_file) is str:
            self.dataset = load_json_file(dataset_file)
        else:
            print("please check if " , dataset_file, " is path")
        self.createIndex()


    def createIndex(self):
        for image_info in self.dataset["images"]:
            self.Imageid2Image[image_info["id"]].append(image_info)
        for cut_image_info in self.dataset["cut_images"]:
            self.CutImageid2CutImage[cut_image_info["id"]].append(cut_image_info)
            self.Imageid2CutImage[cut_image_info["image_id"]].append(cut_image_info)
        if len(self.dataset["cut_masks"]) == 0:
            self.create_cut_masks()
        for cut_mask_info in self.dataset["cut_masks"]:
            self.Imageid2CutMasks[cut_mask_info["image_id"]].append(cut_mask_info)
    

    def create_cut_masks(self):
        cut_masks = []
        cut_mask_id = 0
        for cut_image_info in self.dataset["cut_images"]:
            cut_mask_id += 1
            cut_mask_file_name = add_whole_in_file_suffix(cut_image_info["file_name"])
            cut_masks.append({"file_name": cut_mask_file_name,
                              "id": cut_mask_id,
                              "image_id": cut_image_info["image_id"],
                              "cut_image_id": cut_image_info["id"],
                              "width": cut_image_info["width"],
                              "height": cut_image_info["height"],
                              "cut_bbox_coordinate": cut_image_info["cut_bbox_coordinate"],
                              "vertebrae_category_name": cut_image_info["vertebrae_category_name"],
                              "mask_category_name": "whole"})
        self.dataset["cut_masks"] = cut_masks
        

    def get_vertebrae_name2cut_masks(self, image_id):
        Vertebraename2CutMasks = defaultdict(list)
        for cut_mask_info in self.Imageid2CutMasks[image_id]:
            Vertebraename2CutMasks[cut_mask_info["vertebrae_category_name"]].append(cut_mask_info)
        return Vertebraename2CutMasks
    

    def visual_cut_masks_in_images(self, images_path, cut_masks_path, vis_save_path):
        """
        多个mask可视化到多张drr上
        """
        color_map = Color()
        with multiprocessing.Pool(8) as pool:
            list(tqdm(pool.imap(self.visual_cut_masks_in_image, [(image_id, images_path, cut_masks_path, vis_save_path, color_map) for image_id in self.Imageid2CutImage.keys()]), total=len(self.Imageid2CutImage.keys()), desc="vis masks"))


    def visual_cut_masks_in_image(self, args):
        """
        多个mask可视化到单张整体drr图片上
        """
        image_id, images_path, cut_masks_path, vis_save_path, color_map = args
        Vertebraename2CutMasks = self.get_vertebrae_name2cut_masks(image_id)
        overall_masks_list = []
        vis_img_name = self.Imageid2Image[image_id][0]["file_name"]
        image = cv2.imread(join(images_path, vis_img_name))
        masks_image = np.zeros_like(image, dtype=np.uint8)
        image_shape = image.shape
        for cat_name, cut_masks_info in Vertebraename2CutMasks.items():
            if len(cut_masks_info) == 1:
                single_mask = np.zeros(image_shape, dtype=np.uint8)
                cut_mask = cv2.imread(join(cut_masks_path, cut_masks_info[0]["file_name"]), cv2.IMREAD_GRAYSCALE)
                cat_id = color_map.catname2catid(cat_name)
                color = color_map.catid2rgb(cat_id)
                cut_bbox_coordinate = cut_masks_info[0]["cut_bbox_coordinate"]
                cut_image_region = single_mask[cut_bbox_coordinate[1]: cut_bbox_coordinate[3], cut_bbox_coordinate[0]: cut_bbox_coordinate[2]]
                cut_image_region[cut_mask > 0] = color
                overall_masks_list.append(single_mask)
            else:
                color_list = [[0, 255, 0], [0, 0, 255], [255, 0, 0]]
                for i in range(len(cut_masks_info)):
                    single_mask = np.zeros(image_shape, dtype=np.uint8)
                    cut_mask = cv2.imread(join(cut_masks_path, cut_masks_info[i]["file_name"]), cv2.IMREAD_GRAYSCALE)
                    if cut_masks_info[i]["mask_category_name"] == "body":
                        color = color_list[0]
                    if cut_masks_info[i]["mask_category_name"] == "pedicle":
                        color = color_list[1]
                    if cut_masks_info[i]["mask_category_name"] == "other":
                        color = color_list[2]
                    cut_bbox_coordinate = cut_masks_info[i]["cut_bbox_coordinate"]
                    cut_image_region = single_mask[cut_bbox_coordinate[1]: cut_bbox_coordinate[3], cut_bbox_coordinate[0]: cut_bbox_coordinate[2]]
                    cut_image_region[cut_mask > 0] = color
                    overall_masks_list.append(single_mask)

        for single_mask in overall_masks_list:
            masks_image = cv2.bitwise_or(masks_image, single_mask)
        # print("vis", join(images_path, vis_img_name), "successfully")
        final_image = cv2.add(image, masks_image)
        cv2.imwrite(join(vis_save_path, vis_img_name), final_image)

        
    def visual_cut_masks_in_cut_images(self, cut_images_path, cut_masks_path, vis_save_path):
        """
        多个masks可视化到多个裁剪的drr上
        """
        # multiprocessing.Pool(8) 创建8个进程，提高代码处理效率
        with multiprocessing.Pool(8) as pool:
            list(tqdm(pool.imap(self.visual_cut_masks_in_cut_image, [(image_id, cut_images_path, cut_masks_path, vis_save_path) for image_id in self.Imageid2CutImage.keys()]), total=len(self.Imageid2CutImage.keys()), desc="vis cut masks"))


    def visual_cut_masks_in_cut_image(self, args):
        """
        多个masks可视化到单个裁剪drr上
        """
        image_id, cut_images_path, cut_masks_path, vis_save_path = args
        Vertebraename2CutMasks = self.get_vertebrae_name2cut_masks(image_id)
        for cat_name, cut_masks in Vertebraename2CutMasks.items():
            # self.visual_cut_masks_in_cut_image(cut_masks, cut_images_path, cut_masks_path, vis_save_path)
            cut_image_id = cut_masks[0]["cut_image_id"]
            vis_img_name = self.CutImageid2CutImage[cut_image_id][0]["file_name"]
            cut_image = cv2.imread(join(cut_images_path, vis_img_name))
            merge_img = np.copy(cut_image)
            color_list = [[0, 255, 0], [0, 0, 255], [255, 0, 0]]

            for i in range(len(cut_masks)):
                mask = cv2.imread(join(cut_masks_path, cut_masks[i]["file_name"]), cv2.IMREAD_GRAYSCALE)
                if cut_masks[i]["mask_category_name"] == "body":
                    color = color_list[0]
                if cut_masks[i]["mask_category_name"] == "pedicle":
                    color = color_list[1]
                if cut_masks[i]["mask_category_name"] == "other":
                    color = color_list[2]
                if cut_masks[i]["mask_category_name"] == "whole":
                    color = color_list[0]
                merge_img[mask > 0] = color
            
            # print("vis", join(cut_images_path, vis_img_name), "successfully")
            cv2.imwrite(join(vis_save_path, vis_img_name), merge_img)


if __name__ == "__main__":
    vismask = VisMask("data/segmentation_dataset_test/LA/LA_cut_dataset.json")
    vismask.visual_cut_masks_in_cut_images(cut_images_path = "data/segmentation_dataset_test/LA/cut_images", 
                                           cut_masks_path = "data/segmentation_dataset_test/LA/cut_masks", 
                                           vis_save_path = "data/segmentation_dataset_test/LA/vis")
    
    vismask.visual_cut_masks_in_images(images_path = "data/segmentation_dataset_test/LA/images", 
                                       cut_masks_path = "data/segmentation_dataset_test/LA/cut_masks", 
                                       vis_save_path = "data/segmentation_dataset_test/LA/vis_overall")