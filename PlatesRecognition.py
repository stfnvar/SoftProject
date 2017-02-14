import cv2
import numpy as np
import math
import random

import InitialThreshold
import PossibleChar
import CharRecognition
import PossiblePlate
import PossibleChar


PLATE_WIDTH_PADDING_FACTOR = 1.3
PLATE_HEIGHT_PADDING_FACTOR = 1.5

def recognizePossiblePlates(imgOriginal, imgThreshold):
    listOfPossiblePlates = []

    listOfPossibleChars = findPossibleChars(imgThreshold)
    
    listOfListsOfMatchingChars = CharRecognition.findListOfListsOfMatchingChars(listOfPossibleChars)
    
    for listOfMatchingChars in listOfListsOfMatchingChars:                   
        possiblePlate = extractPlate(imgOriginal, listOfMatchingChars)        

        if possiblePlate.imgPlate is not None:                          
            listOfPossiblePlates.append(possiblePlate)                 
        # end if

    # end for

    return listOfPossiblePlates
# end function

def findPossibleChars(imgThreshold):
    listOfPossibleChars = []               

    intCountOfPossibleChars = 0

    imgThresholdCopy = imgThreshold.copy()

    #RETR_LIST - ista hijearhija
    imgContours, contours, npaHierarchy = cv2.findContours(imgThresholdCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) 
    cv2.imshow("contours", imgContours)
    cv2.waitKey(0)

    # Za prikazivanje
    #height, width = imgContours.shape
    #imgContours = np.zeros((height, width, 3), np.uint8)

    for i in range(0, len(contours)):  
        possibleChar = PossibleChar.PossibleChar(contours[i])
    
        if CharRecognition.checkIfPossibleChar(possibleChar, imgThreshold):                   
            intCountOfPossibleChars = intCountOfPossibleChars + 1           
            listOfPossibleChars.append(possibleChar)
            #prikaz svih kontura mogucih slova
            #cv2.drawContours(imgContours, possibleChar.contour, -1, (0, 255, 0))  
        # end if
    # end for
    #cv2.imshow("1", imgContours)
    #cv2.waitKey(0)                      

    return listOfPossibleChars

# end function

#OBRATIMO PAZNJU
def extractPlate(imgOriginal, listOfMatchingChars):
    possiblePlate = PossiblePlate.PossiblePlate()        

    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)       
    
    listOfMatchingChars = removeOverlaping(listOfMatchingChars)
    
    possiblePlate.listOfPossibleChars = listOfMatchingChars
    ####################

    fltPlateCenterX = (listOfMatchingChars[0].intCenterX + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterX) / 2.0
    fltPlateCenterY = (listOfMatchingChars[0].intCenterY + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY) / 2.0

    ptPlateCenter = fltPlateCenterX, fltPlateCenterY

    intPlateWidth = int((listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectX + listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectWidth - listOfMatchingChars[0].intBoundingRectX) * PLATE_WIDTH_PADDING_FACTOR)

    intTotalOfCharHeights = 0

    for matchingChar in listOfMatchingChars:
        intTotalOfCharHeights = intTotalOfCharHeights + matchingChar.intBoundingRectHeight
    # end for

    fltAverageCharHeight = intTotalOfCharHeights / len(listOfMatchingChars)

    intPlateHeight = int(fltAverageCharHeight * PLATE_HEIGHT_PADDING_FACTOR)

    fltOpposite = listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY - listOfMatchingChars[0].intCenterY
    fltHypotenuse = CharRecognition.distanceBetweenChars(listOfMatchingChars[0], listOfMatchingChars[len(listOfMatchingChars) - 1])
    fltCorrectionAngleInRad = math.asin(fltOpposite / fltHypotenuse)
    fltCorrectionAngleInDeg = fltCorrectionAngleInRad * (180.0 / math.pi)

    possiblePlate.rrLocationOfPlate = ( tuple(ptPlateCenter), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg )

    rotationMatrix = cv2.getRotationMatrix2D(tuple(ptPlateCenter), fltCorrectionAngleInDeg, 1.0)

    height, width, numChannels = imgOriginal.shape      

    imgRotated = cv2.warpAffine(imgOriginal, rotationMatrix, (width, height))      

    imgCropped = cv2.getRectSubPix(imgRotated, (intPlateWidth, intPlateHeight), tuple(ptPlateCenter))

    possiblePlate.imgPlate = imgCropped        

    return possiblePlate

# end function

def removeOverlaping(listOfMatchingChars):
    finalList = listOfMatchingChars
    #puni listu slovima
    for char in listOfMatchingChars:
        for char2 in listOfMatchingChars:
            if char.intCenterX + 2 > char2.intCenterX and char.intCenterX - 2 < char2.intCenterX:
                if char.intBoundingRectArea > char2.intBoundingRectArea:
                    #cv2.imshow("a", char.imgChar)
                    #cv2.imshow("b", char2.imgChar)
                    #cv2.waitKey(0)
                    finalList.remove(char2)
                if char.intBoundingRectArea < char2.intBoundingRectArea:
                    #cv2.imshow("a", char.imgChar)
                    #cv2.imshow("b", char2.imgChar)
                    #cv2.waitKey(0)
                    finalList.remove(char)

    return finalList
#end function