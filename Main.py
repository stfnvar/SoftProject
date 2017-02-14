import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

import InitialThreshold
import PlatesRecognition
import DatasetCreator
import Neural


#run
#Retrieving dataset images and its corresponding filenames
#imageList, filenames = DatasetCreator.get_images('Dataset\*.jpg')

imageCharacterList, characterPaths = DatasetCreator.get_images('Dataset Characters\\Dataset Letters\*.jpg')

characterFilenames = []

for character in characterPaths:
    character.strip()
    array = character.split('\\')
    characterFilenames.append(array[2])
#endfor

xValues = imageCharacterList

with open('dataset_letters.txt', 'r') as f:
    content = f.readlines() 
    yValues = []
    lengthOfContent = len(content) - 1
    for i in range(0, lengthOfContent):
        c = content[i]
        line = c.split("\t")    
        yValues.append(line[1])
    #endfor
#endwith

f.close()

listo = []
for x in xValues:
    ret,thresh1 = cv2.threshold(x,127,255,cv2.THRESH_BINARY)
    listo.append(thresh1)
    #cv2.imshow("yoy", thresh1)
    #cv2.imshow("yoy2", x)
    #cv2.waitKey(0)
#endfor
z = raw_input("Zelite li da unesete sliku[d/n]:")
picture = None


'''
#Writing filenames in a txt file
DatasetCreator.write_image_filenames('car_images.txt', filenames)

#Dataset creation for neural network
DatasetCreator.dataset_letter_and_dataset_number_creation(DatasetCreator.DEPTH_NO)
'''

#DatasetCreator.write_letters_and_nums_seprate_folders('Dataset Letters\*.jpg', 'dataset_letters.txt')


#print len(imageList)

#for image in imageList:
 #   imageThreshold = InitialThreshold.initialThreshold(image)
  #  plates = PlatesRecognition.recognizePossiblePlates(image, imageThreshold)

    #cv2.imshow('Image', image)
    
    #for char in plates[0].listOfPossibleChars:    
        #cv2.imshow('Char', char.imgChar)
        #cv2.waitKey(0)
    #end for
#end for

listOfPlates = []


listOfChars = []
if z == "d" or z == "D":
    pictureName = ""

    pictureName = raw_input("Unesite sliku:\n")
    picturePath = 'Dataset\\' + pictureName
    picture = cv2.imread(picturePath)
    cv2.imshow("slikaorig", picture)

    plates = []

    imgThreshold = InitialThreshold.initialThreshold(picture)

    cv2.imshow("slikathresh", imgThreshold)
    cv2.waitKey(0)

    plates = PlatesRecognition.recognizePossiblePlates(picture, imgThreshold)

    cv2.imshow("11", plates[0].imgPlate)
    cv2.waitKey(0)

    for char in plates[0].listOfPossibleChars:
        ret2,charThresh = cv2.threshold(char.imgChar,50,255,cv2.THRESH_BINARY)

       
        listOfChars.append(charThresh)
    #endfor
    #counterr = 0
    #for char in plates[0].listOfPossibleChars:
        #cv2.imshow(str(counterr), char.imgChar)
        #counterr += 1
        #cv2.waitKey(0)
    #endfor
#print "y", listOfChars[0]
#print "y2", listo[0]

Neural.neural(listo, yValues, listOfChars)

#cv2.imshow("a1", imgThreshold)
#cv2.waitKey(0)


#end main

