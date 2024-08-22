import vapoursynth as vs
from vapoursynth import core
from bssource.bssource import BSSource,Trim, Audio, Video, AudioDub, TextSub, ApplyRange, Register, Filter, CurrentClip

input=r'VTS_01_1-00.00.00.000-00.00.17.818.VOB'

#clip=BSSource(input)
BSSource(input)

subfile="VTS_01_1-trim100.ass"
first=50
last=60

## When a range first, last is specified, TextSub uses FrameEval ,  
## this last requires a absolute path for subfile  in Aegisub else
## you will get "Assrender: inout file does not exist or is not a regular file"
## With vspreview it works only using the file name
import sys
import os
dirname = os.path.dirname(__file__)
subfile=os.path.join(dirname,subfile)


clip=Trim(0,100)

"""
# Filter
def range_sub(n: int, f: vs.VideoFrame,
                     clip: vs.VideoNode, first : int, last: int, subfile:str)  -> vs.VideoNode:
               
    v=clip #core.text.ClipInfo(clip)
                 
    infos=[]
     
    if(n >= first and n <=last) :
        #   
        #    infos.append(str(first)+"<="+str(n)+"<="+str(last))
        #      
        #    for prop, prop_value in CurrentClip().info().items():
        #        infos.append(prop+"="+str(prop_value))
        #       
        #   v=core.text.Text(v,  "\n".join(infos), alignment=9, scale=1) 
        #      
        v=TextSub(subfile,v)

            
    return v
    
from functools import partial
clip.video = clip.video.std.FrameEval(partial(range_sub, clip=clip.video,first=first, last=last, subfile=subfile), prop_src=clip.video)
"""
clip=TextSub(subfile,clip,first=first, last=last ) 


AudioDub(clip.video,clip.audio)

