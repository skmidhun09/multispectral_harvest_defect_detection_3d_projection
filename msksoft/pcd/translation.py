import math

import numpy as np
from msksoft.ds import json_data_store as data_store

correction_factor = 1.1
pos_factor = 1.4

def reset_position(image_face, total, pcd):
    #stored_data = data_store.read_list(str(image_face))
    image_pos = (image_face-1)*(360/total)
    angle_rad = math.radians(image_pos)
    #print("$$$$$$$$$", angle_rad)
    z_correct = 0.00012
    x_correct = 0.00012

    if image_pos < 90:
        translation_matrix = np.array([[1, 0, 0, pos_factor * x_correct * math.cos(np.pi/2 - angle_rad)], [0, 1, 0, 0], [0, 0, 1, pos_factor * z_correct * math.cos(angle_rad)], [0, 0, 0, 1]])
        pcd.transform(translation_matrix)
    elif image_pos < 180:
        translation_matrix = np.array([[1, 0, 0, pos_factor * x_correct * math.cos(angle_rad - np.pi/2)], [0, 1, 0, 0], [0, 0, 1, -pos_factor * z_correct * math.cos(np.pi - angle_rad)], [0, 0, 0, 1]])
        pcd.transform(translation_matrix)
    elif image_pos < 270:
        translation_matrix = np.array([[1, 0, 0, -pos_factor * x_correct * math.cos(3*np.pi/2 - angle_rad)], [0, 1, 0, 0], [0, 0, 1, -pos_factor * z_correct * math.cos(angle_rad - np.pi)], [0, 0, 0, 1]])
        pcd.transform(translation_matrix)
    elif image_pos < 360:
        translation_matrix = np.array([[1, 0, 0, -pos_factor * x_correct * math.cos(angle_rad - 3*np.pi/2)], [0, 1, 0, 0], [0, 0, 1, pos_factor * z_correct * math.cos(2*np.pi - angle_rad)], [0, 0, 0, 1]])
        pcd.transform(translation_matrix)


def align_pcd(pcds):
    front = data_store.read_list(str(1))
    side = data_store.read_list(str(2))
    print("###############", front, "#######")
    translation_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, side["zmax"] * correction_factor], [0, 0, 0, 1]])
    pcds[0].transform(translation_matrix)
    translation_matrix = np.array([[1, 0, 0, front["xmax"] * correction_factor], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    pcds[1].transform(translation_matrix)
    translation_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, side["zmin"] * correction_factor], [0, 0, 0, 1]])
    pcds[2].transform(translation_matrix)
    translation_matrix = np.array([[1, 0, 0, front["xmin"] * correction_factor], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    pcds[3].transform(translation_matrix)