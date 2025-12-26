import open3d as o3d
import numpy as np
import os

input_pcd_path = "/Users/shu/Downloads/merged.pcd"
denoised_pcd_path = "/Users/shu/Downloads/merged_denoised.pcd"
downsampled_pcd_path = "/Users/shu/Downloads/merged_downsampled.pcd"

# デノイズ済み点群があればそれを使う、なければデノイズして保存
if os.path.exists(denoised_pcd_path):
    print("デノイズ済み点群を読み込みます")
    pcd = o3d.io.read_point_cloud(denoised_pcd_path)
else:
    print("元の点群を読み込み、ノイズ除去します")
    pcd = o3d.io.read_point_cloud(input_pcd_path)
    print(f"元の点群数: {len(pcd.points)}")
    # ノイズ除去を厳しめに
    pcd, ind = pcd.remove_statistical_outlier(nb_neighbors=30, std_ratio=0.8)
    print(f"ノイズ除去後の点群数: {len(pcd.points)}")
    o3d.io.write_point_cloud(denoised_pcd_path, pcd)
    print(f"デノイズ済み点群を保存しました: {denoised_pcd_path}")

# 高品質のためボクセルサイズを小さく
voxel_size = 0.001
print(f"ボクセルサイズ {voxel_size} でダウンサンプリング中...")
if os.path.exists(downsampled_pcd_path):
    print("ダウンサンプリング済み点群を読み込みます")
    pcd_down = o3d.io.read_point_cloud(downsampled_pcd_path)
else:
    pcd_down = pcd.voxel_down_sample(voxel_size=voxel_size)
    o3d.io.write_point_cloud(downsampled_pcd_path, pcd_down)
    print(f"ダウンサンプリング後の点群数: {len(pcd_down.points)}")

pcd_down.estimate_normals(
    search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.01, max_nn=100)
)

center = np.mean(np.asarray(pcd_down.points), axis=0)
pcd_down.orient_normals_towards_camera_location(camera_location=center)

print("ポアソン再構成を実行中...")
# depthを高めに（計算時間が長くなります）
mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
    pcd_down, depth=11
)

# 密度閾値を下げてより多くの頂点を残す
vertices_to_remove = densities < np.quantile(densities, 0.01)
mesh.remove_vertices_by_mask(vertices_to_remove)

o3d.io.write_triangle_mesh("output_mesh.ply", mesh)
print("保存が完了しました: output_mesh.ply")

o3d.io.write_triangle_mesh("output_mesh.glb", mesh)
print("GLB保存が完了しました: output_mesh.glb")

o3d.visualization.draw_geometries([mesh], window_name="Poisson Mesh Result")
