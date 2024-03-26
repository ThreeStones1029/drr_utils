import os
import sys
sys.path.insert(0, os.path.dirname(sys.path[0]))
import random
import cv2
from tqdm import tqdm
from io_tools.file_management import load_json_file, join
from transforms_tools.transforms import HorizontalFlip
from segmentation_tools.init_segmentation_json import InitSegmentationDatasetJsonTools


def random_horizontal_flip_images_and_masks(init_dataset_json_path, images_folder, masks_folder, flip_probability):
    """
    随机水平翻转侧位image和mask
    """
    image_horizontal_flip = HorizontalFlip(images_folder)
    mask_horizontal_flip = HorizontalFlip(masks_folder)
    init_json = InitSegmentationDatasetJsonTools(init_dataset_json_path)
    init_dataset = load_json_file(init_dataset_json_path)
    flipped_num = 0
    for image in tqdm(init_dataset["images"], desc="random horizontal flipping"):
        if image["AP_or_LA"] == "LA" and random.random() >= flip_probability:
            flipped_num += 1
            flipped_image = image_horizontal_flip.flip_image(image["image_name"])
            cv2.imwrite(join(images_folder, image["image_name"]), flipped_image)
            masks = init_json.Imageid2Masks[image["id"]]
            for mask in masks:
                flip_mask = mask_horizontal_flip.flip_image(mask["mask_name"])
                cv2.imwrite(join(masks_folder, mask["mask_name"]), flip_mask)
    print("flipped image num: ", flipped_num)


if __name__ == "__main__":
    random_horizontal_flip_images_and_masks("data/segmentation_dataset/all512/all512_init_dataset.json",
                                            "data/segmentation_dataset/all512/images",
                                            "data/segmentation_dataset/all512/masks",0.5)