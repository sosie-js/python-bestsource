

import os
import sys

#Needed to calculate duration
from calc import calc 

import vapoursynth as vs

#equivalent of core = vs.core for .py
#core = vs.get_core() for .vpy
from vapoursynth import core


aegi_vscache: str = ""
aegi_vsplugins: str = "/usr/local/vapoursynth"

plugin_extension = ".dll" if os.name == "nt" else ".so"
if sys.platform == "darwin": plugin_extension = ".dylib"

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
    
    

import subprocess


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
    

#http://www.vapoursynth.com/doc/pythonreference.html#VideoNode.fps
def get_fps_from_vsplugin(videofile):
    fps=0
    video=VSPSource(videofile)
    
    #print(video)
    #plugins=core.plugins()
    #import web_pdb; web_pdb.set_trace()
    
    if(not video is None): #Anny retrival method succeed         
        fps= str(video.fps) #fraction to string
        #print(fps)
        
    return fps
    
#ffprobe -show_streams -select_streams v -v quiet video.mp4 | grep "duration=" | cut -d '=' -f 2    
    
def get_video_duration_from_vsplugin(videofile, method='?'):
    duration=0
   #import web_pdb; web_pdb.set_trace()
    video, audio=VSPSource(videofile,method)
    
    #print(video)
    #plugins=core.plugins()
   
    
    if(not video is None): # retrival method succeed         
        duration= video.num_frames/float(video.fps) #fraction to string
        #print(fps)
        
    return duration
    
def get_audio_duration_from_vsplugin(videofile, method='?'):
    duration=0
   #import web_pdb; web_pdb.set_trace()
    video=VSPSource(videofile,method)
    
    #print(video)
    #plugins=core.plugins()
   
    
    if(not video is None): # retrival method succeed         
        duration= video.num_frames/float(video.fps) #fraction to string
        #print(fps)
        
    return duration
    
method=""
    
def get_method():
     global method
     return method
     
### PUBLIC access
def has_audio():
    global has_audio
    return has_audio

def VSPSource(videofile,wished_method="?") :

    global method
    global has_audio
    has_audio=False
    
    if ".avs" in videofile:
        try:
            ensure_plugin("avisource", "AVISource", "")
            video = core.avisource.AVISource(videofile, audio=false)
            method="avisource"
            return video
        except AttributeError:
            pass
        except vs.Error:
            pass
            
    try:
        if(wished_method != "?" and wished_method !="bs"):
            raise AttributeError("Skip")
        ensure_plugin("bs", "bestsource", "")
        video = core.bs.VideoSource(videofile) 
        method="bestsource"
    except AttributeError or vs.Error:
        try:
            if(wished_method != "?" and wished_method !="lsmas"):
                raise AttributeError("Skip")
            ensure_plugin("lsmas", "libvslsmashsource", "")
            video = core.lsmas.LWLibavSource(videofile) 
            method="lsmas"
        except AttributeError or vs.Error:
            try:
                if(wished_method != "?" and wished_method !="ffms2"):
                    raise AttributeError("Skip")
                ensure_plugin("ffms2", "ffms2", "")
                video=core.ffms2.Source(videofile)
                method="ffms2"
            except AttributeError:
                raise vs.Error("VSPSource : all methods failed!")
                
    try:
        audio=vs.core.bs.AudioSource(source=videofile)
        has_audio=True
    except AttributeError:
        pass
    except vs.Error:
        pass
    #print("VSPSource("+method+")")        
    return video, audio


#will be retrieved from video_file specified in  the ass file
#by get_fps_from_source
fps_ratio='?' 

def get_fps():
    global fps_ratio
    return fps_ratio
    
def get_duration_from_vspipe(video_file):
    """
    get duration using vspipe info and a vpy plugin wrapper
    """

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
          "load_video-ok.vpy",
          "--arg",'source='+video_file
        ]
        
    vspipe_init = subprocess.Popen(cmd, stdout=open(os.devnull, "w"))
    vspipe_init.wait()
    
    vspipe = subprocess.Popen(cmd, stdout=subprocess.PIPE)   
    
    #Helper to extract trimed value without newline
    trim_value=(lambda v: v.decode('utf-8').split(" ")[1].strip() )
    
    #'Width: 720\n'
    Width = vspipe.stdout.readline()
    #'Height: 480\n'
    Height = vspipe.stdout.readline()
    #'Frames: 145778\n'
    Frames = vspipe.stdout.readline()
    Frames = trim_value(Frames)
    # FPS: 30000/1001 (29.970 fps)\n
    FPS = vspipe.stdout.readline()
    FPS = trim_value(FPS)
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
    
    #Now the calculation of the death
    return calc.eval( "round((("+Frames +' - 1)/ ('+ FPS+")),3)")
    
    
def  get_duration_from_source(source, method='?'):
    if ".vpy" in source:
        return  get_duration_from_vspipe(source)
    else:
        return  get_video_duration_from_vsplugin(source, method)
    
def get_fps_from_source(source): 
    
    global fps_ratio
    
    #import web_pdb; web_pdb.set_trace()
    method=0
    if not os.path.exists(source):
        sys.stderr.write("ERROR(get_fps): filename %r was not found!" % (source,))
    else:
        if(".vpy" in source or ".VPY" in source): #vspipe info way
            fps_ratio=get_fps_from_vspipe(source)
            method=1
        elif ".avs" in source:#ffprobe way
            fps_ratio=get_fps_from_ffprobe(source)
            #fps_ratio=get_fps_from_vsplugin(source)
            method=2
        else: #from vs plugin such as bestsource, lsmas, ffms2, 
            fps_ratio=get_fps_from_vsplugin(source)
            method=3
            
   #print("get_fps("+source+") with method#"+str(method)+" gives "+fps_ratio)
    
    return fps_ratio
    
 
    
if __name__ == "__main__":
    source="VTS_01_1-00.00.00.000-00.00.17.818.VOB"
    print(get_duration_from_source(source))