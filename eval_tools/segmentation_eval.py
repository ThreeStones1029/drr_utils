'''
Descripttion: 
version: 
Author: ShuaiLei
Date: 2024-01-07 16:50:18
LastEditors: ShuaiLei
LastEditTime: 2024-04-23 07:49:25
'''
import os
import sys
sys.path.insert(0, sys.path.append(os.path.dirname(sys.path[0])))
import cv2
import numpy as np
import multiprocessing
from tqdm import tqdm
import matplotlib.pyplot as plt
from medpy import metric
from io_tools.file_management import save_json_file, join, get_subfiles


class SegmentationEvaluationMetrics:
    def __init__(self, GT_folder_path=None, Pre_floder_path=None):
        """
        Dice Eval
        self.root_path: root path
        self.eval_result_json_path: eval result save path
        self.eval_result_dice_distribute_bar_save_path: eval dice bar png save path
        self.GT_folder_path: eval gt folder
        self.Pre_floder_path: eval pre folder
        self.label2maskname: label to mask name
        self.eval_dice_result: eval dice result
        self.eval_overall_result: oversll eval result 
        self.eval_detail_result: every png eval result
        """
        self.root_path = os.path.dirname(GT_folder_path)
        self.eval_result_json_path = join(self.root_path, "eval_result.json")
        self.dice_distribute_bar_save_path = join(self.root_path, "dice_distribute.png")
        self.hausdorff_distance_distribute_bar_save_path = join(self.root_path, "hausdorff_distance_distribute.png")
        self.jaccard_coefficient_distribute_bar_save_path = join(self.root_path, "jaccard_coefficient_distribute.png")
        self.average_surface_distance_distribute_bar_save_path = join(self.root_path, "average_surface_distance_distribute.png")
        self.GT_folder_path = GT_folder_path
        self.Pre_floder_path = Pre_floder_path
        self.label2maskname = {255: "vertebrae"}
        self.eval_dice_result = {}
        self.eval_overall_result = {}
        self.eval_detail_result = []


    def calculate_images_mean_metrics(self):
        images_mean_dice_list = []
        images_mean_jc_list = []
        images_mean_hd_list = []
        images_mean_asd_list = []
        gt_files = get_subfiles(self.GT_folder_path, suffix=".png") 
        pre_files = get_subfiles(self.Pre_floder_path, suffix=".png") 
        try:
            if len(gt_files) != len(pre_files):
                raise ValueError("Check that the number of true and predicted images are the same")
        except ValueError as e:
            print(f"error:{e}")
        num_imgs = len(gt_files)
        # multiprocessing.Pool(8) # 创建多个进程，提高代码处理效率,使用进程加速
        with multiprocessing.Pool(8) as pool:
            eval_results = list(tqdm(pool.imap(self.calculate_image_mean_metrics, [(number_and_path) for number_and_path in enumerate(sorted(gt_files))]), total=num_imgs, desc="evaling"))
        for result in eval_results:
            images_mean_dice_list.append(result[2])
            images_mean_jc_list.append(result[3])
            images_mean_hd_list.append(result[4])
            images_mean_asd_list.append(result[5])
            self.eval_detail_result.append({"id": result[0][0], 
                                            "file_name": os.path.basename(result[0][1]), 
                                            "every_label_metrics_list": result[1],
                                            "labels_mean_dice": result[2],
                                            "labels_mean_jaccard_coefficient": result[3],
                                            "labels_mean_hausdorff_distance": result[4],
                                            "labels_mean_average_surface_distance": result[5]})
        mean_dice = np.mean(images_mean_dice_list)
        mean_jaccard_coefficient = np.mean(images_mean_jc_list)
        mean_hausdorff_distance = np.mean(images_mean_hd_list)
        mean_average_surface_distance = np.mean(images_mean_asd_list)
        max_dice = max(images_mean_dice_list)
        max_jaccard_coefficient = max(images_mean_jc_list)
        max_hausdorff_distance = max(images_mean_hd_list)
        max_average_surface_distance = max(images_mean_asd_list)
        min_dice = min(images_mean_dice_list)
        min_jaccard_coefficient = min(images_mean_jc_list)
        min_hausdorff_distance = min(images_mean_hd_list)
        min_average_surface_distance = min(images_mean_asd_list)
        self.eval_overall_result = {"file_number": num_imgs,
                                    "mean_dice": mean_dice,
                                    "max_dice": max_dice,
                                    "min_dice:": min_dice,
                                    "mean_jaccard_coefficient": mean_jaccard_coefficient,
                                    "max_jaccard_coefficient": max_jaccard_coefficient,
                                    "min_jaccard_coefficient:": min_jaccard_coefficient,
                                    "mean_hausdorff_distance": mean_hausdorff_distance,
                                    "max_hausdorff_distance": max_hausdorff_distance,
                                    "min_hausdorff_distance": min_hausdorff_distance,
                                    "mean_average_surface_distance": mean_average_surface_distance,
                                    "max_average_surface_distance": max_average_surface_distance,
                                    "min_average_surface_distance": min_average_surface_distance}
        
        self.eval_dice_result["overall"] = self.eval_overall_result
        self.eval_dice_result["detail"] = self.eval_detail_result
        self.print_eval_overall_result()
        self.plot_bar(title_name="dice distribute bar", metric="dice", save_path=self.dice_distribute_bar_save_path)
        self.plot_bar(title_name="jaccard coefficient distribute bar", metric="jaccard_coefficient", save_path=self.jaccard_coefficient_distribute_bar_save_path)
        self.plot_bar(title_name="hausdorff distance distribute bar", metric="hausdorff_distance", save_path=self.hausdorff_distance_distribute_bar_save_path)
        self.plot_bar(title_name="average surface distance distribute bar", metric="average_surface_distance", save_path=self.average_surface_distance_distribute_bar_save_path)
        self.to_json()


    def calculate_image_mean_metrics(self, number_and_path):
        file_name = os.path.basename(number_and_path[1])
        gt_img_path = join(self.GT_folder_path, file_name)
        pre_img_path = join(self.Pre_floder_path, file_name)
        every_label_metrics_list, single_img_mean_dice, single_img_mean_jaccard_coefficient, single_img_mean_hausdorff_distance, single_img_mean_average_surface_distance = self.calculate_image_muti_labels_metrics(gt_img_path, pre_img_path)
        
        return number_and_path, every_label_metrics_list, single_img_mean_dice, single_img_mean_jaccard_coefficient, single_img_mean_hausdorff_distance, single_img_mean_average_surface_distance


    def calculate_image_muti_labels_metrics(self, gt_img_path, pre_img_path):
        """
        compute two images dice
        :param gt_img_path: gt mask path
        :param pre_img_path: pre mask path
        :return: Dice系数
        """
        every_label_metrics_list = []
        gt = cv2.imread(gt_img_path, cv2.IMREAD_GRAYSCALE)
        pre = cv2.imread(pre_img_path, cv2.IMREAD_GRAYSCALE)
        gt_label_list = np.unique(gt)
        labels_dice_list = []
        labels_jc_list = []
        labels_hd_list = []
        labels_asd_list = []
        for gt_label in gt_label_list:
            if gt_label != 0:
                single_label_dice, single_label_jc, single_label_hausdorff_distance, single_label_asd = self.calculate_image_single_label_metrics(gt, pre, gt_label)
                every_label_metrics_list.append({"label": int(gt_label),
                                                 "mask_name": self.label2maskname[gt_label],
                                                 "dice": single_label_dice,
                                                 "jaccard_coefficient": single_label_jc,
                                                 "hausdorff_distance": single_label_hausdorff_distance,
                                                 "average_surface_distance": single_label_asd})
        for evert_label_info in every_label_metrics_list:
            labels_dice_list.append(evert_label_info["dice"])
            labels_jc_list.append(evert_label_info["jaccard_coefficient"])
            labels_hd_list.append(evert_label_info["hausdorff_distance"])
            labels_asd_list.append(evert_label_info["average_surface_distance"])

        single_img_mean_dice = np.mean(labels_dice_list)
        single_img_mean_jaccard_coefficient = np.mean(labels_jc_list)
        single_img_mean_hausdorff_distance = np.mean(labels_hd_list)
        single_img_mean_average_surface_distance = np.mean(labels_asd_list)

        return every_label_metrics_list, single_img_mean_dice, single_img_mean_jaccard_coefficient, single_img_mean_hausdorff_distance, single_img_mean_average_surface_distance
    

    def calculate_image_single_label_metrics(self, gt, pre, label):
        """
        calculate the single label dice, jc,hd  in image
        dice: dice系数
        jc:Jaccard系数
        hd:hausdorff distance
        asd: Average surface distance
        """
        # compute dice
        gt = (gt == label)
        pre = (pre == label)
        dice = metric.binary.dc(pre, gt)
        jc = metric.binary.jc(pre, gt)
        hd = metric.binary.hd95(pre, gt)
        asd = metric.binary.asd(pre, gt)
        return dice, jc, hd, asd
    

    def to_json(self):
        """
        save the dice eval result to json
        """
        save_json_file(self.eval_dice_result, self.eval_result_json_path)


    def plot_bar(self, metric, title_name, save_path):
        """
        plot dice bar
        """
        metric_value_list = sorted([img_info["labels_mean_" + metric] for img_info in self.eval_dice_result["detail"]])
        x = [i for i in range(len(metric_value_list))]
        plt.bar(x, metric_value_list, color="blue")
        plt.title(title_name)
        plt.xlabel("png num")
        plt.ylabel(metric)
        plt.savefig(save_path)
        plt.close()
        # plt.show()


    def print_eval_overall_result(self):
        """
        print dice evluation result 
        """
        for key, value in self.eval_dice_result["overall"].items():
            print(key, value)


if __name__ == "__main__":
    # 计算Dice系数
    pre_gt_eval = SegmentationEvaluationMetrics("/home/drr_utils/data/detection_segmentation/LA/cut_masks",
                                                "/home/drr_utils/data/detection_segmentation/LA/segmentation_result")
    pre_gt_eval.calculate_images_mean_metrics()