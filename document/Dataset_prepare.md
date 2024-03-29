<!--
 * @Description: 
 * @version: 
 * @Author: ThreeStones1029 2320218115@qq.com
 * @Date: 2024-03-29 07:33:58
 * @LastEditors: ShuaiLei
 * @LastEditTime: 2024-03-29 09:06:24
-->
# Spine Dataset Prepare.
## 1.Download
Spine Dataset
* [verse2019 and verse2020](https://github.com/anjany/verse)

* [CTSpine1K](https://github.com/MIRACLE-Center/CTSpine1K)

## 2.Generate CT Dataset(Separate mask dataset format)
### 2.1.1.check Dataset.
The verse dataset has some subfolders that are empty, some subfolders that have multiple CTS, and some subfolders that only have CT without mask.
* (1) Delete empty subfolder.
~~~bash
python nii_tools/verse_check_images.py
~~~

### 2.1.2. Rename subfolder.
The CT and the ct mask need to be renamed for use easy.
~~~bash
python nii_tools/verse_rename_images.py
~~~

### 2.1.3.choosed vertebrae categories list.
Some CT scans include upper thoracic and cervical vertebrae that need to be discarded.
