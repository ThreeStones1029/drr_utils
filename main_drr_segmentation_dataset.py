'''
Descripttion: this file will be used to generate cut drrs and masks.
version: 1.0
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-12-09 11:29:36
LastEditors: ShuaiLei
LastEditTime: 2024-04-09 02:31:51
'''
import os
import time
import argparse
import shutil
from nii_tools.nii_process import GenPedicles, NiiTools
from segmentation_tools.gen_init_segmentation_dataset import GenInitSegmentationDrrDataset
from segmentation_tools.gen_cut_segmentation_dataset import GenCutSegmentationDrrDataset
from visual_tools.vis_segmentation_mask import VisMask
from visual_tools.vis_coco_detection_bbox import VisCoCo
from io_tools.file_management import dotdict
from detection_tools.object_detection import run_object_detection, load_detection_result
from io_tools.file_management import create_folder, load_config_file, join


class SegmentationDrrDataset:
    def __init__(self, config):
        """
        params
        self.data_root_path: Root directory
        self.ct_mask_path: CT path
        self.dataset_save_root_folder_name: dataset_save_root_folder_name
        self.APorLA_orientation: AP or LA
        self.nii_preproess: nii.gz file preprocess
        self.has_pedicle: Whether pedicle files exist
        self.projection_parameter: projection_parameter
        self.cut_parameter: cut_parameter
        self.vis_parameter: visual parameter setting
        self.segmentation_data_path: Segmentation dataset path
        self.init_dataset_json_path: Initial dataset information file
        self.cut_dataset_json_path: Crop the dataset information file
        self.init_dataset_images_path: Initial dataset drr images save path
        self.init_dataset_masks_path: Initial dataset masks save path
        self.cut_dataset_images_path: Crop dataset drr images save path
        self.cut_dataset_masks_path: Crop dataset drr images save path
        self.vis_path: visualizal label image save path
        """
        self.data_root_path = config.data_root_path
        self.ct_mask_path = config.ct_mask_path
        self.dataset_save_root_folder_name = config.dataset_save_root_folder_name
        self.APorLA_orientation = config.APorLA_orientation
        self.mask_categories = config.mask_categories
        self.nii_preproess = config.nii_preproess
        self.has_pedicle = config.has_pedicle
        self.projection_parameter = config.projection_parameter
        self.cut_parameter = config.cut_parameter
        self.vis_parameter = config.vis_parameter
        self.segmentation_data_path = create_folder(join(self.data_root_path , self.dataset_save_root_folder_name, self.APorLA_orientation))
        self.init_dataset_json_path = join(self.segmentation_data_path, self.APorLA_orientation + "_init_dataset.json")
        self.cut_dataset_json_path = join(self.segmentation_data_path, self.APorLA_orientation + "_cut_dataset.json")
        self.init_dataset_images_path =create_folder(join(self.segmentation_data_path , "images"))
        self.init_dataset_masks_path =create_folder(join(self.segmentation_data_path , "masks"))
        self.cut_dataset_images_path =create_folder(join(self.segmentation_data_path , "cut_images"))
        self.cut_dataset_masks_path =create_folder(join(self.segmentation_data_path , "cut_masks"))
        self.gt_cut_mask_vis_path =create_folder(join(self.segmentation_data_path , "gt_cut_mask_vis"))
        self.gt_mask_vis_path =create_folder(join(self.segmentation_data_path , "gt_mask_vis"))
        self.gt_bbox_json_path = join(self.segmentation_data_path, "gt_bbox.json")
        self.gt_bbox_vis_path =create_folder(join(self.segmentation_data_path , "gt_bbox_vis"))
        self.gt_rotation_bbox_vis_path =create_folder(join(self.segmentation_data_path , "gt_rotation_bbox_vis"))
        
        
    def create_dataset(self):
        start_time = time.time()
        # 第一步:生成椎弓根seg文件,如果有就不需要了
        if not self.has_pedicle:
            sub_folder_names_list = os.listdir(self.ct_mask_path)
            for sub_folder_name in sub_folder_names_list:
                pedicle_nii =  GenPedicles()
                pedicle_nii.gen_pedicles(join(self.ct_mask_path, sub_folder_name))

        # 第二步:预处理nii文件,只保留nii里面最大的物体,来达到预处理的目的
        if self.nii_preproess:
            nii_preprocess = NiiTools(self.ct_mask_path)
            nii_preprocess.extract_largest_volume_objects()

        # 第三步:生成初始数据集,未裁剪
        init_dataset = GenInitSegmentationDrrDataset(ct_root_path=self.ct_mask_path, 
                                                     APorLA_orientation=self.APorLA_orientation, 
                                                     mask_categories = self.mask_categories,
                                                     save_image_file=self.segmentation_data_path,
                                                     init_dataset_json_path=self.init_dataset_json_path,
                                                     gt_bbox_json_path=self.gt_bbox_json_path,
                                                     projection_parameter=self.projection_parameter)
        init_dataset.__call__()

        # 第四步:是否需要加载检测json信息,以检测框为中心方式需要加载,以mask中心不需要加载
        if self.cut_parameter["cut_mode"] == "detection_bbox_center":
            if self.cut_parameter["run_object_detection"]:
                detection_result = run_object_detection(self.init_dataset_images_path)
            else:
                detection_result = load_detection_result(self.cut_parameter["detection_result_json_path"])
        else:
            detection_result = None
                
        # 第五步:裁剪成最终数据集
        cut_dataset = GenCutSegmentationDrrDataset(detection_result = detection_result, 
                                                   init_dataset_json_path = self.init_dataset_json_path, 
                                                   init_drrs_path = self.init_dataset_images_path, 
                                                   init_masks_path = self.init_dataset_masks_path, 
                                                   cut_dataset_json_path = self.cut_dataset_json_path, 
                                                   cut_drrs_save_path = self.cut_dataset_images_path, 
                                                   cut_masks_save_path = self.cut_dataset_masks_path, 
                                                   cut_parameter = self.cut_parameter)
        cut_dataset.cut_drrs_and_masks()
        # Step 6: Do you need to generate visualize files.
        if self.vis_parameter["is_vis"]:
            if os.path.exists(self.gt_bbox_json_path):
                visdetection = VisCoCo(self.gt_bbox_json_path , self.init_dataset_images_path, self.gt_bbox_vis_path, self.gt_rotation_bbox_vis_path)
                # 可视化真实水平框
                visdetection.visualize_bboxes_in_images()
                # 真实旋转框可视化
                visdetection.visualize_rotate_bboxes_in_images()
            vismask = VisMask(self.cut_dataset_json_path)
            vismask.visual_cut_masks_in_cut_images(cut_images_path = self.cut_dataset_images_path, 
                                                   cut_masks_path = self.cut_dataset_masks_path, 
                                                   vis_save_path = self.gt_cut_mask_vis_path)
            vismask.visual_cut_masks_in_images(images_path = self.init_dataset_images_path, 
                                               cut_masks_path = self.cut_dataset_masks_path, 
                                               vis_save_path = self.gt_mask_vis_path)
        print("consume_time:", time.time() - start_time)


def parse_args():
    parser = argparse.ArgumentParser(description="these py file will be used to gen drrs and masks")
    parser.add_argument("-c", "--config", default="config/segmentation_config.yml", help="Path to the YAML configuration file")
    parser.add_argument("-r", "--regenerate_specified_cts", default=["du_xiang.nii.gz"], help="The ct name list will be regenerated drrs")
    parser.add_argument("-continue", "--continue_generating", default=True, help="if ture, Unexpected interruptions continue to be generated, otherwise, it will regenerate from none")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    config = load_config_file(args.config)

    # Accessing values from the YAML file
    config = dotdict(data_root_path = config["data_root_path"],
                     ct_mask_path = config["ct_mask_path"],
                     dataset_save_root_folder_name = config["dataset_save_root_folder_name"],
                     APorLA_orientation = config["APorLA_orientation"],
                     mask_categories = config["mask_categories"],
                     nii_preproess = config["nii_preproess"],
                     has_pedicle = config["has_pedicle"],
                     projection_parameter = config["projection_parameter"],
                     cut_parameter = config["cut_parameter"],
                     vis_parameter = config["vis_parameter"])
    if args.continue_generating == False:
        shutil.rmtree(join(config["data_root_path"] , config["dataset_save_root_folder_name"], config["APorLA_orientation"]))
    for ct_name in args.regenerate_specified_cts:
        print(ct_name)
    dataset = SegmentationDrrDataset(config)
    dataset.create_dataset()

if __name__ == "__main__":
    main()