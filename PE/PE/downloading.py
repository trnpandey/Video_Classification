from youtube_dl import download_one_video
from callthis import frameFeature
import os
file1 = open("hi.txt","r+") 
lines= file1.readlines()
i=0
ch='MR'
for line in lines:
	#os.makedirs(ch+str(i))
	download_one_video(line,ch+str(i))
	path=ch+str(i)
	#os.chdir(path)
	frameFeature(ch+str(i))
	i=i+1
	os.system('rm '+'Data'+'/*.*')
	
#download_data('p5e5mf_G3FI&list=PL3128E15B8D159842','MR1')

