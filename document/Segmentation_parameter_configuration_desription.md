<!--
 * @Description: Segmentation parameters
 * @version: 
 * @Author: ThreeStones1029 2320218115@qq.com
 * @Date: 2024-03-30 06:37:52
 * @LastEditors: ShuaiLei
 * @LastEditTime: 2024-03-30 06:55:30
-->
# The basic parameters are stored in config/segmentation_config.yml.The parameters are explained as follows
# 1.Default configuration
~~~bash
data_root_path: data 
ct_mask_path: data/verse2020 
dataset_save_root_folder_name: verse2020_segmentation_dataset 
APorLA_orientation: all 
mask_categories: ["whole"] 
nii_preproess: False 
has_pedicle: True 

projection_parameter:
  sdr: 500 
  height: 512 
  specific_height_list: {"example1": 3000, "example2": 2500, }
  delx: 1 
  threshold: 0 
  AP_num_samples: 1 
  LA_num_samples: 1 
  AP_rot_range_list : [[90, 90], [170, 190], [180, 180]] 
  AP_trans_range_list : [[-10, 10], [-10, 10], [-10, 10]] 
  LA_rot_range_list: [[90, 90], [170, 190], [90, 90]] 
  LA_trans_range_list: [[-10, 10], [-10, 10], [-10, 10]] 

cut_parameter:
  cut_mode: mask_center 
  run_object_detection: False 
  detection_result_json_path: data/verse2020_segmentation_dataset/all/detection_result/bbox.json 
  AP_expand_coefficient: 1.5 
  LA_expand_coefficient: 1.3 
  Minimum_width_relative_to_the_image: 0.15 
  Minimum_height_relative_to_the_image: 0.15 

vis_parameter:
  is_vis: True 
~~~

# 2.Detailed description
## 2.1.main parameters
* **data_root_path:** data root folder
* **ct_mask_path:** ct root folder
* **dataset_save_root_folder_name:** The generated dataset save path
* **APorLA_orientation:** Choose to generate frontal or lateral or both(AP or LA or all)
* **mask_categories:** Choose to project the vertebral body, pedicle, other, or entire vertebrae(whole or body pedicle other )
* **nii_preproess:** Whether the nii file is preprocessed to avoid the imperfect segmentation mask
* **has_pedicle:** Whether the dataset has a pedicle or not, you can use this to get the pedicle part by subtracting the vertebral body and other parts of the vertebrae

## 2.2.projection_parameter
* **sdr:** as detection project parameter
* **height:** as detection project parameter
* **specific_height_list:** as detection project parameter
* **delx:** as detection project parameter
* **threshold:** as detection project parameter
* **AP_num_samples:** as detection project parameter
* **LA_num_samples:** as detection project parameter
* **AP_rot_range_list:** as detection project parameter
* **AP_trans_range_list:** as detection project parameter
* **LA_rot_range_list:** as detection project parameter
* **LA_trans_range_list:** as detection project parameter

## 2.3.cut_parameter
* **cut_mode:** Select crop by detection box or crop by mask(mask_center or detection_bbox_center)
* **run_object_detection:** Whether to run object detection, if yes, it can be cut according to the object detection result prediction box, otherwise it can be cut according to the projection mask
* **detection_result_json_path:** The result of object detection
* **AP_expand_coefficient:** It is necessary to enlarge the box of the AP images prediction by a certain factor of cutting
* **LA_expand_coefficient:** It is necessary to enlarge the box of the LA images prediction by a certain factor of cutting
* **Minimum_width_relative_to_the_image:** This parameter indicates the proportion of the image with the smallest value and is used to exclude small boxes at the edges of the image.
* **Minimum_height_relative_to_the_image:** This parameter indicates the proportion of the image with the smallest value and is used to exclude small boxes at the edges of the image.

## 2.4.vis_parameter
* **is_vis:** Whether or not to visualize labels