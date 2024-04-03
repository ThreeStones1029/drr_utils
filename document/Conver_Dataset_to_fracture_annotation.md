<!--
 * @Description: # How to convert the generated data set to fracture labeling dataset?
 * @version: 
 * @Author: ThreeStones1029 2320218115@qq.com
 * @Date: 2024-04-03 01:49:19
 * @LastEditors: ShuaiLei
 * @LastEditTime: 2024-04-03 04:33:00
-->
# How to convert the generated dataset to fracture labeling dataset?

## Prepare
### The fracture information json format
you need provide the json file which record the fracture information? the json file data format as follow:
~~~bash
{
    "sub-verse012.nii.gz": {
        "T10": "normal",
        "T11": "normal",
        "T12": "normal",
        "L1": "fracture",
        "L2": "normal",
        "L3": "normal"
    },
    "sub-verse020bottom.nii.gz": {
        "T9": "fracture",
        "T10": "normal",
        "T11": "fracture",
        "T12": "normal",
        "L1": "fracture",
        "L2": "normal",
        "L3": "normal",
        "L4": "normal",
        "L5": "normal"
    }
}
~~~
[Note] the json file only record the T9-L6 fracture information.
### Generate json file according xlsx file.
the verse2019 fracture json file can be generate by the verse2019_fracture_grading_info.xlsx which can be get in [paper supplementary materials](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8082364/)
run the follow command to generate json file.
~~~bash
python dataset_tools/verse2019_fracture_split.py
~~~
[Note]
* 1.This case will only be recorded if there is a grade 3 fracture in T9-L6 of ct.
* 2.The "bottom" indicates that the CT is cropped.
* 3.the generated json file record 33 cts fracture information.
* 4.if you need to process the local dataset.please provide your json file to conver annotation file.

### conver annotation file to fracture annotation file and split cut images to fracture images and normal dataset
~~~bash
python dataset_tools/verse2019_fracture_split.py
~~~
Then you can use the splited images to train 

