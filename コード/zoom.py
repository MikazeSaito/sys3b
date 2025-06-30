import cv2
import numpy as np
import glob

# チェスボードの交点の数（マス数 - 1）
chessboard_size = (11, 8)  # 例：9x6マス → 交点は8x5
square_size = 23.0  # 各マスの1辺の長さ（mmなどの実寸）

# 3D世界座標の準備（Z=0の平面上に並んだ点）
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0],
                       0:chessboard_size[1]].T.reshape(-1, 2) * square_size

# すべての画像に共通のオブジェクト点と画像点
objpoints = []  # 3D点
imgpoints = []  # 2D点

# キャリブレーション用画像のパス
images = glob.glob('chess_board/*.jpg')  

image_size = None  # 画像サイズを保存する変数

for fname in images:
    img = cv2.imread(fname)
    if img is None:
        print(f"画像が読み込めませんでした: {fname}")
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # チェスボードの交点を検出
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)

        if image_size is None:
            image_size = gray.shape[::-1]  # 初回の画像サイズを保存

        # 可視化（任意）
        cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
        cv2.imshow('Corners', img)
        cv2.waitKey(100)
    else:
        print(f"チェスボード検出失敗: {fname}")

cv2.destroyAllWindows()

# チェスボード検出に成功した画像が1つ以上あるか確認
if image_size is None:
    print("チェスボードの検出に失敗しました。画像やパターンを確認してください。")
else:
    # カメラの内部パラメータを推定
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, image_size, None, None
    )

    # 結果出力
    print("=== カメラ内部パラメータ ===")
    print("Camera Matrix:\n", camera_matrix)
    print("\nDistortion Coefficients:\n", dist_coeffs)