'''
Description: 
version: 
Author: ThreeStones1029 221620010039@qq.com
Date: 2023-12-29 19:55:01
LastEditors: ShuaiLei
LastEditTime: 2023-12-30 16:27:42
'''
from io_tools.file_management import load_json_file, save_json_file, join
import json
import os
import subprocess


def run_object_detection(object_detection_parameter):
    script_parameter = [object_detection_parameter["envs_path"],
                        object_detection_parameter["detection_script_path"],
                        "-c", object_detection_parameter["config_path"],
                        "--infer_dir", object_detection_parameter["infer_dir"],
                        "--output_dir", object_detection_parameter["output_dir"],
                        "--draw_threshold", "0.6",
                        "--use_vdl", "False",
                        "--save_results", "True"]
    detection_command = " ".join(script_parameter)
    subprocess.run(detection_command, shell=True)


def load_detection_result(detection_result_json_path):
    flitered_result = []
    detection_result = load_json_file(detection_result_json_path)
    for ann in detection_result:
        if ann["score"] > 0.6:
            flitered_result.append(ann)
    flitered_result_json_path = join(os.path.dirname(detection_result_json_path), "flitered_bbox.json")
    save_json_file(flitered_result, flitered_result_json_path)
    return flitered_result