import cv2
import numpy as np

image = cv2.imread('image.jpg')

mask = np.zeros(image.shape[:2], np.uint8)

rect = (50, 50, 450, 290)  # Format: (x, y, width, height)

bgd_model = np.zeros((1, 65), np.float64)
fgd_model = np.zeros((1, 65), np.float64)
cv2.grabCut(image, mask, rect, bgd_model, fgd_model, iterCount=5, mode=cv2.GC_INIT_WITH_RECT)

mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

segmented_image = image * mask2[:, :, np.newaxis]

cv2.imshow('Segmented Image', segmented_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=5)
sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=5)
high_pass_filtered_image = cv2.magnitude(sobel_x, sobel_y)

cv2.imshow('High Pass Filtered Image (Sobel)', high_pass_filtered_image.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()
