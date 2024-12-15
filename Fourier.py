import cv2
import numpy as np
from matplotlib import pyplot as plt

def demoFFT2(image):
    gray_img = cv2.imread(image,cv2.IMREAD_GRAYSCALE);
    F = np.fft.fft2(gray_img)
    F_shift = np.fft.fftshift(F)
    magnitue = np.log(1 + np.abs(F_shift))
    phase = np.angle(F_shift)
    plt.subplots(1,3,1)
    plt.imshow(gray_img)
    plt.subplots(1,3,2)
    plt.imshow(magnitue)

