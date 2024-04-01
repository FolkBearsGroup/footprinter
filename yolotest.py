import cv2
import torch

# YOLOモデルを読み込む
model = torch.hub.load('ultralytics/yolov5', 'yolov5m', pretrained=True)

# 動画を読み込む
cap = cv2.VideoCapture('aVLtuCAKJx7cFLqF.mp4')

k = 0
while cap.isOpened():
    # 1Fずつ動画を切り出す
    ret, frame = cap.read()
    if not ret:
        print("break")
        break

    # YOLOでフレームから人間を検出
    results = model(frame)

    # 検出された人間にバウンディングボックスを描画
    labels, cords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
    n = len(labels)
    for i in range(n):
        row = cords[i]
        if labels[i] == 0: # 0は通常人間を表す
            x1, y1, x2, y2 = int(row[0]*frame.shape[1]), int(row[1]*frame.shape[0]), int(row[2]*frame.shape[1]), int(row[3]*frame.shape[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # 処理されたフレームを保存
    cv2.imwrite(f"{k:010}.png", frame)
    k+=1

cap.release()
