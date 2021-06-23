import cv2
import time
import os

# Setting up webcam
width_camera, height_camera = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, width_camera)
cap.set(4, height_camera)

# Storing the finger images in a list
folder_path = "finger_numbers"
my_list = os.listdir(folder_path)
print(my_list)

while True:
    # For displaying webcam
    success, img = cap.read()
    cv2.imshow("Image", img)
    cv2.waitKey(1)