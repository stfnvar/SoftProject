import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

import DatasetCreator
import Neural

from Plate import Plate

#Retrieving dataset images and its corresponding filenames
#imageList, filenames = DatasetCreator.get_images('Dataset\*.jpg')

'''
#Writing filenames in a txt file
DatasetCreator.write_image_filenames('car_images.txt', filenames)

#Dataset creation for neural network
DatasetCreator.dataset_letter_and_dataset_number_creation()
'''

#DatasetCreator.write_letters_and_nums_seprate_folders('Dataset Letters\*.jpg', 'dataset_letters.txt')

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

imagesValuesX = []
for x in xValues:
    ret,thresh1 = cv2.threshold(x,127,255,cv2.THRESH_BINARY)
    imagesValuesX.append(thresh1)
#endfor

z = raw_input("Zelite li da unesete sliku[d/n]:")
picture = None

if z == "d" or z == "D":
    pictureName = ""

    pictureName = raw_input("Unesite sliku:\n")
    picturePath = 'Dataset\\' + pictureName
    picture = cv2.imread(picturePath)
    cv2.imshow("Originalna slika ", picture)

    plateObject = Plate(picture)
    final = plateObject.plateSearch(pictureName)

    print("Main length final chars")
    print(len(final))

    plateResult = Neural.neural(imagesValuesX, yValues, final)
    plateObject.setPlateNumber(plateResult)
    plateObject.showResults()
#end main