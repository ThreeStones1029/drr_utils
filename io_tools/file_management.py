'''
Descripttion: 
version: 
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-12-10 14:04:34
LastEditors: ShuaiLei
LastEditTime: 2024-03-27 02:33:38
'''
import os
import platform
from glob import glob
import re
import shutil
import yaml
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class dotdict(dict):
    """
    Dict subclass that allows dot.notation to access attributes.
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def create_folder(path):
    os.makedirs(path, exist_ok=True)
    return path

def join(*args):
    return os.path.join(*args)


def load_json_file(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    return data


def save_json_file(data, json_path):
    dirname = os.path.dirname(json_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(json_path, 'w') as f:
        json.dump(data, f)
    print(json_path, "save successfully")


def load_config_file(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def rename_files(root_folder):
    cat_id2cat_name = {14: "T8", 15: "T9", 16: "T10", 17: "T11", 18: "T12", 19: "L1", 20: "L2", 21: "L3", 22: "L4", 23: "L5"}
    sub_folder_name_list = os.listdir(root_folder)
    for sub_folder_name in  sub_folder_name_list:
        resampled_nii_files = glob(join(root_folder, sub_folder_name, "*resampled.nii.gz"))
        for resampled_nii in resampled_nii_files:
            basename = os.path.basename(resampled_nii)
            cat_id = int(re.findall(r'\d+', basename)[0])
            cat_name = cat_id2cat_name[cat_id]
            os.rename(resampled_nii, join(root_folder, sub_folder_name, cat_name + "_seg.nii.gz"))
            print(join(root_folder, sub_folder_name, cat_name + "_seg.nii.gz"), "rename successfully")


def linux_windows_split_name(path):
    if platform.system().lower() == "linux":
        name = path.split("/")[-1]
    else:
        name = path.split("\\")[-1]
    return  name


def get_sub_folder_paths(root_folder):
    sub_folder_paths = []
    sub_folder_names = os.listdir(root_folder)
    for sub_folder_name in sub_folder_names:
        if os.path.isdir(join(root_folder, sub_folder_name)):
            sub_folder_paths.append(join(root_folder, sub_folder_name))
    return sub_folder_paths


def get_subfiles(image_folder, suffix=None, sort=True):
    """
    get all png files in folder
    """
    imgs_path = glob(join(image_folder, "*" + suffix)) 
    if sort:
        imgs_path.sort()
    return imgs_path


def subtract_whole_in_suffix(images_folder):  
    for root, dirs, files in os.walk(images_folder):
        for filename in files:
            # 通过正则表达式匹配文件名中的部分
            match = re.match(r'^(.+?)_whole_(\d+)\.png$', filename)
            if match:
                # 获取匹配的部分
                prefix = match.group(1)
                number = match.group(2)
                # 构建新的文件名
                new_filename = f"{prefix}_{number}.png"
            else:
                new_filename = filename
            os.rename(os.path.join(root, filename),os.path.join(root, new_filename))
    

def add_0000_in_suffix(images_folder):
    for root, dirs, files in os.walk(images_folder):
        for file in files:
            new_file_name = file.split(".")[0] + "_0000" + ".png"
            os.rename(os.path.join(root, file),os.path.join(root, new_file_name))


def add_whole_in_suffix(images_folder):
    for root, dirs, files in os.walk(images_folder):
        for file in files:
            if file.endswith(".png"):
                new_file_name = file[:-len(file.split("_")[-1])]+ "whole_" + file.split("_")[-1]
                os.rename(os.path.join(root, file),os.path.join(root, new_file_name))

def add_whole_in_file_suffix(file_name):
    new_file_name = file_name[:-len(file_name.split("_")[-1])]+ "whole_" + file_name.split("_")[-1]
    return new_file_name

def copy_folder(input_folder, output_folder):
    for file in os.listdir(input_folder):
        shutil.copy(join(input_folder, file), join(output_folder, file))


def delete_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            os.remove(join(root, file))


def load_npy_file(npy_file):
    data = np.load(npy_file)
    print(data.shape)
    for i in range(data.shape[0]):
        plt.imshow(data[i, :, :], cmap='viridis')
        plt.axis('off')
    # plt.savefig(vis_save_path, bbox_inches='tight', pad_inches=0.0)
        plt.show()


if __name__ == "__main__":
    load_npy_file("data/paxray/labels/RibFrac9lateral.npy")
    