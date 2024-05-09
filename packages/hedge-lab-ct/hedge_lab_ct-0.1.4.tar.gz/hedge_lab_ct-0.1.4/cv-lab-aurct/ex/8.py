import cv2

image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

smoothed_image = cv2.GaussianBlur(image, (5, 5), 0)

sobel_x = cv2.Sobel(smoothed_image, cv2.CV_64F, 1, 0, ksize=5)
sobel_y = cv2.Sobel(smoothed_image, cv2.CV_64F, 0, 1, ksize=5)

cv2.imshow('Smoothed Image', smoothed_image)
cv2.imshow('Sobel X', sobel_x)
cv2.imshow('Sobel Y', sobel_y)
cv2.waitKey(0)
cv2.destroyAllWindows()

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
background = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

subtracted_image = cv2.subtract(image, background)

cv2.imshow('Original Image', image)
cv2.imshow('Estimated Background', background)
cv2.imshow('Subtracted Image', subtracted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
