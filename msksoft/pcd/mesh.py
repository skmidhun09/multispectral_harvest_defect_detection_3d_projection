
import open3d as o3d
from msksoft.config import config_loader as cfg


def generate(pcd):
    # outliers removal
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=10, std_ratio=10)
    pcd = pcd.select_by_index(ind)
    # estimate normals
    pcd.estimate_normals()
    pcd.orient_normals_to_align_with_direction()
    # surface reconstruction
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=15, scale=1.2, width=0, linear_fit=False)[0]
    # rotate the mesh
    bbox = pcd.get_axis_aligned_bounding_box()
    #print(str(bbox))
    mesh = mesh.crop(bbox)
    rotation = mesh.get_rotation_matrix_from_xyz((0, 0, 0))
    mesh.rotate(rotation, center=(0, 0, 0))
    mesh.remove_unreferenced_vertices()
    mesh.remove_non_manifold_edges()
    obj_path = str(cfg.get('objfile'))
    o3d.io.write_triangle_mesh(obj_path, mesh)
    return mesh


def show_axis(pcd):
    vis = o3d.visualization.Visualizer()

    # Add point cloud to the visualizer
    vis.create_window()
    vis.add_geometry(pcd)

    # Create mesh coordinate frame
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.0005, origin=[0, 0, 0])
    vis.add_geometry(mesh_frame)

    # Set camera view
    ctr = vis.get_view_control()
    ctr.set_lookat([0, 0, 0])
    ctr.set_front([1, 0, 0])
    ctr.set_up([0, 0, 1])

    # Run visualizer
    vis.run()