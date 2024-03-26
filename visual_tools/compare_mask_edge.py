'''
Description: 
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-01-14 16:16:03
LastEditors: ShuaiLei
LastEditTime: 2024-01-14 23:41:30
'''
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


def vis_infer_npz_file(npz_file_path, vis_save_path):
    data = np.load(npz_file_path)
    print(data.files)
    print(data["probabilities"].shape)
    # 使用Matplotlib进行可视化
    plt.imshow(data["probabilities"][0, 0, :, :], cmap='viridis')
    plt.axis('off')
    # plt.savefig(vis_save_path, bbox_inches='tight', pad_inches=0.0)
    plt.show()
    

def vis_gt_npz_file(npz_file_path):
    data = np.load(npz_file_path)
    print(data.files)
    print(data["data"].shape)
    print(data["seg"].shape)
    # 使用Matplotlib进行可视化

    plt.subplot(1, 4, 1)
    plt.imshow(data["data"][0, 0, :, :], cmap='viridis')
    plt.title('Array 1')

    plt.subplot(1, 4, 2)
    plt.imshow(data["data"][1, 0, :, :], cmap='viridis')
    plt.title('Array 2')

    plt.subplot(1, 4, 3)
    plt.imshow(data["data"][2, 0, :, :], cmap='viridis')
    plt.title('Array 3')

    plt.subplot(1, 4, 4)
    plt.imshow(data["seg"][0, 0, :, :], cmap='viridis')
    plt.title('Array 4')

    plt.show()

def compare_mask_edge(gt_path, infer_path, output_path):
    # 读取掩码图片
    gt = mpimg.imread(gt_path)
    infer = mpimg.imread(infer_path)

    # 将0/255的值转换为二值图像（0和1）
    gt = (gt > 0).astype(np.uint8)
    infer = (infer > 0).astype(np.uint8)

    # 创建一个彩色的边界差异图像
    boundary_diff = np.zeros_like(gt, dtype=np.uint8)
    boundary_diff[(gt == 1) & (infer == 0)] = 1  # 设置Mask 1的边界为红色
    boundary_diff[(gt == 0) & (infer == 1)] = 2  # 设置Mask 2的边界为绿色

    # 保存边界差异图像
    plt.imsave(output_path, boundary_diff, cmap='viridis')


if __name__ == "__main__":
    gt_path = "data/detection_segmentation/AP/cut_masks/chen_zhi_ying_AP_L3_whole_1.png"
    infer_path = "data/detection_segmentation/AP/segmentation_result/chen_zhi_ying_AP_L3_whole_1.png"
    output_path = "data/detection_segmentation/AP/compare_edge/chen_zhi_ying_AP_L3_whole_1.png" 
    # compare_mask_edge(gt_path, infer_path, output_path)
    vis_infer_npz_file("/home/jjf/ITK/drr_utils/data/test/segmentation_result/weng_gt_L3_drr.npz",
                       "data/detection_segmentation/AP/segmentation_result/chen_zhi_ying_AP_L3_1.png")
    # vis_gt_npz_file("data/detection_segmentation/AP/input_preprocess/fan_ru_lan_AP_L3_1.npz")