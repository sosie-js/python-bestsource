"""
File name: bssource.py
Author: sosie-js / github 
Created: 22.08.2024
Version: 1.2
Thanks to: Arch1t3cht for aegisub-vs.py code parts of this are inspired from https://github.com/arch1t3cht/Aegisub/
                _AI_ for the Clip class I extended from https://forum.doom9.org/showthread.php?t=184300
                myrsloik that suggested clamping in https://github.com/vapoursynth/vapoursynth/issues/1084
Usage: 
1)Create a test.vpy script like:
-------------------8<-------Start-------------------------------------------------------
import vapoursynth as vs
from vapoursynth import core
from bssource import BSSource,Trim, AudioDub

input=r'VTS_08_1.VOB'

#clip=BSSource(input)
BSSource(input)

clip=Trim(0,500)+Trim(501,2000)

#AudioDub() if no trim
AudioDub(clip.video,clip.audio)
------------------8<-----------End-------------------------------------------------------------
2) Install the vapoursynth setting for scite  
3) Load the script in scite and press [F5] it will trigger vspreview test.py and rendre result 

Description: Briging Trim facility like in avisynth to vapoursynth bestource
"""


import vapoursynth as vs
from vapoursynth import core
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple, Callable

DUMP_TRIM=False

def DumpTrim(choice):
    global DUMP_TRIM
    DUMP_TRIM=choice


import logging, os, sys
#if logging.getLogger().level <= logging.DEBUG:
      
#vs.core.log_message(vs.MESSAGE_TYPE_DEBUG, 'hello there')

#### Fetch configuration and configure paths ################################

"""
File name: aegisub-vs.py
Author: sosie-js / github 
Created: 17.08.2024
Version: 1.7
Description: Bridge to vapoursynth using lua config helper 
peagisub (luarocks install --local peagisub-vs 1.7.0)
"""

from dataclasses import dataclass, field
import os, sys

import pexpect
import subprocess
import shlex


"""
 Wrapper to run a peagisub command 
 cmd: str  command to append to peagisub call 
"""
def run_peagisub(cmd:str):
   result=subprocess.run(shlex.split('peagisub '+cmd), capture_output=True)
   return result.stdout.decode('utf-8').replace('\n','')

"""
 Wrapper to run a lua command with luarocks env available
 name : str  name of the variable 
"""
def vsvar(name : str):
   if  name=="UserPluginDir":
       return run_peagisub('--userplugin')
   elif name=="SystemPluginDir":
       return run_peagisub('--systemplugin')
   else:
       return  run_peagisub('--'+name)


aegi_vscache: str = vsvar("cache")
aegi_vsplugins: str = vsvar("UserPluginDir")

plugin_extension = ".dll" if os.name == "nt" else ".so"
if sys.platform == "darwin": plugin_extension = ".dylib"

def set_paths(vars: dict):
    """
    Initialize the wrapper library with the given configuration directories.
    Should usually be called at the start of the default script as
        set_paths(globals())
    """
    global aegi_vscache
    global aegi_vsplugins
    aegi_vscache = vars["__aegi_vscache"]
    aegi_vsplugins = vars["__aegi_vsplugins"]


def ensure_plugin(name: str, loadname: str, errormsg: str):
    """
    Ensures that the VapourSynth plugin with the given name exists.
    If it doesn't, it tries to load it from `loadname`.
    If that fails, it raises an error with the given error message.
    """
    if hasattr(core, name):
        return

    if aegi_vsplugins and loadname:
        try:
            core.std.LoadPlugin(os.path.join(aegi_vsplugins, loadname + plugin_extension))
            if hasattr(core, name):
                return
        except vs.Error:
            pass

    raise vs.Error(errormsg)




## A super class to get sound and video synchronized , bestsource version to replace
## outdated LibavSMASHSource + basaudio 
## Adapted from Clip Class of _AI_ https://forum.doom9.org/showthread.php?t=184300
"""
from vapoursynth import core
#video = core.lsmas.LibavSMASHSource('video.mp4')
#audio = core.bas.Source('video.mp4')
#clip = Clip(video, audio)
clip = BSSource('video.mp4')
clip = clip[0] + clip[20:1001] + clip[1500:2000] + clip[2500:]
#or same trimming calling trim method:
clip = clip.trim(first=0, length=1) + clip.trim(firt=20, last=1000) + clip.trim(1500, length=500) + clip.trim(2500)
clip = clip*2
clip = clip + clip
#clip.video.set_output(0)
#clip.audio.set_output(1)
AudioDub(clip.video,clip.audio)
"""

@dataclass 
class Clip:    
    def __init__(self, video = None, audio=None, attribute_audio_path=None,force_audio=True):
        self.video = video  ## http://www.vapoursynth.com/doc/pythonreference.html#VideoNode
        self.audio = audio ## http://www.vapoursynth.com/doc/pythonreference.html#AudioNode
        if self.video is None:
            self.video = core.std.BlankClip()
        
        self.debug=False
        self.first=0
        self.last=len(self.video)-1
        self.afirst=None
        self.alast=None
        self.alength=None
        
        self.filters= {}
        
        if self.audio is None and force_audio:
            if attribute_audio_path is None:
                raise ValueError('argument attribute_audio_path is needed to get default audio for images (could be a really short video')
            attr_audio = core.bas.Source(attribute_audio_path)
            length = int(attr_audio.sample_rate/self.video.fps*self.video.num_frames)
            self.audio = attr_audio.std.BlankAudio(length=length)


    def register(self, method, function):
        self.filters[method] = function

    def _AudioTrim(self,  **kwargs):
        """
        Clamp to the end version to solver AudioTrim: last sample beyond clip end
        return self.audio.std.AudioTrim(first=afirst,last=alast,length=alength) produces sometimes
        """
        for key, value in kwargs.items():
            ##print(f"{key}: {value}")
            if key=='first' :
                afirst=value
            if key == 'last':
                alast=value
            if key == 'length':
                alength =value
        
        if(alast  is not None and alast > (len(self.audio)-1)):
            alast=len(self.audio)-1
            #keep a track of the clamping for dump
            self.alast=alast

        return self.audio.std.AudioTrim(first=afirst,last=alast,length=alength)


    def trim(self, first=0, last=None, length=None):
    
        global DUMP_TRIM
    
        afirst  = self.to_samples(first)    if first  is not None else None
        alast   = self.to_samples(last+1)-1 if last   is not None else None
        alength = self.to_samples(length)   if length is not None else None
        clip=Clip( self.video.std.Trim(first=first, last=last, length=length),
                     self._AudioTrim(first=afirst,last=alast,length=alength)
                    )
                    
        if DUMP_TRIM:
            #Keep a track
            clip.set_first(first)
            clip.set_last(last)
            clip.afirst=afirst
            clip.alast=alast
            clip.alength=alength
            return clip.dump()
        else:
            return clip
            
    def format(self):
        return self.video.format
        
    def width(self):
        return self.video.width
   
    def height(self):
        return self.video.height
                    
    def num_frames(self):
        return self.video.num_frames
    
    def to_samples(self, frame):
        return int((self.audio.sample_rate/self.video.fps)*frame)
        
    def duration(self):
        duration = 0
        if(not self.video is None): # retrieval method succeed         
            duration= self.video.num_frames/float(self.video.fps) #fraction to string
        return duration
        
    def log_info(self, message):
        vs.core.log_message(vs.MESSAGE_TYPE_INFORMATION, message)               
        
    def log_debug(self, message):
        vs.core.log_message(vs.MESSAGE_TYPE_DEBUG, message)       
        
    def sample_rate(self):
        asr=0
        if(not self.audio is None): #retrieval method succeed         
            asr= str(self.audio.sample_rate) 
        return asr    
        
    def fps(self):
        fps=0
        if(not self.video is None): #retrieval method succeed         
            fps= str(self.video.fps) #fraction to string
        return fps
        
    def set_first(self, val):
        self.first=val
    
    def set_last(self, val):
        self.last=val
    
    def dump(self):
        
        # Filter
        def dump_view(n: int, f: vs.VideoFrame,
                             clip: vs.VideoNode, first : int, last: int)  -> vs.VideoNode:
                       
           # if(n <50) :
                v=clip #core.text.ClipInfo(clip)
                 
                infos=[]
                 
                infos.append(str(first)+"<="+str(n+first)+"<="+str(last))
                  
                for prop, prop_value in self.info().items():
                    infos.append(prop+"="+str(prop_value))
                    
                v=core.text.Text(v,  "\n".join(infos), alignment=9, scale=1) 
                return v
            #else:
            #    return  core.text.FrameNum(clip)
            
        from functools import partial
        self.video = self.video.std.FrameEval(partial(dump_view, clip=self.video,first=self.first, last=self.last), prop_src=self.video)
        
        return self
    
    
    def clip_info(self, alignment=7, scale=1):
        self.video=core.text.ClipInfo(self.video, alignment, scale)
        
    def core_info(self, alignment=7, scale=1):
        self.video=core.text.CoreInfo(self.video, alignment, scale)
    
    def text(self,text, alignment=7, scale=1):   
        self.video=core.text.Text(self.video, text,  alignment, scale)
        
    def frame_num(self, alignment=7, scale=1):   
        self.video=core.text.FrameNum(self.video, alignment, scale)
        
    def frame_props(self, alignment=7, scale=1):   
        self.video=core.text.FrameProps(self.video,  alignment, scale)
        
    def info(self,video_file="",what="*",method="vspipe"):
        
        info ={}
        if video_file == "" :
            ##http://www.vapoursynth.com/doc/pythonreference.html#VideoNode
            info["width"] = self.width()
            info["height"] = self.height()
            info["num_frames"] = self.num_frames()
            info["fps"] = self.fps()
            
            info["video_first"]=self.first
            info["video_last"]=self.last
            info["audio_first"]=self.afirst
            info["audio_last"]=self.alast
            info["audio_length"]=self.alength
            
        else:
            if what=="fps" and method =="ffprobe" :
                """
                get fps using ffprobe method
                """        
                out = subprocess.check_output(["ffprobe",video_file,"-v","0","-of","csv=p=0","-select_streams","v:0","-show_entries","stream=r_frame_rate"])
                rate = out.decode()[0:-1] #get rid of \n
                if len(rate.split('/'))==2:
                    return rate
                return "0"
            
            
            #print(video_file)
            # initialize the script
            # http://www.vapoursynth.com/doc/output.html#options
            # import web_pdb; web_pdb.set_trace()
            if ".vpy" in video_file:
                cmd=[
                  "vspipe",
                  "--info",
                  str(video_file)
                ]
            else:
                cmd=[
                  "vspipe",
                  "--info",
                  "bssource.py",#"load_video-ok.vpy",
                  "--arg",'source='+video_file
                ]
                
            vspipe_init = subprocess.Popen(cmd, stdout=open(os.devnull, "w"))
            vspipe_init.wait()
            
            vspipe = subprocess.Popen(cmd, stdout=subprocess.PIPE)   
            
            #Helper to extract trimed value without newline
            trim_value=(lambda v: v.decode('utf-8').split(" ")[1].strip() )
            
            #'Width: 720\n'
            Width = vspipe.stdout.readline()
            Width=trim_value(Width)
            info["width"] = Width
            if what == "width":
                return Width 

            #'Height: 480\n'
            Height = vspipe.stdout.readline()
            Height = trim_value(Height)
            info["height"] = Height
            if what == "height":
                return Height 

            #'Frames: 145778\n'
            Frames = vspipe.stdout.readline()
            Frames = trim_value(Frames)
            info["num_frames"] = Frames
            if what == "num_frames":
                return Frames

            # FPS: 30000/1001 (29.970 fps)\n
            FPS = vspipe.stdout.readline()
            FPS = trim_value(FPS)
            info["fps"] = FPS
            if what == "fps":
                return  FPS

            #'Format Name: YUV420P8\n'
            Format_Name = vspipe.stdout.readline()
            Format_Name = trim_value(Format_Name)
            info["format"] = Format_Name 
            if what == "format":
                return   Format_Name

            #'Color Family: YUV\n'
            Color_Family = vspipe.stdout.readline()
            Color_Family = trim_value(Color_Family)
            info["color"] = Color_Family
            if what == "color":  
                return Color_Family

            #Alpha: No\n'
            Alpha = vspipe.stdout.readline()
            Alpha = trim_value(Alpha)
            info["alpha"] = Alpha 
            if what == "alpha":  
                return Alpha

            #'Sample Type: Integer\n'
            Sample_Type= vspipe.stdout.readline()
            Sample_Type = trim_value(Sample_Type)
            info["sample_type"] = Sample_Type

            #'SubSampling W: 1\n'
            SubSampling_W= vspipe.stdout.readline()
            SubSampling_W = trim_value(SubSampling_W)
            info["sample_width"] = SubSampling_W

            #'SubSampling H: 1\n'
            SubSampling_H = vspipe.stdout.readline()
            SubSampling_H = trim_value(SubSampling_H)
            info["sample_height"] = SubSampling_H

            #Now the calculation of the death
            from calc import calc
            Duration=calc.eval( "round((("+Frames +' - 1)/ ('+ FPS+")),3)")
            info["duration"] = Duration
            if what == "duration":  
                return Duration

        return info

    def __add__(self, other):
        return Clip(self.video + other.video, self.audio + other.audio)

    def __mul__(self, multiple):
        return Clip(self.video*multiple, self.audio*multiple)

    def __getitem__(self, val):
        if isinstance(val, slice):
            if val.step is not None:
                raise ValueError('Using steps while slicing AudioNode together with VideoNode makes no sense')
            start = self.to_samples(val.start) if val.start is not None else None
            stop =  self.to_samples(val.stop)  if val.stop  is not None else None
            return Clip( self.video.__getitem__(val),
                         self.audio.__getitem__(slice(start,stop))
                         )
        elif isinstance(val, int):
            start = self.to_samples(val)
            stop = int(start + self.audio.sample_rate/self.video.fps)
            return Clip( self.video[val],
                         self.audio.__getitem__(slice(start,stop))
                         )        
    def __repr__(self):
        return '{}\n{}\n{}'.format('Clip():\n-------', repr(self.video), repr(self.audio))

    def __str__(self):
        return '{}\n{}\n{}'.format('Clip():\n-------', str(self.video), str(self.audio))

__clip__=None


##################################
## @ source - filepath to video (having audio or not)
## @ atrack  - audio track number. Default auto. If -2, ignore audio.
## @ vtrack - video track fnumber. Default auto.
##
##
def BSSource(source:str, **kwargs: Any):

    global __clip__
    atrack = kwargs["atrack"] if "atrack" in kwargs else -1
    vtrack = kwargs["vtrack"] if "vtrack" in kwargs else -1
      
    loadnames= {"bestsource": "bs","libvslsmashsource":"lsmas", "ffms2": "ffms2"}
  
    video = None
    for loadname in  loadnames.keys():
        ns = loadnames[loadname]
        try:
            ensure_plugin(ns, loadname, "Plugin "+ loadname+" can not be found or loaded from "+os.path.join(aegi_vsplugins, loadname + plugin_extension))
            if ".avs" in source:
                if loadname =="AVISource":
                    video = core.avisource.AVISource(source, audio=false)
                    break
            else:
                if loadname == "bestsource":
                    video =  core.bs.VideoSource(source=source, track = vtrack)
                    break
                if loadname == "libvslsmashsource":
                    video = core.lsmas.LWLibavSource(source) 
                    break
                if loadname == "ffms2":
                    video=core.ffms2.Source(source)
                    break              
        except vs.Error:
            pass
        
    has_audio=False
    if (atrack==-2) :
       clip = Clip(video)
    else:
        try:
            audio=vs.core.bs.AudioSource(source=source, **kwargs)
            has_audio=True
        except AttributeError:
            pass
        except vs.Error:
            pass
        if has_audio:
            clip = Clip(video, audio)
        else:
            clip = Clip(video,None,None, False)
            
    __clip__=clip
    return clip

def AudioDub(video=None, audio=None):
    global __clip__
    if video is None and audio is None:
        __clip__.video.set_output(0)
        __clip__.audio.set_output(1)
    else:
        if  isinstance(video,Clip):
            clip = video
            clip.video.set_output(0)
            if audio is None:
                clip.video.set_output(0)
        else:
            video.set_output(0)
            audio.set_output(1)

##### Probe stuf :  get_fps_from_source,  get_duration_from_source ###########################


def  get_duration_from_source(source):
   
    if ".vpy" in source:
        #use vspipe info way, we use a fake video just to access to the info method
        video=core.std.BlankClip()
        clip = Clip(video,None,None, False)
        return   clip.info(video_file=source,what="duration",method="vspipe")
    else:
        return  BSSource(source).duration()
    
def get_fps_from_source(source,method="vsplugin"): 
    video=core.std.BlankClip()
    clip = Clip(video,None,None, False)
    if ".vpy" in source:
        return   clip.info(video_file=source,what="fps",method="vspipe")
    elif method =="ffprobe":
        return   clip.info(video_file=source,what="fps",method="ffprobe")
    else:
        return BSSource(source).fps()

################# HELPERS ##############################

def CurrentClip():
    global __clip__
    return __clip__

def Trim(start,end):
    global __clip__
    return __clip__.trim(first=start, last=end)
    
    
def TextSub( subfile, clip=None,first=None, last=None ):
    global __clip__
   
    if clip is None:
        #__clip__.video=vs.core.assrender.TextSub(__clip__.video,subfile)
        __clip__.video=TextSub( subfile, __clip__.video, first, last)
        return __clip__
    else:
        if type(clip) is Clip:
            #vs.core.assrender.TextSub(clip.video,subfile
            clip.video=TextSub( subfile, clip.video, first, last)
            return clip
        elif type(clip) is vs.VideoNode:
            video=clip
            if first is None and last is None:
                try:
                    return vs.core.assrender.TextSub(video,subfile)
                except vs.Error:
                    raise ValueError(subfile)
            else:
                if last is None:
                    last= len(video)-1
                if first is None:
                    first=0
                
                def range_view(n: int, f: vs.VideoFrame,
                     clip: vs.VideoNode, first : int, last: int)  -> vs.VideoNode:
                           
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
                return video.std.FrameEval(partial(range_view, clip=video,first=first, last=last), prop_src=video)
                
### ApplyRange mimic stuff##     

"""
Register a filter by its name and function body
str name: filter name
function : should match def function () 
"""
def Register(name,function):
    global __clip__
    __clip__.register(name,function)
    
"""
Retrieve filter function using filter name previeoisly registered
returns function
"""
def Filter(name):
    global __clip__
    return __clip__.filters[name]
    
"""
clip:Clip|vs.VideoNode|None If None use current active Clip
start_frame:int start frame to apply Filter
end_frame:int end frame to apply Filter
filtername: a registered filter see Register(name, function)
args:Dict a list with args to pass to the filter
return the same type of clip but with the filter applied from start_frame to end_frame
"""
def ApplyRange (clip, start_frame:int, end_frame:int, filtername:str, args: Dict):
    global __clip__
    first=start_frame
    last=end_frame
    if clip is None:
        __clip__.video=ApplyRange (__clip__.video, start_frame, end_frame, filtername, args)
        return __clip__
    else:
        if type(clip) is Clip:
            return  ApplyRange (clip.video, start_frame, end_frame, filtername, args)
        elif type(clip) is vs.VideoNode:
            if filtername not in __clip__.filters:
                 raise NotImplementedError("Method %s not implemented" % filtername)
            filter=Filter(filtername)
            v=filter(**args)
           
            return  clip.std.Trim(first=0, last=first-1)+v.std.Trim(first,last)+clip.std.Trim(last+1,len(v)-1)
            
###############


def Video(clip=None):
    global __clip__
    return __clip__.video if clip is None else clip.video
    
def Audio(clip=None):
    global __clip__
    return __clip__.audio if clip is None else clip.audio
    
def generate(clip: vs.VideoNode, script_name: str):
    """Generates keyframe VSEdit bookmark file.
    some of this stolen from kageru's generate_keyframes
    (https://github.com/Irrational-Encoding-Wizardry/kagefunc)
    :param clip: input clip
        :bit depth: ANY
        :color family: ANY
        :float precision: ANY
        :sample type: ANY
        :subsampling: ANY
    :param script_name: name of VSEdit script with no extension
        i.e. editing 'script.vpy' --> 'script'
    """
    script_name += '.vpy.bookmarks'

    # speed up the analysis by resizing first
    clip = core.resize.Bilinear(clip, 640, 360)
    clip = core.wwxd.WWXD(clip)
    kf = '0'
    for i in range(1, clip.num_frames):
        if clip.get_frame(i).props.Scenechange == 1:
            kf += ", %d" % i

    text_file = open(script_name, "w")
    text_file.write(kf)
    text_file.close()

#core.avs.LoadPlugin(r"B:\Avisynth plugins\GuavaComb.dll")
if __name__ == "__main__":
    source="/media/pi/Nouveau/9_PING_ENGLISH/VIDEO_TS/out/9_PING_ENGLISH_1g_1.vpy"
    print(get_duration_from_source(source))
    print(get_fps_from_source(source))
    #print(get_fps_from_source(source,"ffprobe"))
else:
    #if __name__ == "__vapoursynth__":
    if "source" in globals():
        src=globals()["source"]
        clip=BSSource(src)
        clip.video.set_output(0)
        clip.audio.set_output(1)
    

    
