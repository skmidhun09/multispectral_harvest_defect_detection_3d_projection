import cv2
import matplotlib
from open3d.cpu.pybind.utility import Vector3dVector
from matplotlib import pyplot as plt
from PIL import Image
import torch
from transformers import GLPNImageProcessor, GLPNForDepthEstimation
import numpy as np
import open3d as o3d
from msksoft.pcd import filter, rotation as rot, translation as trans
from msksoft.ds import json_data_store as data_store
from msksoft.img import correction as crct
from msksoft.pcd import mesh
#import save_fbx
matplotlib.use('TkAgg')
x_max_cutoff = 0
z_cutoff = 0
cord_diff = 0
inc = 0
side_count = 1


def pcd_cutoff(i, pcd, xmin, xmax, zmin, zmax):
    points = np.asarray(pcd.points).tolist()
    colors = np.asarray(pcd.colors).tolist()

    if i <= 2:
        if zmax != 0:
            index = 0
            while index < len(points):
                _, _, z = points[index]
                index = index + 1
                #print(z, zmax)
                if z > zmax:
                    del points[index]
                    del colors[index]
                    print("worked")
        if xmax != 0:
            index = 0
            while index < len(points):
                x, _, _ = points[index]
                index = index + 1
                if x > xmax:
                    del points[index]
                    del colors[index]
                    print("worked")
    elif i >= 3:
        if zmin != 0:
            index = 0
            while index < len(points):
                _, _, z = points[index]
                index = index + 1
                if z < zmin:
                    del points[index]
                    del colors[index]
                    print("worked")
        if xmin != 0:
            index = 0
            while index < len(points):
                x, _, _ = points[index]
                index = index + 1
                if x < xmin:
                    del points[index]
                    del colors[index]
                    print("worked")
    colors_array = np.array(colors)
    points_array = np.array(points)
    pcd.points = Vector3dVector(points_array)
    pcd.colors = Vector3dVector(colors_array)
    return pcd


def point_cutoff(pcds):
    pcds[0] = pcd_cutoff(1, pcds[0], 0, 0, 0, data_store.read_list("2")["zmax"])
    pcds[1] = pcd_cutoff(2, pcds[1], 0, data_store.read_list("1")["xmax"], 0, 0)
    pcds[2] = pcd_cutoff(3, pcds[2], 0, 0, data_store.read_list("2")["zmin"], 0)
    pcds[3] = pcd_cutoff(4, pcds[3], data_store.read_list("1")["xmin"], 0, 0, 0)
    return pcds


def combine_point_clouds(pcd1, pcd2):
    # Combine the points and colors from the two point clouds into single numpy arrays
    combined_points = np.vstack((pcd1.points, pcd2.points))
    combined_colors = np.vstack((pcd1.colors, pcd2.colors))

    # Create a new point cloud from the combined arrays
    combined_pcd = o3d.geometry.PointCloud()
    combined_pcd.points = o3d.utility.Vector3dVector(combined_points)
    combined_pcd.colors = o3d.utility.Vector3dVector(combined_colors)
    return combined_pcd


#############################
def createPointCloud(imageName, imageNum):
    feature_extractor = GLPNImageProcessor.from_pretrained("vinvino02/glpn-nyu")
    model = GLPNForDepthEstimation.from_pretrained("vinvino02/glpn-nyu")

    # load and resize the input image
    img = cv2.imread(imageName)
    image = crct.correctedPIl(img)
    #image = Image.open(imageName)
    new_height = 480 if image.height > 480 else image.height
    new_height -= (new_height % 32)
    new_width = int(new_height * image.width / image.height)
    diff = new_width % 32
    new_width = new_width - diff if diff < 16 else new_width + 32 - diff
    new_size = (new_width, new_height)
    image = image.resize(new_size)

    # prepare image for the model
    inputs = feature_extractor(images=image, return_tensors="pt")

    # get the prediction from the model
    with torch.no_grad():
        outputs = model(**inputs)
        predicted_depth = outputs.predicted_depth

    # remove borders
    pad = 16
    output = predicted_depth.squeeze().cpu().numpy() * 1000.0
    output = output[pad:-pad, pad:-pad]
    image = image.crop((pad, pad, image.width - pad, image.height - pad))

    ##########################################

    width, height = image.size

    depth_image = (output * 255 / np.max(output)).astype('uint8')
    plt.imshow(depth_image, cmap="plasma")
    plt.savefig("outputs/depth/" + str(imageNum) + ".png", format="png", bbox_inches='tight', pad_inches=0)
    image = np.array(image)
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
    global max_cord, cord_diff, side_count
    extrinsic[:3, 3] = np.array([0.0, 0.0, 0.0])
    extrinsic[:3, :3] = np.dot(rot.rotation_matrix_y(( side_count - 1 ) * ( np.pi / 2 )), rot.rotation_matrix_x(np.pi))
    # create point cloud
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, camera_intrinsic, extrinsic)
    pcd = filter.color_filter(pcd, side_count)
    trans.reset_position(side_count, pcd)
    side_count = side_count + 1
    return pcd



def main_func():
    plt.axis('off')
    data_store.reset()
    pcds = []
    for i in range(19, 23):
        print(i)
        pcds.append(createPointCloud("input/" + str(i) + ".jpg", i))
    print(data_store.read_all())
    pcds = point_cutoff(pcds)
    trans.align_pcd(pcds)
    o3d.visualization.draw_geometries(pcds)
    #for j in range(1, len(pcds)):
    #    point_cutoff(pcds[j])
    pcd = pcds[0]
    for k in range(1, len(pcds)):
        pcd = combine_point_clouds(pcd, pcds[k])
    o3d.io.write_point_cloud("pointcloud.pcd", pcd)
    pcd_array = np.asarray(pcd.points)
    pcd_colors = np.asarray(pcd.colors)
    with open("point_cloud.txt", "w") as f:
        for i, point in enumerate(pcd_array):
            f.write(f"{point[0]},{point[1]},{point[2]},{pcd_colors[i][0]},{pcd_colors[i][1]},{pcd_colors[i][2]}\n")
    #translation_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -1], [0, 0, 0, 1]])
    #pcd.transform(translation_matrix)
    #mesh.show_axis(pcd)
    object3d = mesh.generate(pcd)
    o3d.io.write_triangle_mesh("copy_of_knot.ply", object3d)
    #save_fbx.save(pcd, object3d)
    # visualize the mesh
    o3d.visualization.draw_geometries([object3d], mesh_show_back_face=True)


main_func()
