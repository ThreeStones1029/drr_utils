'''
Description: this file will be used to generate cut drr for Classification of spinal fracture.
version: 1.0
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-03-29 13:39:46
LastEditors: ShuaiLei
LastEditTime: 2024-03-29 13:57:23
'''
from io_tools.file_management import load_json_file
from pycocotools.coco import COCO


def crop_drrs(annotation_file, drr_images_folder, cut_images_folder):
    """
    The function will be used to cut images according the detection bbox.
    param: annotation_file: the detection annotation file.
    param: drr_images_folder: The drr images folder.
    param: cut_images_folder: The cut images folder.
    """
    dataset = load_json_file(annotation_file)
    gt = COCO(annotation_file)
    imgToAnns = gt.imgToAnns
    for image in gt.dataset["images"]:
        for ann in imgToAnns[image["id"]]:
            pass