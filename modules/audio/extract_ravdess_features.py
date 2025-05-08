import os
import glob
import pandas as pd
import opensmile

# 情绪代码 -> 英文标签映射
emotion_map = {
    "01": "neutral",
    "02": "calm",
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "fearful",
    "07": "disgust",
    "08": "surprised",
}

# 初始化 opensmile
smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.eGeMAPSv02,
    feature_level=opensmile.FeatureLevel.Functionals,
)

# 设置音频目录
base_dir = r"D:\桌面\myenv\InternetDev\EmoSpark-BE\modules\audio\RAVDESS"
output_csv = os.path.join(base_dir, "features_with_labels.csv")

# 收集所有 .wav 文件
wav_files = glob.glob(os.path.join(base_dir, "**", "*.wav"), recursive=True)

# 提取特征并添加情绪标签
all_features = []

for wav_path in wav_files:
    try:
        # 提取特征
        features = smile.process_file(wav_path)

        # 提取文件名
        filename = os.path.basename(wav_path)
        parts = filename.split("-")
        emotion_code = parts[2]
        emotion_label = emotion_map.get(emotion_code, "unknown")

        # 添加标签列
        features["filename"] = filename
        features["emotion"] = emotion_label

        all_features.append(features)

    except Exception as e:
        print(f"❌ Error processing {wav_path}: {e}")

# 合并所有特征并保存
if all_features:
    df = pd.concat(all_features)
    df.to_csv(output_csv, index=False)
    print(f"✅ 特征提取完成，保存为：{output_csv}")
else:
    print("⚠️ 未提取任何音频特征，请检查文件路径和格式。")
