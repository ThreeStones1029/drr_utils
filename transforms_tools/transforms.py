'''
Description: 
version: 
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-12-17 16:40:32
LastEditors: ShuaiLei
LastEditTime: 2024-01-19 20:39:59
'''
import os
import sys
sys.path.insert(0, os.path.dirname(sys.path[0]))
import cv2
import numpy as np
from io_tools.file_management import create_folder, save_json_file, join
from visual_tools.vis_coco_detection_bbox import VisCoCo
from pycocotools.coco import COCO
from tqdm import tqdm
import multiprocessing


class RandomRotate:
    """
    随机旋转数据增强
    """
    def __init__(self, annotation_file, angle_range=(-180, 180)):
        self.images_root_path = "data/detection_dataset_small/images"
        self.transform_images_root_path = create_folder("data/detection_dataset_small/transform_images")
        self.coco_data = COCO(annotation_file)
        self.angle_range = angle_range
        self.transform_annotation_file = join(os.path.dirname(annotation_file), "transform_detection_data.json")

    def rotate_image(self, image, angle):
        # 获取图像中心点
        height, width = image.shape[:2]
        center = (width / 2, height / 2)
        # 旋转矩阵
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        # 进行旋转变换
        rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
        return rotated_image

    def rotate_box(self, box, angle, center):
        # 获取旋转矩阵
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        # 在边界框的四个角点上应用旋转变换
        points = np.array([[box[0], box[1]], [box[0] + box[2], box[1]], [box[0], box[1] + box[3]], [box[0] + box[2], box[1] + box[3]]], dtype=np.float32)
        points_rotated = cv2.transform(points.reshape(1, -1, 2), rotation_matrix).reshape(-1, 2)
        # 计算新的边界框
        x, y, w, h = cv2.boundingRect(points_rotated.astype(np.int64))
        return [x, y, w, h]
    
    def rotate_image_boxes(self, image, annotations):
        # 随机生成旋转角度
        angle = np.random.uniform(self.angle_range[0], self.angle_range[1])
        # 获取图像中心点
        height, width = image.shape[:2]
        center = (width / 2, height / 2)
        # 旋转图像
        rotated_image = self.rotate_image(image, angle)
        # 旋转边界框
        rotated_annotations = []
        for ann in annotations:
            new_ann = ann
            new_ann['bbox'] = self.rotate_box(ann['bbox'], angle, center)
            rotated_annotations.append(new_ann)
        return rotated_image
        

    def __call__(self):
        for image_id in range(len(self.coco_data.dataset["images"])):
            file_name =  self.coco_data.dataset["images"][image_id]["file_name"]
            image = cv2.imread(join(self.images_root_path, file_name))
            annotations = self.coco_data.imgToAnns[image_id + 1]
            rotated_image = self.rotate_image_boxes(image, annotations)
            cv2.imwrite(join(self.transform_images_root_path, file_name), rotated_image)
        save_json_file(self.coco_data.dataset, self.transform_annotation_file)


class Resize:
    """
    固定resize
    """
    def __init__(self, input_folder, output_folder, fixed_size=(512, 512)):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.fixed_size = fixed_size


    def resize_images(self):
        files = os.listdir(self.input_folder)
        with multiprocessing.Pool(8) as pool:
            list(tqdm(pool.imap(self.resize_image, 
            [(join(self.input_folder, file), join(self.output_folder, file)) for file in sorted(files) if file.endswith(".png")]),
             total=len(files), desc="resizing"))


    def resize_image(self, args):
        input_path, output_path = args
        image = cv2.imread(input_path)
        resized_image = cv2.resize(image, self.fixed_size)
        cv2.imwrite(output_path, resized_image)


class HorizontalFlip:
    """
    对于侧位数据做水平翻转
    """
    def __init__(self, images_folder):
        self.images_folder = images_folder

    
    def flip_image(self, file_name):
        img = cv2.imread(join(self.images_folder, file_name))
        flip_img = cv2.flip(img, 1)
        return flip_img


    def __call__(self):
        pass   
    
if __name__ == "__main__":
    # augmenter = RandomRotate(annotation_file="data/detection_dataset_small/detection_data.json", angle_range=(-180, 180))
    # augmenter()
    # transform = Resize(input_folder="/home/jjf/ITK/drr_utils/data/segmentation_dataset/LA/images",
    #                    output_folder="/home/jjf/ITK/drr_utils/data/segmentation_dataset/LA512/images",
    #                    fixed_size=(512, 512))
    # transform.resize_images()
    horizontalflip = HorizontalFlip("/home/jjf/ITK/drr_utils/data/segmentation_dataset/all512")
    flip_img = horizontalflip.flip_image("cao_fei_LA_L1_whole_17.png")
    cv2.imwrite("/home/jjf/ITK/drr_utils/data/segmentation_dataset/all512/flip.png", flip_img)