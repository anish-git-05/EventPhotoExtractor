import cv2
import numpy as np

def imgScore(imgPath):
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        return {
            "blurriness": 0, "brightness": 0,
            "isBlurry": True, "isDark": True
        }

    height, width = img.shape[:2]
    if width > 800:
        scale = 800 / width
        img = cv2.resize(img, (800, int(height * scale)), interpolation=cv2.INTER_AREA)

    brightness = np.mean(img)
    blurriness = cv2.Laplacian(img, cv2.CV_64F).var()

    score = {
        "blurriness": float(blurriness),
        "brightness": float(brightness),
        "isBlurry": blurriness < 100,
        "isDark": brightness < 50
    }

    del img
    return score