# 動画から相互の距離を計算する Python スクリプト

0. 監視カメラなどの角度を固定した動画を利用する
1. YOLOv8 で「人」を認識する
2. Homography を利用し、床平面の座標に変換する
3. 床平面の座標から、相互の「人」の距離を算出する


## install 

```
pip install numpy opencv-python ultralytics torch
```

## run 

1. YOLOv8 で「人」を認識する

- sample.mp4 : 動画ファイル
- trace.csv  : 「人」を認識した座標、「人」は id が振られる

```
python index.py
```

2. Homography を利用し、床平面の座標に変換する

- tarce.csv : 「人」の座標
- trace-post.csv : 床平面の座標に変換した後


```
python trace.py
```

Homography の座標は、trace.py 内に直接記述されている。
変換前（動画）と変換後（床平面）を９点で比較している。


```python
# 変換前の座標
pts1 = np.array([
        [json["pre"][0]["x"], json["pre"][0]["y"]],
        [json["pre"][1]["x"], json["pre"][1]["y"]],
        [json["pre"][2]["x"], json["pre"][2]["y"]],
        [json["pre"][3]["x"], json["pre"][3]["y"]],
        [json["pre"][4]["x"], json["pre"][4]["y"]],
        [json["pre"][5]["x"], json["pre"][5]["y"]],
        [json["pre"][6]["x"], json["pre"][6]["y"]],
        [json["pre"][7]["x"], json["pre"][7]["y"]],
        [json["pre"][8]["x"], json["pre"][8]["y"]],
        ], dtype=np.float32)
# 変換後の座標
pts2 = np.array([
        [json["post"][0]["x"], json["post"][0]["y"]],
        [json["post"][1]["x"], json["post"][1]["y"]],
        [json["post"][2]["x"], json["post"][2]["y"]],
        [json["post"][3]["x"], json["post"][3]["y"]],
        [json["post"][4]["x"], json["post"][4]["y"]],
        [json["post"][5]["x"], json["post"][5]["y"]],
        [json["post"][6]["x"], json["post"][6]["y"]],
        [json["post"][7]["x"], json["post"][7]["y"]],
        [json["post"][8]["x"], json["post"][8]["y"]],
        ], dtype=np.float32)
```


