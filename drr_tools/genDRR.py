'''
Description: ITKCpp生成DRR
version: 1.0
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-12-10 14:11:27
LastEditors: ShuaiLei
LastEditTime: 2024-07-13 08:40:37
'''
import platform
from ITK_tools.linux_genDRR import linuxgenDRR, linuxgen_multiDRRs
from ITK_tools.windows_genDRR import windowsgenDRR


def genDRR(sdr, height, delx, threshold, rotation, translation, ctDir, saveIMG):
    if platform.system().lower() == "linux":
        linuxgenDRR(sdr, height, delx, threshold, rotation, translation, ctDir, saveIMG)
    else:
        windowsgenDRR(sdr, height, delx, threshold, rotation, translation, ctDir, saveIMG)


def gen_multiDRRs(sdr, height, delx, threshold, rotations, translations, ctDir, save_images_folder):
    """
    Generate multiple DRRS simultaneously
    now only support linux
    """
    if platform.system().lower() == "linux":
        linuxgen_multiDRRs(sdr, height, delx, threshold, rotations, translations, ctDir, save_images_folder)