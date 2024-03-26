'''
Description: This document is used to cut large folders because Baidu Net disk can only upload 500 files at a time.
version: 
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-12-15 20:01:51
LastEditors: ShuaiLei
LastEditTime: 2023-12-17 16:43:29
'''
import os
import shutil
from io_tools.file_management import join


def split_images_to_subfolder(source_folder, base_destination_folder):
    # 每个子文件夹中的图片数量
    images_per_folder = 500

    # 获取源文件夹中的所有图片文件
    image_files = [f for f in os.listdir(source_folder) if f.endswith(".png") or f.endswith(".jpg")]

    # 创建多个目标文件夹
    subfolder_num = (len(image_files) // images_per_folder) + (1 if len(image_files) % images_per_folder != 0 else 0)
    for i in range(1, subfolder_num + 1):
        destination_folder = join(base_destination_folder, f"destination_folder_{i}")
        os.makedirs(destination_folder, exist_ok=True)

    # 分组复制图片到每个子文件夹
    for i, start in enumerate(range(0, len(image_files), images_per_folder)):
        end = start + images_per_folder
        image_group = image_files[start:end]

        destination_folder = join(base_destination_folder, f"destination_folder_{i + 1}")
        for image_file in image_group:
            source_path = join(source_folder, image_file)
            destination_path = join(destination_folder, image_file)
            shutil.copy2(source_path, destination_path)

    print("复制完成。")

if __name__ == "__main__":
    split_images_to_subfolder("data/detection_dataset/images", "data/detection_dataset")