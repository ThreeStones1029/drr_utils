"""
this file will be used to generate dataset from paxray dataset
"""
import os
from io_tools.file_management import join, create_folder, load_json_file
import numpy as np
import cv2
from tqdm import tqdm
from detection_tools.coco_detection_data import COCODetectionData
from visual_tools.vis_coco_detection_bbox import VisCoCo


class PaxrayDataset(COCODetectionData):
    def __init__(self, annotation_file, images_folder, labels_folder, masks_folder, gt_bbox_json_path):
        """
        param images_folder: paxray数据集的X线片
        param labels_folder: paxray数据集的npy文件
        param catid2catname: paxray数据集的标签
        param choosed_catids: 选择的类别
        param masks_folder: 保存mask的文件夹
        param min_bbox_w_h: mask的最小框,小于这个大小的mask排除
        """
        super(PaxrayDataset, self).__init__()
        self.images_folder = images_folder
        self.labels_folder = labels_folder
        self.paxray_data = load_json_file(annotation_file)
        self.catid2catname = self.paxray_data["label_dict"]
        self.choosed_catids = ["41", "42", "43", "44", "45", "46", "47", "48", "49", "50"]
        self.masks_folder = create_folder(masks_folder)
        self.min_bbox_w_h = 512 * 0.05
        self.gt_bbox_json_path = gt_bbox_json_path


    def add_image(self, file_name):
        """
        重写继承的COCODetectionData的add_image方法
        """
        self.image_num += 1
        if "lateral" in file_name:
            APorLA = "LA"
        if "frontal" in file_name:
            APorLA = "AP"
        image = {"file_name":  file_name,
                 "id": self.image_num,
                 "APorLA": APorLA,
                 "width": 512,
                 "height": 512}
        self.images.append(image)


    def add_annotation(self, mask_file_name, category_name, bbox, iscrowd=0):
        """
        重写继承的OCODetectionData的add_annotation方法
        """
        self.annotation_num += 1
        category_id = self.catname2catid[category_name]
        annotation = {"mask_file_name": mask_file_name,
                      "id": self.annotation_num,
                      "image_id": self.image_num,
                      "category_id": category_id,
                      "category_name": category_name,
                      "bbox": bbox,
                      "iscrowd": iscrowd}
        self.annotations.append(annotation)


    def from_npy_files_export_masks(self):
        for npy_file_name in tqdm(os.listdir(self.labels_folder), desc="generate paxray dataset..."):
            self.from_npy_file_export_masks(join(self.labels_folder, npy_file_name))
        self.to_json(self.gt_bbox_json_path)
        

    def from_npy_file_export_masks(self, npy_file):
        data = np.load(npy_file)
        basename = os.path.basename(npy_file)
        basename_no_ext = basename.split(".")[0]
        image_name = basename_no_ext + ".png"
        self.add_image(image_name)
        for i in range(data.shape[0]):
            # 只需要留下腰椎与下胸椎T9-L6
            if str(i) in self.choosed_catids:
                catname = self.catid2catname[str(i)].capitalize()
                mask_file_name = basename_no_ext + "_" + catname + ".png"
                vis_save_path = join(self.masks_folder, mask_file_name)
                save_data = data[i].astype(np.uint8)
                bbox = self.get_bbox_from_mask(save_data)
                is_edge = self.whether_bbox_in_edge(bbox)
                # 判断是否为边界框
                if is_edge:
                    if bbox[2] > self.min_bbox_w_h and bbox[3] > self.min_bbox_w_h: 
                        mask = np.zeros_like(save_data, dtype=np.uint8)
                        mask[save_data != 0] = 255
                        cv2.imwrite(vis_save_path, mask)
                        self.add_annotation(mask_file_name, catname, bbox, iscrowd=0)
                else:
                    mask = np.zeros_like(save_data, dtype=np.uint8)
                    mask[save_data != 0] = 255
                    cv2.imwrite(vis_save_path, mask)
                    self.add_annotation(mask_file_name, catname, bbox, iscrowd=0)


    def get_bbox_from_mask(self, mask):
        """计算最小bbox"""
        points = cv2.findNonZero(mask)
        if points is not None:
            x, y, w, h = cv2.boundingRect(points)
            bbox = [int(x), int(y), int(w), int(h)]
        else:
            bbox = [0, 0, 0, 0]
        return bbox


    def whether_bbox_in_edge(self, bbox):
        """
        判断是否是边界框
        """
        if bbox[0] == 0 or bbox[1] == 1 or bbox[0] + bbox[2] == 512 or bbox[1] + bbox[3] == 512:
            return True
        else:
            return False


def main():
    dataset = PaxrayDataset("data/paxray/paxray_quarter.json", "data/paxray/images", "data/paxray/labels", "data/paxray/masks", "data/paxray/gt_bbox.json")
    dataset.from_npy_files_export_masks()
    detection_gt_vis = VisCoCo(annotation_file="data/paxray/gt_bbox.json", images_folder="data/paxray/images", bbox_vis_folder="data/paxray/gt_bbox_vis")
    detection_gt_vis.visualize_bboxes_in_images()


if __name__ == "__main__":
    main()
    