import os
import open3d as o3d
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from PIL import Image


def rotate_pcd(pcd):
    # Define the rotation matrix for 90-degree rotation
    rotation_matrix = np.array([[0, 0, 1],
                                [0, 1, 0],
                                [-1, 0, 0]])
    # Rotate the point cloud
    rotated_pcd = pcd.rotate(rotation_matrix)
    return rotated_pcd


def plot_pcd(pcd_file, out_file):
    r_pcd = o3d.io.read_point_cloud(pcd_file)
    image_list = []
    pcd = r_pcd
    for i in range(4):
        # Extract coordinates and colors from the point cloud
        points = np.asarray(pcd.points)
        colors = np.asarray(pcd.colors)
        # Create a 3D plot
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        # Plot the point cloud with colors
        ax.scatter(points[:, 0], points[:, 2], points[:, 1], c=colors, marker='s', s=0.05)
        # Set labels and title
        ax.xaxis.set_major_locator(ticker.MultipleLocator(0.0001))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(0.0001))
        ax.zaxis.set_major_locator(ticker.MultipleLocator(0.0001))
        ax.tick_params(axis='x', labelsize=16)
        ax.tick_params(axis='y', labelsize=16)
        ax.tick_params(axis='z', labelsize=16)
        ax.zaxis.set_tick_params(pad=15)
        ax.set_xlabel('X', labelpad=15, fontsize=16)
        ax.set_ylabel('Y', labelpad=15, fontsize=16)
        ax.set_zlabel('Z', labelpad=25, fontsize=16)
        ax.set_title('Point Cloud', fontsize=16)
        ax.view_init(elev=20, azim=120)
        ax.set_box_aspect([1, 1, 1])
        #plt.show()
        # Show the plot
        fig.savefig("../data/temp/gif_image/tmp" + str(i) + ".jpg", dpi=300)
        image_list.append(Image.open("../data/temp/gif_image/tmp" + str(i) + ".jpg"))
        plt.close()
        pcd = rotate_pcd(pcd)
    image_list[0].save(out_file, save_all=True, append_images=image_list[1:], duration=500, loop=0)
    print("done")


base_path = '../data/auto/results/'
for folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder)
    print(folder)
    for i in range(4, 13, 2):
        new_folder_path = os.path.join(folder_path, str(i))
        plot_pcd(new_folder_path + "/pointcloud.pcd", new_folder_path + "/plotted_3D.gif")
        # try:
        #     plot_pcd(new_folder_path + "/pointcloud.pcd", new_folder_path + "/plotpcd.png")
        # except Exception as e:
        #     print("ERROR",e)

