'''
Descripttion: 本文件主要用来通过ITK将3D_mask生成2D_mask来制作数据
version: 
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-12-05 15:46:18
LastEditors: ShuaiLei
LastEditTime: 2025-03-19 19:24:54
'''
from drr_tools.genDRR import genDRR
from drr_tools.drr_image_postprocess import gen_2D_mask, compute_min_bbox_coverage_mask, compute_min_rotation_bbox_coverage_mask, compute_keypoints_coverage_mask
from dataset_tools.dataset_sample import Dataset_sample
from detection_tools.coco_detection_data import COCODetectionData
from segmentation_tools.init_segmentation_json import InitSegmentationDatasetJson
from io_tools.file_management import linux_windows_split_name, get_sub_folder_paths, join
from time_tools.consume_time import Timer
import os
from glob import glob


class GenInitSegmentationDrrDataset:
    def __init__(self, ct_root_path, APorLA_orientation, mask_categories, save_image_file, init_dataset_json_path, gt_bbox_json_path, projection_parameter):
        """
        params
        self.projection_parameter: 所有投影参数
        self.sdr: 射线源到投影平面距离的一半
        self.height 图片大小
        self.specific_height_list 指定某些ct生成的图片大小
        self.delx 像素之间距离
        self.threshold 生成阈值
        self.AP_num_samples 正位生成数量
        self.LA_num_samples 侧位生成数量
        self.AP_rot_range_list 正位旋转角度范围
        self.AP_trans_range_list 正位偏移范围
        self.LA_rot_range_list 侧位旋转角度范围
        self.LA_trans_range_list 侧位偏移范围
        self.AP_rotations, self.AP_translations 正位旋转与偏移随机角度集合
        self.LA_rotations, self.LA_translations 侧位旋转与偏移随机角度集合
        self.ct_root_path ct的根目录
        self.APorLA_orientation 生成正位或侧位
        self.mask_categories 选择需要生成的mask类别
        self.save_image_file 保存的文件夹
        self.init_dataset_json_path 生成的json文件记录
        """
        self.projection_parameter = projection_parameter
        self.sdr = projection_parameter["sdr"]
        self.height = projection_parameter["height"]
        self.specific_height_list = projection_parameter["specific_height_list"]
        self.delx = projection_parameter["delx"]
        self.threshold = projection_parameter["threshold"]
        self.AP_num_samples = projection_parameter["AP_num_samples"]
        self.LA_num_samples = projection_parameter["LA_num_samples"]
        self.AP_rot_range_list = projection_parameter["AP_rot_range_list"]
        self.AP_trans_range_list = projection_parameter["AP_trans_range_list"]
        self.LA_rot_range_list = projection_parameter["LA_rot_range_list"]
        self.LA_trans_range_list = projection_parameter["LA_trans_range_list"]
        self.AP_rotations, self.AP_translations = self.gen_random_pose_parameters(self.AP_rot_range_list, self.AP_trans_range_list, self.AP_num_samples)
        self.LA_rotations, self.LA_translations = self.gen_random_pose_parameters(self.LA_rot_range_list, self.LA_trans_range_list, self.LA_num_samples)
        self.rotations_and_translations = {"AP_rotations": self.AP_rotations, "AP_translations": self.AP_translations,
                                           "LA_rotations": self.LA_rotations, "LA_translations": self.LA_translations}
        self.ct_root_path = ct_root_path
        self.APorLA_orientation = APorLA_orientation
        self.mask_categories = mask_categories
        self.save_image_file = save_image_file
        self.init_dataset_json_path = init_dataset_json_path
        self.init_segmentation_dataset = InitSegmentationDatasetJson(projection_parameter, self.rotations_and_translations, init_dataset_json_path)
        self.detection_bbox_annotation = COCODetectionData(self.projection_parameter, self.rotations_and_translations)
        self.min_bbox_percentage_of_height = projection_parameter["min_bbox_percentage_of_height"]
        self.gt_bbox_json_path = gt_bbox_json_path

        
    # 随机生成参数
    def gen_random_pose_parameters(self, rot_range_list, trans_range_list, num_samples):
        dataset_sample = Dataset_sample()
        rotations, translations = dataset_sample.Monte_Carlo_sample_dataset(rot_range_list, trans_range_list, num_samples)
        return rotations, translations
    

    def __call__(self):
        # 判断是否已经有了json文件,若有则读取已经生成的文件
        if os.path.exists(self.init_dataset_json_path):
            self.init_segmentation_dataset.load_json(self.init_dataset_json_path)
            # remain the exist rotations_and_translations
            self.AP_rotations = self.init_segmentation_dataset.info["rotations_and_translations"]["AP_rotations"]
            self.AP_translations = self.init_segmentation_dataset.info["rotations_and_translations"]["AP_translations"]
            self.LA_rotations = self.init_segmentation_dataset.info["rotations_and_translations"]["LA_rotations"]
            self.LA_translations = self.init_segmentation_dataset.info["rotations_and_translations"]["LA_translations"]
        # 判断检测标注是否有了json文件，若有则读取已经生成的文件
        if os.path.exists(self.gt_bbox_json_path):
            self.detection_bbox_annotation.load_json(self.gt_bbox_json_path)
        ct_path_list = get_sub_folder_paths(self.ct_root_path)
        if self.APorLA_orientation == "AP":
            self.gen_multple_cts_AP_drrs_and_masks(ct_path_list)
        if self.APorLA_orientation == "LA":
            self.gen_multple_cts_LA_drrs_and_masks(ct_path_list)
        if self.APorLA_orientation == "all":
            self.gen_multple_cts_AP_drrs_and_masks(ct_path_list)
            self.gen_multple_cts_LA_drrs_and_masks(ct_path_list)


    def gen_multple_cts_AP_drrs_and_masks(self, ct_path_list):
        """
        生成多个ct正位drr图像以及对应的mask
        """
        for single_ct_path in ct_path_list:
            # get ct name
            ct_name = linux_windows_split_name(single_ct_path)
            #------------------------------------------------------------------------------------------------------------------- 
            # Note if you want regenerate completely,just add "-r all", Otherwise, it will automatically read the existing json 
            # file and only generate data for ct that is not in the json file #
            #-------------------------------------------------------------------------------------------------------------------
            if ct_name + ".nii.gz" not in self.init_segmentation_dataset.exist_ct_nii_names["AP"]:
                time_tool = Timer()
                self.gen_single_ct_drrs_and_masks(ct_name, single_ct_path, self.AP_rotations, self.AP_translations, "AP")
                # 生成初始数据集json文件
                self.init_segmentation_dataset.gen_init_dataset_json()
                # 生成检测框标注json文件
                self.detection_bbox_annotation.to_json(self.gt_bbox_json_path)
                time_tool.stop()
                consume_time = time_tool.elapsed_time()
                eval_remain_second_time = consume_time * (len(ct_path_list) - len(self.init_segmentation_dataset.exist_ct_nii_names) - 1)
                eval_remain_hour_time = time_tool.second2hour(eval_remain_second_time)
                print("AP eval remain time is:", eval_remain_hour_time, "hours")


    def gen_multple_cts_LA_drrs_and_masks(self, ct_path_list):
        """
        生成多个ct侧位drr图像以及对应的mask
        """
        for single_ct_path in ct_path_list:
            # get ct name
            ct_name = linux_windows_split_name(single_ct_path)
            #------------------------------------------------------------------------------------------------------------------- 
            # Note if you want regenerate completely,just add "-r all", Otherwise, it will automatically read the existing json 
            # file and only generate data for ct that is not in the json file #
            #-------------------------------------------------------------------------------------------------------------------
            if ct_name + ".nii.gz" not in self.init_segmentation_dataset.exist_ct_nii_names["LA"]:
                time_tool = Timer()
                self.gen_single_ct_drrs_and_masks(ct_name, single_ct_path, self.LA_rotations, self.LA_translations, "LA")
                # 生成初始数据集json文件
                self.init_segmentation_dataset.gen_init_dataset_json()
                # 生成检测框标注json文件
                self.detection_bbox_annotation.to_json(self.gt_bbox_json_path)
                time_tool.stop()
                consume_time = time_tool.elapsed_time()
                eval_remain_second_time = consume_time * (len(ct_path_list) - len(self.init_segmentation_dataset.exist_ct_nii_names) - 1)
                eval_remain_hour_time = time_tool.second2hour(eval_remain_second_time)
                print("LA eval remain time is:", eval_remain_hour_time, "hours")


    def gen_single_ct_drrs_and_masks(self, ct_name, single_ct_path, rotations, translations, AP_or_LA):
        '''
        description: 单个CT生成drr以及masks
        '''
        i = 0
        if ct_name in self.specific_height_list.keys():
            self.height = self.specific_height_list[ct_name]
        else:
            self.height = self.projection_parameter["height"]
        
        self.init_segmentation_dataset.add_ct(ct_name, AP_or_LA)
        for rotation, translation in zip(rotations, translations):
            # 得到需要使用的nii文件列表
            filepaths = self.get_choosed_nii_files(ct_name, single_ct_path)
            i += 1
            # for filepath in filepaths:
            #     basename = os.path.basename(filepath)
            #     basename_wo_ext = basename[:basename.find('.nii.gz')]
            #     if "seg" not in basename_wo_ext:
            #         self.gen_drr(ct_name, i, rotation, translation, filepath, AP_or_LA)
            #     else:
            #         # 正位一般生成body 侧位可以选择生成整体或者生成body, pecidle, other三部分或者只生成body部分
            #         self.gen_masks(basename_wo_ext, ct_name, i, rotation, translation, filepath, AP_or_LA)

            for j, filepath in enumerate(filepaths):
                basename = os.path.basename(filepath)
                basename_wo_ext = basename[:basename.find('.nii.gz')]
                if j == 0 and "seg" not in basename_wo_ext:
                    if not os.path.exists(filepath):
                        filepath = os.path.join("/home/jjf/Desktop/PedScrewPlanning/data/local", ct_name, "CT", "spine", ct_name+".nii.gz")
                    self.gen_drr(ct_name, i, rotation, translation, filepath, AP_or_LA)
                else:
                    # 正位一般生成body 侧位可以选择生成整体或者生成body, pecidle, other三部分或者只生成body部分
                    self.gen_masks(basename_wo_ext, ct_name, i, rotation, translation, filepath, AP_or_LA)
            
                                                                                                                                                                                                    
                
    def gen_masks(self, basename_wo_ext, ct_name, i, rotation, translation, filepath, AP_or_LA):
        # get cur vertebrae name
        vertebrae_name = basename_wo_ext[:basename_wo_ext.find('_seg')]
        if "body" in vertebrae_name or "pedicle" in vertebrae_name or "other" in vertebrae_name:
            mask_name = f"{ct_name}_{AP_or_LA}_{vertebrae_name}_{i}.png"
            category_name = vertebrae_name.split("_")[0]
        else:
            mask_name = f"{ct_name}_{AP_or_LA}_{vertebrae_name}_whole_{i}.png"
            category_name = vertebrae_name
        saveIMG = join(self.save_image_file, "masks", mask_name)
        # generate drr
        genDRR(self.sdr, self.height, self.delx, self.threshold, rotation, translation, filepath, saveIMG)
        # generate 2d mask
        gen_2D_mask(saveIMG)
        # add mask info to json
        width, height = self.height, self.height
        self.init_segmentation_dataset.add_mask(mask_name, AP_or_LA, width, height, rotation, translation)
        self.init_segmentation_dataset.add_ct_vertebrae_categoties(mask_name)
        # add annotation in detection json 
        category_id = self.detection_bbox_annotation.catname2catid[category_name]
        bbox = compute_min_bbox_coverage_mask(image_path=saveIMG)
        rotation_bbox = compute_min_rotation_bbox_coverage_mask(image_path=saveIMG)
        keypoints = compute_keypoints_coverage_mask(image_path=saveIMG) # 计算中心点 (目前比较粗糙，需要后续优化)
        # 边缘上且太小的框排除 不在边缘都可以留下来
        if bbox[1] == 0 or bbox[1] + bbox[3] == self.height or bbox[0] == 0 or bbox[0] + bbox[2] == self.height:
            if bbox[2] >= self.height * self.min_bbox_percentage_of_height and bbox[3] >= self.height * self.min_bbox_percentage_of_height:
                self.detection_bbox_annotation.add_annotation(mask_name, category_id, category_name, bbox, rotation_bbox, keypoints, iscrowd=0)
        else:
            self.detection_bbox_annotation.add_annotation(mask_name, category_id, category_name, bbox, rotation_bbox, keypoints, iscrowd=0)


    def gen_drr(self, ct_name, i, rotation, translation, filepath, AP_or_LA):
        drr_image_name = f"{ct_name}_{AP_or_LA}_{i}.png"
        saveIMG = join(self.save_image_file, "images", drr_image_name)
        genDRR(self.sdr, self.height, self.delx, self.threshold, rotation, translation, filepath, saveIMG)
        # add mask info to json
        width, height = self.height, self.height
        self.init_segmentation_dataset.add_image(drr_image_name, ct_name, AP_or_LA, width, height, rotation, translation)
        self.detection_bbox_annotation.add_image(drr_image_name, ct_name, AP_or_LA, width, height, rotation, translation)

    
    def get_choosed_nii_files(self,  ct_name, single_ct_path):
        filepaths = []
        nii_filepaths = glob(join(single_ct_path, "*seg.nii.gz"))
        for nii_filepath in nii_filepaths:
            filename = os.path.basename(nii_filepath)
            if ("body" in filename and "body" in self.mask_categories) or ("pedicle" in filename and "pedicle" in self.mask_categories) or ("other" in filename and "other" in self.mask_categories):
                filepaths.append(join(single_ct_path, filename))
        
        # 如果生成整体的mask投影
        if self.mask_categories[0] == "whole":
            for nii_filepath in nii_filepaths:
                filename = os.path.basename(nii_filepath)
                if "body" not in filename and "pedicle" not in filename and "other" not in filename and "seg" in filename:
                    filepaths.append(join(single_ct_path, filename))

        # 需呀将CT放到路径开头,这样才能生成正确的json文件
        ct_filepath = join(single_ct_path, ct_name + '.nii.gz')
        filepaths.insert(0, ct_filepath)

        return filepaths