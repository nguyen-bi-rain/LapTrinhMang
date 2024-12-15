import cv2


def canny_edge_detection(img: str) -> None:

    # Load the image in grayscale
    gray = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

    # Display the grayscale image
    cv2.imshow("Anh xam", gray)

    # Apply Gaussian blur
    gray_blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)

    # Perform Canny edge detection with two different threshold sets
    t1, t2 = 0, 255
    dst1 = cv2.Canny(gray_blurred, t1, t2, 4, L2gradient=False)

    t1, t2 = 100, 120
    dst2 = cv2.Canny(gray_blurred, t1, t2, 3, L2gradient=False)

    # Display the results of Canny edge detection
    cv2.imshow("Bien trong anh voi nguong 1", dst1)
    cv2.imshow("Bien trong anh voi nguong 2", dst2)

    # Wait for a key press and close all windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    canny_edge_detection("F:\Desktop\Large_Scaled_Forest_Lizard.jpg")