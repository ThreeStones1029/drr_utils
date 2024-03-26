'''
Description: 检测分割评估可视化流程,用于自己生成的数据来测试评估可视化
version: 
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-01-05 20:32:05
LastEditors: ShuaiLei
LastEditTime: 2024-01-06 11:12:11
'''
import argparse
import subprocess
import os
from segmentation_tools.gen_cut_segmentation_dataset import GenCutSegmentationDrrDataset
from eval_tools.segmentation_eval import SegmentationEvaluationMetrics
from visual_tools.vis_segmentation_mask import VisMask
from visual_tools.vis_coco_detection_bbox import VisCoCo
from visual_tools.gen_html import GenHtmlVis
from io_tools.file_management import dotdict
from io_tools.file_management import load_config_file, join,create_folder
from detection_tools.object_detection import load_detection_result
from segmentation_tools.seg_preprocess import preprocess_images
from segmentation_tools.seg_postpreprocess import postpreprocess_images


class DRRODSEGInferEvalVis:
    def __init__(self, config):
        """
        self.dataset_parameter 生成的数据集参数
        self.object_detection_parameter 目标检测参数
        self.segmentation_parameter 分割参数
        self.eval_parameter 评估参数
        self.vis_parameter 可视化参数
        """
        self.root_path = config.dataset_parameter["root_path"]
        self.images_path = join(self.root_path, config.dataset_parameter["images_folder"])
        self.masks_path = join(self.root_path, config.dataset_parameter["masks_folder"])
        self.cut_images_path =create_folder(join(self.root_path, config.dataset_parameter["cut_images_folder"]))
        self.cut_masks_path =create_folder(join(self.root_path, config.dataset_parameter["cut_masks_folder"]))
        self.init_dataset_json_path = join(self.root_path, config.dataset_parameter["init_dataset_json"])
        self.cut_dataset_json_path = join(self.root_path, config.dataset_parameter["cut_dataset_json"])
        self.object_detection_parameter = config.object_detection_parameter
        self.is_run_object_detection = config.object_detection_parameter["run_object_detection"]
        self.detection_result_save_path = join(self.root_path, config.object_detection_parameter["infer_detection_result_folder"])
        self.infer_bbox_json_path = join(self.detection_result_save_path, config.object_detection_parameter["infer_bbox_json"])
        self.gt_bbox_vis_path =create_folder(join(self.root_path, config.object_detection_parameter["gt_bbox_vis_folder"]))
        self.gt_rotation_bbox_vis_path =create_folder(join(self.root_path, config.object_detection_parameter["gt_rotation_bbox_vis_folder"]))
        self.gt_bbox_json_path = join(self.root_path, config.object_detection_parameter["gt_bbox_json"])
        self.cut_parameter = config.cut_parameter
        self.segmentation_parameter = config.segmentation_parameter
        self.is_run_segmentation = config.segmentation_parameter["run_segmentation"]
        self.infer_segmentation_input_cut_images_path = create_folder(join(self.root_path, config.segmentation_parameter["input_folder"]))
        self.infer_segmentation_result_path =create_folder(join(self.root_path, config.segmentation_parameter["infer_segmentation_result_folder"]))
        self.infer_mask_in_cut_image_vis_path =create_folder(join(self.root_path, config.segmentation_parameter["infer_mask_in_cut_image_vis_folder"]))
        self.infer_mask_in_image_vis_path =create_folder(join(self.root_path, config.segmentation_parameter["infer_mask_in_image_vis_folder"]))
        self.gt_mask_in_cut_image_vis_path =create_folder(join(self.root_path, config.segmentation_parameter["gt_mask_in_cut_image_vis_folder"]))
        self.gt_mask_in_image_vis_path =create_folder(join(self.root_path, config.segmentation_parameter["gt_mask_in_image_vis_folder"]))
        self.eval_parameter = config.eval_parameter
        self.eval_result_save_json_path = join(self.root_path, self.eval_parameter["eval_result_save_json"])
        self.vis_parameter = config.vis_parameter
        self.infer_eval_vis()

    def infer_eval_vis(self):
        # 一、预测
        self.infer_all()
        # 二、评估
        self.eval_all()
        # 三、可视化
        self.vis_all()

    def infer_all(self):
        # 检测预测
        detection_result = self.object_detection_infer()
        # 裁剪
        cut_dataset = GenCutSegmentationDrrDataset(detection_result=detection_result,
                                                   init_dataset_json_path=self.init_dataset_json_path,
                                                   init_drrs_path=self.images_path,
                                                   init_masks_path=self.masks_path,
                                                   cut_dataset_json_path=self.cut_dataset_json_path,
                                                   cut_drrs_save_path=self.cut_images_path,
                                                   cut_masks_save_path=self.cut_masks_path,
                                                   cut_parameter=self.cut_parameter)
        if self.cut_parameter["has_gt_masks"]:
            cut_dataset.cut_drrs_and_masks()
        else:
            cut_dataset.cut_drrs()
        # 分割预测
        self.segmentation_infer()

    def object_detection_infer(self):
        if self.is_run_object_detection:
            self.run_object_detection()
        detection_result = load_detection_result(self.infer_bbox_json_path)
        return detection_result

    def run_object_detection(self):
        script_parameter = [self.object_detection_parameter["envs_path"],
                            self.object_detection_parameter["detection_script_path"],
                            "-c", self.object_detection_parameter["config_path"],
                            "--infer_dir", self.images_path,
                            "--output_dir", self.detection_result_save_path,
                            "--draw_threshold", "0.6",
                            "--use_vdl", "False",
                            "--save_results", "True"]
        detection_command = " ".join(script_parameter)
        subprocess.run(detection_command, shell=True)


    def segmentation_infer(self):
        if self.is_run_segmentation:
            self.run_segmentation()

    def run_segmentation(self):
        preprocess_images(self.cut_images_path, self.infer_segmentation_input_cut_images_path)

        script_parameter = [self.segmentation_parameter["envs_path"],
                            self.segmentation_parameter["segmentation_script_path"],
                            "-i", self.infer_segmentation_input_cut_images_path,
                            "-o", self.infer_segmentation_result_path,
                            "-d", "101",
                            "-p", "nnUNetPlans",
                            "-c", "2d",
                            "-f", "0",
                            "--save_probabilities"]
        segmentation_command = " ".join(script_parameter)
        subprocess.run(segmentation_command, shell=True)

        postpreprocess_images(self.infer_segmentation_result_path)

    def eval_all(self):
        self.eval_object_detection()
        self.eval_segmentation()

    def eval_object_detection(self):
        pass

    def eval_segmentation(self):
        if self.cut_parameter["has_gt_masks"] and self.eval_parameter["is_segmentation_eval"]:
            seg_eval = SegmentationEvaluationMetrics(self.cut_masks_path, self.infer_segmentation_result_path)
            seg_eval.calculate_images_mean_metrics()

    def vis_all(self):
        self.vis_detection_gt()
        self.vis_detection_infer()
        self.vis_segmentation_gt()
        self.vis_segmentation_infer()
        self.gen_gt_infer_html()

    def vis_detection_gt(self):
        if self.vis_parameter["is_vis_detection_gt"] and os.path.exists(self.gt_bbox_json_path):
            visdetection = VisCoCo(self.gt_bbox_json_path, self.images_path, self.gt_bbox_vis_path, self.gt_rotation_bbox_vis_path)
            # 可视化真实水平框
            visdetection.visualize_bboxes_in_images()
            # 真实旋转框可视化
            visdetection.visualize_rotate_bboxes_in_images()

    def vis_detection_infer(self):
        pass

    def vis_segmentation_gt(self):
        if self.vis_parameter["is_vis_segmentation_gt"] and self.cut_parameter["has_gt_masks"]:
            vismask_gt = VisMask(self.cut_dataset_json_path)
            vismask_gt.visual_cut_masks_in_cut_images(cut_images_path=self.cut_images_path,
                                                      cut_masks_path=self.cut_masks_path,
                                                      vis_save_path=self.gt_mask_in_cut_image_vis_path)

            vismask_gt.visual_cut_masks_in_images(images_path=self.images_path,
                                                  cut_masks_path=self.cut_masks_path,
                                                  vis_save_path=self.gt_mask_in_image_vis_path)

    def vis_segmentation_infer(self):
        if self.vis_parameter["is_vis_segmentation_infer"]:
            vismask_infer = VisMask(self.cut_dataset_json_path)
            vismask_infer.visual_cut_masks_in_cut_images(cut_images_path=self.cut_images_path,
                                                         cut_masks_path=self.infer_segmentation_result_path,
                                                         vis_save_path=self.infer_mask_in_cut_image_vis_path)

            vismask_infer.visual_cut_masks_in_images(images_path=self.images_path,
                                                     cut_masks_path=self.infer_segmentation_result_path,
                                                     vis_save_path=self.infer_mask_in_image_vis_path)

    def gen_gt_infer_html(self):
        if self.vis_parameter["is_gen_html"]:
            html = GenHtmlVis()

            html.create_html(gt_images_folder=self.gt_bbox_vis_path,
                             infer_images_folder=self.detection_result_save_path,
                             html_path=join(self.root_path, "vis_bbox.html"))

            html.create_html(gt_images_folder=self.gt_mask_in_cut_image_vis_path,
                             infer_images_folder=self.infer_mask_in_cut_image_vis_path,
                             html_path=join(self.root_path, "vis_color_cut_mask.html"))

            html.create_html(gt_images_folder=self.gt_mask_in_image_vis_path,
                             infer_images_folder=self.infer_mask_in_image_vis_path,
                             html_path=join(self.root_path, "vis_color_mask.html"))

            html.create_html(gt_images_folder=self.cut_masks_path,
                             infer_images_folder=self.infer_segmentation_result_path,
                             html_path=join(self.root_path, "vis_cut_mask.html"))


def parse_args():
    parser = argparse.ArgumentParser(
        description="these py file will be used to object detection and segmentation infer eval and vis")
    parser.add_argument("-c", "--config", default="config/object_detection_segmentation_infer.yml",
                        help="Path to the YAML configuration file")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    config = load_config_file(args.config)
    # Accessing values from the YAML file
    config = dotdict(dataset_parameter=config["dataset_parameter"],
                     object_detection_parameter=config["object_detection_parameter"],
                     cut_parameter=config["cut_parameter"],
                     segmentation_parameter=config["segmentation_parameter"],
                     eval_parameter=config["eval_parameter"],
                     vis_parameter=config["vis_parameter"])

    DRRODSEGInferEvalVis(config)


if __name__ == "__main__":
    main()
