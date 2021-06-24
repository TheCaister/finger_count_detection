import cv2
import time
import os
import hand_tracking_module as htm

# Setting up webcam
width_camera, height_camera = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, width_camera)
cap.set(4, height_camera)

# Storing the finger images in a list
folder_path = "finger_numbers"
my_list = os.listdir(folder_path)
overlay_list = []

for image_path in my_list:
    image = cv2.imread(f'{folder_path}/{image_path}')
    overlay_list.append(image)
print(len(overlay_list))
previous_time = 0

detector = htm.HandDetector(detection_confidence=0.75)
# List of finger tip landmarks
tip_ids = [4, 8, 12, 16, 20]

while True:
    # For displaying webcam
    success, img = cap.read()

    # Find hands and draw them
    img = detector.find_hands(img)

    # Getting a list of landmarks but don't draw them
    landmarks_list = detector.find_position(img, draw=False)
    # print(landmarks_list)

    if len(landmarks_list) != 0:
        for id in range(0, 5):
            # Get the y value of fingertips and their corresponding lower knuckles
            if landmarks_list[tip_ids[id]][2] < landmarks_list[tip_ids[id] - 2][2]:
                print("Index finger up")

    overlay_list[0] = cv2.resize(overlay_list[0], (200, 200))
    height, width, channel = overlay_list[0].shape
    img[0:height, 0:width] = overlay_list[0]

    # Calculating FPS
    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time
    cv2.putText(img, f"FPS: {int(fps)}", (400, 70), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)