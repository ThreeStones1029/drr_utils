# Dataset format
## 1.Separate mask dataset format
This code uses 3D projection to 2D for annotation, and requires the original CT, as well as the segmented mask. Put the data in the **data** folder. The placement format is as follows:
~~~bash
├── ct_dataset1
    ├── example1
    │   ├── L1_seg.nii.gz
    │   ├── L1_body_seg.nii.gz
    │   ├── L2_seg.nii.gz
    │   ├── L2_body_seg.nii.gz
    │   ├── L3_seg.nii.gz
    │   ├── L3_body_seg.nii.gz
    │   ├── L4_seg.nii.gz
    │   ├── L4_body_seg.nii.gz
    │   ├── L5_seg.nii.gz
    │   ├── L5_body_seg.nii.gz
    │   ├── T11_seg.nii.gz
    │   ├── T11_body_seg.nii.gz
    │   ├── T12_seg.nii.gz
    │   ├── T12_body_seg.nii.gz
    │   └── example1.nii.gz
    ├── example2
    │   ├── L1_seg.nii.gz
    │   ├── L1_body_seg.nii.gz
    │   ├── L2_seg.nii.gz
    │   ├── L2_body_seg.nii.gz
    │   ├── L3_seg.nii.gz
    │   ├── L3_body_seg.nii.gz
    │   ├── L4_seg.nii.gz
    │   ├── L4_body_seg.nii.gz
    │   ├── L5_seg.nii.gz
    │   ├── L5_body_seg.nii.gz
    │   ├── T11_seg.nii.gz
    │   ├── T11_body_seg.nii.gz
    │   ├── T12_seg.nii.gz
    │   ├── T12_body_seg.nii.gz
    │   └── example2.nii.gz
~~~
**Where example1 is the subfolder of a CT and the segmented mask, the ct name must be the same as the subfolder name.**

## 2.verse dataset mask format
In order to better adapt to the verse format, the mask of each vertebra can be unified in a nii file without separating it.
~~~bash
├── ct_dataset1
    ├── example1
    │   ├── example1_seg.nii.gz
    │   ├── example1.json
    │   ├── example1.png
    │   └── example1.nii.gz
    ├── example2
    │   ├── example2_seg.nii.gz
    │   ├── example2.json
    │   ├── example2.png
    │   └── example2.nii.gz
~~~
Datasets in this format are used to be updated.