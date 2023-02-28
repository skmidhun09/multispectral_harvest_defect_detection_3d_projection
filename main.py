import matplotlib
from open3d.cpu.pybind.utility import Vector3dVector
from matplotlib import pyplot as plt
from PIL import Image
import torch
from transformers import GLPNFeatureExtractor, GLPNForDepthEstimation
import numpy as np
import open3d as o3d
import pcd_rotation as rot
import pcd_filter
import axis_model as store

matplotlib.use('TkAgg')
x_max_cutoff = 0
z_cutoff = 0
cord_diff = 0
inc = 0
side_count = 1

def reset_position(image_face,pcd):
    if image_face == 1:
        translation_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -1 * store.get_z_max()[0]], [0, 0, 0, 1]])
        pcd.transform(translation_matrix)
    if image_face == 2:
        translation_matrix = np.array([[1, 0, 0, -1 * store.get_x_max()[1]], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        pcd.transform(translation_matrix)
    if image_face == 3:
        translation_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -1 * store.get_z_min()[2]], [0, 0, 0, 1]])
        pcd.transform(translation_matrix)
    if image_face == 4:
        translation_matrix = np.array([[1, 0, 0, -1 * store.get_x_min()[3]], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        pcd.transform(translation_matrix)


def pcd_cutoff(i, pcd, xmin, xmax, zmin, zmax):
    points = np.asarray(pcd.points).tolist()
    colors = np.asarray(pcd.colors).tolist()

    if i <= 2:
        if zmax != 0:
            index = 0
            while index < len(points):
                _, _, z = points[index]
                index = index + 1
                print(z, zmax)
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
    pcds[0] = pcd_cutoff(1, pcds[0], 0, 0, 0, store.get_z_max()[1])
    pcds[1] = pcd_cutoff(2, pcds[1], 0, store.get_x_max()[0], 0, 0)
    pcds[2] = pcd_cutoff(3, pcds[2], 0, 0, store.get_z_min()[1], 0)
    pcds[3] = pcd_cutoff(4, pcds[3], store.get_x_min()[0], 0, 0, 0)
    return pcds


def create_mesh(pcd):
    # outliers removal
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    pcd = pcd.select_by_index(ind)
    # estimate normals
    pcd.estimate_normals()
    pcd.orient_normals_to_align_with_direction()
    # surface reconstruction
    # mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=15, n_threads=1)[0]
    # rotate the mesh
    # rotation = mesh.get_rotation_matrix_from_xyz((np.pi/2, 0, 0))
    # mesh.rotate(rotation, center=(0, 0, 0))
    # save the mesh
    # o3d.io.write_triangle_mesh(f'./mesh.obj', mesh)
    # Convert point cloud to mesh
    mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,
                                                                              o3d.utility.DoubleVector([0.02, 0.04]))

    # Save mesh as STL file
    o3d.io.write_triangle_mesh("mesh.obj", mesh)
    return mesh


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
    feature_extractor = GLPNFeatureExtractor.from_pretrained("vinvino02/glpn-nyu")
    model = GLPNForDepthEstimation.from_pretrained("vinvino02/glpn-nyu")

    # load and resize the input image
    image = Image.open(imageName)
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
    plt.savefig("depth/" + str(imageNum) + ".png", format="png", bbox_inches='tight', pad_inches=0)
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
    extrinsic[:3, :3] = np.dot(rot.rotation_matrix_y(0), rot.rotation_matrix_x(np.pi))
    # np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    if side_count == 2:
        extrinsic[:3, 3] = np.array([0.0, 0.0, 0.0])
        extrinsic[:3, :3] = np.dot(rot.rotation_matrix_y(np.pi / 2), rot.rotation_matrix_x(np.pi))
    if side_count == 3:
        extrinsic[:3, 3] = np.array([0.0, 0.0, 0.0])
        extrinsic[:3, :3] = np.dot(rot.rotation_matrix_y(np.pi), rot.rotation_matrix_x(np.pi))
    if side_count == 4:
        extrinsic[:3, 3] = np.array([0.0, 0.0, 0.0])
        extrinsic[:3, :3] = np.dot(rot.rotation_matrix_y(3 * np.pi / 2), rot.rotation_matrix_x(np.pi))
    # create point cloud
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, camera_intrinsic, extrinsic)
    pcd = pcd_filter.color_filter(pcd,side_count)
    reset_position(1, pcd)
    side_count = side_count + 1
    return pcd


def mainfunc():
    plt.axis('off')
    pcds = []
    for i in range(6, 10):
        print(i)
        pcds.append(createPointCloud("3D/" + str(i) + ".jpg", i))
    print(store.get_x_min())
    pcds = point_cutoff(pcds)
    o3d.visualization.draw_geometries(pcds)
    for j in range(1, len(pcds)):
        point_cutoff(pcds[j])
    pcd = pcds[0]
    for k in range(1, len(pcds)):
        pcd = combine_point_clouds(pcd, pcds[k])
    mesh = create_mesh(pcd)
    # visualize the mesh
    o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)


mainfunc()
