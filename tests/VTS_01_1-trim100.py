#File exposing trim problems

from __future__ import annotations
import vapoursynth as vs
from vapoursynth import core



import sys
import os
dirname = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(dirname,"."))

#our dedicated helper to have trim and audio support in Vapoursynth
from bssource import BSSource,Audio, Video, Trim, AudioDub, CurrentClip, DumpTrim

#get_video_duration_from_ffprobe, get_audio_duration_from_ffprobe,get_fps_from_ffprobe,get_framecount_from_ffprobe, get_sample_rate_from_ffprobe, get_nb_read_frames_from_ffprobe
from ffprobe import *

#ffmpeg_audio_extract_to_mem, framecount_from
from ffmpeg_full import *

#Generic Vapoursynth Plugin Source that wrap all with plugin failsafe autodetection
from load_video import VSPSource, get_method, get_duration_from_source

file='VTS_01_1-00.00.00.000-00.00.17.818.VOB'
input=r''+file
first=0

fps =get_fps_from_ffprobe(input)


print("== Retrieve duration, frames with many ways  to compare ==")

print("--- FFMEG Full ---")
#line=ffmpeg_audio_extract(file)
line = ffmpeg_audio_extract_to_mem(input)
duration=parse_time(line).total_seconds()
print("Duration (ffmpeg):"+str(duration))
print(framecount_from(duration, fps))

print("--- FFPROBE ---")
duration=get_audio_duration_from_ffprobe(input)
print("Duration Audio(FFprobe):"+str(duration))
duration=get_video_duration_from_ffprobe(input)
print("Duration Video(FFprobe):"+str(duration))
print(framecount_from(duration, fps))
print("Frames(FFprobe):"+str(get_framecount_from_ffprobe(input)))

print("--- FFMS2 ---")
video, audio=VSPSource(input,"ffms2")
duration=get_duration_from_source(input,"ffms2")
print("Duration(ffms2):"+str(duration))
a=get_method(), video.num_frames
video=video.std.Trim(first=first, last=video.num_frames-1)
b=get_method(), video.num_frames
print(framecount_from(duration, fps))
print("Frames(FFMS2):"+str(a[1])) if a[1]==b[1] else print("Error "+get_method()) 

print("--- BESTSOURCE ---")
video, audio=VSPSource(input,"bs")
duration=get_duration_from_source(input,'bs')
print("Duration(bs):"+str(duration))
print(framecount_from(duration, fps))
a=get_method(), video.num_frames
video=video.std.Trim(first=first, last=video.num_frames-1)
b=get_method(), video.num_frames
print("Frames(bs):"+str(a[1])) if a[1]==b[1] else print("Error "+get_method()) 


print("\n=== NOW WE ENTER IN TRIMZONE  =====")

def to_samples(clip, frame):
    return int((clip.audio.sample_rate/clip.video.fps)*frame)    

def get_audio_last_trimmable(clip):
    adjust=0
    video=clip.video
    while True:
        try:
            start=0
            last=video.num_frames-1
            afirst  = to_samples(clip, first)    if first  is not None else None
            alast   = to_samples(clip, last)-1-adjust if last  is not None else None
            alength= None
            audio.std.AudioTrim(first=afirst,last=alast,length=alength)
            break;
        except:
            adjust=adjust+1
    return  afirst, alast, adjust

def to_frame(clip, sample):
    return int((clip.video.fps/clip.audio.sample_rate)*sample)    

###############################---

clip=BSSource(input)
video=Video(clip)

print("\n--- Case1: fake trim from 0 to  video.num_frames-1="+str(video.num_frames-1))
a=video.num_frames
adjust=0

#Fix fails vapoursynth.Error: AudioTrim: last sample beyond clip end
while True:
    try:
        clip=Trim(0,  video.num_frames-1-adjust) 
        audio_cut =get_audio_last_trimmable(clip)
        break;
    except:
        adjust=adjust+1
        
#read the new frame number
b=Video(clip).num_frames
print(str(a)) if adjust == 0 else print("Error num_frames for video , need adjustement of "+str(adjust)+") to have audio trimable:\n[FIX] Video num_frames "+ str(a) +" to "+str(b)) 



print("-----> Correct num_frames has been corrected to "+str(b))
if audio_cut[2] == 0:
    print("[GOOD] audio is aligned with video")

print("audio(start,end,adjust)",audio_cut)


print("\n--- Case2 : audio trim with no previous video trim to fix--")
print("Keeping video.num_frames "+str(video.num_frames)+" determine audio last frame using audio trim to clip that succeed with adjust")
clip=BSSource(input)
video=Video(clip)
a=video.num_frames
audio_cut =get_audio_last_trimmable(clip)
adjust= audio_cut[2]

#length = int(attr_audio.sample_rate/self.video.fps*self.video.num_frames)
b=Video(clip).num_frames
print(str(a)) if adjust == 0 else print("Error Audio is not trimmable, fix sampling_frames for audio (adjust="+str(adjust)+"):\nVideo num_frames "+ str(a) +"-->"+str(b)) 
if audio_cut[2] == 0 :
    print("[GOOD] audio is aligned with video")
else:
    print("[FIX] Audio sampling has been ajusted by ", audio_cut[2])
#print(get_sample_rate_from_ffprobe(input))

print("last audio frame (calc from sample "+str(audio_cut[1])+"):"+str(to_frame(clip,audio_cut[1])))

print("-----> Correct num_frames has been corrected to "+str(to_frame(clip,audio_cut[1])))
print("Read nb_num_frames from FFPROBE (containing keys?) is "+str(get_nb_read_frames_from_ffprobe(input)))
#subprocess.DEVNULL,                    stdout=subprocess.STDOUT, 


#video=Video(clip)
#video.set_output()
