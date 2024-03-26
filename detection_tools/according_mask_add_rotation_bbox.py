'''
Description: 
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-01-03 20:23:23
LastEditors: ShuaiLei
LastEditTime: 2024-01-03 20:40:09
'''
import os
import sys
sys.path.insert(0, sys.path.append(os.path.dirname(sys.path[0])))
from drr_tools.drr_image_postprocess import compute_min_rotation_bbox_coverage_mask
from io_tools.file_management import save_json_file, join
from pycocotools.coco import COCO


def insert_text_to_filename(original_filename, insert_text):
    # 获取文件名和扩展名
    root, ext = os.path.splitext(original_filename)
    # 分割文件名和数字部分
    name_parts = root.rsplit('_', 1)
    # 在最后一个下划线后插入文本
    new_filename = f"{name_parts[0]}_{insert_text}_{name_parts[1]}{ext}"
    return new_filename


def add_rotation_bboxes(masks_folder_path, detection_data_json_path):
    """
    根据mask添加旋转框,主要为了防止没有加这个标注
    """
    gt = COCO(detection_data_json_path)

    catid2catname = {}
    for category in gt.dataset["categories"]:
        catid2catname[category["id"]] = category["name"]

    for ann in gt.dataset["annotations"]:
        if "mask_file_name" not in ann.keys():
            category_id = ann["category_id"]
            category_name = catid2catname[category_id]
            image_name = gt.imgs[ann["image_id"]]["file_name"]
            if gt.imgs[ann["image_id"]]["APorLA"] == "LA":
                insert_text = category_name
            else:
                insert_text = category_name + "_body"
            mask_file_name = insert_text_to_filename(image_name, insert_text)
            mask_path = join(masks_folder_path, mask_file_name)
            min_area_rect = compute_min_rotation_bbox_coverage_mask(mask_path)
            ann["segmentation"] = min_area_rect
            ann["mask_file_name"] = mask_file_name
            ann["category_name"] = category_name
        else:
            mask_path = join(masks_folder_path, ann["mask_file_name"])
            min_area_rect = compute_min_rotation_bbox_coverage_mask(mask_path)
            ann["segmentation"] = min_area_rect
        print(mask_path, "add rotate bbox successfully")
    save_json_file(gt.dataset, detection_data_json_path)


def from_masks_add_bbox_and_rotate_bbox_to_json():
    """
    this file will be used to gen json file about bbox and rotate bbox information from masks.
    由于之前生成的分割数据没有生成gt bbox以及rotate bbox,则从生成的mask来生成相应bbox标注
    """

if __name__ == "__main__":
    add_rotation_bboxes("data/detection_dataset2/masks", "data/detection_dataset2/detection_data_copy.json")