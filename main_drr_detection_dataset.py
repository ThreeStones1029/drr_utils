'''
Description: 使用投影方式重新生成DRR检测数据,两种标注方式
version: 
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-12-11 11:32:05
LastEditors: ShuaiLei
LastEditTime: 2024-03-30 00:51:32
'''
from drr_tools.genDRR import genDRR
from detection_tools.coco_detection_data import COCODetectionData
from visual_tools.vis_coco_detection_bbox import VisCoCo
from dataset_tools.dataset_sample import Dataset_sample
from drr_tools.drr_image_postprocess import rot_image, gen_2D_mask, compute_min_bbox_coverage_mask, compute_min_rotation_bbox_coverage_mask
from io_tools.file_management import dotdict
from io_tools.file_management import create_folder, linux_windows_split_name, load_config_file,join
from time_tools.consume_time import Timer
import argparse
import time
import os
from glob import glob


class GenDetectionDataset:
    def __init__(self, config):
        """
        params
        self.sdr: Half of the distance from the ray source to the projection plane
        self.height: Image size
        self.delx: Image pixel distance
        self.threshold: ITK projection threshold
        self.AP_num_samples: Number of AP generated per nii file
        self.LA_num_samples: Number of LA generated per nii file
        self.AP_bbox_label_type: AP Annotation method big or small
        self.LA_bbox_label_type: LA Annotation method big or small
        self.ct_root_path: The root path of ct
        self.dataset_path: save folder path
        self.dataset_json_path: json file generated
        self.AP_rot_range_list: AP Range of Angle
        self.AP_trans_range_list: AP Range of movement
        self.LA_rot_range_list: LA Range of Angle
        self.LA_trans_range_list: LA Range of movement
        self.min_bbox_percentage_of_height: The minimum percentage of the bbox relative to the picture 
        self.AP_rotations, self.AP_translations: The range of AP angles generated, The range of AP movement generated
        self.LA_rotations, self.LA_translations: The range of LA angles generated, The range of LA movement generated
        self.detection_dataset: CoCo format json
        self.delete_mask: Remove mask when disk runs out. mask takes up about 6-7 times the space of images 
        self.specific_height_list: Sometimes the generated image needs to be resized, so you can specify the size manually
        """
        self.config = config
        self.sdr = config.projection_parameter["sdr"]
        self.height = config.projection_parameter["height"]
        self.specific_height_list = config.projection_parameter["specific_height_list"]
        self.delx = config.projection_parameter["delx"]
        self.threshold = config.projection_parameter["threshold"]
        self.AP_num_samples = config.projection_parameter["AP_num_samples"]
        self.LA_num_samples = config.projection_parameter["LA_num_samples"]
        self.AP_bbox_label_type = config.projection_parameter["AP_bbox_label_type"]
        self.LA_bbox_label_type = config.projection_parameter["LA_bbox_label_type"]
        self.ct_root_path = config.ct_root_path
        self.dataset_path = config.dataset_path
        self.dataset_images_path = config.dataset_images_path
        self.dataset_masks_path = config.dataset_masks_path
        self.dataset_json_path = config.dataset_json_path
        self.AP_rot_range_list = config.projection_parameter["AP_rot_range_list"]
        self.AP_trans_range_list = config.projection_parameter["AP_trans_range_list"]
        self.LA_rot_range_list = config.projection_parameter["LA_rot_range_list"]
        self.LA_trans_range_list = config.projection_parameter["LA_trans_range_list"]
        self.min_bbox_percentage_of_height = config.projection_parameter["min_bbox_percentage_of_height"]
        self.AP_rotations, self.AP_translations = self.gen_random_pose_parameters(self.AP_rot_range_list, self.AP_trans_range_list, self.AP_num_samples)
        self.LA_rotations, self.LA_translations = self.gen_random_pose_parameters(self.LA_rot_range_list, self.LA_trans_range_list, self.LA_num_samples)
        self.detection_dataset = COCODetectionData()
        self.delete_mask = True if self.AP_num_samples + self.LA_num_samples >= 2000 else False
        # create save folder
        create_folder(self.dataset_path)
        create_folder(self.dataset_images_path)
        create_folder(self.dataset_masks_path)


    # 随机生成参数
    def gen_random_pose_parameters(self, rot_range_list, trans_range_list, num_samples):
        dataset_sample = Dataset_sample()
        rotations, translations = dataset_sample.Monte_Carlo_sample_dataset(rot_range_list,trans_range_list, num_samples)
        return rotations, translations


    def gen_multple_cts_drrs_and_masks(self):
        '''
        description: 多个CT生成正位drr以及mask
        param {*} self
        param {*} ct_root_path
        return {*}
        '''
        total_start_time = time.time()
        ct_path_list = self.get_sub_folder_path(self.ct_root_path)
        self.check_sub_folders(ct_path_list)
        # 对于每例CT同时侧位与正位
        for single_ct_path in ct_path_list:
            ct_name = linux_windows_split_name(single_ct_path)
            # 读取已经生成的文件
            if os.path.exists(self.dataset_json_path):
                self.detection_dataset.load_json(self.dataset_json_path)
            #------------------------------------------------------------------------------------------------------------------- 
            # 注意如果需要完全重新生,例如修改生成数量, 需要把已经存在的json文件删除,否则会自动读取已经存在的json文件,只对不在json文件中ct生成数据 #
            #-------------------------------------------------------------------------------------------------------------------
            if (ct_name + ".nii.gz" not in self.detection_dataset.exist_ct_nii_names["AP"]) and (ct_name + ".nii.gz" not in self.detection_dataset.exist_ct_nii_names["LA"]):
                time_tool = Timer()
                if ct_name in self.specific_height_list.keys():
                    self.height = self.specific_height_list[ct_name]
                else:
                    # 恢复默认大小
                    self.height = self.config.projection_parameter["height"]
                self.gen_AP_drrs_and_masks(single_ct_path, self.AP_bbox_label_type)
                self.gen_LA_drrs_and_masks(single_ct_path, self.LA_bbox_label_type)
                # 可以实时保存,防止报错导致重复生成浪费时间
                self.detection_dataset.to_json(self.dataset_json_path)
                time_tool.stop()
                consume_time = time_tool.elapsed_time()
                eval_remain_second_time = consume_time * (len(ct_path_list) - len(self.detection_dataset.exist_ct_nii_names) - 1)
                eval_remain_hour_time = time_tool.second2hour(eval_remain_second_time)
                print("Estimated time remaining: ", eval_remain_hour_time, "hours", "\n")
            
        print("total consume", time.time() - total_start_time)


    def gen_AP_drrs_and_masks(self, single_ct_path, AP_bbox_label_type):
        # get ct name
        ct_name = linux_windows_split_name(single_ct_path)
        ct_filepath = join(single_ct_path, ct_name + '.nii.gz')
        filepaths = glob(join(single_ct_path, '*seg.nii.gz'))
        # 需呀将原CT放到路径开头,为了先生成整个CT的drr,再单独生成每节椎体的drr
        filepaths.insert(0, ct_filepath)
        i = 0
        for rotation, translation in zip(self.AP_rotations, self.AP_translations):
            i += 1
            for filepath in filepaths:
                basename = os.path.basename(filepath)
                basename_wo_ext = basename[:basename.find('.nii.gz')]
                if "seg" not in basename_wo_ext:
                    self.gen_drr(ct_name, i, rotation, translation, filepath, "AP")
                if AP_bbox_label_type == "small" and "body_seg" in basename_wo_ext:
                    self.gen_mask(basename_wo_ext, ct_name, i, rotation, translation, filepath, "AP")
                if AP_bbox_label_type == "big" and len(basename_wo_ext.split("_")) == 2 and "seg" in basename_wo_ext:
                    self.gen_mask(basename_wo_ext, ct_name, i, rotation, translation, filepath, "AP")
        

    def gen_LA_drrs_and_masks(self, single_ct_path, LA_bbox_label_type):
        # get ct name
        ct_name = linux_windows_split_name(single_ct_path)
        filepaths = glob(join(single_ct_path, '*seg.nii.gz'))
        # 需要将原CT放到路径开头,为了先生成整个CT的drr,再单独生成每节椎体的drr
        ct_filepath = join(single_ct_path, ct_name + '.nii.gz')
        filepaths.insert(0, ct_filepath)
        i = 0
        for rotation, translation in zip(self.LA_rotations, self.LA_translations):
            i += 1
            for filepath in filepaths:
                basename = os.path.basename(filepath)
                basename_wo_ext = basename[:basename.find('.nii.gz')]
                if "seg" not in basename_wo_ext:
                    self.gen_drr(ct_name, i, rotation, translation, filepath, "LA")
                if LA_bbox_label_type == "big" and len(basename_wo_ext.split("_")) == 2 and "seg" in basename_wo_ext:
                    self.gen_mask(basename_wo_ext, ct_name, i, rotation, translation, filepath, "LA")
                if LA_bbox_label_type == "small" and "body_seg" in basename_wo_ext:
                    self.gen_mask(basename_wo_ext, ct_name, i, rotation, translation, filepath, "LA")


    def gen_drr(self, ct_name, i, rotation, translation, filepath, APorLA):
        drr_image_name = f"{ct_name}_{APorLA}_{i}.png"
        saveIMG = join(self.dataset_images_path, drr_image_name)
        genDRR(self.sdr, self.height, self.delx, self.threshold, rotation, translation, filepath, saveIMG)
        width, height = self.height, self.height
        self.detection_dataset.add_image(drr_image_name, ct_name, APorLA, width, height, rotation, translation)


    def gen_mask(self, basename_wo_ext, ct_name, i, rotation, translation, filepath, APorLA):
        # get cur vertebrae name
        vertebrae_name = basename_wo_ext[:basename_wo_ext.find('seg')]
        mask_name = f"{ct_name}_{APorLA}_{vertebrae_name}{i}.png"
        saveIMG = join(self.dataset_masks_path, mask_name)
        # generate drr
        genDRR(self.sdr, self.height, self.delx, self.threshold, rotation, translation, filepath, saveIMG)
        # generate 2d mask
        gen_2D_mask(saveIMG)

        category_name = vertebrae_name.split("_")[0]
        category_id = self.detection_dataset.catname2catid[category_name]
        bbox = compute_min_bbox_coverage_mask(image_path=saveIMG)
        rotation_bbox = compute_min_rotation_bbox_coverage_mask(image_path=saveIMG)
        # 边缘上且太小的框排除 不在边缘都可以留下来
        if bbox[1] == 0 or bbox[1] + bbox[3] == self.height or bbox[0] == 0 or bbox[0] + bbox[2] == self.height:
            if bbox[2] >= self.height * self.min_bbox_percentage_of_height and bbox[3] >= self.height * self.min_bbox_percentage_of_height:
                self.detection_dataset.add_annotation(mask_name, category_id, category_name, bbox, rotation_bbox, iscrowd=0)
        else:
            self.detection_dataset.add_annotation(mask_name, category_id, category_name, bbox, rotation_bbox, iscrowd=0)
        # 节省磁盘空间,可删除mask
        if self.delete_mask:
            os.remove(saveIMG)


    def gen_sample_drrs(self):
        # Used to generate a drr beforehand to determine the image size
        create_folder(join(self.ct_root_path, "..", "sample"))
        sub_path_list = self.get_sub_folder_path(self.ct_root_path)
        self.check_sub_folders(sub_path_list)
        AP_rotation = [90, 180, 180]
        AP_translation = [0, 0, 0]
        LA_rotation = [0, 90, 0]
        LA_translation = [0, 0, 0]
        for sub_path in sub_path_list:
            ct_name = os.path.basename(sub_path)
            if ct_name in self.specific_height_list.keys():
                self.height = self.specific_height_list[ct_name]
                ct_path = join(sub_path, ct_name + ".nii.gz")
                AP_saveIMG = join(self.ct_root_path, "..", "sample", ct_name + "_AP.png")
                LA_saveIMG = join(self.ct_root_path, "..", "sample", ct_name + "_LA.png")
                genDRR(self.sdr, self.height, self.delx, self.threshold, AP_rotation, AP_translation, ct_path, AP_saveIMG)
                genDRR(self.sdr, self.height, self.delx, self.threshold, LA_rotation, LA_translation, ct_path, LA_saveIMG)
            self.height = self.config.projection_parameter["height"]


    def get_sub_folder_path(self, root_folder):
        sub_path_list = []
        sub_folder_name_list = os.listdir(root_folder)
        # 得到所有ct子文件夹
        for sub_folder_name in sub_folder_name_list:
            if os.path.isdir(join(root_folder, sub_folder_name)):
                sub_path_list.append(join(root_folder, sub_folder_name))
        return sub_path_list
    

    def check_sub_folders(self, sub_folder_paths):
        for sub_folder_path in sub_folder_paths:
            basename = os.path.basename(sub_folder_path) 
            nii_path = join(sub_folder_path, basename + ".nii.gz")
            if not os.path.exists(nii_path):
                raise FileNotFoundError(f"file '{nii_path}  not exist")
        print("check completely!")


def parse_args():
    parser = argparse.ArgumentParser(description="these py file will be used to gen drrs and masks")
    parser.add_argument("-c", "--config", default="config/detection_config.yml", help="Path to the YAML configuration file")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    config = load_config_file(args.config)

    # Accessing values from the YAML file
    config = dotdict(ct_root_path = config["ct_root_path"],
                     dataset_path = config["dataset_path"],
                     dataset_images_path = config["dataset_images_path"],
                     dataset_masks_path = config["dataset_masks_path"],
                     dataset_json_path = config["dataset_json_path"],
                     projection_parameter = config["projection_parameter"],
                     vis_parameter = config["vis_parameter"])
    
    # drr_detection_dataset = GenDetectionDataset(config=config)
    # drr_detection_dataset.gen_multple_cts_drrs_and_masks()
    
    # Visualize label
    if config.vis_parameter["is_vis"]:
        vis_image_label = VisCoCo(config.dataset_json_path, config.dataset_images_path, config.vis_parameter["vis_save_path"], config.vis_parameter["rotation_bbox_vis_save_path"])
        vis_image_label.visualize_bboxes_in_images()
        # 旋转框可视化
        vis_image_label.visualize_rotate_bboxes_in_images()

if __name__ == "__main__":
    main()
    