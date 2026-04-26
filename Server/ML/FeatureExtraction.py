import torch
import torchvision.transforms as transforms
import torch.nn as nn
import torchvision.models as models
from PIL import Image
import os

preprocess=transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])  
_model_cache=None
current_dir = os.path.dirname(os.path.abspath(__file__))
def get_model():
    global _model_cache
    if _model_cache is None:
        print("First run: Loading AI model into memory...", flush=True)
        weights_path = os.path.join(os.path.dirname(__file__), 'mobilenet_v2-7ebf99e0.pth')
        model = models.mobilenet_v2()
        model.load_state_dict(torch.load(weights_path, map_location='cpu'))
        model.eval()
        _model_cache = nn.Sequential(
            model.features,
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten()
        )
    return _model_cache

def extract_features(img_path):
    feature_extractor = get_model()
    img=Image.open(img_path).convert('RGB')
    img.thumbnail((256,256))
    img_tensor=preprocess(img).unsqueeze(0)
    with torch.no_grad():
        features=feature_extractor(img_tensor)
    del img
    del img_tensor
    return features.squeeze().numpy()


