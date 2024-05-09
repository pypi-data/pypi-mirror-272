import cv2

image = cv2.imread('image.jpg')


annotated_image = image.copy()
cv2.line(annotated_image, (50, 50), (200, 200), (255, 0, 0), 5)  # Draw a blue line

cv2.putText(annotated_image, 'OpenCV', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

cv2.circle(annotated_image, (300, 100), 50, (0, 0, 255), -1)  # Draw a filled red circle

cv2.rectangle(annotated_image, (350, 200), (450, 300), (255, 255, 0), 3)  # Draw a cyan rectangle

cv2.ellipse(annotated_image, (200, 400), (100, 50), 0, 0, 180, (0, 255, 255), -1)  # Draw a filled yellow ellipse


blue, green, red = cv2.split(image)

cv2.imshow('Original Image', image)
cv2.imshow('Blue Component', blue)
cv2.imshow('Green Component', green)
cv2.imshow('Red Component', red)
cv2.imshow('Annotated Image', annotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
