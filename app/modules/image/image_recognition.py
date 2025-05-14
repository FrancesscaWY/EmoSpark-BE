import numpy as np
from PIL import Image
from deepface import DeepFace
from io import BytesIO
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import cv2

app = Flask(__name__)

# 分析单张图片
@app.route('/analyze_frame', methods=['POST'])
def analyze_frame():
    try:
        # 接受前端处理过的二进制数据
        image_data = request.get_data()  # 获取原始二进制流

        # 对数据进行解码
        image = Image.open(BytesIO(image_data)).convert('RGB')
        img_array = np.array(image)  # 将图片数据转化为numpy数组

        # 调用 DeepFace 的 analyze 函数
        objs = DeepFace.analyze(
            img_path=img_array,
            actions=['emotion'],
            detector_backend='retinaface',
            enforce_detection=True,  # 确保检测到人脸
            silent=True  # 关闭日志输出
        )

        # 提取情绪结果
        dominant_emotion = objs[0]['dominant_emotion']
        emotion_scores = objs[0]['emotion']  # 各情绪置信度字典

        # 将 emotion_scores 中的 numpy.float32 转换为标准 Python float
        emotion_scores = {emotion: float(score) for emotion, score in emotion_scores.items()}

        # 打印结果
        print(f"主要情绪： {dominant_emotion}")
        print("详细信息：")
        for emotion, score in emotion_scores.items():
            print(f"- {emotion}: {score:.2f}")

        # 返回 JSON 响应
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
