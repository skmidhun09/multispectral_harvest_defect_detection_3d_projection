# Importing Required Modules
from rembg import remove as rm
import open3d as o3d
from open3d.cpu.pybind.utility import Vector3dVector
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


def remove_sparse_points(point_cloud, min_points, eps):
    # Convert point cloud to numpy arrays
    points = np.asarray(point_cloud.points)
    colors = np.asarray(point_cloud.colors)

    # Scale the points for better density estimation
    scaler = StandardScaler()
    scaled_points = scaler.fit_transform(points)

    # Apply DBSCAN to cluster points based on density
    dbscan = DBSCAN(eps=eps, min_samples=min_points)
    labels = dbscan.fit_predict(scaled_points)

    # Filter out points labeled as noise (-1)
    mask = labels != -1
    filtered_points = points[mask]
    filtered_colors = colors[mask]

    # Create a new point cloud with the filtered points and colors
    filtered_point_cloud = o3d.geometry.PointCloud()
    filtered_point_cloud.points = o3d.utility.Vector3dVector(filtered_points)
    filtered_point_cloud.colors = o3d.utility.Vector3dVector(filtered_colors)

    return filtered_point_cloud


def remove(image, pcd):
    color = np.asarray(pcd.colors).tolist()
    points = np.asarray(pcd.points).tolist()
    output = rm(image)
    #output.show()
    pixels = output.load()
    pcd_cnt = 0
    print(image.height * image.width)
    new_color = []
    new_point = []
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            # Check if the pixel is transparent
            if a > 100:
                new_color.append(color[pcd_cnt])
                new_point.append(points[pcd_cnt])
            pcd_cnt = pcd_cnt + 1
    color_array = np.array(new_color)
    point_array = np.array(new_point)
    pcd.points = Vector3dVector(point_array)
    pcd.colors = Vector3dVector(color_array)
    npcd = remove_sparse_points(pcd, 30, 0.1)
    return npcd


