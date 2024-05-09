import cv2
import numpy as np

image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)


sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)

gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

gradient_magnitude = cv2.convertScaleAbs(gradient_magnitude)

cv2.imshow('Gradient Magnitude', gradient_magnitude)
cv2.waitKey(0)
cv2.destroyAllWindows()


kernel_size = (5, 5)

average_filtered_image = cv2.blur(image, kernel_size)

cv2.imshow('Original Image', image)
cv2.imshow('Average Filtered Image', average_filtered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
