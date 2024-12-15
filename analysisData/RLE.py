import cv2

# tim anh khi biet trc ma loat va kich thuoc anh
# cho ma loat tim anh
import numpy as np


def decode_run_length(encoded, rows, cols):
    """Decodes a run-length encoded list to reconstruct the original image matrix.

    Args:
        encoded (list of tuples): Run-length encoded list of tuples (pixel_value, run_length).
        rows (int): Number of rows in the original matrix.
        cols (int): Number of columns in the original matrix.

    Returns:
        np.array: 2D numpy array representing the reconstructed black-and-white image.
    """
    # Initialize an empty list to store the pixels
    pixels = []

    # Decode the run-length encoding
    for pixel_value, run_length in encoded:
        pixels.extend([pixel_value] * run_length)

    # Convert the flat list of pixels into a 2D numpy array (matrix)
    matrix = np.array(pixels).reshape((rows, cols))

    return matrix


# Example usage


def image_to_black_white_matrix(image_path):
    """Reads an image, converts it to black-and-white, and returns it as a matrix.

    Args:
        image_path (str): The path to the image file.

    Returns:
        np.array: A 2D numpy array representing the black-and-white image.
    """
    # Read the image using cv2
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Convert the grayscale image to binary (black and white)
    _, bw_image = cv2.threshold(image, 128, 1, cv2.THRESH_BINARY)

    return bw_image
def run_length_encode(image):
    """Performs run-length encoding on a black-and-white image.

    Args:
        image (list of lists): 2D list representing a black-and-white image (0 for black, 1 for white).

    Returns:
        list of tuples: Each tuple contains (pixel_value, run_length).
    """
    encoded = []
    current_pixel = image[0][0]
    run_length = 0

    rows = len(image)
    cols = len(image[0])
    print(cols,rows)

    for row in image:
        for pixel in row:
            if pixel == current_pixel:
                run_length += 1
            else:
                encoded.append((current_pixel, run_length))
                current_pixel = pixel
                run_length = 1

    encoded.append((current_pixel, run_length))

    return encoded


# Example usage
image = image_to_black_white_matrix("F:\Pictures\Saved Pictures\item3.jpg")

encoded_image = run_length_encode(image)

matrix = decode_run_length(encoded_image, 719, 1280)
# recover to black white image from matrix
cv2.imshow("Image", matrix * 255)
cv2.waitKey(0)

# Destroy all windows
cv2.destroyAllWindows()
print(matrix)
