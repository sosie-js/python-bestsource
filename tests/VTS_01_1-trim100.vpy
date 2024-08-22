import vapoursynth as vs
from vapoursynth import core
from bssource.bssource import BSSource,Trim, Audio, Video, AudioDub, TextSub, ApplyRange, Register, Filter, CurrentClip

input=r'VTS_01_1-00.00.00.000-00.00.17.818.VOB'

#clip=BSSource(input)
BSSource(input)

clip=Trim(0,100)

AudioDub(clip.video,clip.audio)

   



    

