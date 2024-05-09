import cv2

image = cv2.imread('image.jpg')

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresholded_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour_image = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 3)

vertical_flipped_image = cv2.flip(image, 0)

horizontal_flipped_image = cv2.flip(image, 1)

cv2.imshow('Original Image', image)
cv2.imshow('Thresholded Image', thresholded_image)
cv2.imshow('Contour Analysis', contour_image)
cv2.imshow('Vertical Flipped Image', vertical_flipped_image)
cv2.imshow('Horizontal Flipped Image', horizontal_flipped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
