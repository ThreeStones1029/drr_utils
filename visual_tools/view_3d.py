'''
Description: 
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-04-08 09:11:52
LastEditors: ShuaiLei
LastEditTime: 2024-07-12 13:27:00
'''
import open3d as o3d
import numpy as np
import OpenGL.GL as gl
print(gl.glGetString(gl.GL_VERSION))


# 创建平面的点
points = [
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0]
]

# 定义三角形的顶点索引
triangles = [
    [0, 1, 2],
    [0, 2, 3]
]

# 创建Open3D的三角形网格对象
mesh = o3d.geometry.TriangleMesh()
mesh.vertices = o3d.utility.Vector3dVector(points)
mesh.triangles = o3d.utility.Vector3iVector(triangles)

# 计算法线
mesh.compute_vertex_normals()

# 设置网格颜色
mesh.paint_uniform_color([0.1, 0.7, 0.1])  # 绿色

# 创建一个Open3D的可视化窗口并添加网格
o3d.visualization.draw_geometries([mesh])
