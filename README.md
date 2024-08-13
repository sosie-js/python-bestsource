# <img src="https://github.com/sosie-js/python-bestsource/raw/main/icons/pythondia.png" alt="logo" width="32"> python-bestsource

[![Python](https://img.shields.io/badge/Python%20-any-blue)](https://www.python.org/)

A library helper for producing and manipulating videos with audio support in vapoursynth using [bestsource](https://github.com/vapoursynth/bestsource)

## Current state

Sound is working with vspreview as soon as Track1 is selected in the Playback sub panel hidden by default and play is triggered
for a video that has sound and has not been trimmed. I provide a test video in test/ and two examples scripts

### trim.vpy: 

Shows how trim is handled with video that has sound - the player I used is a forked vspreview 0.7.1 
to fix bug in main/window.py that has been handled in new version of vspreview. Easy answer from authors 
is you upgrade your python version due to requirement in one dependency vstools to have the fix done 
with new versions of vspreview. 

>The choice for authors of vspreview not wanting to fix broken old versions for reason of time
>and efficiency,  not taking account current shipped version of Ubuntu claiming fixes has been done 
>with recent versions. Howvever this means focrcing everybody to upgrade python to make it work - 
>this choice exludes however normal ubuntu end users stalled with python 3.10.
>Refusing contributions and  considering everyone is working in a developper destop env 
>is another thing that does not allow arrogance as a group of developpers a place to insult others. 

For now what we can expect is from this: player stalling and sound goes outside boundaries when you insists
on resuming play. It may have bee fixed in latest release of vspreview.
>It is not quite clear that it comes from vspreview as the trim part is still experimental and
>when I trimed to the length of video making normally the video untouched, the audio problems arise.

### frame.vpy

Show frame props of a clip different ways. Under scite you can trigger vspreview with [F5]
or compile - In test I let you the scite config file. Both works fine for a non trimed video. 

## Installation

as local user

```shell
pip3 install -U python-bssource
```

for all

```shell
sudo pip3 install python-bssource
```


For those who want to bridge to [arch1tech's aegisub fork](https://github.com/arch1t3cht/Aegisub/tree/vapoursynth), use my lua helper [peagisub](https://github.com/sosie-js/peagisub-vs) to get the path of the vapoursynth plugin needed by aegisub_vs.py. 


## Limitations / Considerations

I for now wondering if the userplugin path should be aegisub vapoursynth directory ?data/vapoursynth where bestsource should be installed like in windows letting the system plugin only core plugins. I have to stabilize plugin generation script before and make vspreview working ..I get annoyed lately by env stuff to make vspreview happy with python.

## History


**1.0.0** - First release


## Contributing

Feel free to add other object and fixes.

## Development

### Compile .egg

```shell
$ ./package.sh
```

### Upload to PyPI

1. Create an API Token from the Web UI. (Edit your `~/.pypirc` with the generated token.)
2. Install Twine
```shell
$ python3 -m pip install --user --upgrade twine
```
3. Upload the bundle
```shell
$ python3 -m twine upload dist/*
```

Note: The upload to PyPI is currently assured by GitHub Actions.


### Release

1. Increase the version number in `setup.py`.
2. Commit and push.
3. Create a new tag in GitHub to trigger the CI pipeline.

