import cv2
import numpy as np

# カメラ内部パラメータ（焦点距離と主点の仮定値）
camera_matrix = np.array([
    [800, 0, 640],
    [0, 800, 360],
    [0, 0, 1]
], dtype=np.float32)

dist_coeffs = np.zeros((4, 1), dtype=np.float32)  # 歪みなし

# ArUco マーカー辞書と検出パラメータ
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters_create()

# 画像を読み込む（画像パスを適切に設定）
image = cv2.imread("IMG_4531.jpg")

# マーカー検出
corners, ids, _ = cv2.aruco.detectMarkers(image, aruco_dict, parameters=parameters)

if ids is None or len(ids) < 4:
    print("4つのマーカーが検出できませんでした。")
    exit()

# マーカーID → 3D座標の対応
id_to_position = {
    0: [0, 0, 0],
    1: [1, 0, 0],
    2: [0, 1, 0],
    3: [1, 1, 0]
}

image_points = []
object_points = []

for i in range(len(ids)):
    marker_id = int(ids[i][0])
    if marker_id in id_to_position:
        # マーカーの画像上の中心座標を求める
        pts = corners[i][0]
        center = np.mean(pts, axis=0)
        image_points.append(center)
        object_points.append(id_to_position[marker_id])

# 2D/3D点に変換
image_points = np.array(image_points, dtype=np.float32)
object_points = np.array(object_points, dtype=np.float32)

# solvePnPでカメラ姿勢推定
success, rvec, tvec = cv2.solvePnP(
    object_points, image_points, camera_matrix, dist_coeffs
)

if not success:
    print("カメラ姿勢推定に失敗しました。")
    exit()

# カメラ位置を算出
R, _ = cv2.Rodrigues(rvec)
camera_position = -R.T @ tvec

# 結果表示
print("=== カメラの位置と姿勢 ===")
print("回転ベクトル (rvec):\n", rvec)
print("並進ベクトル (tvec):\n", tvec)
print("カメラ位置（世界座標系）:\n", camera_position)