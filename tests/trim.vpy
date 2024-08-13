import vapoursynth as vs
from vapoursynth import core
from bssource import BSSource,Trim, AudioDub, CurrentClip, DumpTrim

input=r'VTS_01_1-00.00.00.000-00.00.17.818.VOB'

#clip=BSSource(input)
BSSource(input)

if __name__ == "__main__":
    print("The whole clip has:\n")
    clip=CurrentClip()
    print("Duration (s):"+clip.duration())
    print("Frames Per Second:"+clip.fps())
    print("Clip Info:"+clip.info())
else:
    #Enable the right left panel with custom dump
    DumpTrim(True)
    
    #Now do an equivalent to Trim(0,100) in two pieces,(100-0+1)=(50-0+1)+(100-51+1)=Clip with 101 frames
    clip=Trim(0,50)+Trim(51,100)
    
    #AudioDub() if no trim
    AudioDub(clip.video,clip.audio)
