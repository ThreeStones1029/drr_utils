'''
Description: this file will be used visualize 3d point and seg mask in 2d image.
version: 
Author: According https://github.com/anjany/verse modify
Date: 2024-03-25 08:57:02
LastEditors: ShuaiLei
LastEditTime: 2024-06-17 11:22:36
'''
import os
import sys
sys.path.insert(0, os.path.dirname(sys.path[0]))
import numpy as np
import nibabel as nib
import nibabel.orientations as nio
import nibabel.processing as nip
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, Normalize
from matplotlib.patches import Circle
from io_tools.file_management import load_json_file


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


def load_image_mask_centroid_json(image_path, mask_path, json_path):
    """
    Load the image mask and centroid.
    param: image_path: The ct file.
    param: mask_path: The ct seg file.
    param: json_path: The centroid json file.
    return:
    img_nib: The image.
    msk_nib: The mask.
    ctd_list: The centroid list.
    """
    img_nib = nib.load(image_path)
    msk_nib = nib.load(mask_path)
    ctd_list = load_centroids(json_path)
    return img_nib, msk_nib, ctd_list


def check_image_space_direction_centroids(img_nib, ctd_list):
    zooms = img_nib.header.get_zooms()
    print('img zooms = {}'.format(zooms))
    #check img orientation
    axs_code = nio.ornt2axcodes(nio.io_orientation(img_nib.affine))
    print('img orientation code: {}'.format(axs_code))
    #check centroids
    print('Centroid List: {}'.format(ctd_list))


def resample_nib(img, voxel_spacing=(1, 1, 1), order=3):
    """
    Resamples the nifti from its original spacing to another specified spacing
    param: img: nibabel image
    param: voxel_spacing: a tuple of 3 integers specifying the desired new spacing
    param: order: the order of interpolation
    Returns:new_img: The resampled nibabel image 
    """
    # resample to new voxel spacing based on the current x-y-z-orientation
    aff = img.affine
    shp = img.shape
    zms = img.header.get_zooms()
    # Calculate new shape
    new_shp = tuple(np.rint([
        shp[0] * zms[0] / voxel_spacing[0],
        shp[1] * zms[1] / voxel_spacing[1],
        shp[2] * zms[2] / voxel_spacing[2]
        ]).astype(int))
    new_aff = nib.affines.rescale_affine(aff, shp, voxel_spacing, new_shp)
    new_img = nip.resample_from_to(img, (new_shp, new_aff), order=order, cval=-1024)
    print("[*] Image resampled to voxel size:", voxel_spacing)
    return new_img


def rescale_centroids(ctd_list, img, voxel_spacing=(1, 1, 1)):
    """
    rescale centroid coordinates to new spacing in current x-y-z-orientation
    param: ctd_list: list of centroids
    param: img: nibabel image 
    param: voxel_spacing: desired spacing
    Returns: out_list: rescaled list of centroids 
    
    """
    ornt_img = nio.io_orientation(img.affine)
    ornt_ctd = nio.axcodes2ornt(ctd_list[0])
    if np.array_equal(ornt_img, ornt_ctd):
        zms = img.header.get_zooms()
    else:
        ornt_trans = nio.ornt_transform(ornt_img, ornt_ctd)
        aff_trans = nio.inv_ornt_aff(ornt_trans, img.dataobj.shape)
        new_aff = np.matmul(img.affine, aff_trans)
        zms = nib.affines.voxel_sizes(new_aff)
    ctd_arr = np.transpose(np.asarray(ctd_list[1:]))
    v_list = ctd_arr[0].astype(int).tolist()  # vertebral labels
    ctd_arr = ctd_arr[1:]
    ctd_arr[0] = np.around(ctd_arr[0] * zms[0] / voxel_spacing[0], decimals=1)
    ctd_arr[1] = np.around(ctd_arr[1] * zms[1] / voxel_spacing[1], decimals=1)
    ctd_arr[2] = np.around(ctd_arr[2] * zms[2] / voxel_spacing[2], decimals=1)
    out_list = [ctd_list[0]]
    ctd_list = np.transpose(ctd_arr).tolist()
    for v, ctd in zip(v_list, ctd_list):
        out_list.append([v] + ctd)
    print("[*] Rescaled centroid coordinates to spacing (x, y, z) =", voxel_spacing, "mm")
    return out_list


def reorient_to(img, axcodes_to=('P', 'I', 'R'), verb=False):
    """
    Reorients the nifti from its original orientation to another specified orientation
    param: img: nibabel image
    param: axcodes_to: a tuple of 3 characters specifying the desired orientation
    Returns: newimg: The reoriented nibabel image 
    
    """
    aff = img.affine
    arr = np.asanyarray(img.dataobj, dtype=img.dataobj.dtype)
    ornt_fr = nio.io_orientation(aff)
    ornt_to = nio.axcodes2ornt(axcodes_to)
    ornt_trans = nio.ornt_transform(ornt_fr, ornt_to)
    arr = nio.apply_orientation(arr, ornt_trans)
    aff_trans = nio.inv_ornt_aff(ornt_trans, arr.shape)
    newaff = np.matmul(aff, aff_trans)
    newimg = nib.Nifti1Image(arr, newaff)
    if verb:
        print("[*] Image reoriented from", nio.ornt2axcodes(ornt_fr), "to", axcodes_to)
    return newimg


def reorient_centroids_to(ctd_list, img, decimals=1, verb=False):
    """
    reorient centroids to image orientation
    param: ctd_list: list of centroids
    param: img: nibabel image 
    param: decimals: rounding decimal digits
    Returns: out_list: reoriented list of centroids 
    """
    ctd_arr = np.transpose(np.asarray(ctd_list[1:]))
    if len(ctd_arr) == 0:
        print("[#] No centroids present") 
        return ctd_list
    v_list = ctd_arr[0].astype(int).tolist()  # vertebral labels
    ctd_arr = ctd_arr[1:]
    ornt_fr = nio.axcodes2ornt(ctd_list[0])  # original centroid orientation
    axcodes_to = nio.aff2axcodes(img.affine)
    ornt_to = nio.axcodes2ornt(axcodes_to)
    trans = nio.ornt_transform(ornt_fr, ornt_to).astype(int)
    perm = trans[:, 0].tolist()
    shp = np.asarray(img.dataobj.shape)
    ctd_arr[perm] = ctd_arr.copy()
    for ax in trans:
        if ax[1] == -1:
            size = shp[ax[0]]
            ctd_arr[ax[0]] = np.around(size - ctd_arr[ax[0]], decimals)
    out_list = [axcodes_to]
    ctd_list = np.transpose(ctd_arr).tolist()
    for v, ctd in zip(v_list, ctd_list):
        out_list.append([v] + ctd)
    if verb:
        print("[*] Centroids reoriented from", nio.ornt2axcodes(ornt_fr), "to", axcodes_to)
    return out_list


def resample_and_reorient_data(img_nib, msk_nib, ctd_list):
    # Resample and Reorient data
    img_iso = resample_nib(img_nib, voxel_spacing=(1, 1, 1), order=3)
    msk_iso = resample_nib(msk_nib, voxel_spacing=(1, 1, 1), order=0) # or resample based on img: resample_mask_to(msk_nib, img_iso)
    ctd_iso = rescale_centroids(ctd_list, img_nib, (1,1,1))
    img_iso = reorient_to(img_iso, axcodes_to=('I', 'P', 'L'))
    msk_iso = reorient_to(msk_iso, axcodes_to=('I', 'P', 'L'))
    ctd_iso = reorient_centroids_to(ctd_iso, img_iso)
    #check img zooms 
    zooms = img_iso.header.get_zooms()
    print('img zooms = {}'.format(zooms))
    #check img orientation
    axs_code = nio.ornt2axcodes(nio.io_orientation(img_iso.affine))
    print('img orientation code: {}'.format(axs_code))
    #check centroids
    print('new centroids: {}'.format(ctd_iso))
    return img_iso, msk_iso, ctd_iso, zooms


def create_figure(dpi, *planes):
    """
    creates a matplotlib figure
    param: dpi: desired dpi
    param: *planes: numpy arrays to include in the figure 
    Returns: fig, axs
    """
    fig_h = round(2 * planes[0].shape[0] / dpi, 2)
    plane_w = [p.shape[1] for p in planes]
    w = sum(plane_w)
    fig_w = round(2 * w / dpi, 2)
    x_pos = [0]
    for x in plane_w[:-1]:
        x_pos.append(x_pos[-1] + x)
    fig, axs = plt.subplots(1, len(planes), figsize=(fig_w, fig_h))
    for a in axs:
        a.axis('off')
        idx = axs.tolist().index(a)
        a.set_position([x_pos[idx]/w, 0, plane_w[idx]/w, 1])
    return fig, axs


def plot_sag_centroids(axs, ctd, zms):
    """
    plots sagittal centroids on a plane axes
    param: axs: matplotlib axs
    param: ctd: list of centroids
    param: zms: the spacing of the image
    """
    # requires v_dict = dictionary of mask labels
    for v in ctd[1:]:
        axs.add_patch(Circle((v[2]*zms[1], v[1]*zms[0]), 2, color=colors_itk[v[0]-1]))
        axs.text(4, v[1]*zms[0], v_dict[v[0]], fontdict={'color': cm_itk(v[0]-1), 'weight': 'bold'})


def plot_cor_centroids(axs, ctd, zms):
    """
    plots coronal centroids on a plane axes
    param: axs: matplotlib axs
    param: ctd: list of centroids
    param: zms: the spacing of the image
    """
    # requires v_dict = dictionary of mask labels
    for v in ctd[1:]:
        axs.add_patch(Circle((v[3]*zms[2], v[1]*zms[0]), 2, color=colors_itk[v[0]-1]))
        axs.text(4, v[1]*zms[0], v_dict[v[0]], fontdict={'color': cm_itk(v[0]-1), 'weight': 'bold'})


def visualize_mask_and_centroid(img_iso, msk_iso, ctd_iso, zooms, vis_save_path):
    # get vocel data
    im_np  = img_iso.get_fdata()
    msk_np = msk_iso.get_fdata()
    # get the mid-slice of the scan and mask in both sagittal and coronal planes
    im_np_sag = im_np[:,:,int(im_np.shape[2]/2)]
    im_np_cor = im_np[:,int(im_np.shape[1]/2),:]
    msk_np_sag = msk_np[:,:,int(msk_np.shape[2]/2)]
    msk_np_sag[msk_np_sag==0] = np.nan
    msk_np_cor = msk_np[:,int(msk_np.shape[1]/2),:]
    msk_np_cor[msk_np_cor==0] = np.nan
    # plot 
    fig, axs = create_figure(96,im_np_sag, im_np_cor)
    axs[0].imshow(im_np_sag, cmap=plt.cm.gray, norm=wdw_sbone)
    axs[0].imshow(msk_np_sag, cmap=cm_itk, alpha=0.3, vmin=1, vmax=64)
    plot_sag_centroids(axs[0], ctd_iso, zooms)
    axs[1].imshow(im_np_cor, cmap=plt.cm.gray, norm=wdw_sbone)
    axs[1].imshow(msk_np_cor, cmap=cm_itk, alpha=0.3, vmin=1, vmax=64)
    plot_cor_centroids(axs[1], ctd_iso, zooms)
    fig.savefig(vis_save_path)


def main(image_path, mask_path, json_path, vis_save_path):
    """
    visualize 3d point and mask in 2d image.
    """
    img_nib, msk_nib, ctd_list = load_image_mask_centroid_json(image_path, mask_path, json_path)
    check_image_space_direction_centroids(img_nib, ctd_list)
    img_iso, msk_iso, ctd_iso, zooms = resample_and_reorient_data(img_nib, msk_nib, ctd_list)
    visualize_mask_and_centroid(img_iso, msk_iso, ctd_iso, zooms, vis_save_path)


if __name__ == "__main__":
    v_dict = {1: 'C1', 2: 'C2', 3: 'C3', 4: 'C4', 5: 'C5', 6: 'C6', 7: 'C7',
              8: 'T1', 9: 'T2', 10: 'T3', 11: 'T4', 12: 'T5', 13: 'T6', 14: 'T7',15: 'T8', 16: 'T9', 17: 'T10', 18: 'T11', 19: 'T12', 
              20: 'L1',21: 'L2', 22: 'L3', 23: 'L4', 24: 'L5', 25: 'L6', 26: 'Sacrum',27: 'Cocc', 28: 'T13'}
    colors_itk = (1/255)*np.array([[255,  0,  0], [  0,255,  0], [  0,  0,255], [255,255,  0], [  0,255,255],
                                   [255,  0,255], [255,239,213],  # Label 1-7 (C1-7)
                                   [  0,  0,205], [205,133, 63], [210,180,140], [102,205,170], [  0,  0,128],
                                   [  0,139,139], [ 46,139, 87], [255,228,225], [106, 90,205], [221,160,221],
                                   [233,150,122], [165, 42, 42],  # Label 8-19 (T1-12)
                                   [255,250,250], [147,112,219], [218,112,214], [ 75,  0,130], [255,182,193],
                                   [ 60,179,113], [255,235,205],  # Label 20-26 (L1-6, sacrum)
                                   [255,235,205], [255,228,196],  # Label 27 cocc, 28 T13,
                                   [218,165, 32], [  0,128,128], [188,143,143], [255,105,180],  
                                   [255,  0,  0], [  0,255,  0], [  0,  0,255], [255,255,  0], [  0,255,255],
                                   [255,  0,255], [255,239,213],  # 29-39 unused
                                   [  0,  0,205], [205,133, 63], [210,180,140], [102,205,170], [  0,  0,128],
                                   [  0,139,139], [ 46,139, 87], [255,228,225], [106, 90,205], [221,160,221],
                                   [233,150,122],   # Label 40-50 (subregions)
                                   [255,250,250], [147,112,219], [218,112,214], [ 75,  0,130], [255,182,193],
                                   [ 60,179,113], [255,235,205], [255,105,180], [165, 42, 42], [188,143,143],
                                   [255,235,205], [255,228,196], [218,165, 32], [  0,128,128] # rest unused     
                                   ])
    cm_itk = ListedColormap(colors_itk)
    cm_itk.set_bad(color='w', alpha=0)  # set NaN to full opacity for overlay

    # define HU windows
    wdw_sbone = Normalize(vmin=-500, vmax=1300, clip=True)
    wdw_hbone = Normalize(vmin=-200, vmax=1000, clip=True)
    image_path = "data/verse2020_fracture/sub-verse513/sub-verse513bottom.nii.gz"
    mask_path = "data/verse2020_fracture/sub-verse513/sub-verse513bottom_seg.nii.gz"
    json_path = "data/verse2020_fracture/sub-verse513/sub-verse513bottom.json"
    vis_save_path = "data/verse2020_fracture/sub-verse513/sub-verse513bottom_vis.png"
    main(image_path, mask_path, json_path, vis_save_path)

    