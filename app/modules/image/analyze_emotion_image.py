from deepface import DeepFace
import numpy as np
from PIL import Image
from io import BytesIO

def analyze_emotion_from_image(image_data: bytes)->dict:
    """
    分析图像数据中的面部情绪，并返回七种情绪的占比
    :param image_data:图像的二进制数据
    :return: dict: 包含七种情绪占比的字典
    """
    try:
        # 将二进制数据转换为图像
        image = Image.open(BytesIO(image_data)).convert('RGB')
        image_array = np.array(image)

        # 使用 DeepFace.analyze() 分析情绪
        analysis = DeepFace.analyze(img_path = image_array, actions=['emotion'],enforce_detection = False)
        # 提取情绪得分
        emotion_scores = analysis[0]['emotion']
        # 将情绪得分转换为字典，确保值为 float 类型
        emotion_scores = {emotion: float(score) for emotion, score in emotion_scores.items()}

        return emotion_scores
    except Exception as e:
        print(f"分析失败: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # 图像文件路径
    image_path = '0RZPD93P2SUQ.jpg'
    try:
        # 以二进制模式读取图像文件
        with open(image_path,'rb') as img_file:
            image_data = img_file.read()

        # 调用 analyze_emotion_from_image 函数进行情绪分析
        result = analyze_emotion_from_image(image_data)
        print(result)
    except Exception as e:
        print(f"读取图像文件失败: {e}")

