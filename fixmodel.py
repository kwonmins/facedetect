import tensorflow as tf
from tensorflow.keras.models import load_model, save_model

# 모델 로드
model_path = "keras_model.h5"
model = load_model(model_path, compile=False)

# DepthwiseConv2D에서 groups=1 제거
for layer in model.layers:
    if isinstance(layer, tf.keras.layers.DepthwiseConv2D):
        config = layer.get_config()
        if 'groups' in config:
            del config['groups']  # 'groups' 제거
        new_layer = tf.keras.layers.DepthwiseConv2D.from_config(config)
        layer = new_layer

# 수정된 모델 저장
fixed_model_path = "keras_model_fixed.h5"
save_model(model, fixed_model_path)
print("수정된 모델 저장 완료:", fixed_model_path)
