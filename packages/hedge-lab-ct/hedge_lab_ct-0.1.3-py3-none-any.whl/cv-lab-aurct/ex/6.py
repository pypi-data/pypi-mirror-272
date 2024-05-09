import cv2

image = cv2.imread('image.jpg')

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)    # Convert to HSV

cv2.imshow('Original Image', image)
cv2.imshow('Grayscale Image', gray_image)
cv2.imshow('HSV Image', hsv_image)


_, thresholded_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

cv2.imshow('Thresholded Image', thresholded_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
