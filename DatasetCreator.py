import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import re

import InitialThreshold
import PlatesRecognition

DEPTH_NO = 1
DEPTH_YES = 2


#Creating a dataset containing letters and a dataset containing numbers
def dataset_letter_and_dataset_number_creation(depth):
    images = []
    filenames = []
    print 'Creating datasets...'
    images, filenames = get_images('Dataset\*.jpg')
    counter = 0
    nameCounter = 10000
    file = open('dataset_letters.txt', 'w+')

    for image in images:
        imageThreshold = InitialThreshold.initialThreshold(image)
        plates = PlatesRecognition.recognizePossiblePlates(image, imageThreshold)
        if depth == DEPTH_YES:
            for plate in plates:
                for char in plate.listOfPossibleChars:
                    imgChar = char.imgChar
                    cv2.imshow('Char', imgChar)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    recognizedChar = raw_input("")
                    if recognizedChar != 'no':
                        imgChar = image_resize(imgChar)
                        location = 'Dataset Letter/'
                        name = 'P' + str(nameCounter) + '.jpg'
                        nameCounter += 1
                        counter +=1
                        write_image(imgChar, location, name)
                        file.write(name)
                        file.write('\t')
                        file.write(recognizedChar)
                        file.write(os.linesep)
                    #end if
                #end for
            #end for
        
        if depth == DEPTH_NO:
            if len(plates) > 0:
                plate = plates[0]
                for char in plate.listOfPossibleChars:
                    imgChar = char.imgChar
                    cv2.imshow('Char', imgChar)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    recognizedChar = raw_input("")
                    if recognizedChar != 'no':
                        imgChar = image_resize(imgChar)
                        location = 'Dataset Letters/'
                        name = 'P' + str(nameCounter) + '.jpg'
                        counter += 1
                        nameCounter += 1
                        write_image(imgChar, location, name)
                        file.write(name)
                        file.write('\t')
                        file.write(recognizedChar)
                        file.write(os.linesep)
                    #end if
                #end for
            #end if 
        #end for
    file.write(str(counter))
    file.close()   
#end function           

def image_resize(image, size=(32, 32)):
	return cv2.resize(image, size)
#end function


def write_image(image, location, name):
    path = location + name
    cv2.imwrite(path, image)
#end function


def get_images(path):
    imageList = []
    filenames = []
    for filename in glob.glob(path): 
        imageNext= cv2.imread(filename, flags=0)
        imageList.append(imageNext)
        filenames.append(filename)
    #end for
    return imageList, filenames
#end function


def write_image_filenames(path, filenames):
    file = open(path, 'w+')
    for filename in filenames:
        file.write(filename)
        file.write(os.linesep)
    #end for
    file.close()
#end function


def write_letters_and_nums_seprate_folders(images_path, dataset_txt):
    images, filenames = get_images(images_path)
    with open(dataset_txt) as file:
        content = file.readlines()
    file.close()

    counter = 0
    txt_numbers = open('numbers.txt','w+')
    txt_letters = open('letters.txt', 'w+')
    nums = 0
    letts = 0
    for line in content:
        line_split_list = re.split(r'\t+', line)
        if len(line_split_list) > 1:
            image_name = line_split_list[0]
            image_char = line_split_list[1].strip()
            if image_char.isalpha() == True:
                letts += 1
                txt_letters.write(image_name + '\t' + image_char + '\n')
                filename_split = filenames[counter].split('\\')
                write_image(images[counter], 'Letters/', filename_split[1])
                counter += 1
            else:
                nums += 1
                txt_numbers.write(image_name + '\t' + image_char + '\n')
                filename_split = filenames[counter].split('\\')
                write_image(images[counter], 'Numbers/', filename_split[1])
                counter += 1
            #end if
        #end if
    #end for
    txt_numbers.close()
    txt_letters.close()
    print str(nums) + ' Numbers'
    print str(letts) + ' Letters' 

#end function


