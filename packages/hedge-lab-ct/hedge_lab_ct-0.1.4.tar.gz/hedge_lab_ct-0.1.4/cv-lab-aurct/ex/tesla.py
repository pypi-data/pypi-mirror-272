1.
import cv2

# (i) Basic Image Processing Techniques

# Load an image
image = cv2.imread('input_image.jpg')

# Crop the image (example: crop a 100x100 region starting from pixel (50, 50))
cropped_image = image[50:150, 50:150]

# Resize the image to a new width and height (example: resize to 200x200)
resized_image = cv2.resize(image, (200, 200))

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to create a binary image
_, thresholded_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

# (ii) Change Brightness of Image

# Change brightness by adding a constant value to all pixels
brightness_value = 50  # Example brightness value, can be adjusted
brightened_image = cv2.add(image, brightness_value)

# Show the original and processed images
cv2.imshow('Original Image', image)
cv2.imshow('Cropped Image', cropped_image)
cv2.imshow('Resized Image', resized_image)
cv2.imshow('Grayscale Image', gray_image)
cv2.imshow('Thresholded Image', thresholded_image)
cv2.imshow('Brightened Image', brightened_image)

# Wait for a key press and close all windows
cv2.waitKey(0)
cv2.destroyAllWindows()



2.
import cv2

# Load an image
image = cv2.imread('image.jpg')

# (i) Thresholding
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresholded_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

# Contour Analysis
contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour_image = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 3)

# (ii) Flip the image
# Vertical Flip
vertical_flipped_image = cv2.flip(image, 0)
# Horizontal Flip
horizontal_flipped_image = cv2.flip(image, 1)

# Display the images
cv2.imshow('Original Image', image)
cv2.imshow('Thresholded Image', thresholded_image)
cv2.imshow('Contour Analysis', contour_image)
cv2.imshow('Vertical Flipped Image', vertical_flipped_image)
cv2.imshow('Horizontal Flipped Image', horizontal_flipped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

3.
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

4.
import cv2
import numpy as np

# Load an image
image = cv2.imread('image.jpg')

# (i) Image Annotation
# Drawing Lines
annotated_image = image.copy()
cv2.line(annotated_image, (50, 50), (200, 200), (255, 0, 0), 5)  # Draw a blue line

# Drawing Text
cv2.putText(annotated_image, 'OpenCV', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Drawing Circle
cv2.circle(annotated_image, (300, 100), 50, (0, 0, 255), -1)  # Draw a filled red circle

# Drawing Rectangle
cv2.rectangle(annotated_image, (350, 200), (450, 300), (255, 255, 0), 3)  # Draw a cyan rectangle

# Drawing Ellipse
cv2.ellipse(annotated_image, (200, 400), (100, 50), 0, 0, 180, (0, 255, 255), -1)  # Draw a filled yellow ellipse

# (ii) Display Color Components
# Split the image into its color channels
blue, green, red = cv2.split(image)

# Display the color components
cv2.imshow('Original Image', image)
cv2.imshow('Blue Component', blue)
cv2.imshow('Green Component', green)
cv2.imshow('Red Component', red)
cv2.imshow('Annotated Image', annotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

5.
import cv2

# Load an image
image = cv2.imread('image.jpg')

# (i) Image Enhancement - Understanding Color Spaces and Conversion
# Convert the image to different color spaces
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)    # Convert to HSV

# Display the original and converted images
cv2.imshow('Original Image', image)
cv2.imshow('Grayscale Image', gray_image)
cv2.imshow('HSV Image', hsv_image)

# (ii) Finding Threshold of Grayscale Image
# Apply thresholding to the grayscale image
_, thresholded_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

# Display the thresholded image
cv2.imshow('Thresholded Image', thresholded_image)

cv2.waitKey(0)
cv2.destroyAllWindows()

6.
import cv2
import matplotlib.pyplot as plt

# Load an image
image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# (i) Calculate Histogram of the Image
hist = cv2.calcHist([image], [0], None, [256], [0, 256])

# Plot the histogram
plt.plot(hist, color='black')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')
plt.title('Histogram of Image')
plt.show()

# (ii) Histogram Equalization
# Perform histogram equalization
equalized_image = cv2.equalizeHist(image)

# Display the original and equalized images
cv2.imshow('Original Image', image)
cv2.imshow('Equalized Image', equalized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

7.
import cv2
import numpy as np

# Load an image
image = cv2.imread('image.jpg')

# (i) Edge Detection with Gradient and Convolution
# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Sobel edge detection
sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=5)
sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=5)

# Combine the results to obtain the gradient magnitude
gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

# Convert to uint8 and scale the values to be in the range [0, 255]
gradient_magnitude = cv2.convertScaleAbs(gradient_magnitude)

# Display the gradient magnitude image
cv2.imshow('Gradient Magnitude', gradient_magnitude)
cv2.waitKey(0)
cv2.destroyAllWindows()

# (ii) Convert Color Image to Grayscale and HSV
# Convert the color image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Convert the color image to HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Display the grayscale and HSV images
cv2.imshow('Grayscale Image', gray_image)
cv2.imshow('HSV Image', hsv_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

8.
import cv2

# Load an image
image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# (i) Image Smoothing and Gradients
# Apply Gaussian blur for image smoothing
smoothed_image = cv2.GaussianBlur(image, (5, 5), 0)

# Calculate gradients using Sobel operator
sobel_x = cv2.Sobel(smoothed_image, cv2.CV_64F, 1, 0, ksize=5)
sobel_y = cv2.Sobel(smoothed_image, cv2.CV_64F, 0, 1, ksize=5)

# Display the smoothed image and gradients
cv2.imshow('Smoothed Image', smoothed_image)
cv2.imshow('Sobel X', sobel_x)
cv2.imshow('Sobel Y', sobel_y)
cv2.waitKey(0)
cv2.destroyAllWindows()

# (ii) Estimate and Subtract Background
# Apply morphological opening to estimate the background
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
background = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

# Subtract the background from the original image
subtracted_image = cv2.subtract(image, background)

# Display the original image, estimated background, and subtracted image
cv2.imshow('Original Image', image)
cv2.imshow('Estimated Background', background)
cv2.imshow('Subtracted Image', subtracted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

9.
import cv2
import numpy as np

# Load an image
image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# (i) Edge Detection with Gradient and Convolution
# Apply Sobel edge detection
sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)

# Combine the results to obtain the gradient magnitude
gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

# Convert to uint8 and scale the values to be in the range [0, 255]
gradient_magnitude = cv2.convertScaleAbs(gradient_magnitude)

# Display the gradient magnitude image
cv2.imshow('Gradient Magnitude', gradient_magnitude)
cv2.waitKey(0)
cv2.destroyAllWindows()

# (ii) Low Pass Image Filtering using Average Filter
# Define the kernel size for the average filter
kernel_size = (5, 5)

# Apply average filtering
average_filtered_image = cv2.blur(image, kernel_size)

# Display the original and average filtered images
cv2.imshow('Original Image', image)
cv2.imshow('Average Filtered Image', average_filtered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

10
import cv2
import numpy as np

# Load two images
image1 = cv2.imread('image1.jpg', cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread('image2.jpg', cv2.IMREAD_GRAYSCALE)

# (i) Image Features Detection and Image Alignment
# Initialize the ORB detector
orb = cv2.ORB_create()

# Find keypoints and descriptors
keypoints1, descriptors1 = orb.detectAndCompute(image1, None)
keypoints2, descriptors2 = orb.detectAndCompute(image2, None)

# Initialize a Brute-Force matcher
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors
matches = bf.match(descriptors1, descriptors2)

# Sort them in the order of their distance
matches = sorted(matches, key=lambda x: x.distance)

# Draw first 10 matches
matched_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# Display the matched image
cv2.imshow('Matched Image', matched_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# (ii) Low Pass Image Filtering using Median Filter
# Apply median filtering
median_filtered_image = cv2.medianBlur(image1, 5)

# Display the original and median filtered images
cv2.imshow('Original Image', image1)
cv2.imshow('Median Filtered Image', median_filtered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

11
import cv2
import numpy as np

# Load an image
image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# (i) Fourier Image Transforms
# Compute the 2D Discrete Fourier Transform (DFT)
dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)

# Shift the zero frequency component to the center
dft_shift = np.fft.fftshift(dft)

# Compute the magnitude spectrum
magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

# Display the magnitude spectrum
cv2.imshow('Magnitude Spectrum', np.uint8(magnitude_spectrum))
cv2.waitKey(0)
cv2.destroyAllWindows()

# (ii) Hough Image Transforms
# Apply Hough Line Transform
lines = cv2.HoughLines(image, 1, np.pi / 180, 200)

# Draw detected lines on the original image
hough_lines_image = image.copy()
if lines is not None:
    for rho, theta in lines[:, 0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(hough_lines_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Display the image with detected lines
cv2.imshow('Hough Lines', hough_lines_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# (ii) High Pass Image Filtering using Sobel Operator
# Apply Sobel edge detection to obtain high pass filtered image
sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)
high_pass_filtered_image = cv2.magnitude(sobel_x, sobel_y)

# Display the high pass filtered image
cv2.imshow('High Pass Filtered Image', high_pass_filtered_image.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()

12.
import cv2
import numpy as np

# Load an image
image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# (i) Hough Image Transforms
# Apply Hough Circle Transform
circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=0, maxRadius=0)

# Draw detected circles on the original image
hough_circles_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
if circles is not None:
    circles = np.uint16(np.around(circles))
    for circle in circles[0, :]:
        center = (circle[0], circle[1])
        radius = circle[2]
        cv2.circle(hough_circles_image, center, radius, (0, 255, 0), 2)

# Display the image with detected circles
cv2.imshow('Hough Circles', hough_circles_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# (ii) Extract ORB Image Features
# Initialize the ORB detector
orb = cv2.ORB_create()

# Find keypoints and descriptors
keypoints, descriptors = orb.detectAndCompute(image, None)

# Draw keypoints on the original image
orb_keypoints_image = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0), flags=0)

# Display the image with keypoints
cv2.imshow('ORB Keypoints', orb_keypoints_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# (iii) High Pass Image Filtering using Laplacian Operator
# Apply Laplacian edge detection to obtain high pass filtered image
laplacian_filtered_image = cv2.Laplacian(image, cv2.CV_64F)

# Display the high pass filtered image
cv2.imshow('High Pass Filtered Image (Laplacian)', laplacian_filtered_image.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()

13.

import cv2
import numpy as np

# Load two images
image1 = cv2.imread('image1.jpg', cv2.IMREAD_COLOR)
image2 = cv2.imread('image2.jpg', cv2.IMREAD_COLOR)

# (i) Feature Matching and Cloning
# Convert images to grayscale
gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# Initialize the ORB detector
orb = cv2.ORB_create()

# Find keypoints and descriptors
keypoints1, descriptors1 = orb.detectAndCompute(gray_image1, None)
keypoints2, descriptors2 = orb.detectAndCompute(gray_image2, None)

# Initialize a Brute-Force matcher
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors
matches = bf.match(descriptors1, descriptors2)

# Sort them in the order of their distance
matches = sorted(matches, key=lambda x: x.distance)

# Draw first 10 matches
matched_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# Display the matched image
cv2.imshow('Matched Image', matched_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# (ii) Low Pass Image Filtering using Median Filter
# Apply median filtering to both images
median_filtered_image1 = cv2.medianBlur(image1, 5)
median_filtered_image2 = cv2.medianBlur(image2, 5)

# Display the original and median filtered images
cv2.imshow('Original Image 1', image1)
cv2.imshow('Median Filtered Image 1', median_filtered_image1)
cv2.imshow('Original Image 2', image2)
cv2.imshow('Median Filtered Image 2', median_filtered_image2)
cv2.waitKey(0)
cv2.destroyAllWindows()

14.
import cv2
import numpy as np

# Load two images
image1 = cv2.imread('image1.jpg', cv2.IMREAD_COLOR)
image2 = cv2.imread('image2.jpg', cv2.IMREAD_COLOR)

# (i) Cloning and Feature Matching based Image Alignment
# Convert images to grayscale
gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# Initialize the ORB detector
orb = cv2.ORB_create()

# Find keypoints and descriptors
keypoints1, descriptors1 = orb.detectAndCompute(gray_image1, None)
keypoints2, descriptors2 = orb.detectAndCompute(gray_image2, None)

# Initialize a Brute-Force matcher
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors
matches = bf.match(descriptors1, descriptors2)

# Sort them in the order of their distance
matches = sorted(matches, key=lambda x: x.distance)

# Draw first 10 matches
matched_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# Display the matched image
cv2.imshow('Matched Image', matched_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# (ii) Low Pass Image Filtering using Average Filter
# Apply average filtering to both images
average_filtered_image1 = cv2.blur(image1, (5, 5))
average_filtered_image2 = cv2.blur(image2, (5, 5))

# Display the original and average filtered images
cv2.imshow('Original Image 1', image1)
cv2.imshow('Average Filtered Image 1', average_filtered_image1)
cv2.imshow('Original Image 2', image2)
cv2.imshow('Average Filtered Image 2', average_filtered_image2)
cv2.waitKey(0)
cv2.destroyAllWindows()


15.
import cv2
import numpy as np

# Load an image
image = cv2.imread('image.jpg')

# (i) Image Segmentation using Graphcut / Grabcut
# Create a mask initialized with zeros (background)
mask = np.zeros(image.shape[:2], np.uint8)

# Define the region of interest (ROI) for segmentation
rect = (50, 50, 450, 290)  # Format: (x, y, width, height)

# Apply Grabcut algorithm
bgd_model = np.zeros((1, 65), np.float64)
fgd_model = np.zeros((1, 65), np.float64)
cv2.grabCut(image, mask, rect, bgd_model, fgd_model, iterCount=5, mode=cv2.GC_INIT_WITH_RECT)

# Update the mask: all 0 and 2 pixels are set to 0 (background), others to 1 (foreground)
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

# Apply the mask to the original image
segmented_image = image * mask2[:, :, np.newaxis]

# Display the segmented image
cv2.imshow('Segmented Image', segmented_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# (ii) High Pass Image Filtering using Sobel Operator
# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Sobel edge detection to obtain high pass filtered image
sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=5)
sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=5)
high_pass_filtered_image = cv2.magnitude(sobel_x, sobel_y)

# Display the high pass filtered image
cv2.imshow('High Pass Filtered Image (Sobel)', high_pass_filtered_image.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()

15.
import cv2
import numpy as np

# Load an image
image = cv2.imread('image.jpg')

# (i) Image Segmentation using Graphcut / Grabcut
# Create a mask initialized with zeros (background)
mask = np.zeros(image.shape[:2], np.uint8)

# Define the region of interest (ROI) for segmentation
rect = (50, 50, 450, 290)  # Format: (x, y, width, height)

# Apply Grabcut algorithm
bgd_model = np.zeros((1, 65), np.float64)
fgd_model = np.zeros((1, 65), np.float64)
cv2.grabCut(image, mask, rect, bgd_model, fgd_model, iterCount=5, mode=cv2.GC_INIT_WITH_RECT)

# Update the mask: all 0 and 2 pixels are set to 0 (background), others to 1 (foreground)
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

# Apply the mask to the original image
segmented_image = image * mask2[:, :, np.newaxis]

# Display the segmented image
cv2.imshow('Segmented Image', segmented_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# (ii) High Pass Image Filtering using Sobel Operator
# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Sobel edge detection to obtain high pass filtered image
sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=5)
sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=5)
high_pass_filtered_image = cv2.magnitude(sobel_x, sobel_y)

# Display the high pass filtered image
cv2.imshow('High Pass Filtered Image (Sobel)', high_pass_filtered_image.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()


