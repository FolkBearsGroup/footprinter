import cv2
import torch
from PIL import Image
from ultralytics import YOLO
import numpy as np

# 学習済みのモデルをロード
# model = torch.hub.load('ultralytics/yolov8', 'yolov8x', pretrained=True, trust_repo=True)
model = YOLO('yolov8n.pt')


# 動画ファイル(or カメラ)を開く
video_path = "sample.mp4"
cap = cv2.VideoCapture(video_path)

with open("trace.csv", "a") as f:
    f.write(f"time,id,x,y,w,h\n")

    # キーが押されるまでループ
    while cap.isOpened():
        # １フレーム読み込む
        success, frame = cap.read()
        # フレームの時刻を得る msec
        time = cap.get(cv2.CAP_PROP_POS_MSEC)

        if success:
            # YOLOv8でトラッキング
            results = model.track(frame, persist=True)
            # 結果を画像に変換
            annotated_frame = results[0].plot()

            # 検出された人間(0)のバウンディングボックスを取得
            for box in results[0].boxes:
                if box.cls[0] == 0 :
                    id = int(box.id[0]) 
                    x, y, w, h = map( float, box.xywh[0] ) 
                    print( time, id, x, y, w, h )

                    # 結果を CSV 形式で出力する
                    f.write(f"{time},{id},{x},{y},{w},{h}\n")

            # OpenCVで表示＆キー入力チェック
            cv2.imshow("YOLOv8 Tracking", annotated_frame)
            key = cv2.waitKey(1)
            if key != -1 : 
                print("STOP PLAY")
                break
    # クローズ処理
    f.close()






