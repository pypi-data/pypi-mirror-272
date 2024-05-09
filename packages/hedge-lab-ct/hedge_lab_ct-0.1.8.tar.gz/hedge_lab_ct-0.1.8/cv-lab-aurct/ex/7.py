import cv2
import numpy as np

# Load the image
image = cv2.imread('image.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (3, 3), 0)

# Sobel operator for gradient calculation
sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)

# Compute gradient magnitude
gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)

edges = cv2.convertScaleAbs(gradient_magnitude)

kernel = np.array([[1,1,1],
                   [1,-8,1],[1,1,1]])
conv= cv2.filter2D(image,-1,kernel)


# Display the original and edge-detected images
cv2.imshow('Original Image', image)
cv2.imshow('Edges', edges)
cv2.imshow("covoluted img",conv)
cv2.waitKey(0)
cv2.destroyAllWindows()
