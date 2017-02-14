#Metode za obradu slike 
#Prima originalnu sliku, a vraca threshold 
#http://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html
#http://docs.opencv.org/3.1.0/d4/d13/tutorial_py_filtering.html
#http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html

import cv2
import numpy as np
import math


GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
#Testiraj parametar
ADAPTIVE_THRESH_WEIGHT = 9 

def initialThreshold(imgOriginal):

    height, width, numChannels = imgOriginal.shape
    
    imgHSV = np.zeros((height, width, 3), np.uint8)

    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

    imgHue, imgSaturation, imgValue = cv2.split(imgHSV)
   
    imgGray = imgValue

    #cv2.imshow("grayImg", imgGray)
    #cv2.waitKey(0)

    height, width = imgGray.shape

    imgBlurred = np.zeros((height, width, 1), np.uint8)

    imgBlurred = cv2.GaussianBlur(imgGray, GAUSSIAN_SMOOTH_FILTER_SIZE, 0)
    
    imgThreshold = cv2.adaptiveThreshold(imgBlurred, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)
    
    return imgThreshold

# end function

