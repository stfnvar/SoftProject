# USAGE
# python simple_neural_network.py --dataset kaggle_dogs_vs_cats

# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from keras.models import Sequential
from keras.layers import Activation
from keras.optimizers import SGD
from keras.layers import Dense
from keras.utils import np_utils
import numpy as np
import argparse
import cv2
import os

def reshapeAndThreshold(imgGray):
	
    height, width = imgGray.shape
    imgBlurred = np.zeros((height, width, 1), np.uint8)
    imgBlurred = cv2.GaussianBlur(imgGray, (5, 5), 0)
    imgThreshold = cv2.adaptiveThreshold(imgBlurred, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    return imgThreshold
#end function

def image_to_feature_vector(image, size=(32, 32)):

    cv2.imshow("Resized letter", image)
    cv2.waitKey(0)
    height, width, numChannels = image.shape
    imgHSV = np.zeros((height, width, 3), np.uint8)
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    imgHue, imgSaturation, imgValue = cv2.split(imgHSV)
    imgGray = imgValue

    imgThreshold = reshapeAndThreshold(imgGray)
    
    return cv2.resize(imgThreshold, size).flatten()
#end function

def neural(xValues, yValues, listOfChars):
	inputX = []
	outputY = []
	LOC = []
	if not listOfChars:
		print "Nije prosledjena tablica"
	else:
		print "Prosledjena tablica"
		for c in listOfChars:
			c = image_to_feature_vector(c)
			LOC.append(c)
		#endfor
		LOC = np.array(LOC) / 255.0
	#endif

	for x in xValues:
		x = x.flatten()
		inputX.append(x)	
	#endfor
	#outputY = yValues

	le = LabelEncoder()
	outputY = le.fit_transform(yValues)

	inputX = np.array(inputX) / 255.0
	outputY = np_utils.to_categorical(outputY, 35)
	
	(trainData, testData, trainLabels, testLabels) = train_test_split(
		inputX, outputY, test_size=0.20, random_state=42)
	

	# define the architecture of the network
	model = Sequential()
	model.add(Dense(768, input_dim=1024, init="uniform", activation="relu"))
	model.add(Dense(384, init="uniform", activation="relu"))
	model.add(Dense(35))
	model.add(Activation("softmax"))

	# train the model using SGD
	print("[INFO] Kompajliranje modela...")
	sgd = SGD(lr=0.9)
	model.compile(loss="binary_crossentropy", optimizer=sgd,metrics=["accuracy"])
	model.fit(trainData, trainLabels, nb_epoch=50, batch_size=128, verbose=1)

	t = model.predict(inputX[1150:1302] )
	#print t

	result = findResult(t)
	print result
	yRealValues = outputY[1150:1302]
	for i in range(0, len(result)):
		print str(unichr(result[i])), str(unichr(convertToChar(yRealValues[i])))

	
	print "---------------------------------------"
	count = 0
	for i in range(0, len(result)):
		if result[i] - convertToChar(yRealValues[i]) != 0:
			count += 1
	
	print count
	print  "Testirano na 152 uzoraka. Uspesno: ",(1.0 - float(count )/ float(len(result))) * 100, "%"

	if not listOfChars:
		print "Nije prosledjena tablica"
	else:
		t2 = model.predict(LOC)
		result2 = findResult(t2)
		print "\n"
		concatenated = ""
		for i in range(0, len(result2)):
			concatenated += str(unichr(result2[i]))
		print concatenated
		return concatenated
#end function

def convertToChar(array):
	position = np.argmax(array)
	if position < 10:
		realChar = 48 + position
	if position >= 10:
		realChar = 55 + position
	if position > 25:
		realChar += 1
	return realChar
#end function

def findResult(predictedValues):
	ret = []
	for value in predictedValues:
		temp = convertToChar(value)
		ret.append(temp)
	return ret
#end function
