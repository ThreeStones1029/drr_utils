import os
import sys
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import SimpleITK as sitk
from tqdm import tqdm
import shutil
from io_tools.file_management import get_sub_folder_paths, get_subfiles, load_json_file, join, save_json_file


class VerseCategoriesFormat:
    def __init__(self):
        self.catid2catname = {1: "C1", 2: "C2", 3: "C3", 4: "C4", 5: "C5", 6: "C6", 7: "C7",
                              8: "T1", 9: "T2", 10: "T3", 11: "T4", 12: "T5", 13: "T6", 14: "T7", 15: "T8", 16: "T9", 17: "T10", 18: "T11", 19: "T12",
                              20: "L1", 21: "L2", 22: "L3", 23: "L4", 24: "L5", 25: "L6",
                              26: "sacrum", 27: "cocygis", 28: "T13"}
        self.catname2catid = {name: id for id, name in self.catid2catname.items()}

    def get_catid2catname(self):
        return self.catid2catname
    
    def get_catname2catid(self):
        return self.catname2catid


class VerseFormatConver:
    """
    用于将verse数据集格式转换为代码投影DRR所用格式
    """
    def __init__(self, root_path):
        self.root_path = root_path
        self.catid2catname = VerseCategoriesFormat().get_catid2catname()
    
    def run(self):
        sub_folder_paths = get_sub_folder_paths(self.root_path) 
        for sub_folder_path in tqdm(sub_folder_paths, desc="convering"):
            self.single_ct_conver(sub_folder_path)
        

    def single_ct_conver(self, path):
        sub_folder_name = os.path.basename(path)
        nii_file_paths = get_subfiles(path, "_seg.nii.gz")
        json_paths = get_subfiles(path, ".json")
        if len(nii_file_paths) == 1:
            file_path = nii_file_paths[0]
            seg_image = sitk.ReadImage(file_path)
            cats_info = load_json_file(json_paths[0])
            choosed = self.choose_lumbar_and_lower_thoracic_ct(cats_info)
            # choosed = True # all ct will be choosed
            if choosed:
                for cat_info in cats_info:
                    if "label" in cat_info.keys():
                        catid = cat_info["label"]
                        catname = self.catid2catname[catid]
                        vertebrae_mask_array = sitk.GetArrayFromImage(seg_image==catid)
                        vertebrae_image = sitk.GetImageFromArray(vertebrae_mask_array)
                        vertebrae_image.SetSpacing(seg_image.GetSpacing())
                        vertebrae_image.SetOrigin(seg_image.GetOrigin())
                        vertebrae_image.SetDirection(seg_image.GetDirection())
                        vertebrae_image_save_path = join(path, catname + "_seg.nii.gz")
                        sitk.WriteImage(vertebrae_image, vertebrae_image_save_path)
                os.remove(file_path)
            else:
                print(sub_folder_name, "not lumbar or lower thoracic so don't need it!")
                shutil.rmtree(path)
        else:
            print("it has be processed!")


    def choose_lumbar_and_lower_thoracic_ct(self, cats_info):
        """
        选择腰椎和下胸椎的脊柱,保留腰椎骶化以及骶椎腰化CT。T13的排除
        """
        choosed = True
        for cat_info in cats_info:
            if "label" in cat_info.keys() and (cat_info["label"] <= 15 or cat_info["label"] >= 26):
                choosed = False
        return choosed


def ct_dataset_statistics(ct_dataset_path, statistics_information_json_path):
    """
    数据集CT椎体标签统计
    """
    # 初始化
    vertebrae_dataset_info = {"overall": {"number": 0, "categories": []}}
    sub_folder_paths = get_sub_folder_paths(ct_dataset_path) 
    for sub_folder_path in sub_folder_paths:
        for file in os.listdir(sub_folder_path):
            if file.endswith("seg.nii.gz"):
                catname = file.split("_")[0]
                vertebrae_dataset_info["overall"]["number"] += 1
                # 初始化这个类别的信息
                if catname not in vertebrae_dataset_info["overall"]["categories"]:
                    vertebrae_dataset_info["overall"]["categories"].append(catname)
                    vertebrae_dataset_info[catname] = {"category_name": catname,
                                                       "number": 1,
                                                       "percentage": 0}
                # 更新这个类别的信息
                else:
                    vertebrae_dataset_info[catname]["number"] += 1
                    vertebrae_dataset_info[catname]["percentage"] = vertebrae_dataset_info[catname]["number"] / vertebrae_dataset_info["overall"]["number"]
    save_json_file(vertebrae_dataset_info, statistics_information_json_path)


if __name__ == "__main__":
    format_conver = VerseFormatConver("data/verse2019_test1")
    format_conver.run()