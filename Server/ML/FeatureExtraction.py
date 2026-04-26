import onnxruntime as ort
import numpy as np
from PIL import Image
import os

def preprocess_image(img_path):
    img = Image.open(img_path).convert('RGB')
    img = img.resize((224, 224), Image.BILINEAR)
    
    img_data = np.array(img, dtype=np.float32) / 255.0
    
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    
    img_data = (img_data - mean) / std
    img_data = img_data.transpose(2, 0, 1)
    img_data = np.expand_dims(img_data, axis=0).astype(np.float32)
    
    return img_data

_session = None

def get_model():
    global _session
    if _session is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, 'mobilenet_v2.onnx')
        _session = ort.InferenceSession(model_path)
    return _session

def extract_features(img_path):
    session = get_model()
    input_tensor = preprocess_image(img_path)
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: input_tensor})
    return outputs[0].flatten()