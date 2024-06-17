'''
Description: 
version: 
Author: 
Date: 2024-03-23 07:14:28
LastEditors: ShuaiLei
LastEditTime: 2024-06-17 03:10:12
'''
import sys
import os
import itk
sys.path.insert(0, sys.path.append(os.path.dirname(sys.path[0])))
import numpy as np
from io_tools.file_management import get_sub_folder_paths, create_folder, join, get_subfiles, load_json_file, save_json_file
from tqdm import tqdm
import nibabel.orientations as nio
import nibabel as nib


def reorient_to_rai(image):
    """
    Reorient image to RAI orientation.
    :param image: itk read image
    """
    filter = itk.OrientImageFilter.New(image)
    filter.UseImageDirectionOn()
    filter.SetInput(image)
    m = itk.GetMatrixFromArray(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], np.float64))
    filter.SetDesiredCoordinateDirection(m)
    filter.Update()
    reoriented = filter.GetOutput()
    return reoriented


def load_centroids(ctd_path):
    """
    Load the centorids file.
    param: ctd_path: the path of json file.
    return ctd_list: a list containing the orientation and coordinates of the centroids.
    """
    dict_list = load_json_file(ctd_path)
    ctd_list = []
    for d in dict_list:
        if 'direction' in d:
            ctd_list.append(tuple(d['direction']))
        elif 'nan' in str(d):            #skipping NaN centroids
            continue
        else:
            ctd_list.append([d['label'], d['X'], d['Y'], d['Z']]) 
    return ctd_list


def save_centroids(ctd_list, ctd_path):
    """
    
    """
    ctd_json_data = []
    ctd_json_data.append({"direction": [ctd_list[0][0], ctd_list[0][1], ctd_list[0][2]]})
    for i in range(1, len(ctd_list)):
        landmarks = {"label": ctd_list[i][0],
                     "X": ctd_list[i][1],
                     "Y": ctd_list[i][2],
                     "Z": ctd_list[i][3]}
        ctd_json_data.append(landmarks)
    save_json_file(ctd_json_data, ctd_path)


def reorient_points(ctd_path, reoriented_image, decimals=1, verb=True):
    """
    reorient centroids to image orientation
    param: ctd_list: list of centroids
    param: img: nibabel image 
    param: decimals: rounding decimal digits
    Returns: out_list: reoriented list of centroids 
    """
    origin_coordinates = load_centroids(ctd_path)
    origin_coordinates_array = np.transpose(np.asarray(origin_coordinates[1:]))
    if len(origin_coordinates_array) == 0:
        print("[#] No centroids present") 
        return origin_coordinates
    vertebrae_label_list = origin_coordinates_array[0].astype(int).tolist()  # vertebral labels
    origin_coordinates_array = origin_coordinates_array[1:]
    number_orientation_from = nio.axcodes2ornt(origin_coordinates[0])  # original centroid orientation
    letter_orientation_to = nio.aff2axcodes(reoriented_image.affine) # Letters indicate centroid orientation
    number_orientation_to = nio.axcodes2ornt(letter_orientation_to)
    transform = nio.ornt_transform(number_orientation_from, number_orientation_to).astype(int)
    perm = transform[:, 0].tolist()
    shape = np.asarray(reoriented_image.dataobj.shape)
    origin_coordinates_array[perm] = origin_coordinates_array.copy()
    for ax in transform:
        if ax[1] == -1:
            size = shape[ax[0]]
            origin_coordinates_array[ax[0]] = np.around(size - origin_coordinates_array[ax[0]], decimals)
    out_list = [letter_orientation_to]
    origin_coordinates = np.transpose(origin_coordinates_array).tolist()
    for vertebrae_label, ctd in zip(vertebrae_label_list, origin_coordinates):
        out_list.append([vertebrae_label] + ctd)
    if verb:
        print("[*] Centroids reoriented from", nio.ornt2axcodes(number_orientation_from), "to", letter_orientation_to)
    save_centroids(out_list, ctd_path)
    return out_list


def reoriented_images(input_folder, output_folder):
    """
    Reoriented verse2020 dataset,unify coordinate、direction and origin
    :param input_folder: verse2020 dataset folder
    :param output_folder: oriented image save path
    """
    sub_folder_paths = get_sub_folder_paths(input_folder)
    for sub_folder_path in tqdm(sub_folder_paths, desc="reorienting"):
        sub_folder_name = os.path.basename(sub_folder_path)
        sub_output_folder = create_folder(join(output_folder, sub_folder_name))
        nii_file_paths = get_subfiles(sub_folder_path, ".nii.gz")
        json_file_paths = get_subfiles(sub_folder_path, "json")
        for nii_file_path in nii_file_paths:
            basename = os.path.basename(nii_file_path)
            basename_wo_ext = basename[:basename.find('.nii.gz')]
            ImageType = itk.Image[itk.SS, 3] 
            reader = itk.ImageFileReader[ImageType].New()
            reader.SetFileName(nii_file_path)
            image = reader.GetOutput() 
            reoriented = reorient_to_rai(image)
            reoriented.SetOrigin([0, 0, 0])
            m = itk.GetMatrixFromArray(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], np.float64))
            reoriented.SetDirection(m)
            reoriented.Update()
            itk.imwrite(reoriented, join(sub_output_folder, basename_wo_ext + '.nii.gz'))
            reoriented_nib = nib.load(join(sub_output_folder, basename_wo_ext + '.nii.gz'))
            reorient_points(json_file_paths[0], reoriented_nib)
            print(join(sub_output_folder, basename_wo_ext + '.nii.gz'),"conver to RAI coordinate succeccfully!\n")


if __name__ == "__main__":
    reoriented_images("data/verse2020_fracture","data/verse2020_fracture")