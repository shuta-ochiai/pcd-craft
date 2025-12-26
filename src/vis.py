import open3d as o3d
from fire import Fire

def visualize_pcd(pcd_path):
    pcd = o3d.io.read_point_cloud(pcd_path)
    o3d.visualization.draw_geometries([pcd])

if __name__ == "__main__":
    Fire(visualize_pcd)
