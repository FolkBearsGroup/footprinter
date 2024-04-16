import cv2
import numpy as np

# JSON 形式から、変化前(pre)、変化後(post)の座標を読み込む
json = { 
    "pre": [
        { "x": 395, "y":  323 },
        { "x": 418, "y":  320 },
        { "x": 438, "y":  318 },
        { "x": 404, "y":  340 },
        { "x": 427, "y":  338 },
        { "x": 448, "y":  335 },
        { "x": 411, "y":  362 },
        { "x": 435, "y":  358 },
        { "x": 456, "y":  355 },
    ],
    "post": [
        { "x": 300, "y":  300 },
        { "x": 390, "y":  300 },
        { "x": 480, "y":  300 },
        { "x": 300, "y":  390 },
        { "x": 390, "y":  390 },
        { "x": 480, "y":  390 },
        { "x": 300, "y":  480 },
        { "x": 390, "y":  480 },
        { "x": 480, "y":  480 },
    ]
}




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

# ホモグラフィ変換
M, status = cv2.findHomography(pts1, pts2)
print(M)


# CSVファイルから座標を読み込んで、
# 1フレームごとに変換後の座標を計算する

data = np.genfromtxt('trace.csv', delimiter=',')
pts1 = data[:, :2]

with open("trace-post.csv", "a") as f:
    f.write(f"time,id,x,y,w,h\n")
    for i in range(len(data)):
        # 変換前の座標を表示
        time = data[i][0]
        id = data[i][1]
        x = data[i][2]
        y = data[i][3]
        w = data[i][4]
        h = data[i][5]
        print("pre ", time, x, y, w, h)

        pts = np.float32([[x, y], [x+w, y], [x+w, y+h], [x, y+h]]).reshape(-1,1,2)    
        # 変換後の座標を表示
        transformed_pts = cv2.perspectiveTransform(pts, M)
        x1 = transformed_pts[0][0][0]
        y1 = transformed_pts[0][0][1]
        x2 = transformed_pts[2][0][0]
        y2 = transformed_pts[2][0][1]
        w = x2 - x1
        h = y2 - y1
        print("post", time, x, y, w, h)
        # 結果を CSV 形式で出力する
        f.write(f"{time},{id},{x},{y},{w},{h}\n")

    # クローズ処理
    f.close()

