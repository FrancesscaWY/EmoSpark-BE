import numpy as np_long
import opensmile
import tensorflow as tf
from tensorflow.keras.models import load_model
form tensorflow.keras.preprocessing import sequence

# 初始化openSMILE特征提取器
smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.GeMAPSv01b,
    feature_level=opensmile.FeatureLevel.Functionals,
)

# 加载预训练的Light-SERNet模型
model = load_model('light_sernet_model.h5')