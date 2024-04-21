from pycocotools.coco import COCO
from glob import glob
import os
import numpy as np
import multiprocessing
from multiprocessing import Process
from PIL import Image, ImageOps, ImageDraw, ImageFont
from io_tools.file_management import create_folder, join
from tqdm import tqdm
import time


class VisCoCo(COCO):
    def __init__(self, annotation_file, images_folder, bbox_vis_folder=None, rotate_bbox_vis_folder=None):
        super(VisCoCo, self).__init__(annotation_file)
        assert images_folder is not None , "{} is None".format(images_folder)
        self.images_folder = images_folder
        assert bbox_vis_folder is not None , "{} is None".format(bbox_vis_folder)
        if bbox_vis_folder:
            create_folder(bbox_vis_folder)
        if rotate_bbox_vis_folder:
            create_folder(rotate_bbox_vis_folder)
        self.bbox_vis_folder = bbox_vis_folder
        self.rotate_bbox_vis_folder = rotate_bbox_vis_folder
        self.file_name2img_id, self.img_id2file_name = dict(), dict()
        self.categories_id2name, self.categories_name2id = dict(), dict()
        self.cat_name_cat_id()
        self.file_name_img_id()
        self.draw_text = True
        self.fontsize = 40
        if self.draw_text:
            try:
                self.font = ImageFont.truetype('arial.ttf', self.fontsize)
            except IOError:
                self.font = ImageFont.load_default(size=self.fontsize)


    def visualize_bboxes_in_images(self):
        """
        多张图片可视化水平框
        """
        files_path = self.get_files_path()
        vis = []
        for i in tqdm(range(len(sorted(files_path))), total=len(files_path), desc="vis bbox"):
            if  os.path.basename(files_path[i]) in self.file_name2img_id.keys():
                vis.append(Process(target=self.visualize_bboxes_in_image, args=(files_path[i],)))
                vis[i].start()
        for i in range(len(sorted(files_path))):
            if  os.path.basename(files_path[i]) in self.file_name2img_id.keys():
                vis[i].join()
        

    def visualize_bboxes_in_image(self, file_path):
        """
        单张图片可视化水平框
        """
        file_name = os.path.basename(file_path)
        image_id = self.file_name2img_id[file_name]
        save_image_path = join(self.bbox_vis_folder, file_name)
        image_info = self.loadImgs(image_id)[0]
        file_name = image_info['file_name']
        img_path = join(self.images_folder, file_name)
        image = Image.open(img_path).convert('RGB')
        image = ImageOps.exif_transpose(image)
        # 获取这张图片的ann
        ann_ids = self.getAnnIds(imgIds=image_id)
        annotations = self.loadAnns(ann_ids)
        # 可视化
        image = self.draw_bbox(image, annotations)
        # 保存
        self.save_result(save_image_path, image)


    def draw_bbox(self, image, annotations):
        """
        Draw bbox on image 分别可视化bbox和label是为了文字不被挡住
        """
        draw = ImageDraw.Draw(image)
        for ann in annotations:
            bbox = ann['bbox']
            # draw bbox
            if len(bbox) == 4:
                # draw bbox
                xmin, ymin, w, h = bbox
                xmax = xmin + w
                ymax = ymin + h
                draw.line(
                    [(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin),
                    (xmin, ymin)],
                    width=2,
                    fill='red')
            else:
                print('the shape of bbox must be [M, 4]')

        for ann in annotations:
            catid, bbox = ann['category_id'], ann['bbox']
            xmin, ymin, w, h = bbox
            # draw label
            if self.categories_id2name:
                text = "{} ".format(self.categories_id2name[catid])
            else:
                catname = ann['category_name']
                text = "{}".format(catname)
            # tw, th = draw.textsize(text)
            left, top, right, bottom = draw.textbbox((0, 0), text, font=self.font)
            tw, th = right - left, bottom - top
            #label框
            draw.rectangle([(xmin + 1, ymin + 1), (xmin + tw + 1, ymin + th + 1 + 10)], fill='white') 
            # draw.rectangle([(xmin + 1, ymin - th), (xmin + tw + 1, ymin)], fill = color)
            # label文字 
            # (xmin + 1, ymin - th)
            draw.text((xmin + 1, ymin + 1), text, fill='red', font=self.font) 
            # draw.text((xmin + 1, ymin - th), text, fill=(255, 255, 255))
        return image
    

    def visualize_rotate_bboxes_in_images(self):
        """
        多张图片可视化旋转框
        """
        files_path = self.get_files_path()
        vis = []
        for i in tqdm(range(len(sorted(files_path))), total=len(files_path), desc="vis rotation bbox"):
            if  os.path.basename(files_path[i]) in self.file_name2img_id.keys():
                vis.append(Process(target=self.visualize_rotate_bboxes_in_image, args=(files_path[i],)))
                vis[i].start()
        for i in range(len(sorted(files_path))):
            if  os.path.basename(files_path[i]) in self.file_name2img_id.keys():
                vis[i].join()


    def visualize_rotate_bboxes_in_image(self, file_path):
        """
        单张图片可视化旋转框
        """
        file_name = os.path.basename(file_path)
        image_id = self.file_name2img_id[file_name]
        save_image_path = join(self.rotate_bbox_vis_folder, file_name)
        image_info = self.loadImgs(image_id)[0]
        file_name = image_info['file_name']
        img_path = join(self.images_folder, file_name)
        image = Image.open(img_path).convert('RGB')
        image = ImageOps.exif_transpose(image)
        # 获取这张图片的ann
        ann_ids = self.getAnnIds(imgIds=image_id)
        annotations = self.loadAnns(ann_ids)
        # 可视化
        image = self.draw_rotate_bbox(image, annotations)
        # 保存
        self.save_result(save_image_path, image)


    def draw_rotate_bbox(self, image, annotations):
        """
        Draw bbox on image 分别可视化bbox和label是为了文字不被挡住
        """
        draw = ImageDraw.Draw(image)
        for ann in annotations:
            rotate_bbox = ann['segmentation']
            # draw rotate_bbox
            if len(rotate_bbox[0]) == 8:
                # draw bbox
                x1, y1 = rotate_bbox[0][0], rotate_bbox[0][1]
                x2, y2 = rotate_bbox[0][2], rotate_bbox[0][3]
                x3, y3 = rotate_bbox[0][4], rotate_bbox[0][5]
                x4, y4 = rotate_bbox[0][6], rotate_bbox[0][7]
                draw.line([(x1, y1), (x2, y2), (x3, y3), (x4, y4),(x1, y1)], width=2, fill='red')
            else:
                print('the shape of rotation bbox shape must be [1, 8]')

        for ann in annotations:
            catid, rotate_bbox = ann['category_id'], ann['segmentation']
            # rect_points = np.array([[rotate_bbox[0][0], rotate_bbox[0][1]],
            #                         [rotate_bbox[0][2], rotate_bbox[0][3]],
            #                         [rotate_bbox[0][4], rotate_bbox[0][5]],
            #                         [rotate_bbox[0][6], rotate_bbox[0][7]]])
            # (xmin, ymin) = np.min(rect_points, axis=0)
            xmin, ymin = rotate_bbox[0][0], rotate_bbox[0][1]
            # draw label
            if self.categories_id2name:
                text = "{} ".format(self.categories_id2name[catid])
            else:
                catname = ann['category_name']
                text = "{}".format(catname)
            # tw, th = draw.textsize(text)
            left, top, right, bottom = draw.textbbox((0, 0), text, font=self.font)
            tw, th = right - left, bottom - top
            #label框
            draw.rectangle([(xmin + 1, ymin + 1), (xmin + tw + 1, ymin + th + 1 + 10)], fill='white') 
            # draw.rectangle([(xmin + 1, ymin - th), (xmin + tw + 1, ymin)], fill = color)
            # label文字 
            # (xmin + 1, ymin - th)
            draw.text((xmin + 1, ymin + 1), text, fill='red',font=self.font) 
            # draw.text((xmin + 1, ymin - th), text, fill=(255, 255, 255))
        return image
    

    def save_result(self, save_path, image):
        """
        save visual result 
        """
        image.save(save_path, quality=95)     
        # print("coco bbox visual results save in {}".format(save_path))

    
    def file_name_img_id(self):
        """
        gen file_name2img_id dict
        """
        for img in self.dataset['images']:
            self.file_name2img_id[img['file_name']] = img['id']
            self.img_id2file_name[img['id']] = img['file_name']


    def get_files_path(self):

        exts = ['jpg', 'jpeg', 'png', 'bmp']
        files_path = set()
        for ext in exts:
            files_path.update(glob('{}/*.{}'.format(self.images_folder, ext)))
        files_path = list(files_path)
        assert len(files_path) > 0, "no image found in {}".format(files_path)
        return files_path
    

    def cat_name_cat_id(self):
        if "categories" in self.dataset.keys():
            for cat in self.dataset["categories"]:
                self.categories_id2name[cat['id']] = cat["name"]
                self.categories_name2id[cat['name']] = cat["id"]

