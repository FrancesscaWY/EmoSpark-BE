from pyAudioAnalysis import ShortTermFeatures
import scipy.io.wavfile as wav

[rate, signal] = wav.read("example.wav")
features, feature_names = ShortTermFeatures.feature_extraction(signal, rate, 0.050*rate, 0.025*rate)

print("特征矩阵形状:", features.shape)  # 每行一个特征
print("特征名称:", feature_names)
