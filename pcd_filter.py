import numpy as np
from open3d.cpu.pybind.utility import Vector3dVector
import axis_model as store


def color_filter(pcd, side_count):
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
    store.set_x_max(max(x_cordinates))
    store.set_x_min(min(x_cordinates))
    y_max_cord = max(y_cordinates)
    y_min_cord = min(y_cordinates)
    store.set_z_max(max(z_cordinates))
    store.set_z_min(min(z_cordinates))
    x_cord_diff = store.get_x_max()[side_count - 1] - store.get_x_min()[side_count - 1]
    y_cord_diff = y_max_cord - y_min_cord
    z_cord_diff = store.get_z_max()[side_count - 1] - store.get_z_min()[side_count - 1]
    print("x_max: " + str(store.get_x_max()[side_count - 1]) + ", x_min: " + str(
        store.get_x_min()[side_count - 1]) + ", x_length: " + str(x_cord_diff))
    print("y_max: " + str(y_max_cord) + ", y_min: " + str(y_min_cord) + ", y_length: " + str(y_cord_diff))
    print("z_max: " + str(store.get_z_max()[side_count - 1]) + ", z_min: " + str(
        store.get_z_min()[side_count - 1]) + ", z_length: " + str(z_cord_diff))
    color_array = np.array(color)
    point_array = np.array(points)
    pcd.points = Vector3dVector(point_array)
    pcd.colors = Vector3dVector(color_array)
    return pcd
