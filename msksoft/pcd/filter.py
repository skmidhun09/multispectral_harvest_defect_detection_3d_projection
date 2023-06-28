import numpy as np
from open3d.cpu.pybind.utility import Vector3dVector
from msksoft.ds import json_data_store as data_store


def color_filter(pcd, side_count):
    color = np.asarray(pcd.colors).tolist()
    points = np.asarray(pcd.points).tolist()
    index = 0
    x_cordinates = []
    y_cordinates = []
    z_cordinates = []

    while index < len(color):
        r, g, b = color[index]
        if ((r < 0.3 or g < 0.3) and b > 0.05):
            del color[index]
            del points[index]
        else:
            # print(points[index])
            x, y, z = points[index]
            x_cordinates.append(x)
            y_cordinates.append(y)
            z_cordinates.append(z)
            index = index + 1
    image_map = {"xmax": max(x_cordinates), "xmin": min(x_cordinates), "ymax": max(y_cordinates),
                 "ymin": min(y_cordinates), "zmax": max(z_cordinates), "zmin": min(z_cordinates)}
    #data_store.save_list(str(side_count), image_map)
    x_cord_diff = image_map["xmax"] - image_map["ymin"]
    y_cord_diff = image_map["ymax"] - image_map["ymin"]
    z_cord_diff = image_map["zmax"] - image_map["zmin"]
    # print("x_max: " + str(image_map["xmax"]) + ", x_min: " + str(image_map["xmin"]) + ", x_length: " + str(x_cord_diff))
    # print("y_max: " + str(image_map["ymax"]) + ", y_min: " + str(image_map["ymin"]) + ", y_length: " + str(y_cord_diff))
    # print("z_max: " + str(image_map["zmax"]) + ", z_min: " + str(image_map["zmin"]) + ", z_length: " + str(z_cord_diff))
    color_array = np.array(color)
    point_array = np.array(points)
    pcd.points = Vector3dVector(point_array)
    pcd.colors = Vector3dVector(color_array)
    return pcd
