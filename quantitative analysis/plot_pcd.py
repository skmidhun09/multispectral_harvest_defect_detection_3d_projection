import os
import open3d as o3d
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import numpy as np


def plot_pcd(pcd_file, out_file):
    #pcd_file = '../data/auto/results/beet/12/pointcloud.pcd'
    pcd = o3d.io.read_point_cloud(pcd_file)

    # Extract coordinates and colors from the point cloud
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)

    # Create a 3D plot
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the point cloud with colors
    ax.scatter(points[:, 0], points[:, 2], points[:, 1], c=colors, marker='s', s=0.05)

    # Set labels and title
    # x_ticks = [-0.0003,-0.0002,-0.0001, 0, 0.0001, 0.0002, 0.0003]  # Set the desired tick values
    # y_ticks = [-0.0003, -0.0002, -0.0001, 0, 0.0001, 0.0002, 0.0003]
    # z_ticks = [-0.0003, -0.0002, -0.0001, 0, 0.0001, 0.0002, 0.0003]
    # ax.set_xticks(x_ticks)
    # ax.set_yticks(y_ticks)
    # ax.set_zticks(z_ticks)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.0001))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.0001))
    ax.zaxis.set_major_locator(ticker.MultipleLocator(0.0001))
    ax.zaxis.set_tick_params(pad=15)
    ax.set_xlabel('X', labelpad=15)
    ax.set_ylabel('Y', labelpad=15)
    ax.set_zlabel('Z', labelpad=25)
    ax.set_title('Point Cloud')
    ax.view_init(elev=20, azim=120)
    ax.set_box_aspect([1, 1, 1])
    #plt.show()
    # Show the plot
    fig.savefig(out_file, dpi=300)
    plt.close()


base_path = '../data/auto/old results/'
for folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder)
    print(folder)
    for i in range(4, 13, 2):
        new_folder_path = os.path.join(folder_path, str(i))
        try:
            plot_pcd(new_folder_path + "/pointcloud.pcd", new_folder_path + "/plotpcd.png")
        except Exception as e:
            print("ERROR")

