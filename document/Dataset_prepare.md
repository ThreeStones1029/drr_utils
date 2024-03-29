<!--
 * @Description: 
 * @version: 
 * @Author: ThreeStones1029 2320218115@qq.com
 * @Date: 2024-03-29 07:33:58
 * @LastEditors: ShuaiLei
 * @LastEditTime: 2024-03-29 12:41:29
-->
# Spine Dataset Prepare.
## 1.Download
Spine Dataset
* [verse2019 and verse2020](https://github.com/anjany/verse)

* [CTSpine1K](https://github.com/MIRACLE-Center/CTSpine1K)

## 2.Generate CT Dataset(Separate mask dataset format)
### 2.1.1.init dataset format.
~~~bash
verse2019
    ├── sub-verse012
    │   ├── sub-verse012_ct.nii.gz
    │   ├── sub-verse012_seg-subreg_ctd.json
    │   ├── sub-verse012_seg-vert_msk.nii.gz
    │   └── sub-verse012_seg-vert_snp.png
    └── sub-verse013
        ├── sub-verse013_ct.nii.gz
        ├── sub-verse013_seg-subreg_ctd.json
        ├── sub-verse013_seg-vert_msk.nii.gz
        └── sub-verse013_seg-vert_snp.png
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

### 2.1.5.choosed vertebrae categories list and Separate mask.
Some CT scans include upper thoracic and cervical vertebrae that need to be discarded. So you need choose the categories you need.\
Default selection category list is [T9 T10 T11 T12 L1 L2 L3 L4 L5 L6]
~~~bash
python nii_tools/verse_separate_mask.py
~~~

### 2.1.6.start generate drr and detection annotation json file.
~~~bash
python main_drr_detection_dataset.py
~~~

