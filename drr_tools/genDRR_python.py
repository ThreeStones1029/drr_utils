'''
Description: python版本的ITK生成DRR,根据C++版本编写,cpu版本生成效率慢
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-02-04 00:33:09
LastEditors: ShuaiLei
LastEditTime: 2024-04-10 02:11:10
'''
import itk
import math
import time


def generate_drr(rx, ry, rz, tx, ty, tz, cx, cy, cz, sid, sx, sy, dx, dy, o2Dx, o2Dy, threshold, ct_file_path, drr_save_path):
    # 定义维度和像素类型
    Dimension = 3
    InputPixelType = itk.F
    OutputPixelType = itk.UC
    # 定义输入和输出图像类型
    InputImageType = itk.Image[InputPixelType, Dimension]
    OutputImageType = itk.Image[OutputPixelType, Dimension]
    # Read CT image
    # 创建图像文件阅读器
    reader = itk.ImageFileReader[InputImageType].New()
    # 设置文件路径
    reader.SetFileName(ct_file_path)
    reader.Update()
    # try:
    #     # 更新阅读器
    #     reader.Update()
    # except itk.ExceptionObject as err:
    #     print("Error: Exception object caught!")
    #     print(err)
    #     exit(1)
    # 获取输出图像
    image = reader.GetOutput()

    # 滤波器
    filter = itk.ResampleImageFilter[InputImageType, InputImageType].New()
    # 设置输入图像和默认像素值
    filter.SetInput(image)
    filter.SetDefaultPixelValue(0)
    # Define Euler3DTransform
    transform = itk.CenteredEuler3DTransform[itk.D].New()
    # 设置ComputeZYX属性为True
    transform.SetComputeZYX(True)
    dtr = math.pi / 180
    transform.SetTranslation([tx, ty, tz])
    transform.SetRotation(rx * dtr, ry * dtr , rz * dtr)
    imOrigin = image.GetOrigin()
    imRes = image.GetSpacing()
    # 获取图像的缓冲区域
    imRegion = image.GetBufferedRegion()
    # 获取缓冲区域的大小
    imSize = imRegion.GetSize()
    imOrigin[0] = imRes[0] * float(imSize[0]) / 2.0
    imOrigin[1] = imRes[1] * float(imSize[1]) / 2.0
    imOrigin[2] = imRes[2] * float(imSize[2]) / 2.0
    center = [cx + imOrigin[0], cy + imOrigin[1], cz + imOrigin[2]]
    transform.SetCenter(center)

    # 创建插值器对象
    interpolator = itk.RayCastInterpolateImageFunction[InputImageType, itk.D].New()
    # 设置变换
    interpolator.SetTransform(transform)
    # 设置阈值
    interpolator.SetThreshold(threshold)
    focalpoint = [0, 0, 0]
    # 设置焦点坐标
    focalpoint[0] = imOrigin[0]
    focalpoint[1] = imOrigin[1]
    focalpoint[2] = imOrigin[2] - sid / 2.0
    # 设置插值器的焦点
    interpolator.SetFocalPoint(focalpoint)
    # 输出插值器信息
    # interpolator.Print(std.cout, itk.Indent())
    # 设置滤波器的插值器和变换
    filter.SetInterpolator(interpolator)
    filter.SetTransform(transform)
    # 设置滤波器的大小
    size = filter.GetSize()
    size[0] = dx  # number of pixels along X of the 2D DRR image
    size[1] = dy  # number of pixels along Y of the 2D DRR image
    size[2] = 1   # only one slice
    filter.SetSize(size)
    # 设置滤波器的输出间距
    spacing = filter.GetOutputSpacing()
    spacing[0] = sx  # pixel spacing along X of the 2D DRR image [mm]
    spacing[1] = sy  # pixel spacing along Y of the 2D DRR image [mm]
    spacing[2] = 1.0  # slice thickness of the 2D DRR image [mm]
    filter.SetOutputSpacing(spacing)

    # 设置滤波器的输出原点
    origin = filter.GetOutputOrigin()
    # origin[0] = imOrigin[0] + o2Dx - sx * (dx - 1.0) / 2.0
    # origin[1] = imOrigin[1] + o2Dy - sy * (dy - 1.0) / 2.0
    origin[0] = imOrigin[0] + o2Dx - sx * (dx - 1.0)
    origin[1] = imOrigin[1] + o2Dx - sx * (dy - 1.0)
    origin[2] = imOrigin[2] + sid / 2.0
    filter.SetOutputOrigin(origin)

    # 强度重缩放滤波器
    rescaler = itk.RescaleIntensityImageFilter[InputImageType, OutputImageType].New()
    rescaler.SetOutputMinimum(0)
    rescaler.SetOutputMaximum(255)
    rescaler.SetInput(filter.GetOutput())
    # 创建图像文件写入器
    writer = itk.ImageFileWriter[OutputImageType].New()
    # 新建png对象
    pngIO1 = itk.PNGImageIO.New()
    # 设置文件路径
    writer.SetFileName(drr_save_path)
    # 设置图像IO
    writer.SetImageIO(pngIO1)
    writer.SetImageIO(itk.PNGImageIO.New())
    # 设置写入器的输入
    writer.SetInput(rescaler.GetOutput())
    try:
        # 更新写入器
        print(f"Writing image: {drr_save_path}")
        writer.Update()
    except itk.ExceptionObject as err:
        print("ERROR: ExceptionObject caught!")
        print(err)

# Example usage:
start_time = time.time()
rx_value = 90.0
ry_value = 180.0
rz_value = 90.0
tx_value = 0.0
ty_value = 0.0
tz_value = 0.0
cx_value = 0.0
cy_value = 0.0
cz_value = 0.0
sid_value = 1000.0
sx_value = 1
sy_value = 1
dx_value = 512
dy_value = 512
o2Dx_value = 0.0
o2Dy_value = 0.0
threshold_value = 0.0
ct_file_path = "data/verse2020/verse005/verse005.nii.gz"
drr_save_path = "data/verse2020/verse005/verse005_drr.png"

generate_drr(rx_value, ry_value, rz_value, tx_value, ty_value, tz_value,
             cx_value, cy_value, cz_value, sid_value,
             sx_value, sy_value, dx_value, dy_value,
             o2Dx_value, o2Dy_value, threshold_value,
             ct_file_path, drr_save_path)
print(time.time() - start_time)