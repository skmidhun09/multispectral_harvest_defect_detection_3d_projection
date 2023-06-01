import pyassimp
import numpy as np


def save(point_cloud, triangle_mesh):
    scene = pyassimp.structs.scene.Scene()
    cloud_node = pyassimp.structs.Node("PointCloud")
    mesh_node = pyassimp.structs.Node("TriangleMesh")

    # Add the point cloud vertices to the mesh node
    cloud_mesh = pyassimp.structs.Mesh(
        vertices=np.asarray(point_cloud.points, dtype=np.float32)
    )
    mesh_node.meshes.append(cloud_mesh)

    # Add the triangle mesh to the mesh node
    mesh_mesh = pyassimp.structs.Mesh(
        vertices=np.asarray(triangle_mesh.vertices, dtype=np.float32),
        faces=np.asarray(triangle_mesh.triangles, dtype=np.uint32)
    )
    mesh_node.meshes.append(mesh_mesh)

    # Add the nodes to the scene
    scene.rootnode.children.append(cloud_node)
    scene.rootnode.children.append(mesh_node)

    # Export the scene to an FBX file
    pyassimp.export(scene, "output.fbx", file_type="fbx")
