'''
Description: this file used to generate drr dataset which not cut
version: 
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2024-01-23 20:07:20
LastEditors: ShuaiLei
LastEditTime: 2024-01-23 21:05:59
'''
import os
import cv2
import argparse
import numpy as np
from detection_tools.object_detection import run_object_detection, load_detection_result
from io_tools.file_management import join, load_config_file, create_folder, dotdict
from detection_tools.detection_result_json import coco_annotations
from segmentation_tools.gen_cut_segmentation_dataset import GenCutSegmentationDrrDataset


class GenNotCutSegmentationDrrDataset(GenCutSegmentationDrrDataset):
    def __init__(self, config):
        super(GenNotCutSegmentationDrrDataset, self).__init__(detection_result=None, 
                                                              init_dataset_json_path=None, 
                                                              init_drrs_path=None, 
                                                              init_masks_path=None, 
                                                              cut_dataset_json_path=None, 
                                                              cut_drrs_save_path=None, 
                                                              cut_masks_save_path=None, 
                                                              cut_parameter=None)
        self.root_path = config.dataset_parameter["root_path"]
        self.images_path = join(self.root_path, config.dataset_parameter["images_folder"])
        self.masks_path = join(self.root_path, config.dataset_parameter["masks_folder"])
        self.single_vertebrae_images_path = create_folder(join(self.root_path, config.dataset_parameter["single_vertebrae_images_folder"]))
        self.detection_result_path = join(self.root_path, config.dataset_parameter["detection_result_folder"])
        self.AP_expand_coefficient = config.dataset_parameter["AP_expand_coefficient"]
        self.LA_expand_coefficient = config.dataset_parameter["LA_expand_coefficient"]
        self.Minimum_width_relative_to_the_image = config.dataset_parameter["Minimum_width_relative_to_the_image"]
        self.Minimum_height_relative_to_the_image = config.dataset_parameter["Minimum_height_relative_to_the_image"]
        self.run_object_detection = config.object_detection_parameter["run_object_detection"]
        self.detection_envs_path = config.object_detection_parameter["envs_path"]
        self.detection_script_path = config.object_detection_parameter["detection_script_path"]
        self.detection_config_path = config.object_detection_parameter["config_path"]
        self.detection_result_bbox_json_path = join(self.detection_result_path, config.object_detection_parameter["bbox_json_file"])
        self.detection_result = self.object_detection()
        self.detection_predict = coco_annotations(self.detection_result)


    def object_detection(self):
        if not os.path.exists(self.detection_result_bbox_json_path):
            run_object_detection(self.config)
        detection_result = load_detection_result(join(self.detection_result_bbox_json_path))
        return detection_result


    def create_not_cut_drrs_datset(self):
        imgToAnns = self.detection_predict.imgToAnns
        for image_id, anns in imgToAnns.items():
            self.image_out_bbox_set_zero(anns)


    def image_out_bbox_set_zero(self, anns):
        image_path = join(self.object_detection_parameter["infer_dir"], anns[0]["file_name"])
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        width, height = image.shape
        copy_image = np.zeros((width, height), dtype=np.uint8)
        for ann in anns:
            bbox = ann["bbox"]
            cat_name = ann["category_name"]
            single_vertebrae_image_name = self.get_single_vertebrae_image_name(ann["file_name"], cat_name)
            APorLA = self.get_APorLA(ann["file_name"])
            expand_bbox_coordinate = self.get_expand_bbox_coordinate(APorLA, width, height, bbox)


    def get_APorLA(self, file_name):
        if "AP" in file_name:
            return "AP"
        if "LA" in file_name:
            return "LA"


    def get_expand_bbox_coordinate(self, APorLA, width, height, bbox):
        # 扩大了适当倍 侧位设置为1.3,正位为1.9倍
        if APorLA == "LA":
            cut_bbox_coordinate = self.get_expand_bbox(bbox, width, height, 1.3)
        if APorLA == "AP":
            cut_bbox_coordinate = self.get_expand_bbox(bbox, width, height, 1.9)
        return cut_bbox_coordinate


def parse_args():
    parser = argparse.ArgumentParser(description="these py file will be used to gen drrs and masks")
    parser.add_argument("-c", "--config", default="config/not_cut_segmentation_config.yml", help="Path to the YAML configuration file")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    config_parmater = load_config_file(args.config)

    # Accessing values from the YAML file
    config = dotdict(dataset_parameter = config_parmater["dataset_parameter"],
                     object_detection_parameter = config_parmater["object_detection_parameter"])
    dataset = GenNotCutSegmentationDrrDataset(config)
    dataset.create_not_cut_drrs_datset()
    
if __name__ == "__main__":
    main()