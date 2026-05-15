import cv2
import numpy as np

def tune_quality(old_isBlurry,old_isDark,Feedback_quality,alpha=0.02):
    quality=Feedback_quality
    change=4.95-quality
    isBlurry=old_isBlurry
    isDark=old_isDark
    new_isBlurry=alpha*change+isBlurry
    new_isDark=alpha*change+isDark
    return {'isBlurry':new_isBlurry,'isDark':new_isDark}
    
def imgScore(imgPath,isBlurry,isDark):
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
        "isBlurry": blurriness < isBlurry,
        "isDark": brightness < isDark
    }

    del img
    return score