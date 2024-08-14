import vapoursynth as vs
from vapoursynth import core
from bssource.bssource import BSSource,Trim, Audio, Video, AudioDub

input=r'VTS_01_1-00.00.00.000-00.00.17.818.VOB'

#clip=BSSource(input)
BSSource(input)

clip=Trim(0,100)

from pprint import pprint
with open( "dump_audio_globals.txt" , "w" ) as fwrite:
    pprint(globals(), indent=2,stream=fwrite)

Audio(clip).set_output()

    
