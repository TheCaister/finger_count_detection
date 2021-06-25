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
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    # Find hands and draw them
    img = detector.find_hands(img)

    # Getting a list of landmarks but don't draw them
    landmarks_list = detector.find_position(img, draw=False)
    # print(landmarks_list)

    # Only process and draw things if landmarks and hands are detected
    if len(landmarks_list) != 0:
        fingers = []

        # Get the x value of thumb tips and their corresponding lower knuckles
        # Code for the thumb is different since it's not like the other fingers
        # If the tip is to the right of the lower knuckle, we can say the thumb is up
        # Have yet to check for handedness
        if landmarks_list[tip_ids[0]][1] > landmarks_list[tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            # Get the y value of fingertips and their corresponding lower knuckles
            # If the tip is above the lower knuckle, we can say it's up
            # Then append it to the fingers list
            if landmarks_list[tip_ids[id]][2] < landmarks_list[tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        # Find how many ones are in the fingers list
        total_fingers = fingers.count(1)

        # Display the appropriate finger image
        overlay_list[total_fingers - 1] = cv2.resize(overlay_list[total_fingers - 1], (200, 200))
        height, width, channel = overlay_list[total_fingers - 1].shape
        img[0:height, 0:width] = overlay_list[total_fingers - 1]

        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(total_fingers), (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    10, (255, 0, 0), 25)

    # Calculating FPS
    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time
    cv2.putText(img, f"FPS: {int(fps)}", (250, 70), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)