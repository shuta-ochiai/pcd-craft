import open3d as o3d
from fire import Fire

def pcd2ply(pcd_path, ply_path):
    pcd = o3d.io.read_point_cloud(pcd_path)
    o3d.io.write_point_cloud(ply_path, pcd)
    print(f"変換完了: {ply_path}")

if __name__ == "__main__":
    Fire(pcd2ply)
