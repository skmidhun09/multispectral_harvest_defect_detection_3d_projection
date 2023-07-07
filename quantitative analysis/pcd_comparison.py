import open3d as o3d
import numpy as np


pcd_file_1 = '../data/auto/results/beet/12/pointcloud.pcd'
pcd1 = o3d.io.read_point_cloud(pcd_file_1)
point_list1 = np.asarray(pcd1.colors).tolist()

pcd_file_2 = '../data/auto/old results/beet/12/pointcloud.pcd'
pcd2 = o3d.io.read_point_cloud(pcd_file_2)
point_list2 = np.asarray(pcd2.colors).tolist()
count = 0

set1 = set(tuple(point) for point in point_list1)
set2 = set(tuple(point) for point in point_list2)

# Find common elements
common_elements = set1.intersection(set1, set2)

#common_elements = np.intersect1d(point_list1, point_list2)
print(len(set1))
print(len(set2))
print(len(common_elements))
# for point1 in point_list1:
#     index = 0
#     for point2 in point_list2:
#         if np.array_equal(point1, point2):
#             # n_points2 = point_list2[:index] + point_list2[index + 1:]
#             # point2 = n_points2
#             count = count + 1
#         index = index + 1

print(count)
