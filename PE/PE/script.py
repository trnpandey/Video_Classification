import os
import subprocess
import numpy as np
import pafy
import requests 
import re
import csv
import urllib2
class ScriptBuilding:
	def youtubeFeature(self):
		url=self.url
		try:
			#pafy is used to fetch details like duration,rating,view count etc
			video = pafy.new(url)
			rating=video.rating
			viewcount,length,duration = video.viewcount,video.length,video.duration
			
			#call to get number of likes
			likes=self.getStats(url)
			
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
		print("likes",val)
		print("rating",rating)
		print("views",viewcount)
		print("length",length)
		print("duration",duration)
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
		print("number of syllables:-",float(result[0])) 
		print("number of pauses:-",float(result[1])) 
		print("original duration:-",float(result[2])) 
		print("phonation time:-",float(result[3])) 
		print("speech rate:-",float(result[4])) 
		print("articulation rate:-",float(result[5])) 
		print("average syllable duration:-",float(result[6])) 		
		#appending result fetched from praat into self.feature
		for val in result:
			#print(val)
			self.feature.append(float(val))
		os.system('rm '+directory+'/*.*')	
	#purpose of this function is to call function to extract features
	def processing(self):
		features=[]
		#read csv file which contain name of file and its relative youtube link
		with open("Videofiles.csv", 'rb') as f:
			reader = csv.reader(f)
			headers = reader.next()
			column = {h:[] for h in headers}
			#reading csv file
			for row in reader:
				fileName=row[0]
				url=row[1]
				print(fileName)
				print(url)
				if(fileName!=""):
					self.feature=[]
					self.fileName=fileName
					self.url=url
					#calling function to fetch yourube metadata
					self.youtubeFeature()
					#calling function to fetch audio features
					self.audioFeature()
					#deleting directory
					_notused=subprocess.check_output(["rm -r "+fileName],shell=True)			
					print ('Feature array:-', self.feature)
					
		
#creating object for class which contain Scipt for building feature vector
obj=ScriptBuilding()

#calling script for extracting features
obj.processing()
