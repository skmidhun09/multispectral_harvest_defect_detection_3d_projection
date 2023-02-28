import numpy as np
from open3d.cpu.pybind.utility import Vector3dVector


def color_filter(pcd):
    color = np.asarray(pcd.colors).tolist()
    points = np.asarray(pcd.points).tolist()
    index = 0
    x_cordinates = []
    y_cordinates = []
    z_cordinates = []
    while index < len(color):
        r, g, b = color[index]
        if (r < 0.2 and g < 0.2 and b > 0.8):
            del color[index]
            del points[index]
        else:
            # print(points[index])
            x, y, z = points[index]
            x_cordinates.append(x)
            y_cordinates.append(y)
            z_cordinates.append(z)
            index = index + 1
    global x_max_cord
    global x_min_cord
    global z_max_cord
    global z_min_cord
    x_max_cord.append(max(x_cordinates))
    x_min_cord.append(min(x_cordinates))
    y_max_cord = max(y_cordinates)
    y_min_cord = min(y_cordinates)
    z_max_cord.append(max(z_cordinates))
    z_min_cord.append(min(z_cordinates))
    global cord_diff, side_count
    x_cord_diff = x_max_cord[side_count - 1] - x_min_cord[side_count - 1]
    y_cord_diff = y_max_cord - y_min_cord
    z_cord_diff = z_max_cord[side_count - 1] - z_min_cord[side_count - 1]
    print("x_max: " + str(x_max_cord[side_count - 1]) + ", x_min: " + str(
        x_min_cord[side_count - 1]) + ", x_length: " + str(x_cord_diff))
    print("y_max: " + str(y_max_cord) + ", y_min: " + str(y_min_cord) + ", y_length: " + str(y_cord_diff))
    print("z_max: " + str(z_max_cord[side_count - 1]) + ", z_min: " + str(
        z_min_cord[side_count - 1]) + ", z_length: " + str(z_cord_diff))
    color_array = np.array(color)
    point_array = np.array(points)
    pcd.points = Vector3dVector(point_array)
    pcd.colors = Vector3dVector(color_array)
    return pcd