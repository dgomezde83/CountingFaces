import evaluate
import cv2 as cv
import numpy as np
import argparse
import sys
import os

dir_path = os.getcwd()
INPUT_PATH = dir_path+"\\input\\"
OUTPUT_PATH = dir_path+"\\output\\"
WEIGHT_PATH = dir_path+"\\dataImg.pkl"
TOP_PERCENT = 0.2

#launch of the Face Detection. Comment this if you just want to run automata on already detected pictures
#---------------------------------------------------------------------------------------------------------------------------
#arguments: py automata.py alpha = ; beta = ;
#if user desires to modify contrast and brightness
if len(sys.argv) > 1:
	for fl in os.listdir(INPUT_PATH):
		image = cv.imread(INPUT_PATH+fl)
		
		#try open the image
		if image is None:
			print('Could not open or find the image: ' + INPUT_PATH + fl)
			break
		new_image = np.zeros(image.shape, image.dtype)
		alpha = int(sys.argv[1]) # Simple contrast control
		beta = int(sys.argv[2])    # Simple brightness control
		new_image = cv.convertScaleAbs(image, alpha=alpha, beta=beta)
		os.remove(INPUT_PATH+fl)
		cv.imwrite(INPUT_PATH+fl, new_image)
		
#now run the algorithm
evaluate.evaluate(WEIGHT_PATH, output_dir=OUTPUT_PATH,data_dir=INPUT_PATH)
#---------------------------------------------------------------------------------------------------------------------------

dicCounts = {}
nbFiles = 0
nbEntries = 0
#once the program finishes we're going to extract in a table the counts of each one
for fl in os.listdir(OUTPUT_PATH):
	nbCount = int(fl.split("_")[0])
	if not nbCount in dicCounts:
		dicCounts[nbCount] = 1
		nbEntries += 1
	else:
		dicCounts[nbCount] += 1
	
	nbFiles += 1

top30 = round(TOP_PERCENT*nbFiles)
#now lets check the top 30% of the dic:
hightestNum = 0
counter = 0
finalValues = []
haveToGo1 = False
for entry in sorted(dicCounts.keys(),reverse=True):
	if haveToGo1 == False:
		for i in range(dicCounts[entry]):
			finalValues.append(entry)
			counter += 1
			if counter >= top30:
				haveToGo1 = True
				break
		
#now that we have the top 30% in our list, we compute a mean
meanVal = 0
for i in finalValues:
		meanVal += i

finalVal = round(meanVal/len(finalValues))
print("There are " + str(finalVal) + " students in this room")