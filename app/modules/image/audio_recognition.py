import numpy as np
from PIL import Image
from deepface import DeepFace
from io import BytesIO
from flask import Flask, request, jsonify

import matplotlib.pyplot as plt
import cv2

app = Flask(__name__)

# 分析单张图片
#img_path = "images\\0RZPD93P2SUQ.jpg"  # 替换为你的图片路径

@app.route('/analyze_frame', methods=['POST'])#定义api端点，用于处理http请求，
def analyze_frame():
    try:
        #接受前端处理过的二进制数据
        image_data = request.get_data() #获取原始二进制流

        image = Image.open(BytesIO(image_data)).convert('RGB') #对数据进行解码
        img_array = np.array(image) #将图片数据转化为numpy数组


        #调用api
        #返回结果为一个列表，存放每一个检测到的人脸
        objs = DeepFace.analyze(
            img_path=img_array, actions=['emotion'],#路径为图片数据转化的数组
            detector_backend='retinaface',    # 修正2：移除等号多余空格
            enforce_detection=True,  # 确保检测到人脸
            silent=True  # 关闭日志输出
        )

        # 提取情绪结果
        dominant_emotion = objs[0]['dominant_emotion']
        emotion_scores = objs[0]['emotion']  # 各情绪置信度字典

        #打印结果
        print("主要情绪： {dominant_emotion}<UNK>".format(dominant_emotion=dominant_emotion))
        print("详细信息：")
        for emotion, score in emotion_scores.items():
            print(f"- {emotion}: {score:.2f}")

        return jsonify({
            "success": True,
            "dominant_emotion": dominant_emotion,
            "emotion_scores": emotion_scores,
        })

    except Exception as e:
        print(f"分析失败: {e}")
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)