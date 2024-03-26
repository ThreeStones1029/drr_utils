'''
Description: ITKCpp生成DRR
version: 1.0
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-12-10 14:11:27
LastEditors: ShuaiLei
LastEditTime: 2023-12-14 15:40:42
'''
import platform
from ITK_tools.linux_genDRR import linuxgenDRR
from ITK_tools.windows_genDRR import windowsgenDRR


def genDRR(sdr, height, delx, threshold, rotation, translation, ctDir, saveIMG):
    if platform.system().lower() == "linux":
        linuxgenDRR(sdr, height, delx, threshold, rotation, translation, ctDir, saveIMG)
    else:
        windowsgenDRR(sdr, height, delx, threshold, rotation, translation, ctDir, saveIMG)