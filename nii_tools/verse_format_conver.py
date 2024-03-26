from logging import root
import os
import sys
import json
sys.path.insert(0, sys.path.append(os.path.dirname(sys.path[0])))
import SimpleITK as sitk
from tqdm import tqdm
import numpy as np
import shutil
from io_tools.file_management import get_sub_folder_paths, get_subfiles, load_json_file, join, create_folder, save_json_file


class VerseFormatConver:
    """
    用于将verse数据集格式转换为代码投影DRR所用格式
    """
    def __init__(self, root_path):
        self.root_path = root_path
        self.catid2catname = {1: "C1", 2: "C2", 3: "C3", 4: "C4", 5: "C5", 6: "C6", 7: "C7",
                              8: "T1", 9: "T2", 10: "T3", 11: "T4", 12: "T5", 13: "T6", 14: "T7", 15: "T8", 16: "T9", 17: "T10", 18: "T11", 19: "T12",
                              20: "L1", 21: "L2", 22: "L3", 23: "L4", 24: "L5", 25: "L6",
                              26: "sacrum", 27: "cocygis", 28: "T13"}

    
    def run(self):
        sub_folder_paths = get_sub_folder_paths(self.root_path) 
        for sub_folder_path in tqdm(sub_folder_paths, desc="convering"):
            self.single_ct_conver(sub_folder_path)
        

    def single_ct_conver(self, path):
        sub_folder_name = os.path.basename(path)
        nii_file_paths = get_subfiles(path, "_seg.nii.gz")
        json_paths = get_subfiles(path, ".json")
        if len(nii_file_paths) == 1:
            file_path = nii_file_paths[0]
            seg_image = sitk.ReadImage(file_path)
            cats_info = load_json_file(json_paths[0])
            # choosed = self.choose_lumbar_and_lower_thoracic_ct(cats_info)
            choosed = True # all ct will be choosed
            if choosed:
                for cat_info in cats_info:
                    if "label" in cat_info.keys():
                        catid = cat_info["label"]
                        catname = self.catid2catname[catid]
                        vertebrae_mask_array = sitk.GetArrayFromImage(seg_image==catid)
                        vertebrae_image = sitk.GetImageFromArray(vertebrae_mask_array)
                        vertebrae_image.SetSpacing(seg_image.GetSpacing())
                        vertebrae_image.SetOrigin(seg_image.GetOrigin())
                        vertebrae_image.SetDirection(seg_image.GetDirection())
                        vertebrae_image_save_path = join(path, catname + "_seg.nii.gz")
                        sitk.WriteImage(vertebrae_image, vertebrae_image_save_path)
                os.remove(file_path)
            else:
                print(sub_folder_name, "not lumbar or lower thoracic so don't need it!")
                shutil.rmtree(path)
        else:
            print("it has be processed!")


    def choose_lumbar_and_lower_thoracic_ct(self, cats_info):
        """
        选择腰椎和下胸椎的脊柱,保留腰椎骶化以及骶椎腰化CT。T13的排除
        """
        choosed = True
        for cat_info in cats_info:
            if "label" in cat_info.keys() and (cat_info["label"] <= 15 or cat_info["label"] >= 26):
                choosed = False
        return choosed


def check_root_folder(root_path):
    """
    整理verse2020数据集,对于子文件夹多个ct需要拆出来, 没有ct则删除该文件夹
    """
    sub_folder_paths = get_sub_folder_paths(root_path) 
    for sub_folder_path in tqdm(sub_folder_paths, desc="checking"):
        nii_file_paths = get_subfiles(sub_folder_path, ".nii.gz")
        if len(nii_file_paths) > 2:
            print(sub_folder_path, "exist multi cts")
            split_sub_folder(sub_folder_path)


def check_none_folder(root_path):
    sub_folder_paths = get_sub_folder_paths(root_path) 
    for sub_folder_path in tqdm(sub_folder_paths, desc="checking None folder"):
        nii_file_paths = get_subfiles(sub_folder_path, ".nii.gz")
        if len(nii_file_paths) == 0:
            print(sub_folder_path, "don't exist ct")
        if len(nii_file_paths) == 1:
            print("please check", sub_folder_path)


def split_sub_folder(sub_folder_path):
    """
    verse2020数据集,有的子文件夹保存的是同一个人的CT,需要单独将ct分开
    """
    root_folder = os.path.dirname(sub_folder_path)
    print(root_folder)
    for file_name in os.listdir(sub_folder_path):
        new_sub_folder_name = file_name.split("_")[1]
        print(new_sub_folder_name)
        new_sub_folder_path = join(root_folder, new_sub_folder_name)
        create_folder(new_sub_folder_path)
        new_file_name = file_name[9:]
        os.rename(join(sub_folder_path, file_name), join(sub_folder_path, new_file_name))
        shutil.copy(join(sub_folder_path, new_file_name), join(new_sub_folder_path, new_file_name))
    shutil.rmtree(sub_folder_path)


def rename_cts(root_path):
    """
    重新命名文件名字,让ct名字与子文件名字一样,方便生成数据
    """
    sub_folder_paths = get_sub_folder_paths(root_path) 
    for sub_folder_path in tqdm(sub_folder_paths, desc="renaming"):
        ct_folder_name = os.path.basename(sub_folder_path)
        for file in os.listdir(sub_folder_path):
            if file.endswith("seg.nii.gz"):
                new_file = ct_folder_name + "_seg.nii.gz"
            if file.endswith(".nii.gz") and "seg" not in file:
                new_file = ct_folder_name + ".nii.gz"
            if file.endswith(".png"):
                new_file = ct_folder_name + ".png"
            if file.endswith("w.png"):
                new_file = ct_folder_name + "_w.png"
            if file.endswith(".json"):
                new_file = ct_folder_name + ".json"
            os.rename(join(sub_folder_path, file), join(sub_folder_path, new_file))


def rename_verse2019_cts(root_path):
    """
    The function will used to rename verse2019 ct mask png json.
    """
    sub_folder_paths = get_sub_folder_paths(root_path) 
    for sub_folder_path in tqdm(sub_folder_paths, desc="renaming"):
        ct_folder_name = os.path.basename(sub_folder_path)
        for file in os.listdir(sub_folder_path):
            if file.endswith("ct.nii.gz"):
                new_file = ct_folder_name + ".nii.gz"
            if file.endswith("msk.nii.gz"):
                new_file = ct_folder_name + "_seg.nii.gz"
            if file.endswith(".png"):
                new_file = ct_folder_name + ".png"
            if file.endswith("w.png"):
                new_file = ct_folder_name + "_w.png"
            if file.endswith("ctd.json"):
                new_file = ct_folder_name + ".json"
            os.rename(join(sub_folder_path, file), join(sub_folder_path, new_file))


def ct_dataset_statistics(ct_dataset_path, statistics_information_json_path):
    """
    数据集CT椎体标签统计
    """
    # 初始化
    vertebrae_dataset_info = {"overall": {"number": 0, "categories": []}}
    sub_folder_paths = get_sub_folder_paths(ct_dataset_path) 
    for sub_folder_path in sub_folder_paths:
        for file in os.listdir(sub_folder_path):
            if file.endswith("seg.nii.gz"):
                catname = file.split("_")[0]
                vertebrae_dataset_info["overall"]["number"] += 1
                # 初始化这个类别的信息
                if catname not in vertebrae_dataset_info["overall"]["categories"]:
                    vertebrae_dataset_info["overall"]["categories"].append(catname)
                    vertebrae_dataset_info[catname] = {"category_name": catname,
                                                       "number": 1,
                                                       "percentage": 0}
                # 更新这个类别的信息
                else:
                    vertebrae_dataset_info[catname]["number"] += 1
                    vertebrae_dataset_info[catname]["percentage"] = vertebrae_dataset_info[catname]["number"] / vertebrae_dataset_info["overall"]["number"]
    save_json_file(vertebrae_dataset_info, statistics_information_json_path)


if __name__ == "__main__":
    # format_conver = VerseFormatConver("data/verse")
    # format_conver.run()
    # ct_dataset_statistics("data/verse", "data/verse/vertebrae_information.json")
    rename_verse2019_cts("data/verse2019")