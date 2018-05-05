import csv
import os
import subprocess
class ScriptBuilding:
	def frameFeature(self):
			fileName=self.fileName+".mp4"
			foraudio=fileName
			directory=self.fileName
			#create directory with same file name if not existing
			if not os.path.exists(directory):
				os.makedirs(directory)
			#removing all folder inside the directory 	
			os.system('rm '+directory+'/*.*')
			#command to get and store key frame in the directory folder and store transition time of each keu frames
			os.system('ffmpeg -i Data/'+fileName+' -vf "select=eq(pict_type\,I),scale=1366x768,showinfo[out]" -vsync vfr -qscale:v 2 '+directory+'/thumbnails-%02d.png 2>'+directory+'/positions.txt')
			i=0
			count=0
			cmd1="ls "+directory+"/*.png"
			for fileName in subprocess.check_output([cmd1],shell=True).split("\n"):
				#print fileName
				if(fileName!="" and i%5!=0 and count<80):
					os.system('rm '+fileName)
					count+=1
					i+=1
				else:
					i+=1
		
			#code written to convert video into audio wav file
			cmd="ffmpeg -i Data/"+foraudio +" "+directory+"/out.wav"
			v=subprocess.check_output([cmd],shell=True)
			
	def processing(self):
			fileName=raw_input()
			if(fileName!=""):
					self.fileName=fileName
					self.frameFeature()
				
obj=ScriptBuilding()
obj.processing()
