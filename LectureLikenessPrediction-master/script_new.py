import os
import subprocess
import argparse
import json

import sys
import cv2
import numpy as np

#from image_mining.figure_extraction import FigureExtractor
#from image_mining.utils import open_image

import time

import pafy
import requests 
import re

import csv

import sklearn
from sklearn.linear_model import LinearRegression

import urllib2

threshold_number_of_slides=10
threshold_number_of_lines=41
threshold_number_of_figures=19
threshold_number_of_speakers=1
threshold_number_of_syallbles=8544.5
threshold_number_of_pauses=1295.75
threshold_phonation=1816.18
threshold_number_of_speech_rate=2.77
threshold_number_of_articulation_rate=4.7025
threshold_number_of_average_syllable=0.21325




#('Threshold for number of slides: ',10)
#('Threshold for number of lines: ', 41)
#('Threshold for number of figures: ', 19)
#('Threshold for number of speakers: ', 3)
#number of syllables:- 8544.5
#number of pauses:- 1295.75
#phonation time:- 1816.18
#speech rate:- 2.77
#articulation rate:-4.7025
#average syllable duration 0.21325
class ScriptBuilding:
	
	#code to find all frame related features like number of lines, number of figures, scale of letters.
	def frameFeature(self):
		flag=0
		#assumping all mp4 file are used
		fileName=self.fileName+".mp4"
		directory=self.fileName
		#create directory with same file name if not existing
		if not os.path.exists(directory):
			os.makedirs(directory)
		#removing all folder inside the directory 	
		os.system('rm '+directory+'/*.*')
		#command to get and store key frame in the directory folder and store transition time of each keu frames
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
	
		#initializing initially all paramters with 0 value
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
			#print fileName
			#condition testing added because feature extraction was taking huge timing
			if(fileName!=""):
				i+=1
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
				if(i>0):
					time_transition+=(float(time[i])-float(time[i-1]))
				
		
		#frame feature extraction completed
		#removing all files from the directory location		
		#os.system('rm '+directory+'/*.*')
		#appending features in a list self.feature which is use to collect all feature of 1 video
		if(countLines>=threshold_number_of_lines):
			self.number_of_visual_features_matched+=1;
		if(noOfSlides>=threshold_number_of_slides):
			self.number_of_visual_features_matched+=1;
		if(flag==1):
			self.number_of_visual_features_matched+=1;
		if(noOfFig>=threshold_number_of_figures):
			self.number_of_visual_features_matched+=1;
		
	
			
		#print("countLines",countLines)
		#print("noOfSlides",noOfSlides)
		#print("Speaker is present(1) or not (0)",flag)
		#print("noOfFig",noOfFig)
		#print(time_transition)		
		self.feature.append(flag)
		self.feature.append(countLines/noOfSlides)
		self.feature.append(scale/noOfSlides)
		self.feature.append(noOfFig)
		self.feature.append(time_transition)
		#4 length of self.feature
		
	#code for audio feature data collection	
	def audioFeature(self):
		fileName=self.fileName+".mp4"
		directory=self.fileName
		if not os.path.exists(directory):
			os.makedirs(directory)
		os.system('rm '+directory+'/*.*')
		
		#code written to convert video into audio wav file
		cmd="ffmpeg -i Data/"+fileName +" "+directory+"/out.wav"
		v=subprocess.check_output([cmd],shell=True)
		
		#praat tool is used to fetch audio feature wich include speech rate, etc
		cmd="praat --run speechRateV2.praat -25 2 0.3 1 "+directory+"/"
		result=subprocess.check_output([cmd],shell=True)
		result=result[151:].split(",")
		if(float(result[0])>=threshold_number_of_syallbles):
			self.number_of_audio_features_matched+=1;
		if(float(result[1])>=threshold_number_of_pauses):
			self.number_of_audio_features_matched+=1;
		if(float(result[3])>=threshold_phonation):
			self.number_of_audio_features_matched+=1;
		if(float(result[4])>=threshold_number_of_speech_rate):
			self.number_of_audio_features_matched+=1;
		if(float(result[5])>=threshold_number_of_articulation_rate):
			self.number_of_audio_features_matched+=1;
		if(float(result[6])>=threshold_number_of_average_syllable):
			self.number_of_audio_features_matched+=1;
		
		#print("number of syllables:-",float(result[0])) 
		#print("number of pauses:-",float(result[1])) 
		#print("original duration:-",float(result[2])) 
		#print("phonation time:-",float(result[3])) 
		#print("speech rate:-",float(result[4])) 
		#print("articulation rate:-",float(result[5])) 
		#print("average syllable duration:-",float(result[6])) 		
		
		#appending result fetched from praat into self.feature
		for val in result:
			#print(float(val))
			self.feature.append(float(val))
		os.system('rm '+directory+'/*.*')	
		# 7 length feature here total =11
		
	#code for fetching metadata from youtube	
	def youtubeFeature(self):
		url=self.url
		try:
			#pafy is used to fetch details like duration,rating,view count etc
			video = pafy.new(url)
			rating=video.rating
			viewcount,length,duration = video.viewcount,video.length,video.duration
			
			#call to get number of likes
			likes=self.getStats(url)
			print("rating",rating)
			print("views",viewcount)
			print("length",length)
			print("duration",duration)
		except urllib2.URLError:
			#this error happens when there is internet issue
			print("Oops!  There was URL issue.  Try again...")
			#calling again fucntion to get value
			self.youtubeFeature()
		self.feature.append(float(viewcount))
		try:
			val=float(likes)
		except ValueError:
			val=0.0
		
		#appending result fetched into self.feature	
		self.feature.append(length)	
		self.feature.append(val)
		self.feature.append(float(rating))
		# 4 length feature here and total length of self.feature=15

	#code to fetch likes of video 
	def getStats(self,link):
		page = requests.get(link)
		likes = re.search("with (\d*.\d*.\d*)", page.text).group(1)
		return likes.split(" ")[0]

	#purpose of this function is to call function to extract features
	def processing(self):
		features=[]
		self.result_feature=np.empty((0,16))
		#is feature exists we will apppend it to have more data set into our dataset
		if os.path.isfile('result.npy'):
			self.result_feature=np.load('result.npy')
		
		#read csv file which contain name of file and its relative youtube link
		#assumption made
		with open("Videofiles.csv", 'rb') as f:
			reader = csv.reader(f)
			headers = reader.next()
			column = {h:[] for h in headers}
			#reading csv file
			for row in reader:
				fileName=row[0]
				url=row[1]
				
				if(fileName!=""):
					self.feature=[]
					self.fileName=fileName
					self.url=url
					self.number_of_visual_features_matched=0

					#calling function to fetch frame features
					self.frameFeature()
					#calling function to fetch audio features
					self.number_of_audio_features_matched=0
					self.audioFeature()
					#print('audio',self.number_of_audio_features_matched)
					#print('visual',self.number_of_visual_features_matched)
					temp1=self.number_of_audio_features_matched
					temp2=self.number_of_visual_features_matched
					self.number_of_audio_features_matched/=6
					self.number_of_visual_features_matched/=4
					if(temp1>=3 and temp2>=2):
						print('Hey, this is a lively teaching style video')
					elif(temp1>=3 and self.number_of_audio_features_matched>=self.number_of_visual_features_matched):
						print('Hey, this is a verbal teaching style video')
					elif(temp2>=2 and self.number_of_audio_features_matched<=self.number_of_visual_features_matched):
						print('Hey, this is a visual teaching style video')
					else:
						print('Oops!, this is not any type of teaching style')
					#calling function to fetch yourube metadata
					#self.youtubeFeature()
					#print (self.feature)
					#appending final features of a video in result feature
					#self.result_feature=np.append(self.result_feature,np.array([self.feature]),axis=0)
					#deleting directory
					_notused=subprocess.check_output(["rm -r "+fileName],shell=True)					
					#print self.result_feature.shape
					#every time saving it in a file so that no data is loss if any error comes in
					#np.save("result",self.result_feature)
					
#		print self.result_feature.shape
		#saving all features in a file
		np.save("result",self.result_feature)
#		#display=np.load("result.npy")
		#print display
		
	#model is build and tested	
	def model_creation(self):
		result=np.load('result.npy')
		result = result.astype(np.float32, copy=False)
		train=result[:40]
		test=result[40:49]
		#using logisitic regression
		model=LinearRegression()
		#print (result)		
		model.fit(train[:,0:14], train[:,14], sample_weight=None)
		#print model.get_params(deep=True)
		
		#predict value of rating 
		prediction=model.predict(test[:,0:14])
		print("prediction ",prediction)
		#print(test[:,14])
		
		#sum of square error is found
		error = np.sum((prediction-test[:,14])**2)
		print("error ",error)
		
			
		
#creating object for class which contain Scipt for building feature vector and doing prediction
obj=ScriptBuilding()

#calling script for building predictors
obj.processing()

#code to build model by split data into 80-20 ration and calculate/print error
#obj.model_creation()
