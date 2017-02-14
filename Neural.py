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

def image_to_feature_vector(image, size=(32, 32)):
	return cv2.resize(image, size).flatten()

# grab the list of images that we'll be describing
def neural(xValues, yValues, listOfChars):
	inputX = []
	outputY = []
	LOC = []
	if not listOfChars:
		print "noone"
	else:
		print "nije nonne"
		for c in listOfChars:
			#c = c.flatten()
				c = image_to_feature_vector(c)
			LOC.append(c)
		LOC = np.array(LOC) / 255.0
		

	for x in xValues:
		x = x.flatten()
		inputX.append(x)
		
	#endfor
	#outputY = yValues

	le = LabelEncoder()
	outputY = le.fit_transform(yValues)

	inputX = np.array(inputX) / 255.0
	outputY = np_utils.to_categorical(outputY, 35)

	print len(LOC[0])
	print len(inputX[0])
	print len(inputX[1])
	#convertToChar(outputY[3])
	#convertToChar(outputY[125])

	# encode the labels, converting them from strings to integers
	#le = LabelEncoder()
	#labels = le.fit_transform(labels)

	#data = np.array(data) / 255.0
	#labels = np_utils.to_categorical(labels, 5)

	
	(trainData, testData, trainLabels, testLabels) = train_test_split(
		inputX, outputY, test_size=0.20, random_state=42)
	

	# define the architecture of the network
	model = Sequential()
	model.add(Dense(768, input_dim=1024, init="uniform", activation="relu"))
	model.add(Dense(384, init="uniform", activation="relu"))
	model.add(Dense(35))
	model.add(Activation("softmax"))



	# train the model using SGD
	print("[INFO] compiling model...")
	sgd = SGD(lr=0.9)
	model.compile(loss="binary_crossentropy", optimizer=sgd,
		metrics=["accuracy"])
	model.fit(trainData, trainLabels, nb_epoch=50, batch_size=128,
		verbose=1)

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
	print  "Tested on 152 examples. Sucessful: ",(1.0 - float(count )/ float(len(result))) * 100, "%"

	t2 = model.predict(LOC)
	result2 = findResult(t2)
	print "\n"
	concatenated = ""
	for i in range(0, len(result2)):
		concatenated += str(unichr(result2[i]))
	print concatenated
	#print testLabels

	#print("[INFO] evaluating on testing set...")
	#(loss, accuracy) = model.evaluate(testData, testLabels,
		#batch_size=128, verbose=1)
	#print("[INFO] loss={:.4f}, accuracy: {:.4f}%".format(loss,
		#accuracy * 100))


def convertToChar(array):
	position = np.argmax(array)
	#print position
	if position < 10:
		realChar = 48 + position
	if position >= 10:
		realChar = 55 + position
	if position > 25:
		realChar += 1

	#realChar = str(unichr(realChar))
	#print realChar
	return realChar

def findResult(predictedValues):
	ret = []
	for value in predictedValues:
		temp = convertToChar(value)
		ret.append(temp)
	
	return ret
