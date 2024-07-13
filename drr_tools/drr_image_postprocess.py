'''
Descripttion: 
version: 
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-12-05 15:49:06
LastEditors: ShuaiLei
LastEditTime: 2024-07-13 08:36:08
'''
import cv2
import numpy as np
import os
from tqdm import tqdm
from PIL import Image


def flipdrr(image_path):
    image = cv2.imread(image_path)
    h, w, channels = image.shape[0:3]
    for row in range(h):
        for col in range(w):
            for c in range(channels):
                pixel = image[row, col, c]
                image[row, col, c] = 255-pixel
    cv2.imwrite(image_path, image)


def blackwhite_inverse_images(image_path_list):
    """
    The function will flip black and white.
    param: image_path
    """
    for image_path in tqdm(image_path_list, desc="inversing"):
        image = Image.open(image_path)
        image_array = np.array(image)
        max_pixel_value = image_array.max()
        new_imaeg_array = max_pixel_value - image_array
        new_image = Image.fromarray(new_imaeg_array)
        new_image.save(image_path)


def gen_2D_mask(img_path):
    image = cv2.imread(img_path)
    threshold_value = 0
    _, threshold_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    cv2.imwrite(img_path, threshold_image)


def rot_image(image_path):
    image = cv2.imread(image_path)
    imageR270 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite(image_path, imageR270)


def compute_min_bbox_coverage_mask(image_path="", image=None):
    if image_path != "":
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return [0, 0, 0, 0]
    max_bbox_area = 0
    max_bbox = cv2.boundingRect(contours[0])
    for contour in contours:
        bbox = cv2.boundingRect(contour)
        bbox_area = bbox[2] * bbox[3]  
        if bbox_area > max_bbox_area:
            max_bbox_area = bbox_area
            max_bbox = bbox
    return max_bbox


# 计算的最小的旋转框
def compute_min_rotation_bbox_coverage_mask(image_path="", image=None):
    if image_path != "":
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return [[0, 0, 0, 0, 0, 0, 0, 0]]
    # 计算每个轮廓的最小外接矩形
    rotation_rects = [cv2.minAreaRect(contour) for contour in contours]
    # 找到最大面积的最小外接矩形
    rotation_max_rect = max(rotation_rects, key=lambda x: x[1][0] * x[1][1])
    # 将最小外接矩形的四个角点转换为整数
    rotation_bbox = np.intp(cv2.boxPoints(rotation_max_rect))
    segmentation = [[int(rotation_bbox[0][0]), int(rotation_bbox[0][1]),
                    int(rotation_bbox[1][0]), int(rotation_bbox[1][1]),
                    int(rotation_bbox[2][0]), int(rotation_bbox[2][1]),
                    int(rotation_bbox[3][0]), int(rotation_bbox[3][1])]]
    return segmentation
 

if __name__ == "__main__":
    # rot_image("data/LA/images/cha_zhi_lin_1.png")
    bbox = compute_min_bbox_coverage_mask(image_path="data/detection_dataset/masks/hu_yue_ling_AP_L5_1.png")
    print(bbox)