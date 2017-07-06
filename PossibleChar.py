import cv2
import numpy as np
import math

class PossibleChar:

    def __init__(self, _contour):
        self.contour = _contour

        self.boundingRect = cv2.boundingRect(self.contour)

        [intX, intY, intWidth, intHeight] = self.boundingRect

        self.intBoundingRectX = intX
        self.intBoundingRectY = intY
        self.intBoundingRectWidth = intWidth
        self.intBoundingRectHeight = intHeight

        self.charImg = None
    # end constructor

    def getIntBoundingRectArea(self):
        return self.intBoundingRectWidth * self.intBoundingRectHeight
    #end function

    def getIntCenterX(self):
        return (self.intBoundingRectX + self.intBoundingRectX + self.intBoundingRectWidth) / 2
    #end function

    def getIntCenterY(self):
        return (self.intBoundingRectY + self.intBoundingRectY + self.intBoundingRectHeight) / 2
    #end function

# end class








