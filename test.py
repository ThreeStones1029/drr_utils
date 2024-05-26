'''
Description: 
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-03-23 07:14:28
LastEditors: ShuaiLei
LastEditTime: 2024-05-24 01:26:53
'''
import cv2
import numpy as np
import matplotlib.pyplot as plt
from drr_tools.genDRR import genDRR
from visual_tools.vis_coco_detection_bbox import VisCoCo


def test(origin_image_path, mask_path, cut_bbox_coordinate, save_path):
    origin_image = cv2.imread(origin_image_path)
    image_shape = origin_image.shape
    print(image_shape)
    overall_mask = np.zeros((600, 600), dtype=np.uint8)
    cut_mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    overall_mask[cut_bbox_coordinate[1]: cut_bbox_coordinate[3], cut_bbox_coordinate[0]: cut_bbox_coordinate[2]] = cut_mask
    cv2.imwrite(save_path, overall_mask)

# test("/home/jjf/ITK/drr_utils/data/test/images/weng_gt_drr_600x600.png",
#     "/home/jjf/ITK/drr_utils/data/test/segmentation_result/weng_gt_drr_L2_600x600.png",
#     [4,8,437,303],
#     "/home/jjf/ITK/drr_utils/data/test/weng_gt_drr_L2_600x600.png")

def gen_512_512_drr(sdr, ctDir):
    height = 512
    delx = 1
    threshold = 0
    rotation = [90, 180, 180]
    translation = [0, 0, 0]
    saveIMG = "test" + str(sdr) + ".png"
    genDRR(sdr, height, delx, threshold, rotation, translation, ctDir, saveIMG)


def gen_2000_2000_resize512_512(sdr, ctDir):
    height = 2000
    delx = 0.25
    threshold = 0
    rotation = [90, 180, 180]
    translation = [0, 0, 0]
    saveIMG = "test_resize.png"
    genDRR(sdr, height, delx, threshold, rotation, translation, ctDir, saveIMG)

    image = cv2.imread(saveIMG)
    resized_image = cv2.resize(image, (512, 512))
    cv2.imwrite(saveIMG, resized_image)

def show_drr(ctDir):
    gen_512_512_drr(400, ctDir)
    gen_512_512_drr(500, ctDir)
    gen_512_512_drr(582, ctDir)

    img400 = cv2.imread("test400.png", cv2.IMREAD_GRAYSCALE)
    img500 = cv2.imread("test500.png", cv2.IMREAD_GRAYSCALE)
    img582 = cv2.imread("test582.png", cv2.IMREAD_GRAYSCALE)

    plt.figure()
    plt.subplot(1, 3, 1)
    plt.imshow(img400, cmap=plt.cm.gray), plt.axis("off"), plt.title("sdr400")
    plt.subplot(1, 3, 2)
    plt.imshow(img500, cmap=plt.cm.gray), plt.axis("off"), plt.title("sdr500")
    plt.subplot(1, 3, 3)
    plt.imshow(img582, cmap=plt.cm.gray), plt.axis("off"), plt.title("sdr582")
    plt.show()





if __name__ == "__main__":
    # gen_512_512_drr()
    # gen_2000_2000_resize512_512(500, "/home/jjf/ITK/drr_utils/data/ct_mask/zhang_guo_quan/zhang_guo_quan.nii.gz")
    # show_drr("/home/jjf/ITK/drr_utils/data/ct_mask/zhang_guo_quan/zhang_guo_quan.nii.gz")
    # VisCoCo(annotation_file="data/S0000328_example/voc.json", 
    #         images_folder="data/S0000328_example/JPEGImages",
    #         bbox_vis_folder="data/S0000328_example/vis").visualize_bboxes_in_images()
    import matplotlib.pyplot as plt

    plt.plot(range(10))
    plt.show()
