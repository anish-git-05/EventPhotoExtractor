import torch
import torchvision.transforms as transforms
import torch.nn as nn
import torchvision.models as models
from PIL import Image

preprocess=transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])  

weight=models.MobileNet_V2_Weights.DEFAULT
model=models.mobilenet_v2(weights=weight)
model.eval()
feature_extractor=nn.Sequential(
    model.features,
    nn.AdaptiveAvgPool2d((1, 1)),
    nn.Flatten()
)

def extract_features(img_path):
    img=Image.open(img_path).convert('RGB')
    img.thumbnail((256,256))
    img_tensor=preprocess(img).unsqueeze(0)
    with torch.no_grad():
        features=feature_extractor(img_tensor)
    del img
    del img_tensor
    return features.squeeze().numpy()


