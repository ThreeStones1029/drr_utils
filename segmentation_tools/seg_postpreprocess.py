import os
from PIL import Image
import numpy as np


class MasksPreprocess:
    def __init__(self, images_folder) -> None:
        self.images_folder = images_folder

    
    def conver_to0_255images(self):
        """把label转换为二值图像,也即只有0, 255两个值"""
        for root, dirs, files in os.walk(self.images_folder):
            for file in files:
                if file.endswith(".png"):
                    img = Image.open(os.path.join(root, file))
                    img_array = np.array(img)
                    binary_array = np.where(img_array == 0, 0, 255)
                    binary_img = Image.fromarray(binary_array.astype(np.uint8))
                    binary_img.save(os.path.join(root,  file))

    
    def check_channels_num(self):
        for root, dirs, files in os.walk(self.images_folder):
            for file in files:
                img = Image.open(os.path.join(root, file))
                print(file, " channels num = ", len(img.getbands()))


def postpreprocess_images(images_path):
    Data_preprocess = MasksPreprocess(images_path)
    Data_preprocess.conver_to0_255images()