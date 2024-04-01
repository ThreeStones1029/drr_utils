'''
Description: 
version: 
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-12-11 11:21:50
LastEditors: ShuaiLei
LastEditTime: 2024-03-30 10:55:38
'''
from datetime import datetime
from io_tools.file_management import load_json_file, save_json_file


class COCODetectionData:
    def __init__(self):
        self.info = {
            "description": "Spine Detection DataSet",
            "url": "https://github.com/ThreeStones1029",
            "version": "1.0",
            "year": datetime.now().year,
            "contributor": "ShuaiLei",
            "Date": datetime.today().strftime('%Y-%m-%d')
        }
        self.annotation_num = 0
        self.image_num = 0
        self.images = []
        self.categories = []
        self.annotations = []
        self.exist_ct_nii_names = {"AP": [], "LA": []}
        self.catid2catname = dict()
        self.catname2catid = dict()
        self.add_categories()

    def add_image(self, file_name, ct_name, APorLA, width, height, rotation, translation):
        self.image_num += 1
        image = {
                "id": self.image_num,
                "width": width,
                "height": height,
                "file_name": file_name,
                "ct_name": ct_name + ".nii.gz",
                "APorLA": APorLA,
                "rotation": rotation,
                "translation": translation
                }
        self.images.append(image)

    def add_categories(self):
        self.categories = [ {"id": 1,
                            "name": "L6",
                            "supercategory": "vertebrae"},
                            {"id": 2,
                            "name": "L5",
                            "supercategory": "vertebrae"},
                            {"id": 3,
                            "name": "L4",
                            "supercategory": "vertebrae"},
                            {"id": 4,
                            "name": "L3",
                            "supercategory": "vertebrae"},
                            {"id": 5,
                            "name": "L2",
                            "supercategory": "vertebrae"},
                            {"id": 6,
                            "name": "L1",
                            "supercategory": "vertebrae"},
                            {"id": 7,
                            "name": "T12",
                            "supercategory": "vertebrae"},
                            {"id": 8,
                            "name": "T11",
                            "supercategory": "vertebrae"},
                            {"id": 9,
                            "name": "T10",
                            "supercategory": "vertebrae"},
                            {"id": 10,
                            "name": "T9",
                            "supercategory": "vertebrae"}]
        
        for category in self.categories:
            self.catid2catname[category["id"]] = category["name"]
            self.catname2catid[category["name"]] = category["id"]
        

    def add_annotation(self, mask_file_name, category_id, category_name, bbox, rotation_bbox, iscrowd=0):
        self.annotation_num += 1
        annotation = {
            "mask_file_name": mask_file_name,
            "id": self.annotation_num,
            "image_id": self.image_num,
            "category_id": category_id,
            "category_name": category_name,
            "area": bbox[2] * bbox[3],
            "bbox": bbox,
            "segmentation": rotation_bbox,
            "iscrowd": iscrowd
        }
        self.annotations.append(annotation)

    def to_json(self, save_path):
        coco_data = {
            "info": self.info,
            "images": self.images,
            "categories": self.categories,
            "annotations": self.annotations
        }
        save_json_file(coco_data, save_path)

    def load_json(self, coco_annotations_file):
        coco_data = load_json_file(coco_annotations_file)
        self.info = coco_data["info"]
        self.images = coco_data["images"]
        self.categories = coco_data["categories"]
        self.annotations = coco_data["annotations"]
        self.image_num = len(self.images)
        self.annotation_num = len(self.annotations)
        for image_info in self.images:
            if image_info["APorLA"] == "AP" and image_info["ct_name"] not in self.exist_ct_nii_names["AP"]:
                self.exist_ct_nii_names["AP"].append(image_info["ct_name"])
            if image_info["APorLA"] == "LA" and image_info["ct_name"] not in self.exist_ct_nii_names["LA"]:
                self.exist_ct_nii_names["LA"].append(image_info["ct_name"])
