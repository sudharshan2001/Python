import cv2
import numpy as np
import sys

cap = cv2.VideoCapture(0)

while True:
    _, img = cap.read()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, (30, 125, 40), (225, 225, 255))
    mask_3d = np.repeat(mask[:, :, np.newaxis], 3, axis=2)

    blurred_frame = cv2.GaussianBlur(img, (5, 5), 0)

    alter = np.where(mask_3d == (255, 255, 255), img, blurred_frame)

    gray = cv2.cvtColor(alter, cv2.COLOR_BGR2GRAY)

    canny = cv2.Canny(gray, 60, 60)
    _, mask = cv2.threshold(canny, 10, 255, cv2.THRESH_BINARY)

    cv2.imshow('Video', mask)
    print(mask)
    print(mask.shape)

    if cv2.waitKey(1) == 13:
        break

cap.release()
cv2.destroyAllWindows()
