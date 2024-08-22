import vapoursynth as vs
from vapoursynth import core
from bssource.bssource import BSSource,Trim, Audio, Video, AudioDub, TextSub, ApplyRange, Register, Filter, CurrentClip

input=r'VTS_01_1-00.00.00.000-00.00.17.818.VOB'

#clip=BSSource(input)
BSSource(input)



clip=Trim(0,100)

#from pprint import pprint
#with open( "dump_globals.txt" , "a" ) as fwrite:
#    pprint(globals(), indent=2,stream=fwrite)
    
subfile="VTS_01_1-trim100.ass"
first=50
last=60

"""
#The Next lines will apply the filter TextSub on the range first to last equivalent to:
v=TextSub(subfile,clip.video)
clip.video=clip.video.std.Trim(first=0, last=first-1)+v.std.Trim(first,last)+clip.video.std.Trim(last+1,len(v)-1)
"""

## custom filter that will be applied on the range defined duringthe ApplyRange call.
## so we will be able to subtitle a part of the video in the range first to last
def range_sub(clip:vs.VideoNode, subfile:str) -> vs.VideoNode:
    v=TextSub(subfile,clip)
    return v

Register("range_sub", range_sub)
        
clip.video=ApplyRange(clip.video, first, last ,  "range_sub", {"clip":clip.video, "subfile":subfile} )


AudioDub(clip.video,clip.audio)

   



    

