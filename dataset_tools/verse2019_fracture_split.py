'''
Description: this file arrording the spine fracture xlsx to split verse2019.The xlsx file can be get in https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8082364/
version: 1.0
Author: Shuai Lei
Date: 2024-03-23 11:58:45
LastEditors: ShuaiLei
LastEditTime: 2024-03-26 13:36:49
'''
import sys
import os
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
if project_root not in sys.path:
    sys.path.insert(0, os.path.dirname(sys.path[0]))
from openpyxl import load_workbook
from io_tools.file_management import load_json_file, save_json_file


def split_fracture_ct_dataset(xlsx_file, choosed_vertebrae_label_list):
    """
    load xlsx file to split verse2019 dataset.
    param: xlsx_file: A document that records specific fracture information.
    param: choosed_vertebrae_label_list: 

    """
    fracture_grad1_dataset = []
    fracture_grad2_dataset = []
    fracture_grad3_dataset = []
    normal_dataset = []
    choosed_vertebrae_label_fx_g_list = [label + "_fx-g" for label in choosed_vertebrae_label_list]
    workbbok = load_workbook(xlsx_file, data_only=True)
    sheet = workbbok.active
    # get header
    header = [cell.value for cell in sheet[1]]
    for row in sheet.iter_rows(min_row=2, values_only=True):
        # get ct name
        if row[header.index('verse_ID')] != None and row[header.index('verse_ID')] != row[header.index('subject_ID')]:
            ct_name = "sub-verse{:03d}_split-verse{:03d}_ct.nii.gz".format(row[header.index('subject_ID')], row[header.index('verse_ID')])
        if row[header.index('verse_ID')] != None and row[header.index('verse_ID')] == row[header.index('subject_ID')]:  
            ct_name = "sub-verse{:03d}_ct.nii.gz".format(row[header.index('verse_ID')])
        if row[0] != None and row[header.index('N_Fx')] != 0:
            fx_g_id_list = [row[header.index(col)] for col in choosed_vertebrae_label_fx_g_list]
            if 3 in fx_g_id_list:
                fracture_grad3_dataset.append(ct_name)
            if 2 in fx_g_id_list and 3 not in fx_g_id_list:
                fracture_grad2_dataset.append(ct_name)
            if 2 not in fx_g_id_list and 3 not in fx_g_id_list:
                fracture_grad1_dataset.append(ct_name)
        if row[0] != None and row[header.index('N_Fx')] == 0:
            normal_dataset.append(ct_name)
        
    print("CT Facture grad = 3 number is: ", len(fracture_grad3_dataset))
    print(fracture_grad3_dataset)
    print("CT Facture grad = 2 number is: ", len(fracture_grad2_dataset))
    print(fracture_grad2_dataset)
    print("CT Facture grad = 1 number is: ", len(fracture_grad1_dataset))
    print(fracture_grad1_dataset)
    print("normal number is: ", len(normal_dataset))
    print(normal_dataset)


def fracture_normal_label_conver(xlsx_file, annotation_file, fracture_annotation_file):
    """
    conver the T9-L6 to fracture and normal label.
    param: xlsx_file: The verse2019 fracture record file.
    param: annotation_file: The drr images detection annotation file.
    param: fracture_annotation_file: The fracture and normal label annotation file.
    """
    dataset = load_json_file(annotation_file)
    workbbok = load_workbook(xlsx_file, data_only=True)
    sheet = workbbok.active
    # get header
    header = [cell.value for cell in sheet[1]]
    save_json_file(dataset, fracture_annotation_file)



if __name__ == "__main__":
    split_fracture_ct_dataset("data/verse2019/verse2019_fracture_grading_info.xlsx", 
                              ["T9", "T10", "T11", "T12","L1", "L2", "L3", "L4", "L5", "L6"])
    # fracture_normal_label_conver("data/verse2019_drr/")