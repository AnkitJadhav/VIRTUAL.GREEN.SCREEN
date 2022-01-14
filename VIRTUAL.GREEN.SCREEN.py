import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
time.sleep(2)

background = 0
for i in range(80):
    ret, background = cap.read()

while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 100, 40])
    upper_red = np.array([0, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([110, 110, 80])
    upper_red = np.array([190, 255, 255])

    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask1 = mask1 + mask2
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)

    mask2 = cv2.bitwise_or(mask1)

    res1 = cv2.bitwise_and(background, background, mask1)
    res2 = cv2.bitwise_and(img, img, mask=mask2)
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow('VIRTUAL GREEN SCREEN', final_output)

    k = cv2.waitKey(10)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()