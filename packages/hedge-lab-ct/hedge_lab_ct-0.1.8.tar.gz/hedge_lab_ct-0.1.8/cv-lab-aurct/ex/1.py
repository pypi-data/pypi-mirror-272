import cv2

image = cv2.imread('image.jpg')

x, y, w, h = 100, 100, 300, 200
cropped_image = image[y:y+h, x:x+w]

width, height = 200, 150
resized_image = cv2.resize(image, (width, height))

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresholded_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

cv2.imshow('Original Image', image)
cv2.imshow('Cropped Image', cropped_image)
cv2.imshow('Resized Image', resized_image)
cv2.imshow('Thresholded Image', thresholded_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


# b

import cv2
import numpy as np

def change_brightness(image, alpha, beta):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv_image)

    v = cv2.addWeighted(v, alpha, np.zeros_like(v), 0, beta)

    adjusted_hsv = cv2.merge([h, s, v])

    adjusted_image = cv2.cvtColor(adjusted_hsv, cv2.COLOR_HSV2BGR)

    return adjusted_image

image = cv2.imread('image.jpg')

brightness_adjusted = change_brightness(image, alpha=1.5, beta=50)

cv2.imshow('Original Image', image)
cv2.imshow('Brightness Adjusted Image', brightness_adjusted)
cv2.waitKey(0)
cv2.destroyAllWindows()

