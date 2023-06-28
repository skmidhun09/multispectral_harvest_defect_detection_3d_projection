import open3d as o3d
from msksoft.pcd import mesh


# Specify the path to the PCD file
pcd_file_path = "data/auto/results/lime/12/pointcloud.pcd"

# Read the PCD file
pcd = o3d.io.read_point_cloud(pcd_file_path)
o3d.visualization.draw_geometries([pcd])
object3d = mesh.generate(pcd)
o3d.visualization.draw_geometries([object3d], mesh_show_back_face=True)
