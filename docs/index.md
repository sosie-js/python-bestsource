# The python Bestsource helper

The audio support in vapoursynth has always been a piece of puzzle with headache
to compile plugins on linux . Till now was based on bestaudio plugin and lsmas. 
The new comer [bestsource](https://github.com/vapoursynth/bestsource) changes the horizon but its integration and doc are not clear.


## Motivations

I just needed to be able to trim videos with audio with vapoursynth avoiding
to encode video with ffmpeg. This topic is not new and [started far far 
ago on Doom9 forums](https://forum.doom9.org/showthread.php?t=184300).

## Demo


![Demo live](https://sosie-js.github.io/python-bestsource/screenshot.png)


## Dev and contributions

Have a look on my repository on github [python-bestsource](https://github.com/sosie-js/python-bestsource)

## vapoursynth plugins on linux

I recommend to use script [hybrid vapourynth addon](https://github.com/Selur/hybrid-vapoursynth-addon) from Selur to compile lsmas, bestsource, wwxd. A big talk on porting vapoursynth plugins on linux [can be found here](https://github.com/vapoursynth/vapoursynth/issues/1064)

## Installation 

It requires a working vapoursynth env, and at least version 1.7.0 of [peagisub](https://github.com/sosie-js/peagisub-vs) for vapoursynth plugins path configuration.

I use [scite](https://scintilla.org/SciTE.html) , a lightweight editor to trigger vspreview by pressing [F5] (or compile) after adding the /etc/scite/vapoursynth.properties

```
# Define SciTE settings for Vapoursynth Python files.

file.patterns.vpy=*.vpy
file.patterns.scons=SConstruct;SConscript

*source.patterns.vapoursynth=$(file.patterns.vpy);

shbang.vapoursynth=vpy

filter.vapoursynh=Python (vpy pyw)|$(file.patterns.vpy)|

*filter.vapoursynth=$(filter.vapoursynth)

lexer.$(file.patterns.vpy)=python
lexer.$(file.patterns.scons)=python

*language.vapoursynth=Pytho&n|vpy||

keywordclass.vapoursynth=False None True and as assert break class continue \
def del elif else except finally for from global if import in is lambda \
nonlocal not or pass raise return try while with yield

# Extra keywords for cython
keywordclass.cython=cdef cimport cpdef

keywords.$(file.patterns.py)=$(keywordclass.vapoursynth) $(keywordclass.cython)
keywords.$(file.patterns.scons)=$(keywordclass.vapoursynth)

# If you uncomment the 3 lines below,
# and put some words after "keywordclass2.python=",
# those words will be styled by style.python.14

#keywordclass2.python=
#keywords2.$(file.patterns.py)=$(keywordclass2.python)
#keywords2.$(file.patterns.scons)=$(keywordclass2.python)

# Use 2 sets of substyles to highlight standard library modules and
# imports from the future.
# Additional identifier sets can be added by incrementing the  next
# line's value and adding extra definitions similar to below.
substyles.vapoursynth.11=2

substylewords.11.1.$(file.patterns.py)=\
__main__ _dummy_thread _thread abc aifc argparse \
array ast asynchat asyncio asyncore atexit audioop \
base64 bdb binascii binhex bisect builtins bz2 \
calendar cgi cgitb chunk cmath cmd code codecs \
codeop collections colorsys compileall concurrent \
configparser contextlib copy copyreg crypt csv \
ctypes curses datetime dbm decimal difflib dis \
distutils dummy_threading email ensurepip enum \
errno faulthandler fcntl filecmp fileinput fnmatch \
formatter fpectl fractions ftplib functools gc getopt \
getpass gettext glob grp gzip hashlib heapq hmac \
html http http imaplib imghdr importlib inspect io \
ipaddress itertools json keyword linecache locale \
logging lzma macpath mailbox mailcap marshal math \
mimetypes mmap modulefinder msilib msvcrt \
multiprocessing netrc nis nntplib numbers operator \
os os ossaudiodev parser pathlib pdb pickle \
pickletools pipes pkgutil platform plistlib poplib posix \
pprint pty pwd py_compile pyclbr queue quopri \
random re readline reprlib resource rlcompleter runpy \
sched select selectors shelve shlex shutil signal site \
smtpd smtplib sndhdr socket socketserver spwd \
sqlite3 ssl stat statistics string stringprep struct \
subprocess sunau symbol symtable sys sysconfig \
syslog tabnanny tarfile telnetlib tempfile termios \
textwrap threading time timeit tkinter token \
tokenize trace traceback tracemalloc tty turtle \
types unicodedata unittest urllib uu uuid venv warnings \
wave weakref webbrowser winreg winsound wsgiref \
xdrlib xml xmlrpc zipfile zipimport zlib
style.python.11.1=fore:#DD9900

substylewords.11.2.$(file.patterns.vpy)=__future__ \
with_statement unicode_literals print_function
style.vapoursynth.11.2=fore:#EE00AA,italics

#~ statement.indent.$(file.patterns.py)=10 :
statement.indent.$(file.patterns.vpy)=5 class def elif else except finally \
for if try while with

statement.lookback.$(file.patterns.vpy)=0
block.start.$(file.patterns.vpy)=
block.end.$(file.patterns.vpy)=

view.indentation.examine.*.vpy=2

tab.timmy.whinge.level=1

#fold.quotes.python=1

comment.block.vapoursynth=#~

indent.vapoursynth.colon=1

# Python styles
# White space
style.vapoursynth.0=fore:#808080
# Comment
style.vapoursynth.1=fore:#007F00,$(font.comment)
# Number
style.vapoursynth.2=fore:#007F7F
# String
style.vapoursynth.3=fore:#7F007F,$(font.monospace)
# Single quoted string
style.vapoursynth.4=fore:#7F007F,$(font.monospace)
# Keyword
style.vapoursynth.5=fore:#00007F,bold
# Triple quotes
style.vapoursynth.6=fore:#7F0000
# Triple double quotes
style.vapoursynth.7=fore:#7F0000
# Class name definition
style.vapoursynth.8=fore:#0000FF,bold
# Function or method name definition
style.vapoursynth.9=fore:#007F7F,bold
# Operators
style.vapousynth.10=bold
# Identifiers
style.vapoursynth.11=
# Comment-blocks
style.vapoursynth.12=fore:#7F7F7F
# End of line where string is not closed
style.vapoursynth.13=fore:#000000,$(font.monospace),back:#E0C0E0,eolfilled
# Highlighted identifiers
style.vapoursynth.14=fore:#407090
# Decorators
style.vapoursynth.15=fore:#805000
# F-String
style.vapoursynth.16=fore:#7F007F,$(font.monospace)
# Single quoted f-string
style.vapoursynth.17=fore:#7F007F,$(font.monospace)
# Triple quoted f-string
style.vapoursynth.18=fore:#7F0000
# Triple double quoted f-string
style.vapoursynth.19=fore:#7F0000
# Matched Operators
style.vapoursynth.34=fore:#0000FF,bold
style.vapoursynth.35=fore:#FF0000,bold
# Braces are only matched in operator style
braces.vapoursynth.style=10

if PLAT_WIN
	vapoursynth.command=vspreview
if PLAT_GTK
	vapoursynth.command=vspreview
if PLAT_MAC
	vapoursynth.command=vspreview

if PLAT_WIN
	command.go.*.vpy=$(vapoursynth.command) "$(FileNameExt)"
	command.go.subsystem.*.vpy=1
	command.build.SConscript=scons.bat --up .
	command.build.SConstruct=scons.bat .

if PLAT_GTK
	command.go.*.vpy=$(vapoursynth.command) "$(FileNameExt)"
	command.build.SConscript=scons --up .
	command.build.SConstruct=scons .

if PLAT_MAC
	command.go.*.vpy=$(vapoursynth.command) "$(FileNameExt)"
	command.build.SConscript=scons --up .
	command.build.SConstruct=scons .

command.name.1.$(file.patterns.vpy)=Compile
command.1.$(file.patterns.vpy)=$(python.command) "$(FilePath)"
```



