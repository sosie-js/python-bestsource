

"""
#~/.local/lib/python3.10/site-packages/ffmpeg
#pip3 install python-ffmpeg
from ffmpeg import FFmpeg, FFmpegFileNotFound, FFmpegInvalidCommand
import subprocess
from ffmpeg import Progress

ffmpeg_cmd =None

def ffmpeg_full(input):
    global ffmpeg_cmd 
    ffmpeg_cmd = (
        FFmpeg()
        .option("y")
        .input(input)
        .output(
            "pipe:1",
            f="null"
        )
    )
    
    @ffmpeg_cmd.on("progress")
    def on_progress(progress: Progress):
        print(progress,  flush=True)

    @ffmpeg_cmd.on("completed")
    def on_completed():
        stdout=subprocess.PIPE
        print(stdout.readline(),  flush=True)
        import web_pdb; web_pdb.set_trace()
        print("completed",  flush=True)

    @ffmpeg_cmd.on("terminated")
    def on_terminated():
        print("terminated", flush=True)
    try:
        ret=ffmpeg_cmd.execute()
        print(ret)
    except FFmpegFileNotFound as exception:
        print("An exception has been occurred!")
        print("- Message from ffmpeg:", exception.message)
        print("- Arguments to execute ffmpeg:", exception.arguments)

#print("ffmpeg -i "+input+" -f null -")
ffmpeg_full(file)
"""


import os
import time
import subprocess

import sys
from subprocess import PIPE, Popen
from threading  import Thread

import re
from datetime import timedelta
from typing import IO, Any, Iterable

#from ffmpeg import types
from calc import calc


def parse_time(time: str) -> timedelta:
    
    match = re.search(r"(-?\d+):(\d+):(\d+)\.(\d+)", time)
    assert match is not None
   # print('Time to decode in seconds:"'+str(match[0])+'"')
    return timedelta(
        hours=int(match.group(1)),
        minutes=int(match.group(2)),
        seconds=int(match.group(3)),
        milliseconds=int(match.group(4)) * 10,
    )

#https://trac.ffmpeg.org/wiki/FFprobeTips#Getdurationbydecoding

try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty  # python 2.x

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def ffmpeg_full(input):
    ON_POSIX = 'posix' in sys.builtin_module_names
    cmd= ["ffmpeg", "-i", input, "-f",  "null","-" ]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1, close_fds=ON_POSIX, text=True)
    q = Queue()
    t = Thread(target=enqueue_output, args=(p.stderr, q))
    t.daemon = True # thread dies with the program
    t.start()

    # ... do other things here
    
    break_on_next=False
    while True:
        # read line without blocking
        try:  
            line = q.get_nowait() # or q.get(timeout=.1)
        except Empty:
            pass #print('no output yet')
        else: # got line
            if  break_on_next:
                break
            if "out#" in line:
                break_on_next=True
            
    p.terminate()
    return line
   
def framecount_from(duration, fps):
    return "Frames (calc with duration "+str(duration)+"):"+ str(calc.eval( "round("+str(duration) +" * ("+str(fps)+"))"))


def ffmpeg_audio_extract_to_mem(input):
    ON_POSIX = 'posix' in sys.builtin_module_names
    cmd= ["ffmpeg", "-y" , "-i", input, "-vn", "-c:a", "copy", "-f",  "null","-" ]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1, close_fds=ON_POSIX, text=True)
  
    break_on_next=False
    while True:
        line = p.stderr.readline()
        #print("line", line)
        if line == '' and p.poll() is not None:
            break
        if line:
            if  break_on_next:
                break
            if "out#" in line:
                break_on_next=True   
        rc = p.poll()
    p.terminate()
    return line
