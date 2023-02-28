from matplotlib import pyplot as plt
import open3d as o3d
import multiprocessing as mp
import main
def create_point_cloud_wrapper(args):
    return main.createPointCloud(args[0], args[1])



def mainfuncMultiProcess():
    plt.axis('off')
    pcds = []
    pool = mp.Pool(processes=4)
    jobs = [(f"3D/{i}.jpg", i) for i in range(6, 10)]
    pcds = pool.map(create_point_cloud_wrapper, jobs)
    pool.close()
    pool.join()
    o3d.visualization.draw_geometries(pcds)
    pcd = pcds[0]
    for j in range(1, len(pcds)):
        pcd = main.combine_point_clouds(pcd, pcds[j])
    mesh = main.create_mesh(pcd)
    # visualize the mesh
    o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)