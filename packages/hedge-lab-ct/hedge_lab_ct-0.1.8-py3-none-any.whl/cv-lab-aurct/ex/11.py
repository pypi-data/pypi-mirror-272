import cv2
import numpy as np

image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)

dft_shift = np.fft.fftshift(dft)

magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

cv2.imshow('Magnitude Spectrum', np.uint8(magnitude_spectrum))
cv2.waitKey(0)
cv2.destroyAllWindows()


lines = cv2.HoughLines(image, 1, np.pi / 180, 200)

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

cv2.imshow('Hough Lines', hough_lines_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)
high_pass_filtered_image = cv2.magnitude(sobel_x, sobel_y)

cv2.imshow('High Pass Filtered Image', high_pass_filtered_image.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()
