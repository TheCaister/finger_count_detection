import cv2
import time
import os

width_camera, height_camera = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, width_camera)
cap.set(4, height_camera)

while True:
    success, img = cap.read()
    cv2.imshow("Image", img)
    cv2.waitKey(1)