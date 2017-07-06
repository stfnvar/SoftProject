import cv2
import numpy as np
import logging
import PossibleChar
from PIL import Image
from matplotlib import pyplot as plt
from copy import deepcopy, copy
from logging.config import fileConfig
from PossibleChar import PossibleChar
import os


PLATE_AREA_MIN = 6000
PLATE_AREA_MAX = 40000

PLATE_WIDTH_MIN = 100
PLATE_WIDTH_MAX = 300
PLATE_HEIGHT_MIN = 20
PLATE_HEIGHT_MAX = 125

PLATE_RATIO_MAX = 0.5
PLATE_RATIO_MIN = 0.15

CHAR_AREA_MIN = 120
CHAR_AREA_MAX = 2000

CHAR_WIDTH_MIN = 4
CHAR_WIDTH_MAX = 50
CHAR_HEIGHT_MIN = 20
CHAR_HEIGHT_MAX = 90

CHAR_RATIO_MAX = 1.3

CHARS_NUM_MIN = 4
CHARS_NUM_MAX = 9

#logger setup
fileConfig("logging_config.ini")
logger = logging.getLogger()

path = os.getcwd() + "\\app.log"
hdlr = logging.FileHandler(path)
logger.addHandler(hdlr)

class Plate:
	def __init__(self, image):				
		self.original_image = image			
		self.plate_located_image = deepcopy(image)
		self.plate_image = None			
		self.plate_image_char = None			
		self.gray_image = None
		self.final_chars = []		
		self.final_chars_img = []					
		self.plate_number = ""				
		self.roi = []					
		self.plate_characters = []
		logger.info("New plate created.")
	#end constructor

	
	def grayImage(self, image):
		logger.info("Image converted to grayscale")
		return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#end function

	def plateSearch(self, pictureName):
		logger.info("Picture: %s", pictureName)
		if self.original_image is not None:
			self.findContour()
			if len(self.roi) > 1:

				x = 0
				y = 0
				w = 0
				h = 0
				
				[x,y,w,h] = self.roi[0]
				self.plate_image = self.original_image[y:y+h,x:x+w]
				self.plate_image_char = deepcopy(self.plate_image)
			#end if
			if self.plate_image is not None:
				self.findCharacterContour()
			#end if
			print("Return value")
			print(len(self.final_chars_img))
			logger.info("Image fully processed.")
			return self.final_chars_img
		else:
			logger.error("Invalid picture plate import")
			return False
	#end function

	def findContour(self):
		self.gray_image = self.grayImage(deepcopy(self.original_image))
		self.gray_image = cv2.GaussianBlur(self.gray_image, (5, 5), 0)

		self.gray_image = cv2.adaptiveThreshold(self.gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 2)
		imgContours, contours,_ = cv2.findContours(self.gray_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		cv2.imshow("Contours", imgContours)
		cv2.waitKey(0)
		
		x=0
		y=0
		w=0
		h=0

		for contour in contours:
			area = cv2.contourArea(contour)
			if area > PLATE_AREA_MIN and area < PLATE_AREA_MAX:
				[x,y,w,h] = cv2.boundingRect(contour)
				print(x, y, w, h)
			#end if
			if w > PLATE_WIDTH_MIN and w < PLATE_WIDTH_MAX and h > PLATE_HEIGHT_MIN and h < PLATE_HEIGHT_MAX:
				if float(h)/float(w) > PLATE_RATIO_MIN and float(h)/float(w) < PLATE_RATIO_MAX:
					self.roi.append([x,y,w,h])
					cv2.rectangle(self.plate_located_image, (x,y), (x+w, y+h), (0,255,255), 10)
				#end if
			#end if
		#end for
		logger.info("%s potential regions with plates found.", str(len(self.roi)))
		return True
	#end function

	def cropCharacter(self, dimensions):
		
		x = 0
		y = 0
		w = 0
		h = 0

		[x,y,w,h] = dimensions
		character = deepcopy(self.plate_image)
		character = deepcopy(character[y:y+h,x:x+w])
		return character
	#end function

	def findCharacterContour(self):
		gray_plate = self.grayImage(deepcopy(self.plate_image))
		gray_plate = cv2.GaussianBlur(gray_plate, (3,3), 0)


		threshold = cv2.adaptiveThreshold(gray_plate, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17,2)
		_,contours,_ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		x=0
		y=0
		w=0
		h=0

		chars = []

		logger.info("%s contours found.", str(len(contours)))
		for contour in contours:
			area = cv2.contourArea(contour)
			if area > CHAR_AREA_MIN and area < CHAR_AREA_MAX:
				[x,y,w,h] = cv2.boundingRect(contour)
				if h > CHAR_HEIGHT_MIN and h < CHAR_HEIGHT_MAX and w > CHAR_WIDTH_MIN and w < CHAR_WIDTH_MAX:
					if float(w)/h <= CHAR_RATIO_MAX:
						character = self.cropCharacter([x,y,w,h])
						char = PossibleChar(contour)
						char.charImg = self.cropCharacter([x,y,w,h])
						chars.append(char)
					#end if
				#end if
			#end if
		#end for

		print(len(chars))
		logger.info("%s possible chars found on the plate.", str(len(chars)))
		self.final_chars = self.removeOverlaping(chars)

		logger.info("Removed overlaped contorus.")

		if(len(self.final_chars) <= CHARS_NUM_MIN or len(self.final_chars) >= CHARS_NUM_MAX):
			return False

		self.final_chars = self.bubbleSortPossibleCharsByPositionX(self.final_chars)

		logger.info("Sorted characters by position.")
		
		for char in self.final_chars:
			self.plate_characters.append([char.intBoundingRectX, char.charImg])
			cv2.rectangle(self.plate_image_char, (char.intBoundingRectX, char.intBoundingRectY), (char.intBoundingRectX+char.intBoundingRectWidth, char.intBoundingRectY+char.intBoundingRectHeight), (0,0,255), 1)
		#end for

		print("Objects")
		print(len(self.final_chars))
		logger.info("%s char objects contained.", str(len(self.final_chars)))

		count = 0
		for char in self.final_chars:
			count += 1
			print("Next")
			print(count)
			print(char.getIntCenterX())
			print(char.intBoundingRectHeight)
			print(char.intBoundingRectWidth)
			print(float(char.intBoundingRectWidth)/char.intBoundingRectHeight)
		#end for

		
		for final in self.final_chars:
			self.final_chars_img.append(final.charImg)
		#end for

		print("Images only")
		print(len(self.final_chars_img))
		logger.info("%s char images contained.", str(len(self.final_chars_img)))

		logger.info("%s plate characters found", str(len(self.plate_characters)))
		return True
	#end function


	def plot(self, figure, subplot, image, title):
		figure.subplot(subplot)
		figure.imshow(image)
		figure.xlabel(title)
		figure.xticks([])
		figure.yticks([])
		return True
	#end function

	def showResults(self):
		logger.info("Plate number found: %s",self.plate_number)
		logger.info("-------------------------------------------")
		plt.figure(self.plate_number)

		self.plot(plt, 321, self.original_image, "Original image")
		self.plot(plt, 322, self.gray_image, "Threshold image")
		self.plot(plt, 323, self.plate_located_image, "Plate located")

		if self.plate_image is not None:
			self.plot(plt, 324, self.plate_image, "License plate")
			self.plot(plt, 325, self.plate_image_char, "Characters outlined")
			plt.subplot(326);plt.text(0,0,self.plate_number, fontsize=30)
			plt.xticks([])
			plt.yticks([])
		#end if
		plt.tight_layout()
		plt.show()
		return True
	#end function

	def removeOverlaping(self, chars):
		finalList = chars
		for char in chars:
			for char2 in chars:
				if char.getIntCenterX() + float(char.intBoundingRectWidth)/2 >= char2.getIntCenterX() and char.getIntCenterX() - float(char.intBoundingRectWidth)/2 <= char2.getIntCenterX():
					if char.getIntBoundingRectArea() > char2.getIntBoundingRectArea():
						finalList.remove(char2)
					elif char.getIntBoundingRectArea() < char2.getIntBoundingRectArea():
						finalList.remove(char)
				#end if
			#end for
		#end for
		return chars
	#end function

	def bubbleSortPossibleCharsByPositionX(self, chars):
		for i in range(len(chars)-1,0,-1):
			for j in range(i):
				if chars[j].getIntCenterX() > chars[j+1].getIntCenterX():
					temp = chars[j]
					chars[j] = chars[j+1]
					chars[j+1] = temp
				#end if
			#end for
		#end for
		return chars	
	#end function

	def setPlateNumber(self, plateNumber):
		self.plate_number = plateNumber
	#end function

