
import os
import sys

import subprocess


def get_sample_rate_from_ffprobe(video_file):
    """
    get audio sample_rate using ffprobe method
    """        
    #nb_read_packets
    cmd=["ffprobe", '-v', "error", "-select_streams", "a:0", "-count_frames", "-show_entries", "stream=sample_rate", "-of", "csv=p=0", video_file]
    
    
    out = subprocess.check_output(cmd)
    framecount = out.decode()[0:-1] #get rid of \n
    return framecount


def get_nb_read_frames_from_ffprobe(video_file):
    """
    get audio sample_rate using ffprobe method
    """        
    #nb_read_packets
    cmd=["ffprobe", '-v', "error", "-select_streams", "a:0", "-count_frames", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", video_file]
    
    
    out = subprocess.check_output(cmd)
    framecount = out.decode()[0:-1] #get rid of \n
    return framecount


##see https://stackoverflow.com/questions/2017843/fetch-frame-count-with-ffmpeg
def get_framecount_from_ffprobe(video_file):
    """
    get num_frames using ffprobe method
    """        
    #nb_read_packets
    cmd=["ffprobe", '-v', "error", "-select_streams", "v:0", "-count_frames", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", video_file]
    
    
    out = subprocess.check_output(cmd)
    framecount = out.decode()[0:-2] #get rid of \n
    return framecount


def get_fps_from_ffprobe(video_file):
    """
    get fps using ffprobe method
    """        
    out = subprocess.check_output(["ffprobe",video_file,"-v","0","-of","csv=p=0","-select_streams","v:0","-show_entries","stream=r_frame_rate"])
    rate = out.decode()[0:-2] #get rid of \n
    if len(rate.split('/'))==2:
        return rate
    return "0"

def get_fps_from_vspipe(video_file):
    """
    get fps using vspipe info and a vpy plugin wrapper
    """
    vpy_script="load_video-ok.vpy"
    #print(video_file)
    # initialize the script
    # http://www.vapoursynth.com/doc/output.html#options
   # import web_pdb; web_pdb.set_trace()
    
    vspipe_init = subprocess.Popen([
      "vspipe",
      "--info",
      str(vpy_script),
      "--arg",'source='+video_file
    ], stdout=open(os.devnull, "w"))
    vspipe_init.wait()
  
    vspipe = subprocess.Popen([
      "vspipe",
      "--info",
      str(vpy_script),
      "--arg",'source='+video_file
    ], stdout=subprocess.PIPE)   
    
    #'Width: 720\n'
    Width = vspipe.stdout.readline()
    #'Height: 480\n'
    Height = vspipe.stdout.readline()
    #'Frames: 145778\n'
    Frames = vspipe.stdout.readline()
    # FPS: 30000/1001 (29.970 fps)\n
    FPS = vspipe.stdout.readline()
    #'Format Name: YUV420P8\n'
    Format_Name = vspipe.stdout.readline()
    #'Color Family: YUV\n'
    Color_Family = vspipe.stdout.readline()
    #Alpha: No\n'
    Alpha = vspipe.stdout.readline()
    #'Sample Type: Integer\n'
    Sample_Type= vspipe.stdout.readline()
    #'SubSampling W: 1\n'
    SubSampling_W= vspipe.stdout.readline()
    #'SubSampling H: 1\n'
    SubSampling_H = vspipe.stdout.readline()
    
    #wash  'FPS: ' and ' (\d+ fps)'
    return FPS.decode('utf-8').split(" ")[1].strip()
    
    
def get_video_duration_from_ffprobe(video_file):
    """
    get video duration using ffprobe method
    """        
    
    #Correct: ffmpeg -i input.webm -f null -
    #seems to be eq to other variant in https://trac.ffmpeg.org/wiki/FFprobeTips
    #ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1
    cmd=["ffprobe",video_file,"-v","0","-of","csv=p=0","-select_streams","v:0","-show_entries","format=duration"]
    out = subprocess.check_output(cmd)
    duration = out.decode()[0:-1] #get rid of \n
    return duration
    
def get_audio_duration_from_ffprobe(video_file):
    """
    get audio duration using ffprobe method
    """        
   # cmd=["ffprobe",video_file,"-v","0","-of","csv=p=0","-select_streams","a","-show_entries","format=duration"]
    cmd=["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_file] 
    #print(" ".join(cmd))
    out = subprocess.check_output(cmd)
    duration = out.decode()[0:-1] #get rid of \n
    return duration

def get_audio_ext_from_ffprobe(video_file):
    """
    get audio extention using ffprobe method
    """        
    # "format=format_name"
    cmd=["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", " stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", video_file] 
    #print(" ".join(cmd))
    out = subprocess.check_output(cmd)
    duration = out.decode()[0:-1] #get rid of \n
    return duration

   
import json
from subprocess import check_output

def ffprobe_media_info(filename, print_result=True):
    """
    Returns:
        result = dict with audio info where:
        result['format'] contains dict of tags, bit rate etc.
        result['streams'] contains a dict per stream with sample rate, channels etc.
    """
    result = check_output(['ffprobe',
                            '-hide_banner', '-loglevel', 'panic',
                            '-show_format',
                            '-show_streams',
                            '-of',
                            'json', filename])

    result = json.loads(result)

    if print_result:
        print('\nFormat')

        for key, value in result['format'].items():
            print('   ', key, ':', value)

        print('\nStreams')
        for stream in result['streams']:
            for key, value in stream.items():
                print('   ', key, ':', value)

        print('\n')

    return result