import numpy as np
import cv2

# Define the input matrix from the image

matrix = np.array([
    [2, 4, 2, 4, 4, 3, 3, 3],
    [4, 3, 1, 4, 2, 1, 3, 1],
    [2, 3, 1, 2, 1, 1, 3, 2],
    [4, 1, 1, 2, 2, 2, 2, 3],
    [1, 4, 1, 2, 1, 4, 3, 4],
    [2, 3, 1, 4, 1, 1, 2, 1],
    [1, 2, 2, 2, 4, 1, 3, 4],
    [1, 3, 1, 1, 4, 1, 1, 4]
], dtype=np.float32)

# Define Roberts kernels
roberts_kernel_x = np.array([[1, 0], [0, -1]], dtype=np.float32)
roberts_kernel_y = np.array([[0, 1], [-1, 0]], dtype=np.float32)

# Apply Roberts kernels to compute gradients in x and y directions
G_x = cv2.filter2D(matrix, -1, roberts_kernel_x)
G_y = cv2.filter2D(matrix, -1, roberts_kernel_y)

# Calculate the gradient magnitude
G = np.sqrt(G_x**2 + G_y**2)

print("Gradient in x direction:", G_x)
print("Gradient in y direction:", G_y)
print("Gradient magnitude:", G)
