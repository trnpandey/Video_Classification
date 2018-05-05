import csv
import os
import subprocess
#str is the name of the .mp4 files
def frameFeature(str):
			fileName=str
			fileName=fileName+".mp4"
			foraudio=fileName
			directory=str
			#create directory with same file name if not existing
			if not os.path.exists(directory):
				os.makedirs(directory)
			#removing all folder inside the directory 	
			os.system('rm '+directory+'/*.*')
			#command to get and store key frame in the directory folder
			#os.system('ffmpeg -i Data/'+fileName+' -vf "select=eq(pict_type\,I),scale=1366x768,showinfo[out]" -vsync vfr -qscale:v 2 '+directory+'/thumbnails-%02d.png 2>'+directory+'/positions.txt')
			#i=0
			#count=0
			#cmd1="ls "+directory+"/*.png"
			#for fileName in subprocess.check_output([cmd1],shell=True).split("\n"):
				#print fileName
			#	if(fileName!="" and i%5!=0 and count<80):
			#		os.system('rm '+fileName)
			#		count+=1
			#		i+=1
			#	else:
			#		i+=1
		
			#code written to convert video into audio wav file
			cmd="ffmpeg -i Data/"+foraudio +" "+directory+"/out.wav"
			v=subprocess.check_output([cmd],shell=True)
			result=result[151:].split(",")
			print("number of syllables:-",float(result[0])) 
			print("number of pauses:-",float(result[1])) 
			print("original duration:-",float(result[2])) 
			print("phonation time:-",float(result[3])) 
			print("speech rate:-",float(result[4])) 
			print("articulation rate:-",float(result[5])) 
			print("average syllable duration:-",float(result[6]))
