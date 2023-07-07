import os

import cv2
import numpy as np
from PIL import Image, ImageEnhance
import open3d as o3d
from matplotlib import pyplot as plt, ticker

from msksoft.pcd import rotation as rot, translation as trans, removebg as bg

def plot_pcd_density(y1,y2, outpath):
    # Create sample data as lists
    x = [4, 6, 8, 10, 12]  # X values

    x = np.array(x)
    y1 = np.array(y1)
    y2 = np.array(y2)

    # Create a plot
    plt.plot(x, y1, color="green", marker='^', markersize=8, label='Reflection', markerfacecolor='none',
             markeredgewidth=1.4)
    plt.plot(x, y2, color="red", marker='o', markersize=8, label='Shadow', markerfacecolor='none',
             markeredgewidth=1.4)

    # Set the minor locator for the x-axis
    plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(1))

    # Set the minor locator for the y-axis
    plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(0.2))

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
    plt.ylabel('Pixel Overlap %')
    # Adjust plot layout to make space for the legend
    # plt.subplots_adjust(top=1.2)
    # plt.legend(loc='upper right')
    # plt.tight_layout()
    plt.legend(loc='upper left')

    plt.savefig(outpath, dpi=300)
    # Show the plot
    #plt.show()
    plt.close()


def align_pcd_to_center(pcd):
    # Compute centroid
    centroid = pcd.get_center()

    # Calculate translation vector
    translation = -centroid

    # Apply translation to point cloud
    pcd.translate(translation)

    return pcd


def display_point_cloud(pcd, path):
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()
    vis.capture_screen_image(path)
    vis.destroy_window()


def create_pcd(path):
    image_num = "1"
    total = 4
    inp_image = Image.open(path + "/1.jpg")
    width, height = inp_image.size
    print(path + "/d1.jpg")
    depth_image = Image.open(path + "/d1.jpg")
    depth_image = np.array(depth_image)
    image = np.array(inp_image)
    # create rgbd image
    depth_o3d = o3d.geometry.Image(depth_image)
    image_o3d = o3d.geometry.Image(image)
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(image_o3d, depth_o3d,
                                                                    convert_rgb_to_intensity=False)
    # camera settings
    camera_intrinsic = o3d.camera.PinholeCameraIntrinsic()
    camera_intrinsic.set_intrinsics(width, height, 500, 500, width / 2, height / 2)

    # Create an identity transformation matrix
    extrinsic = np.identity(4)
    # Set the translation component of the matrix
    extrinsic[:3, 3] = np.array([0.0, 0.0, 0.0])
    sidecount = 1
    extrinsic[:3, :3] = np.dot(rot.rotation_matrix_y(((sidecount - 1) * ((2 * np.pi) / total))),
                               rot.rotation_matrix_x(np.pi))

    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, camera_intrinsic, extrinsic)
    pcd = bg.remove(inp_image, pcd)
    # o3d.visualization.draw_geometries([pcd])

    print("points", len(pcd.points))
    pcd = align_pcd_to_center(pcd)
    trans.reset_position(sidecount, total, pcd)
    display_point_cloud(pcd, "../data/temp/overlapimage/pcd1.jpg")
    img = Image.open("../data/temp/overlapimage/pcd1.jpg")
    img = img.convert("L")
    return img


# def project_and_save_point_cloud(path, output_file):
#     img = cv2.imread(path + "1.jpg")
#     sample = crct.correctedPIl(img)
#     sample.show()
#     sample = Image.open(path + "1.jpg")
#
#     image.save(output_file)


# project_and_save_point_cloud("../data/auto/results/tomato/4/", "../data/auto/results/beet/4/pcdtoimg.png")

def est_reflec_shadow(image):
    out = []
    width, height = image.size
    white_pxl = 0
    shadow_pxl = 0
    reflect_pxl = 0
    # Loop through the pixels
    for y in range(height):
        for x in range(width):
            # Get the RGB values of the pixel
            pixel = image.getpixel((x, y))
            if pixel == 255:
                white_pxl = white_pxl + 1
            else:
                if pixel < 80:
                    shadow_pxl = shadow_pxl + 1
                elif pixel > 230:
                    reflect_pxl = reflect_pxl + 1

    total = height * width
    obj_pxl = total - white_pxl
    #print("object", obj_pxl)
    #print("reflection", reflect_pxl)
    #print("shadow", shadow_pxl)
    ref_percent = reflect_pxl/obj_pxl * 100
    sha_percent = shadow_pxl/obj_pxl * 100
    out.append(ref_percent)
    out.append(sha_percent)
    #print("ref, shadow in %", out)
    return out



base_path = "../data/auto/results/"
for folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder)
    print(folder)
    shadow = []
    reflect = []
    for i in range(4, 13, 2):
        new_folder_path = os.path.join(folder_path, str(i))
        real_img = create_pcd(new_folder_path)
        pcd_img = Image.open(new_folder_path+"/pcd.jpg")
        pcd_img = pcd_img.convert("L")
        real = est_reflec_shadow(real_img)
        pcd = est_reflec_shadow(pcd_img)
        reflect.append(pcd[0])
        shadow.append(pcd[1])
    print(reflect)
    print(shadow)
    plot_pcd_density(reflect, shadow, new_folder_path + "/shadow_overlap.png")
