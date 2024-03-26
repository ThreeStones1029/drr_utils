'''
Descripttion: this file in order to show GT and Result bboxes in a html.
version: 
Author: ShuaiLei
Date: 2024-1-6 21:43:40
LastEditors: ShuaiLei
LastEditTime: 2024-1-6 21:50:25
'''
from dominate import document
from dominate.tags import div, img, h3, span
import os
from glob import glob
from io_tools.file_management import join


class GenHtmlVis:
    def __init__(self):
        pass

    def create_html(self, gt_images_folder, infer_images_folder, html_path):
        images_path = self.gen_images_path(gt_images_folder, infer_images_folder)
        self.gen_gt_infer_html(images_path, html_path)


    def gen_images_path(self, gt_images_folder, infer_images_folder):
        # 将图片路径加入到列表
        images_path = []
        gt_files_path = glob(join(gt_images_folder, "*.png"))
        for file_path in gt_files_path:
            file_name = os.path.basename(file_path)
            gt_file_path = os.path.abspath(file_path)
            infer_file_path = os.path.abspath(join(infer_images_folder, file_name))
            images_path.append({"gt": gt_file_path, "infer": infer_file_path})
        return images_path


    def gen_gt_infer_html(self, images_path, html_path):
        doc = document(title="Gt and Infer")
        with doc:
            with div(style="display: flex"):
                with div(style="flex: 1; text-align:center"):
                    h3("GT")
                    for i, path in enumerate(images_path, start=1):
                        img(src=path['gt'], style="max-width: 90%")
                        with h3():
                            span(f"Image {i}", ":", style="color: red")
                            span(os.path.basename(path['gt']))

                with div(style="flex: 1; text-align:center"):
                    h3("Infer")
                    for i, path in enumerate(images_path, start=1):
                        img(src=path['infer'], style="max-width: 90%") 
                        with h3():
                            span(f"Image {i}", ":", style="color: red")
                            span(os.path.basename(path['infer']))   

        with open(html_path, "w") as f:
            f.write(doc.render())