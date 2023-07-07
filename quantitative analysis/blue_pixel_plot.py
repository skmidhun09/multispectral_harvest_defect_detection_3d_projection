import os
import open3d as o3d
import numpy as np
from matplotlib import pyplot as plt, ticker
from open3d.cpu.pybind.utility import Vector3dVector


def get_blue_points(pcd):
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    n_colors = []
    n_points = []
    count = 0
    n = 0
    for color in colors:
        r, g, b = color
        if b > g and b > r:
            if g >= r:
                thresh = 1 - b
                if g < (b - thresh):
                    count = count + 1
                else:
                    n_colors.append(color)
                    n_points.append(points[n])
            else:
                if r < 0.2352941 and b > 0.2352941:
                    count = count + 1
                elif (r - g) < 0.15686274:
                    count = count + 1
                elif (r - g) > 0.15686274 and b > 0.86274509:
                    count = count + 1
                else:
                    n_colors.append(color)
                    n_points.append(points[n])
        else:
            n_colors.append(color)
            n_points.append(points[n])
        n = n + 1
    colors_array = np.array(n_colors)
    points_array = np.array(n_points)
    pcd.points = Vector3dVector(points_array)
    pcd.colors = Vector3dVector(colors_array)
    # o3d.visualization.draw_geometries([pcd])

    return (count / len(points)) * 100


def plot_graph(y1, y2, outpath):
    # Create sample data as lists
    x = [4, 6, 8, 10, 12]  # X values

    x = np.array(x)
    y1 = np.array(y1)
    y2 = np.array(y2)

    # Set the width of each bar
    bar_width = 0.35

    # Calculate the positions of the bars
    bar_positions1 = np.arange(len(x))
    bar_positions2 = bar_positions1 + bar_width

    # Create the bar graph
    plt.bar(bar_positions1, y1, width=bar_width, label='Upgraded Implementation', color="#ff3f34")
    plt.bar(bar_positions2, y2, width=bar_width, label='Initial Implementation', color="#263252")

    # Add labels and title
    plt.xlabel('Number of Images')
    plt.ylabel('Total Blue Points %')
    plt.title('Background Noise')
    plt.ylim(top=max(max(y1), max(y2)) * 1.3)  # Increase the top limit by 20%

    # Set the x-axis tick positions and labels
    plt.xticks(bar_positions1 + bar_width / 2, x)
    plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(0.2))
    # Show all spines
    plt.gca().tick_params(axis='both', which='both', direction='in', top=True, right=True)
    plt.gca().spines['top'].set_visible(True)
    plt.gca().spines['right'].set_visible(True)
    # Add percentage values on top of each bar
    for i, (value1, value2) in enumerate(zip(y1, y2)):
        plt.text(bar_positions1[i], value1, f'{value1:.2f}', ha='center', va='bottom')
        plt.text(bar_positions2[i], value2, f'{value2:.2f}', ha='center', va='bottom')
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    # Display the graph
    #plt.show()
    plt.savefig(outpath, dpi=300)
    plt.close()


base_path = '../data/auto/results/'
old_base_path = '../data/auto/old results/'
for folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder)
    folder_path1 = os.path.join(old_base_path, folder)
    print(folder)
    pcd_blue = []
    old_pcd_blue = []

    new_folder_path = ""

    for i in range(4, 13, 2):
        new_folder_path = os.path.join(folder_path, str(i))
        old_folder_path = os.path.join(folder_path1, str(i))
        try:
            pcd = o3d.io.read_point_cloud(new_folder_path + "/pointcloud.pcd")
            new_points = get_blue_points(pcd)
            pcd_blue.append(new_points)

            old_pcd = o3d.io.read_point_cloud(old_folder_path + "/pointcloud.pcd")
            old_points = get_blue_points(old_pcd)
            old_pcd_blue.append(old_points)

        except Exception as e:
            print("ERROR", e)
    try:
        print([pcd_blue], [old_pcd_blue])
        plot_graph(pcd_blue, old_pcd_blue, new_folder_path + "/pcd_blue_pixel.png")
    except Exception as e:
        print("ERROR", e)
