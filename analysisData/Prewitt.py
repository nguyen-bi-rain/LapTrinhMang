import cv2
import numpy as np

# Load the image in grayscale
gray = cv2.imread("F:\\Pictures\\Camera Roll\\item3.jpg", cv2.IMREAD_GRAYSCALE)

# Define Prewitt kernels for X and Y directions
kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])

# Apply Prewitt operator in the X and Y directions
prewitt_x = cv2.filter2D(gray, cv2.CV_32F, kernelx)
prewitt_y = cv2.filter2D(gray, cv2.CV_32F, kernely)

# Combine the two directions using absolute summation
prewitt_combined = cv2.magnitude(prewitt_x, prewitt_y)

# Normalize the result for proper display
prewitt_combined = cv2.normalize(prewitt_combined, None, 0, 255, cv2.NORM_MINMAX)

# Convert the result to an 8-bit image for display
prewitt_combined = np.uint8(prewitt_combined)

# Display the results
cv2.imshow('Prewitt X', np.uint8(prewitt_x))
cv2.imshow('Prewitt Y', np.uint8(prewitt_y))
cv2.imshow('Prewitt Combined', prewitt_combined)

# Wait for a key press and close all windows
cv2.waitKey(0)
cv2.destroyAllWindows()
