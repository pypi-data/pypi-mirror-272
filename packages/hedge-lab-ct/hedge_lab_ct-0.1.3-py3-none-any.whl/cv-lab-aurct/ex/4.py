import cv2
import numpy as np

# Load an image
image = cv2.imread('image.jpg')

# (i) Contour Analysis
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresholded_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour_image = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 3)

# (ii) Blob Detection
# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create()
# Detect blobs.
keypoints = detector.detect(gray_image)
# Draw detected blobs as red circles.
blob_image = cv2.drawKeypoints(image.copy(), keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# (ii) Negative of an Image
negative_image = cv2.bitwise_not(image)

# Display the images
cv2.imshow('Original Image', image)
cv2.imshow('Contour Analysis', contour_image)
cv2.imshow('Blob Detection', blob_image)
cv2.imshow('Negative Image', negative_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
