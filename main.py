import os
import threading
import time
from datetime import datetime
import cv2
import matplotlib
from open3d.cpu.pybind.utility import Vector3dVector
from PIL import Image
import torch
from transformers import GLPNImageProcessor, GLPNForDepthEstimation
import numpy as np
import open3d as o3d
from msksoft.pcd import rotation as rot, translation as trans, removebg as bg
from msksoft.ds import json_data_store as data_store
from msksoft.img import correction as crct
from msksoft.pcd import mesh


class GeneratePCD:
    base = "data/auto1/results/"
    path = ""

    input_range = [1, 5]
    # import save_fbx
    matplotlib.use('TkAgg')
    x_max_cutoff = 0
    z_cutoff = 0
    cord_diff = 0
    inc = 0
    side_count = 1

    def save_pcd(self, side, pcd):
        o3d.io.write_point_cloud(self.path + side + ".pcd", pcd)

    def read_pcd(self, side):
        pcd = o3d.io.read_point_cloud(self.path + side + ".pcd")
        return pcd

    def display_point_cloud(self, pcd, path):
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        vis.add_geometry(pcd)
        vis.update_geometry(pcd)
        vis.poll_events()
        vis.update_renderer()
        vis.capture_screen_image(path)
        vis.destroy_window()

    def align_pcd_to_center(self, pcd):
        # Compute centroid
        centroid = pcd.get_center()

        # Calculate translation vector
        translation = -centroid

        # Apply translation to point cloud
        pcd.translate(translation)

        return pcd

    def pcd_cutoff(self, i, pcd, xmin, xmax, zmin, zmax):
        points = np.asarray(pcd.points).tolist()
        colors = np.asarray(pcd.colors).tolist()

        if i <= 2:
            if zmax != 0:
                index = 0
                while index < len(points):
                    _, _, z = points[index]
                    index = index + 1
                    # print(z, zmax)
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

    def point_cutoff(self, pcds):
        pcds[0] = self.pcd_cutoff(1, pcds[0], 0, 0, 0, data_store.read_list("2")["zmax"])
        pcds[1] = self.pcd_cutoff(2, pcds[1], 0, data_store.read_list("1")["xmax"], 0, 0)
        pcds[2] = self.pcd_cutoff(3, pcds[2], 0, 0, data_store.read_list("2")["zmin"], 0)
        pcds[3] = self.pcd_cutoff(4, pcds[3], data_store.read_list("1")["xmin"], 0, 0, 0)
        return pcds

    def combine_point_clouds(self, pcd1, pcd2):
        # Combine the points and colors from the two point clouds into single numpy arrays
        combined_points = np.vstack((pcd1.points, pcd2.points))
        combined_colors = np.vstack((pcd1.colors, pcd2.colors))

        # Create a new point cloud from the combined arrays
        combined_pcd = o3d.geometry.PointCloud()
        combined_pcd.points = o3d.utility.Vector3dVector(combined_points)
        combined_pcd.colors = o3d.utility.Vector3dVector(combined_colors)
        return combined_pcd

    def estimate_depth_glpn(self, imagePath, imageName):
        glpn_start = datetime.now()
        feature_extractor = GLPNImageProcessor.from_pretrained("vinvino02/glpn-nyu")
        model = GLPNForDepthEstimation.from_pretrained("vinvino02/glpn-nyu")
        # load and resize the input image
        img = cv2.imread(imagePath + imageName)
        image = crct.correctedPIl(img)
        # image = Image.open(imagePath + imageName)
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
        formatted = (output * 255 / np.max(output)).astype('uint8')
        depth_image = Image.fromarray(formatted)
        depth_image.save(self.path + "d" + imageName)
        image.save(self.path + imageName)
        print("GLPN Time taken for ", imageName, ": ", (datetime.now() - glpn_start).total_seconds(), "s")

    #############################
    def create_pcd(self, image_num, image_ext, sidecount, total, pcds, lock):
        pcs_start = datetime.now()
        inp_image = Image.open(self.path + image_num + image_ext)
        width, height = inp_image.size
        print(self.path + "d" + image_num + image_ext)
        depth_image = Image.open(self.path + "d" + image_num + image_ext)
        # plt.imshow(depth_image, cmap="plasma")
        # plt.savefig("outputs/depth/" + str(image_num) + ".png", format="png", bbox_inches='tight', pad_inches=0)
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
        self.cord_diff
        extrinsic[:3, 3] = np.array([0.0, 0.0, 0.0])
        # sidecount = 1
        extrinsic[:3, :3] = np.dot(rot.rotation_matrix_y(((sidecount - 1) * ((2 * np.pi) / total))),
                                   rot.rotation_matrix_x(np.pi))

        pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, camera_intrinsic, extrinsic)
        self.display_point_cloud(pcd, self.path + "pcd" + str(sidecount) + ".jpg")
        # pcd = filter.color_filter(pcd, sidecount)
        pcd = bg.remove(inp_image, pcd)
        self.display_point_cloud(pcd, self.path + "pcdfilt" + str(sidecount) + ".jpg")
        # o3d.visualization.draw_geometries([pcd])

        # color = [153, 0, 0]  # Red color as an example
        # colors = np.full_like(pcd.points, color)
        # pcd.colors = o3d.utility.Vector3dVector(colors / 255.0)
        # random_indices = np.random.choice(len(pcd.points), size=20000, replace=False)
        # downsampled_pcd = pcd.select_by_index(random_indices)
        # o3d.visualization.draw_geometries([downsampled_pcd])

        print("points", len(pcd.points))
        pcd = self.align_pcd_to_center(pcd)
        trans.reset_position(sidecount, total, pcd)
        print("Time taken for image :", image_num, ": ", (datetime.now() - pcs_start).total_seconds(), "s")
        with lock:
            pcds.append(pcd)

    def main_func(self):
        data_store.reset()
        pcds = []
        image_count = self.input_range[1] - self.input_range[0]
        if __name__ != "__main__":
            thread_list1 = []
            tglpn_start = datetime.now()
            for i in range(self.input_range[0], self.input_range[1]):
                # print(i)
                self.estimate_depth_glpn(self.path, str(i) + ".jpg")
            #     thread = threading.Thread(target=estimate_depth_glpn, args=(path, str(i) + ".jpg",))
            #     thread.start()
            #     thread_list1.append(thread)
            # thread_list2 = []
            # for n in range(len(thread_list1)):
            #     thread_list1[n].join()
            print("Total GLPN Time taken :", (datetime.now() - tglpn_start).total_seconds(), "s")
            lock = threading.Lock()
            tpcd_start = datetime.now()
            for j in range(self.input_range[0], self.input_range[1]):
                self.create_pcd(str(j), ".jpg", self.side_count, image_count, pcds, lock)
                #     thread = threading.Thread(target=create_pcd, args=(str(j), ".jpg", side_count, image_count, pcds, lock,))
                self.side_count = self.side_count + 1
            #     thread.start()
            #     thread_list2.append(thread)
            # for k in range(len(thread_list2)):
            #     thread_list2[k].join()
        print("Total PCD Time taken :", (datetime.now() - tpcd_start).total_seconds(), "s")
        # print(data_store.read_all())
        # o3d.visualization.draw_geometries(pcds)
        pcd = pcds[0]

        for k in range(1, len(pcds)):
            pcd = self.combine_point_clouds(pcd, pcds[k])
        self.display_point_cloud(pcd, self.path + "pcd.jpg")
        if len(pcds) == 4:
            o3d.visualization.draw_geometries([pcd])
        o3d.io.write_point_cloud(self.path + "pointcloud.pcd", pcd)
        object3d = mesh.generate(pcd)
        o3d.io.write_triangle_mesh(self.path + "image" + str(image_count) + ".ply", object3d)

    def main_caller(self, name, angles):
        self.path = self.base + name + '/' + str(angles) + '/'
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.input_range[1] = angles + 1
        print(self.input_range[1] - self.input_range[0], " images")
        start = datetime.now()
        self.main_func()
        print("Program Total Time taken :", (datetime.now() - start).total_seconds(), "s")

# main_caller("lime", 6)

# print(input_range[1] - input_range[0], " images")
# start = datetime.now()
# main_func()
# print("Program Total Time taken :", (datetime.now() - start).total_seconds(), "s")
