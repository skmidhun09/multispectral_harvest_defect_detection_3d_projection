import numpy as np


# Rotation about the x-axis by angle 'theta' (in radians)
def rotation_matrix_x(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


# Rotation about the y-axis by angle 'theta' (in radians)
def rotation_matrix_y(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


# Rotation about the z-axis by angle 'theta' (in radians)
def rotation_matrix_z(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
