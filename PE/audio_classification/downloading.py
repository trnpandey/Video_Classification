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
file1 = open("maintextfile.txt","r+") 
lines= file1.readlines()
i=0
ch='MR'
threshold_syllables=0
threshold_pauses=0
threshold_phonation=0
threshold_speechrate=0
threshold_articulation=0
threshold_averagesyllableduration=0
threshold_syllables=0

for line in lines:
	#os.makedirs(ch+str(i))
	download_one_video(line,ch+str(i))
	path=ch+str(i)
	#os.chdir(path)
	#frameFeature(ch+str(i))
	directory=ch+str(i)
	if not os.path.exists(directory):
				os.makedirs(directory)
	#praat tool is used to fetch audio feature wich include speech rate, etc
	foraudio=ch+str(i)+".mp4"
	cmd="ffmpeg -i Data/"+foraudio +" "+directory+"/out.wav"
	v=subprocess.check_output([cmd],shell=True)
	os.system('rm ' + 'Data'+'/*.*')
	#praat tool is used to fetch audio feature wich include speech rate, etc
	cmd="praat --run speechRateV2.praat -25 2 0.3 1 "+directory+"/"
	result=subprocess.check_output([cmd],shell=True)
	result=result[151:].split(",")
	threshold_syllables+=float(result[0])
	threshold_pauses+=float(result[1])
	threshold_phonation+=float(result[3])
	threshold_speechrate+=float(result[4])
	threshold_articulation+=float(result[5])
	threshold_averagesyllableduration+=float(result[6])

	print("number of syllables:-",float(result[0])) 
	print("number of pauses:-",float(result[1])) 
	print("original duration:-",float(result[2])) 
	print("phonation time:-",float(result[3])) 
	print("speech rate:-",float(result[4])) 
	print("articulation rate:-",float(result[5])) 
	print("average syllable duration:-",float(result[6])) 	
	#os.system('rm '+'Data'+'/*.*')
	i=i+1	
	os.system('rm -r ' +directory)
	print('      ')
	threshold_syllables/=i
	threshold_pauses/=i
	threshold_phonation/=i
	threshold_speechrate/=i
	threshold_articulation/=i
	threshold_averagesyllableduration/=i
	print("Threshold of number of syllables is:- ",float(threshold_syllables))
	print("Threshold of number of pauses is:- ",float(threshold_pauses))
	print("Threshold of number of phonation time is:- ",float(threshold_phonation))
	print("Threshold of number of speech rate is:- ",float(threshold_speechrate))
	print("Threshold of number of articulation rate is:- ",float(threshold_articulation))
	print("Threshold of number of average syllable duration is:- ",float(threshold_averagesyllableduration))

threshold_syllables/=i
threshold_pauses/=i
threshold_phonation/=i
threshold_speechrate/=i
threshold_articulation/=i
threshold_averagesyllableduration/=i
print("Threshold of number of syllables is:- ",float(threshold_syllables))
print("Threshold of number of pauses is:- ",float(threshold_pauses))
print("Threshold of number of phonation time is:- ",float(threshold_phonation))
print("Threshold of number of speech rate is:- ",float(threshold_speechrate))
print("Threshold of number of articulation rate is:- ",float(threshold_articulation))
print("Threshold of number of average syllable duration is:- ",float(threshold_averagesyllableduration))
	#appending result fetched from praat into self.feature
	#for val in result:
		#print(val)
	#	self.feature.append(float(val))
	#	os.system('rm '+directory+'/*.*')	
	
#download_data('p5e5mf_G3FI&list=PL3128E15B8D159842','MR1')

