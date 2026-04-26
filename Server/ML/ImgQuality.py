import cv2
import numpy as np

def calculate_blurriness(imgPath):
    img=cv2.imread(imgPath)
    if img is None:
        raise ValueError(f"Could not read image at path: {imgPath}")
    grayImg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)    
    lap=cv2.Laplacian(grayImg,cv2.CV_64F).var()
    return lap

def calculate_brightness(imgPath):
    img=cv2.imread(imgPath)
    if img is None:
        raise ValueError(f"Could not read image at path: {imgPath}")
    grayImg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    brightness=np.mean(grayImg)
    return brightness

def imgScore(imgPath):
    blurriness=calculate_blurriness(imgPath)
    brightness=calculate_brightness(imgPath)
    score={
        "blurriness": blurriness,
        "brightness": brightness,
        "isBlurry": blurriness < 100,
        "isDark": brightness < 50
    }
    return score
