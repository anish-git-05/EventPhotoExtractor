import os
from ML.ImgCluster import cluster_images
from ML.FeatureExtraction import extract_features
from ML.ImgQuality import imgScore
import numpy as np
import shutil
import gc

def ImgPipeline(inputFolder,outputFolder):
    scores={}
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    img_path=[]
    features=[]
    for img in os.listdir(inputFolder):
        if not img.lower().endswith(('.png','.jpg','.jpeg')):
            continue
        imgPath=os.path.join(inputFolder,img)
        img_path.append(imgPath)
        features.append(extract_features(imgPath))
        scores[imgPath]=imgScore(imgPath)
        gc.collect()
    features = np.array(features, dtype=np.float32)
    best_photos=[]
    clusters=cluster_images(features,img_path,eps=0.09)
    for label,img_list in clusters.items():
        if label=='noise':
            for noisy_img in img_list:
                if not scores[noisy_img]['isBlurry']:
                    best_photos.append(noisy_img)
        else:
            best_img=img_list[0]
            for img in img_list:
                if scores[img]['blurriness']<scores[best_img]['blurriness']:
                    best_img=img
            best_photos.append(best_img)
    for img in best_photos:
        imgName=os.path.basename(img)
        outputPath=os.path.join(outputFolder,imgName)
        shutil.copy2(img,outputPath)

