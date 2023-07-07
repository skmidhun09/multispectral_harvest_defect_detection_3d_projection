import os
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker


def plot_pcd_density(y1,y2, outpath):
    # Create sample data as lists
    x = [4, 6, 8, 10, 12]  # X values

    x = np.array(x)
    y1 = np.array(y1)
    y2 = np.array(y2)

    # Create a plot
    plt.plot(x, y1, color="blue", marker='^', markersize=8, label='Upgraded Implementation', markerfacecolor='none',
             markeredgewidth=1.4)
    plt.plot(x, y2, color="red", marker='o', markersize=8, label='Initial Implementation', markerfacecolor='none',
             markeredgewidth=1.4)

    # Set the minor locator for the x-axis
    plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(0.5))

    # Set the minor locator for the y-axis
    plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(20000))

    # Set the tick parameters
    plt.gca().tick_params(axis='both', which='both', direction='in', top=True, right=True)

    # Create a ScalarFormatter with the desired power of 10
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((-3, 3))  # Set the power range

    # Apply the ScalarFormatter to the y-axis
    plt.gca().yaxis.set_major_formatter(formatter)
    major_ticks = plt.gca().yaxis.get_majorticklocs()
    for tick in major_ticks:
        plt.axhline(y=tick, color='gray', linewidth=0.5)

    # Show all spines
    plt.gca().spines['top'].set_visible(True)
    plt.gca().spines['right'].set_visible(True)

    # Set the x and y axis labels
    plt.xlabel('Number of Images')
    plt.ylabel('Point Count')
    # Adjust plot layout to make space for the legend
    # plt.subplots_adjust(top=1.2)
    # plt.legend(loc='upper right')
    # plt.tight_layout()
    plt.legend(loc='upper left')

    plt.savefig(outpath, dpi=300)
    # Show the plot
    #plt.show()
    plt.close()


base_path = '../data/auto/results/'
old_base_path = '../data/auto/old results/'
for folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder)
    folder_path1 = os.path.join(old_base_path, folder)
    print(folder)
    pcd_density = []
    old_pcd_density = []

    new_folder_path = ""

    for i in range(4, 13, 2):
        new_folder_path = os.path.join(folder_path, str(i))
        old_folder_path = os.path.join(folder_path1, str(i))
        try:
            pcd = o3d.io.read_point_cloud(new_folder_path + "/pointcloud.pcd")
            points = np.asarray(pcd.points)
            pcd_density.append(len(points))

            old_pcd = o3d.io.read_point_cloud(old_folder_path + "/pointcloud.pcd")
            old_points = np.asarray(old_pcd.points)
            old_pcd_density.append(len(old_points))

        except Exception as e:
            print("ERROR", e)
    print([pcd_density], [old_pcd_density])
    plot_pcd_density(pcd_density, old_pcd_density, new_folder_path + "/pcd_density.png")
