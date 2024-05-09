import cv2
import numpy as np

image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)


circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=0, maxRadius=0)

hough_circles_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
if circles is not None:
    circles = np.uint16(np.around(circles))
    for circle in circles[0, :]:
        center = (circle[0], circle[1])
        radius = circle[2]
        cv2.circle(hough_circles_image, center, radius, (0, 255, 0), 2)

cv2.imshow('Hough Circles', hough_circles_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


orb = cv2.ORB_create()

keypoints, descriptors = orb.detectAndCompute(image, None)

orb_keypoints_image = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0), flags=0)

cv2.imshow('ORB Keypoints', orb_keypoints_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


laplacian_filtered_image = cv2.Laplacian(image, cv2.CV_64F)

cv2.imshow('High Pass Filtered Image (Laplacian)', laplacian_filtered_image.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()
