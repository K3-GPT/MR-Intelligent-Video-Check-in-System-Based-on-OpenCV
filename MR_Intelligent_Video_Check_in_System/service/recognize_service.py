"""
人脸识别服务
提供人脸识别相关的服务，包括训练识别器、识别图像中的人脸等。
"""

import cv2
import numpy as np
import os

# 必须导入 face 模块
from cv2 import face  # 或使用: import cv2.face

RECOGNIZER = face.LBPHFaceRecognizer_create()  # LBPH识别器
PASS_CONF = 45  # 最高评分，LBPH最高建议用45，特征脸最高建议用22000

base_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在路径
# cascade_path = os.path.join(base_dir, "cascades", "haarcascade_frontalface_default.xml")

# cascade_path = r"D\haarcascade_frontalface_default.xml"
cascade_path = "./cascades/haarcascade_frontalface_default.xml"
# cascade_path = (r"D:\Python Files\Personal projects\OpenCV\MR智能视频打卡系统\service\cascades\haarcascade_frontalface_default.xml")
FACE_CASCADE = cv2.CascadeClassifier(cascade_path)

# 训练识别器
def train(photos, labels):
    RECOGNIZER.train(photos, np.array(labels))  # 识别器开始训练


# 识别器识别图像中的人脸
def recognise_face(photo):
    label, confidence = RECOGNIZER.predict(photo)  # 识别器开始分析人脸图像
    if confidence > PASS_CONF:  # 忽略评分大于最高评分的结果
        return -1
    return label


# 判断图像中是否有正面人脸
def found_face(gray_img):
    faces = FACE_CASCADE.detectMultiScale(gray_img, 1.15, 4)  # 找出图像中所有的人脸
    return len(faces) > 0  # 返回人脸数量大于0的结果

