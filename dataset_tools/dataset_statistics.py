'''
Description: 
version: 
Author: ThreeStones1029 221620010039@qq.com
Date: 2023-12-31 17:13:53
LastEditors: ShuaiLei
LastEditTime: 2023-12-31 17:22:23
'''
import json


class DatasetStatistics:
    def __init__(self, annotation_file, save_json_file) -> None:
        self.annotation_file = annotation_file
        self.save_json_file = save_json_file
        self.dataset = self.load_json()
        self.dataset_info_statistics = dict()
        self.overall_information = dict()
        self.categories_number_information = dict()
        self.statistic()

    # 统计分析数据集
    def statistic(self):
        self.overall_information_statistic()
        self.categories_statistic()
        self.print_information()
        self.save_information()

    # 整体信息统计
    def overall_information_statistic(self):
        self.overall_information["images_num"] = len(self.dataset["images"])
        self.overall_information["annnotations_num"] = len(self.dataset["annotations"])
        self.overall_information["categories_num"] = len(self.dataset["categories"])
        self.dataset_info_statistics["Overall information"] = self.overall_information

    # 类别统计分析
    def categories_statistic(self):
        self.init_categories_number()
        for ann in self.dataset["annotations"]:
            self.categories_number_information[ann["category_name"]]["number"] += 1
        self.compute_proportion_of_categries()
        self.dataset_info_statistics["categories_information"] = self.categories_number_information


    # 初始化类别数量
    def init_categories_number(self):
        for cat in self.dataset["categories"]:
            cat_info = dict() # 注意字典初始化若在循环外面会统计所有类别数量，因为修改每个类别数量时修改的是同一个字典
            cat_info["number"] = 0
            self.categories_number_information[cat["name"]] = cat_info


    # 计算类别数量比例
    def compute_proportion_of_categries(self):
        for cat in self.dataset["categories"]:
            self.categories_number_information[cat["name"]]["ratio"] = self.categories_number_information[cat["name"]]["number"] / self.overall_information["annnotations_num"]*100


    def print_information(self):
        for key, value in self.dataset_info_statistics.items():
            print(key)
            print(value)


    # 保存信息
    def save_information(self):
        with open(self.save_json_file, "w") as f:
            json.dump(self.dataset_info_statistics, f)

    # 加载数据集文件
    def load_json(self):
        if type(self.annotation_file) == str:
            with open(self.annotation_file, "r") as f:
                dataset = json.load(f)
        return dataset
    
if __name__ == "__main__":
    DatasetStatistics(annotation_file="/home/jjf/Desktop/RT-DETR/rtdetr_paddle/datasets/New_ITK_Pre/annotations/detection_data.json",
                      save_json_file="/home/jjf/Desktop/RT-DETR/rtdetr_paddle/datasets/New_ITK_Pre/annotations/detection_data_statistic.json")