import cv2
import numpy as np

def tune_quality(old_isBlurry,old_isDark,Feedback_quality,alpha=20.0):
    quality=Feedback_quality
    change=4.95-quality
    isBlurry=old_isBlurry
    isDark=old_isDark
    new_isBlurry=alpha*change+isBlurry
    new_isDark=1.5*change+isDark
    return {'isBlurry':new_isBlurry,'isDark':new_isDark}
    

def imgScore(imgPath,isBlurry,isDark):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
    if img is None:
        return {
            "blurriness": 0, "brightness": 0,
            "isBlurry": True, "isDark": True
        }
    height, width = img.shape[:2]
    if width > 800:
        scale = 800 / width
        img = cv2.resize(img, (800, int(height * scale)), interpolation=cv2.INTER_AREA)
    img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(img_gray,1.1,2)
    H,W=img_gray.shape[:2]
    powerpoints=[(W/3,H/3),(2*W/3,H/3),(2*W/3,2*H/3),(W/3,2*H/3)]
    bonus_aesthetic=0
    for face in faces:
        face_center=(face[0]+face[2]/2,face[1]+face[3]/2)
        min_dst=float('inf')
        for pt in powerpoints:
            dst=(pt[0]-face_center[0])**2+(pt[1]-face_center[1])**2
            min_dst=min([min_dst,dst])
        if min_dst<10000:
            bonus_aesthetic+=50
    brightness = np.mean(img_gray)
    contrast=np.std(img_gray)
    saturation=np.mean(img_hsv[:,:,1])
    sharpness = cv2.Laplacian(img_gray, cv2.CV_64F).var()
    aestheticness=saturation*2.5+sharpness+contrast*3+bonus_aesthetic*0.75
    score = {
        "aestheticness": float(aestheticness),
        "brightness": float(brightness),
        "isBlurry": aestheticness < isBlurry,
        "isDark": brightness < isDark
    }

    del img
    return score