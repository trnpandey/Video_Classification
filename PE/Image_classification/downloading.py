from youtube_dl import download_one_video
from callthis import frameFeature
import os
import subprocess
import numpy as np
import pafy
import requests 
import re
import csv
import urllib2

import argparse
import json
import sys
import cv2
#from image_mining.figure_extraction import FigureExtractor
#from image_mining.utils import open_image
import time

file1 = open("maintextfile.txt","r+") 
lines= file1.readlines()
i=0
ch='MR'
threshold_numberofslides=0
threshold_numberoflines=0
threshold_numberoffigures=0
threshold_numberofspeakers=0
for line in lines:
	#os.makedirs(ch+str(i))
	download_one_video(line,ch+str(i))
	path=ch+str(i)
	#os.chdir(path)
	#frameFeature(ch+str(i))
	directory=ch+str(i)
	fileName=ch+str(i)+".mp4"
	if not os.path.exists(directory):
			os.makedirs(directory)
	#removing all folder inside the directory 	
	os.system('rm '+directory+'/*.*')
	#command to get and store key frame in the directory folder
	os.system('ffmpeg -i Data/'+fileName+' -vf "select=eq(pict_type\,I),scale=1366x768,showinfo[out]" -vsync vfr -qscale:v 2 '+directory+'/thumbnails-%02d.png 2>'+directory+'/positions.txt')
	j=0
	count=0
	cmd1="ls "+directory+"/*.png"
	for fileName in subprocess.check_output([cmd1],shell=True).split("\n"):
			#print fileName
			if(count>80):
				os.system('rm '+fileName)
			if(fileName!="" and j%5!=0) :
				os.system('rm '+fileName)
				#count+=1
				j+=1
			else:
				count+=1
				j+=1
	countLines=0
	noOfSlides=0
	scale=0
	noOfFig=0
	time_transition=0
	
	#command line statement used to fetch transition time frame wise
	cmd1="grep 'pts_time' "+directory+"/positions.txt"
	result=subprocess.check_output([cmd1],shell=True).split("\n")
	
	#appending time values
	time=[]
	for strV in result:
		time.append(strV[strV.find("pts_time")+9:strV.find("pts_time")+16])
	i=0
	cmd1="ls "+directory+"/*.png"
	prevLine=-1
	prevScale=-1
	# fetch all key frames for processing
	for fileName in subprocess.check_output([cmd1],shell=True).split("\n"):
		print fileName
		#condition testing added because feature extraction was taking huge timing
		if(fileName!=""):
			face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
 			image = cv2.imread(fileName)
			grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 			faces = face_cascade.detectMultiScale(grayImage)
			if len(faces) == 0:
    				flag=0
 				#print "No faces found"
			else:
			    #print faces
			    #print faces.shape
			    flag=1
    			    #print "Number of faces detected: " + str(faces.shape[0])
			for (x,y,w,h) in faces:
       				cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)
			#ocropus processing to fetch features
			cmd='ocropus-nlbin -n '+fileName+' -o book'
			#ocropus command to convert frame into black and white format and doing eroding
			v=subprocess.check_output([cmd],shell=True)
			try:
				#ocropus function used to get feature value
				val=subprocess.check_output(["ocropus-gpageseg -n --maxcolseps 0 book/0001.bin.png"],shell=True)
				val=val.split("\n")
				lastLine=val[len(val)-2].split(" ")
				#print("lastLine  ",lastLine[len(lastLine)-1]," and scale ",lastLine[len(lastLine)-2])
				
				# checking if key is not key frame and there is come person gesture movement
				if(prevLine==int(lastLine[len(lastLine)-1]) and prevScale==float(lastLine[len(lastLine)-2])):
					continue
				
				#updating feature values	
				scale+=float(lastLine[len(lastLine)-2])
				countLines+=int(lastLine[len(lastLine)-1])
				noOfSlides+=1
				#print("countLines",countLines)
				#print("noOfSlides",noOfSlides)
				#print("noOfFig",noOfFig)
				#print(time_transition)		
				prevLine=int(lastLine[len(lastLine)-1])
				prevScale=float(lastLine[len(lastLine)-2])
			except ValueError:
				#come here when font is less than default minscale 
				print("Oops!  That was no valid number.  Try again...")
				#skip this frame for processing
				continue
			#code to fetch number of figures in frame
			#used image mining code	
			#print(fileName)
			#code to fetch number of figures in frame
			#used image mining code	
			cmd="image-mining/extract-figures.py --interactive "+fileName
			#print(" cmd -->", cmd)
			figures=subprocess.check_output([cmd],shell=True).split("\n")
				
			#print("figure output --->",figures[len(figures)-2])
			figures=figures[len(figures)-2].split(" ")
			#print number of figure present in frame
			#print"no of figures is ",figures[len(figures)-1]
			noOfFig+=int(figures[len(figures)-1])
			#print('total number of figures till now is:-',noOfFig)
			#code to find transition timing between two key frames
			
	
	#frame feature extraction completed
	#removing all files from the directory location		
	#os.system('rm '+directory+'/*.*')
		
	i=i+1
	#appending features in a list self.feature which is use to collect all feature of 1 video
	print("countLines",countLines)
	print("noOfSlides",noOfSlides)
	print("Speaker is present(1) or not (0)",flag)
	print("noOfFig",noOfFig)
	threshold_numberofslides+=noOfSlides
	threshold_numberoflines+=countLines
	threshold_numberoffigures+=noOfFig
	threshold_numberofspeakers+=flag
	threshold_numberofslides/=i
	threshold_numberoflines/=i
	threshold_numberoffigures/=i
	threshold_numberofspeakers/=i
	print("Threshold for number of slides: ",threshold_numberofslides)
	print("Threshold for number of lines: ",threshold_numberoflines)
	print("Threshold for number of figures: ",threshold_numberoffigures)
	print("Threshold for number of speakers: ",threshold_numberofspeakers)
	#print(time_transition)		
	#self.feature.append(flag)
	#self.feature.append(countLines/noOfSlides)
	#self.feature.append(scale/noOfSlides)
	#self.feature.append(noOfFig)
	#self.feature.append(time_transition)
	os.system('rm -r ' +directory)
	os.system('rm '+'Data'+'/*.*')
