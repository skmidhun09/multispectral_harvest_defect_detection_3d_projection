from matplotlib import pyplot as plt
import open3d as o3d
import threading

import main

def mainfuncMultiThread():
    plt.axis('off')
    pcds = []
    threads = []
    for i in range(6, 10):
        print(i)
        t = threading.Thread(target=main.createPointCloud, args=("input/" + str(i) + ".jpg", i, pcds))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
        # pcds.append(t.result)
    o3d.visualization.draw_geometries(pcds)
    pcd = pcds[0]
    for j in range(1, len(pcds)):
        pcd = main.combine_point_clouds(pcd, pcds[j])
    mesh = main.create_mesh(pcd)
    # visualize the mesh
    o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)