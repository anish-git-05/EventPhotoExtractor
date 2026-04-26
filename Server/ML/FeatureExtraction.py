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

weight=models.ResNet50_Weights.DEFAULT
model=models.resnet50(weights=weight)

feature_extractor=nn.Sequential(*list(model.children())[:-1])
feature_extractor.eval()

def extract_features(img_path):
    img=Image.open(img_path).convert('RGB')
    img_tensor=preprocess(img).unsqueeze(0)
    with torch.no_grad():
        features=feature_extractor(img_tensor)
    return features.squeeze().numpy()


