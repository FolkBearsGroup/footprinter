import cv2
from ultralytics import YOLO

# 学習済みのモデルをロード
model = YOLO('yolov8n.pt')

# 動画ファイル(or カメラ)を開く
video_path = "MOV_1503.mp4"
cap = cv2.VideoCapture(video_path)

# キーが押されるまでループ
while cap.isOpened():
    # １フレーム読み込む
    success, frame = cap.read()

    if success:
        # YOLOv8でトラッキング
        results = model.track(frame, persist=True)

        # 結果を画像に変換
        annotated_frame = results[0].plot()

        # OpenCVで表示＆キー入力チェック
        cv2.imshow("YOLOv8 Tracking", annotated_frame)
        key = cv2.waitKey(1)
        if key != -1 : 
            print("STOP PLAY")
            break
