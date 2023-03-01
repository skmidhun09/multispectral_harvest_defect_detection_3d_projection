import numpy as np
import save_list_as_json as ds


def reset_position(image_face,pcd):
    stored_data = ds.read_list(str(image_face))
    if image_face == 1:
        translation_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -1 * stored_data["zmax"]], [0, 0, 0, 1]])
        pcd.transform(translation_matrix)
    if image_face == 2:
        translation_matrix = np.array([[1, 0, 0, -1 * stored_data["xmax"]], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        pcd.transform(translation_matrix)
    if image_face == 3:
        translation_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -1 * stored_data["zmin"]], [0, 0, 0, 1]])
        pcd.transform(translation_matrix)
    if image_face == 4:
        translation_matrix = np.array([[1, 0, 0, -1 * stored_data["xmin"]], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        pcd.transform(translation_matrix)


def align_pcd(pcds):
    front = ds.read_list(str(1))
    side = ds.read_list(str(2))
    translation_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, side["zmax"]], [0, 0, 0, 1]])
    pcds[0].transform(translation_matrix)
    translation_matrix = np.array([[1, 0, 0, front["xmax"]], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    pcds[1].transform(translation_matrix)
    translation_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, side["zmin"]], [0, 0, 0, 1]])
    pcds[2].transform(translation_matrix)
    translation_matrix = np.array([[1, 0, 0, front["xmin"]], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    pcds[3].transform(translation_matrix)