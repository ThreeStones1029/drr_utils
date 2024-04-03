<!--
 * @Description: 
 * @version: 
 * @Author: ThreeStones1029 2320218115@qq.com
 * @Date: 2024-03-29 07:33:58
 * @LastEditors: ShuaiLei
 * @LastEditTime: 2024-04-03 01:45:48
-->
# Spine Dataset Prepare.
## 1.Download
Spine Dataset
* [verse2019 and verse2020](https://github.com/anjany/verse)

* [CTSpine1K](https://github.com/MIRACLE-Center/CTSpine1K)

## 2.Generate CT Dataset(Separate mask dataset format)
### 2.1.1.init dataset format.
~~~bash
├── verse2019
    ├── sub-verse012
    │   ├── sub-verse012_ct.nii.gz
    │   ├── sub-verse012_seg-subreg_ctd.json
    │   ├── sub-verse012_seg-vert_msk.nii.gz
    │   └── sub-verse012_seg-vert_snp.png
    ├── sub-verse013
    │   ├── sub-verse013_ct.nii.gz
    │   ├── sub-verse013_seg-subreg_ctd.json
    │   ├── sub-verse013_seg-vert_msk.nii.gz
    │   └── sub-verse013_seg-vert_snp.png
    └── sub-verse014
        ├── sub-verse014_ct.nii.gz
        ├── sub-verse014_seg-subreg_ctd.json
        ├── sub-verse014_seg-vert_msk.nii.gz
        └── sub-verse014_seg-vert_snp.png
~~~
### 2.1.2.check Dataset.
The verse dataset has some subfolders that are empty, some subfolders that have multiple CTS, and some subfolders that only have CT without mask.
~~~bash
python nii_tools/verse_check_images.py
~~~
* (1) Delete empty sub folders directly.
* (2) Delete only one nii.gz sub folders directly.
* (3) Manually divide subfolders containing multiple CTs.

### 2.1.3. Rename subfolder.
The CT and the ct mask need to be renamed for use easy.
~~~bash
python nii_tools/verse_rename_images.py
~~~

### 2.1.4. Reoriented ct and ct mask.
In order to generate DRR for projection, the coordinate system and the origin need to be unified.
* The unified coordinate system direction is LPS.
* The unified origin is [0, 0, 0]
* The json file will also be modified.
~~~bash
python nii_tools/reoriented_images.py
~~~
you can run this command to check that the reorientation is correct.
~~~bash
python visual_tools/vis_3d_point_and_mask.py
~~~

### 2.1.5.crop cts and masks(selectable)
In order to add Number of CTs available, we run the follow command to crop the long spine which contain T9-L6.
~~~bash
python nii_tools/crop_images.py
~~~
when you after crop the image, you should add "bottom" in the subfolder name to sure subfolder name same as ct name.example
~~~bash
sub-verse014 -->> sub-verse014bottom
~~~
also you can run the follow command to check the reorientation of croppped images is correct.
~~~bash
python visual_tools/vis_3d_point_and_mask.py
~~~

### 2.1.6.choosed vertebrae categories list and Separate mask.
Some CT scans include upper thoracic and cervical vertebrae that need to be discarded. So you need choose the categories you need.\
Default selection category list is [T9 T10 T11 T12 L1 L2 L3 L4 L5 L6]
~~~bash
python nii_tools/verse_separate_mask.py
~~~

### 2.1.7.final format.
~~~bash
├── verse2019
    ├── sub-verse012
    │   ├── L1_seg.nii.gz
    │   ├── L2_seg.nii.gz
    │   ├── L3_seg.nii.gz
    │   ├── L4_seg.nii.gz
    │   ├── L5_seg.nii.gz
    │   ├── T11_seg.nii.gz
    │   ├── T12_seg.nii.gz
    │   └── sub-verse012.nii.gz
    ├── sub-verse013
    │   ├── L1_seg.nii.gz
    │   ├── L2_seg.nii.gz
    │   ├── L3_seg.nii.gz
    │   ├── L4_seg.nii.gz
    │   ├── L5_seg.nii.gz
    │   ├── T11_seg.nii.gz
    │   ├── T12_seg.nii.gz
    │   └── sub-verse013.nii.gz
    ├── sub-verse014bottom
    │   ├── L1_seg.nii.gz
    │   ├── L2_seg.nii.gz
    │   ├── L3_seg.nii.gz
    │   ├── L4_seg.nii.gz
    │   ├── L5_seg.nii.gz
    │   ├── T11_seg.nii.gz
    │   ├── T12_seg.nii.gz
    │   └── sub-verse014bottom.nii.gz
~~~

### 2.1.7.start generate drr and detection annotation json file.
~~~bash
python main_drr_detection_dataset.py
~~~

## 3.Generate CT Dataset(verse dataset mask format)
The Separate mask dataset format process is tedious,so we hope we don't separate the original seg mask and don't rename the ct masks.\
the init formart is the final format.
~~~bash
├── verse2019
    ├── sub-verse012
    │   ├── sub-verse012_ct.nii.gz
    │   ├── sub-verse012_seg-subreg_ctd.json
    │   ├── sub-verse012_seg-vert_msk.nii.gz
    │   └── sub-verse012_seg-vert_snp.png
    ├── sub-verse013
    │   ├── sub-verse013_ct.nii.gz
    │   ├── sub-verse013_seg-subreg_ctd.json
    │   ├── sub-verse013_seg-vert_msk.nii.gz
    │   └── sub-verse013_seg-vert_snp.png
    └── sub-verse014
        ├── sub-verse014_ct.nii.gz
        ├── sub-verse014_seg-subreg_ctd.json
        ├── sub-verse014_seg-vert_msk.nii.gz
        └── sub-verse014_seg-vert_snp.png
~~~
so just run the follow command can generate dataset.
~~~bash
To be update!!!
~~~


