import cv2
import numpy as np
import math
import random

MIN_PIXEL_WIDTH = 2
MIN_PIXEL_HEIGHT = 8
MIN_ASPECT_RATIO = 0.25
#MAX_ASPECT_RATIO = 1.0
MAX_ASPECT_RATIO = 1.2
MIN_PIXEL_AREA = 80


MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0

MAX_CHANGE_IN_AREA = 0.5

MAX_CHANGE_IN_WIDTH = 0.8
MAX_CHANGE_IN_HEIGHT = 0.2

MAX_ANGLE_BETWEEN_CHARS = 12.0

#MIN_NUMBER_OF_MATCHING_CHARS = 2
MIN_NUMBER_OF_MATCHING_CHARS = 4

RESIZED_CHAR_IMAGE_WIDTH = 20
RESIZED_CHAR_IMAGE_HEIGHT = 30

MIN_CONTOUR_AREA = 100


def checkIfPossibleChar(possibleChar, imgThreshold):
    # PROVERI KONSTANTE (MIN_PIXEL_HEIGHT, MIN_PIXEL_WIDTH, MIN_PIXEL_AREA)
    if (possibleChar.intBoundingRectArea > MIN_PIXEL_AREA and
        possibleChar.intBoundingRectWidth > MIN_PIXEL_WIDTH and possibleChar.intBoundingRectHeight > MIN_PIXEL_HEIGHT and
        MIN_ASPECT_RATIO < possibleChar.fltAspectRatio and possibleChar.fltAspectRatio < MAX_ASPECT_RATIO):
        possibleChar.imgChar = imgThreshold[possibleChar.intBoundingRectY:possibleChar.intBoundingRectHeight + possibleChar.intBoundingRectY, possibleChar.intBoundingRectX:possibleChar.intBoundingRectWidth + possibleChar.intBoundingRectX]
        #cv2.imshow('PossibleChar', possibleChar.imgChar)
        #cv2.waitKey(0)
        return True
    else:
        return False 
    # end if

# end function


def findListOfListsOfMatchingChars(listOfPossibleChars):
    listOfListsOfMatchingChars = []                 
    #za svako slovo njegova lista matching charova
    for possibleChar in listOfPossibleChars:                       
        listOfMatchingChars = findListOfMatchingChars(possibleChar, listOfPossibleChars)        

        listOfMatchingChars.append(possibleChar)                

        if len(listOfMatchingChars) < MIN_NUMBER_OF_MATCHING_CHARS:     
            continue
        # end if

        #lista koja sadrzi liste predvodjenih slova   
        listOfListsOfMatchingChars.append(listOfMatchingChars)     

        #ukloni one koje si dodao u listu lista
        listOfPossibleCharsWithCurrentMatchesRemoved = []
                       
        listOfPossibleCharsWithCurrentMatchesRemoved = list(set(listOfPossibleChars) - set(listOfMatchingChars))

        recursiveListOfListsOfMatchingChars = findListOfListsOfMatchingChars(listOfPossibleCharsWithCurrentMatchesRemoved)     

        for recursiveListOfMatchingChars in recursiveListOfListsOfMatchingChars:        
            listOfListsOfMatchingChars.append(recursiveListOfMatchingChars)       
        
        

        # end for

        break       # exit for

    # end for

    #ZA PRIKAZIVANJE grupnih tablica u konturama(LIST OF LISTS)
    imgContours = np.zeros((768, 1024, 3), np.uint8)
    for lol in listOfListsOfMatchingChars:
        for i in lol:
            cv2.drawContours(imgContours, i.contour, -1, (0, 255, 0))
        
    cv2.imshow("1Contours", imgContours)
    cv2.waitKey(0)

    return listOfListsOfMatchingChars
# end function


def findListOfMatchingChars(possibleChar, listOfChars):
            
    listOfMatchingChars = []                

    for possibleMatchingChar in listOfChars:                
        if possibleMatchingChar == possibleChar:                                                        
            continue                               
        # end if
                    
        fltDistanceBetweenChars = distanceBetweenChars(possibleChar, possibleMatchingChar)

        fltAngleBetweenChars = angleBetweenChars(possibleChar, possibleMatchingChar)

        fltChangeInArea = float(abs(possibleMatchingChar.intBoundingRectArea - possibleChar.intBoundingRectArea)) / float(possibleChar.intBoundingRectArea)

        fltChangeInWidth = float(abs(possibleMatchingChar.intBoundingRectWidth - possibleChar.intBoundingRectWidth)) / float(possibleChar.intBoundingRectWidth)
        fltChangeInHeight = float(abs(possibleMatchingChar.intBoundingRectHeight - possibleChar.intBoundingRectHeight)) / float(possibleChar.intBoundingRectHeight)

        if (fltDistanceBetweenChars < (possibleChar.fltDiagonalSize * MAX_DIAG_SIZE_MULTIPLE_AWAY) and
            fltAngleBetweenChars < MAX_ANGLE_BETWEEN_CHARS and
            fltChangeInArea < MAX_CHANGE_IN_AREA and
            fltChangeInWidth < MAX_CHANGE_IN_WIDTH and
            fltChangeInHeight < MAX_CHANGE_IN_HEIGHT):
            listOfMatchingChars.append(possibleMatchingChar)    
        # end if
    # end for


    return listOfMatchingChars                  # return result
# end function

def distanceBetweenChars(firstChar, secondChar):
    intX = abs(firstChar.intCenterX - secondChar.intCenterX)
    intY = abs(firstChar.intCenterY - secondChar.intCenterY)

    return math.sqrt((intX ** 2) + (intY ** 2))
# end function

def angleBetweenChars(firstChar, secondChar):
    fltAdj = float(abs(firstChar.intCenterX - secondChar.intCenterX))
    fltOpp = float(abs(firstChar.intCenterY - secondChar.intCenterY))

    if fltAdj != 0.0:                          
        fltAngleInRad = math.atan(fltOpp / fltAdj)      
    else:
        fltAngleInRad = 1.5708                         
    # end if

    fltAngleInDeg = fltAngleInRad * (180.0 / math.pi)     

    return fltAngleInDeg
# end function

#extract karaktera
def recognizePossibleChars(listsOfMatchingChars):
    listCroppedChars = []
    #for char in listsOfMatchingChars:

#end function
