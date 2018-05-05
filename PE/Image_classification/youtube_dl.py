'''
objective: Get the follwoing data for a videe with youtube id, 
like_count
format_note
duration
fulltitle
view_count
tags
is_live
dislike_count
average_rating
categories
acodec
description
uploader_id
uploader
subtitles
age_limit
resolution
'''


import subprocess as sp
import os
import sys
import shutil
import json
from multiprocessing import Pool
import codecs

def command_to_download_mp4video_and_srt_from_youtube(youtube_id, output_file_name_without_ext):
    #youtube-dl -o 'rK4sXm_MPWo.%(ext)s' -f mp4 --write-sub --sub-lang "en" --convert-subs srt https://www.youtube.com/watch?v=rK4sXm_MPWo --write-auto-sub
    cmd = "youtube-dl" + " -o '" + output_file_name_without_ext + ".%(ext)s' -f mp4 --write-sub --sub-lang 'en' --convert-subs srt --write-info-json " \
  + youtube_id
    print "Built cmd: ",cmd
    return cmd

def execute_command(command):
    p = sp.Popen(command,
                 bufsize=2048,
                 shell=True,
                 stdin=sp.PIPE,
                 stdout=sp.PIPE,
                 stderr=sp.PIPE,
                 close_fds=(sys.platform != 'win32'))
    output = p.communicate()
    print("Executed cmd: " + command)

def download_one_video(video_id, download_dir_name):
    #video_id = sys.argv[1]
    download_dir_path = 'Data'+"/"
    download_file_path = 'Data'+'/'+download_dir_name
    print "Downloading... ("+video_id+")"+ " to "+download_dir_path
    if os.path.exists(download_dir_path):
        shutil.rmtree(download_dir_path)
    os.mkdir(download_dir_path)
    #os.mkdir(download_file_path)
    execute_command(command_to_download_mp4video_and_srt_from_youtube(video_id,download_file_path))
    print "Download complete.("+video_id+")"

def download_data(video_id_list, download_dir_name):
    sp.call(['mkdir', download_dir_name])
    for video_id in video_id_list:
    	print(str(video_id).strip())
        download_one_video(str(video_id).strip(), download_dir_name)

def get_info(video_id, download_dir_name):
    info = None
    path = download_dir_name+'/'+video_id+'/'+video_id+'.info.json'
    if not os.path.exists(path):
        download_one_video(str(video_id).strip(), download_dir_name)
    if os.path.exists(path):
        with open(path) as data_file:
            info = json.load(data_file)
    return info
