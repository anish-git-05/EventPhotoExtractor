import os
from ML.ImgCluster import cluster_images
from ML.FeatureExtraction import extract_features
from ML.ImgQuality import imgScore
import numpy as np
import shutil
import gc

def ImgPipeline(inputFolder,outputFolder,hParams,top_k):
    eps=hParams['eps']
    isBlurry=hParams['isBlurry']
    isDark=hParams['isDark']
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
        scores[imgPath]=imgScore(imgPath,isBlurry=isBlurry,isDark=isDark)
        gc.collect()
    features = np.array(features, dtype=np.float32)
    best_photos=[]
    clusters=cluster_images(features,img_path,eps=eps)
    for label,img_list in clusters.items():
        if label=='noise':
            for noisy_img in img_list:
                if not scores[noisy_img]['isBlurry'] and not scores[noisy_img]['isDark']:
                    best_photos.append(noisy_img)
        else:
            best_img=img_list[0]
            for img in img_list:
                if scores[img]['aestheticness']>scores[best_img]['aestheticness']:
                    best_img=img
            best_photos.append(best_img)
    best_photos_tmp=[]
    for img in best_photos:
        if scores[img]['brightness']<200 and not scores[img]['isBlurry'] and not scores[img]['isDark']:
            best_photos_tmp.append(img)
    best_photos=best_photos_tmp
    best_photos.sort(key=lambda x:scores[x]['aestheticness'],reverse=True)
    best_photos=best_photos[0:min(top_k,len(best_photos))]
    for img in best_photos:
        imgName=os.path.basename(img)
        outputPath=os.path.join(outputFolder,imgName)
        shutil.copy2(img,outputPath)

