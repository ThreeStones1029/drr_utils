<!--
 * @Descripttion: 
 * @version: 
 * @Author: ShuaiLei
 * @Date: 2023-12-06 11:21:07
 * @LastEditors: ShuaiLei
 * @LastEditTime: 2024-03-26 13:00:17
-->
---
layout:     post   				    # 使用的布局（不需要改）
title:      实例分割 				# 标题 
subtitle:   nnUnet分割X线片椎骨 #副标题
date:       2023-12-10 				# 时间
author:     BY ThreeStones1029 						# 作者
header-img: img/about_bg.jpg 	    #这篇文章标题背景图片
catalog: true 						# 是否归档
tags:	图像分割							#标签
---

[TOC]

# X线片分割
说明：本项目目的在于使用ITK投影DRR生成标注数据，目前已完成水平检测框、旋转框生成（coco格式），分割数据生成（可以与目标检测结合裁剪）
# 一.DRR检测分割关键点数据生成
## 1.1.检测数据生成
### 1.1.1.运行
~~~bash
python main_drr_detection_dataset.py -c config/detection_config.yml
~~~
### 1.1.2.参数解释
基本参数都保存在config/detection_config.yml.参数解释如下:
文件夹参数
~~~bash
ct_root_path: data/ct_mask (ct路径)
dataset_path: data/detection_dataset (生成的检测数据集路径)
dataset_images_path: data/detection_dataset/images (生成的drr路径)
dataset_masks_path: data/detection_dataset/masks (生成的每一节椎体mask的路径)
dataset_json_path: data/detection_dataset/detection_data.json (coco格式的检测框标注)
~~~
投影参数
~~~bash
projection_parameter:
  sdr: 500 放射源到投影平面距离一半
  height: 2000 默认生成的图片大小
  specific_height_list: {"chen_jing": 3000, "chen_min_hua": 2500, "hang_hui_fang": 1000, "wang_xing_di":1000, "xu_ye":3000, "zhang_jian_min":2500, "zhou_yuan_ying":1000} 手动指定某个CT生成图片大小
  delx: 0.25 像素之间距离
  threshold: 0 阈值
  AP_num_samples: 1 默认正位生成数量
  LA_num_samples: 1 默认侧位生成数量
  AP_rot_range_list: [[75, 105], [165, 195], [165, 195]] 正位随机角度范围
  AP_trans_range_list: [[-15, 15], [-15, 15], [-15, 15]] 正位随机移动范围
  LA_rot_range_list: [[-15, 15], [75, 105], [-15, 15]]   侧位随机角度范围
  LA_trans_range_list: [[-15, 15], [-15, 15], [-15, 15]] 侧位随机移动范围
  AP_bbox_label_type: big 正位标注框格式,一共两种,一种大框,一种小框 大框对每一节整个椎骨投影标注, small对每一节椎骨的椎体投影标注(body_seg.nii.gz)
  LA_bbox_label_type: big 侧位标注框格式,一共两种,一种大框,一种小框 大框对每一节整个椎骨投影标注, small对每一节椎骨的椎体投影标注(body_seg.nii.gz)
  min_bbox_percentage_of_height: 0.05 用于排除边缘小框,数值为最小的框的高占图片比例
~~~
可视化参数
~~~bash
vis_parameter:
  is_vis: True 是否可视化标注
  vis_save_path: data/detection_dataset/image_label_vis 生成的标注文件保存路径
~~~
### 1.1.3.断点生成
生成的json文件在每一例CT生成后都会自动保存,由于意外被终止或者主动打断可以继续生成,重新运行命令
~~~bash
python main_drr_detection_dataset.py -c config/detection_config.yml
~~~
PS:如果生成完毕想要重新生成更大的数据集,需要手动删除位于data/detection_dataset下的detection_data.json,否则会自动检测在json文件中的已经投影过的CT.
完善断点生成，主要增加判断侧位CT和正位CT,来适应分割部分代码（2024-1-6）
### 1.1.4.数据增强
主要是加入旋转的数据增强,考虑到旋转bbox会使bbox变的不紧贴,所以我们可以采取先旋转drr生成mask,这样得到的bbox就是紧贴的


## 1.2.分割数据集生成
### 1.2.1.运行
~~~bash
python main_drr_segmentation_dataset.py -c config/segmentation_config.yml
~~~
### 1.2.2.整体流程
~~~bash
第一步:根据情况是否需要代码生成椎弓根
第二步:对所有nii文件预处理,防止有分割的较小的物体投影影响真实mask的生成.主要椎弓根保留两块,其余物体保留一块
第三步:生成初始分割数据集
第四步：加载检测文件，可选择根据检测框或者mask来裁剪（本质一样，因为检测框就是由mask标注后生成的，预测的检测框基本会与mask重合）
第五步:裁剪生成最终数据集
第六步:选择是否可视化标注查看，可以可视化映射到整体文件
~~~
### 1.2.3.参数解释
基本参数都保存在config/segmentation_config.yml.参数解释如下:

~~~bash
data_root_path: data # 数据集根目录
ct_mask_path: data/ct_mask # ct以及分割mask文件夹
dataset_save_root_folder_name: segmentation_dataset # 生成的分割保存文件夹名字
APorLA_orientation: LA # AP LA all 选择生成正位或者侧位或者都生成
mask_categories: ["whole"] # whole body pedicle other 选择投影椎体、椎弓根、其他或者整体投影
nii_preproess: False # 是否对nii文件做预处理，去除小型的杂质对于投影mask影响
has_pedicle: True # 是否有椎弓根，可以使用这个来裁剪出椎弓根

# 3D to 2d parameter
projection_parameter:
  sdr: 500 # 射线源到投影平面距离的一半
  height: 2000 # 生成的drr默认大小
  specific_height_list: {"chen_jing": 3000, "chen_min_hua": 2500, "hang_hui_fang": 1000, "wang_xing_di": 1000, "xu_ye": 3000, "zhang_jian_min": 2500, "zhou_yuan_ying": 1000} # 制定某个ct生成的drr大小
  delx: 0.25 # 像素之间距离
  threshold: 0 # 投影阈值
  AP_num_samples: 2 # 单例默认正位生成数量
  LA_num_samples: 2 # 单例默认侧位生成数量
  AP_rot_range_list : [[90, 90], [170, 190], [180, 180]] # 正位投影角度范围
  AP_trans_range_list : [[-10, 10], [-10, 10], [-10, 10]] # 正位投影移动范围
  LA_rot_range_list: [[90, 90], [170, 190], [90, 90]] # 侧位投影角度范围
  LA_trans_range_list: [[-10, 10], [-10, 10], [-10, 10]] # 侧位投影移动范围


# Mode of clipping
cut_parameter:
  cut_mode: detection_bbox_center # mask_center detection_bbox_center 选择根据检测框裁剪或者根据mask裁剪
  run_object_detection: False # 是否运行目标检测
  detection_result_json_path: data/segmentation_dataset/LA/detection_result/bbox.json #目标检测结果
  AP_expand_coefficient: 1.5 # 正位框扩大倍数
  LA_expand_coefficient: 1.3 # 侧位框扩大倍数
  Minimum_width_relative_to_the_image: 0.15 # 自动过滤小框
  Minimum_height_relative_to_the_image: 0.15 # 自动过滤小框

vis_parameter:
  is_vis: True # 是否可视化标签
~~~

问题：目前发现还需要加入生成分割数据的时候加入框的标注，包括旋转框以及水平框，为了方便评估检测（2024-1-5）
解决：已完成加入生成分割数据的时候加入框的标注，同时优化断点生成时的image_id问题（2024-1-6）


## 1.3.标志点数据集生成


# 二、DRR目前检测分割结果
## 2.1.检测模型
### 2.1.1.已完成（水平框检测）2023-12-26
数据生成：以正位小框，侧位大框生成数据10000张，每一例CT生成正位100张，侧位100张，总共50例CT
数据增强：旋转360度随机
算法模型：RTDETR-50
数据集划分：训练集8000张，验证集1000张，测试集1000张
检测框标注：水平框
数据集标签分布：
迭代轮数：100
学习率：0.00025
batch_size: 8
训练时长：28小时
验证集：AP0.5:0.95 = 0.868
测试集： AP0.5: 0.95 = 0.864
分析：检测算法可以实现正侧位水平框检测，总体来说检测结果基本准确

### 2.1.2.待完成（旋转框检测）
数据生成：以正位小框，侧位大框生成数据10000张，每一例CT生成正位100张，侧位100张，总共50例CT
数据增强：旋转360度随机
算法模型：
数据集划分：训练集8000张，验证集1000张，测试集1000张
检测框标注：旋转框标注（代码已写完）
数据集标签分布：

## 2.2.分割模型
### 2.2.1.已完成
侧位数据生成：已整体投影生成1000张侧位DRR,每一例生成20张，总共50例数据，裁剪出5937张（检测框扩大1.3倍裁剪）。
算法模型：nnUnet
数据集划分：4000为训练集，1000张为验证集，937张为测试集
训练时长：1小时半
迭代轮数：150
初始学习率：0.01
存在问题1： 当前结果有待提升，主要在于裁剪图片较大时会分割到其他椎体
解决方法: 1、缩小裁剪框（尝试1.1倍），2、增加约束，3、实例分割，4、只分割椎体部分
存在问题2：nnUnet过于复杂，生成预处理占用硬盘空间大
解决方法：1、换成简单一点的网络
正位数据生成：已整体投影生成1000张正位DRR,每一例生成20张，总共50例数据，裁剪出5937张（检测框扩大1.5倍裁剪）。

## 2.3.检测与分割流程全自动流程
目前完成： 
1、重新优化检测与分割生成数据的代码结构与规范命名
2、将分割与检测串联起来
3、优化断点生成部分
4、编写完计算评估dice部分同时生成json评估结果文件以及dice柱状分布图（2024-01-08）
5、分割部分评估代码、评估dice、hausdorff distance、杰卡德系数、平均表面距离（2024-01-10）
6、多线程优化评估以及可视化部分（2024-01-11）
7、加入检测预测以及分割预测，不再需要手动分别运行（2024-01-15）

待完成：
1、检测评估部分代码
2、将检测与分割同时可视化到一张图上
3、裁剪部分多线程优化

## 2.4.需要改进的点
需要统一图片大小，分割网络输入图像需要统一大小，
（1）统一大小才能批次训练，加快训练效率
（2）由于全连接层的存在需要统一大小，FCN不需要是因为没有全连接层
（3）图片大小不能狭长，主要在于太窄的边多次下采样会损失信息
需要实验：
1、生成512*512大小的DRR和目前图片缩放到512*512的区别
测试后：人眼较难分别出来，可直接使用已生成的数据进行缩放
2、实验置零但是不裁剪的分割，以及裁剪后resize的分割
若需要统一resize,可以先测试置零训练，先resize再置零
再测试裁剪后resize训练
3、


# 三、检测分割预测评估可视化流程
## 3.1.参数介绍
### 3.1.1.生成文件的保存路径
dataset_parameter:
  root_path: "data/detection_segmentation/AP" # 测试的根目录
  images_folder: "images" # 生成的DRR路径
  masks_folder: "masks" # 对应的每一节的mask
  cut_images_folder: "cut_images" # 裁剪后DRR
  cut_masks_folder: "cut_masks" # 裁剪后的mask
  init_dataset_json: "init_dataset.json" # 初始数据集信息，记录DRR与mask对应关系
  cut_dataset_json: "cut_dataset.json" # 裁剪数据集信息，记录裁剪DRR与裁剪mask信息，以及裁剪位置坐标信息

检测参数
object_detection_parameter:
  run_object_detection: False # 是否运行目标检测

运行检测模型参数
  envs_path: "/home/jjf/anaconda3/envs/paddle/bin/python"
  detection_script_path: "/home/jjf/RT-DETR/rtdetr_paddle/tools/infer.py"
  config_path: "/home/jjf/RT-DETR/rtdetr_paddle/configs/rtdetr/rtdetr_r50vd_6x_coco.yml"

  infer_detection_result_folder: "detection_result" # 检测预测可视化
  infer_bbox_json: "bbox.json" # 检测预测标注信息
  gt_bbox_json: "gt_bbox.json" # 检测框GT标注信息
  gt_bbox_vis_folder: "gt_bbox_vis" # 真实水平框可视化
  gt_rotation_bbox_vis_folder: "gt_rotation_bbox_vis" # 真实旋转框可视化

裁剪参数
cut_parameter:
  has_gt_masks: False # 是否有真实mask
  cut_mode: detection_bbox_center # mask_center detection_bbox_center 裁剪方式，可根据投影mask或者检测结果裁剪
  AP_expand_coefficient: 1.9 # 正位扩大框倍数
  LA_expand_coefficient: 1.3 # 侧位扩大倍数
  Minimum_width_relative_to_the_image: 0.15 # 最小框相对图片大小，小于排除
  Minimum_height_relative_to_the_image: 0.15 # 最小框相对图片大小 小于排除

分割参数
segmentation_parameter:
  run_segmentation: True # 是否运行分割

  envs_path: "/home/jjf/anaconda3/envs/nnunet/bin/python"
  segmentation_script_path: "/home/jjf/nnUNet/nnunetv2/inference/predict_from_raw_data.py"
  input_folder: "input_seg"

  infer_segmentation_result_folder: "segmentation_result" # 分割预测mask
  infer_mask_in_cut_image_vis_folder: "infer_cut_mask_vis" # 分割预测mask可视化在裁剪图片上
  infer_mask_in_image_vis_folder: "infer_mask_vis" # 分割预测mask可视化在裁剪图片上
  gt_mask_in_cut_image_vis_folder: "gt_cut_mask_vis" # 分割真实mask可视化在裁剪图片上
  gt_mask_in_image_vis_folder: "gt_mask_vis" # 分割真实mask可视化在整张图片上

评估参数
eval_parameter:
  is_detection_eval: True # 是否评估检测
  is_segmentation_eval: True # 是否评估分割
  eval_result_save_json: "eval_result.json" # 评估结果保存路径


可视化参数
vis_parameter:
  is_vis_detection_gt: True # 是否可视化检测真实标注
  is_vis_detection_infer: True # 是否可视化检测预测标注
  is_vis_segmentation_gt: True # 是否可视化分割真实标注
  is_vis_segmentation_infer: True # 是否可视化分割预测标注
  is_gen_html: True # 是否生成可视化网页
## 3.1.对于drr数据流程测试完成，包括预测，评估，可视化
## 3.2.对于真实X线片流程代码编写完成，包括检测预测，可视化，分割预测，可视化，已完成跑通

# 四、MICCAI
## 4.1.local数据集实验
1、随机正位挑选500张与侧位500张（完成）
2、统一图片大小为512*512，减小配准资源消耗（完成缩小代码编写2024-01-23）
3、编写合并正侧位init_json代码
4、对于适应真实X线片需要对于侧位需要做随机左右翻转数据增强
5、预训练感觉是需要裁剪出与真实X线片大小的视野范围，目前不管是drr和BUU视野范围都远大于真实X线片，需要实验测试是否优于不裁剪预训练

## 4.2.verse2020生成DRR数据集
需要编写读取verse数据集代码，将完整seg文件单独取每一节（2024-01-30完成代码编写）
使用数据信息
CT数量：98例
椎体标签：T9-L6
生成图片大小：512*512
对比：相比医院数据，CT质量较差，投影不清楚

## 4.3.paxray数据集检测以及分割标注
编写代码读取paxray数据，生成检测以及分割标注
## 4.4.BUU数据集检测


# 五、verse2019生成骨折drr数据集以及标注
## 5.1.先筛选出数据集
目前筛选出来大概要33例数据
## 5.2.正常生成检测数据集标注

## 5.3.根据论文A Vertebral Segmentation Dataset with Fracture Grading附件中的对于椎体标注
修改正常的椎体标签为normal

修改骨折椎体标签为abnormal