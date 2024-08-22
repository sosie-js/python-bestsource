# <img src="https://github.com/sosie-js/python-bssource/blob/1.2.0/icons/python-bssource.png?raw=true" alt="logo" width="32"> python-bestsource

[![Python](https://img.shields.io/badge/Python%20->=3.10-blue)](https://www.python.org/) ![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)  

A library helper for producing and manipulating videos with audio support in vapoursynth using [bestsource](https://github.com/vapoursynth/bestsource)

## Current state

Version 1.2 bring filter range support with both ApplyRange and FrameEval in TextSub  : a door to make Animations easier in vapoursynth is now open =)

Sound is working with vspreview as soon as Track1 is selected in the Playback sub panel hidden by default and play is triggered for a video that has sound. I provide a test video in test/ and two examples scripts

### trim.vpy: 

Shows how trim is handled with video that has sound - the player I used is a forked [release of vspreview 0.7.1 is available here](https://github.com/sosie-js/vs-preview/releases/tag/v0.7.1-ubuntu22.04) is for users using a [still supported python 3.10 version](https://pyreadiness.org/3.10/) as ubuntu 22.04 user, install it using the git way.

### frame.vpy

Show frame props of a clip different ways. Under scite you can trigger vspreview with [F5]
or compile - In test I let you the scite config file. 

### aegisub audio tests support in vapoursynth

This requires vapoursynth fork from Arch1t3cht and the use of [peagisub](https://github.com/sosie-js/peagisub-vs) 
for vapoursynth plugin dir configuration. Two subtitles files are provided (1+2) and a probe system (3):

(1) Open tests/VTS_01_1-trim100.ass 
then tests/VTS_01_1-trim100.vpy delivers video as channel 0 and audio as channel 1
this is not supported by current release that disable Open Audio from Video feature. 
>As I did not find a way to know which type of channel audio or video is requested.
>I opened thus a [Request for feature](https://github.com/arch1t3cht/Aegisub/issues/148)
Sound works fine in vspreview you can trigger with scite by opening tests/VTS_01_1-trim100.vpy and press [F5]
Note you will have no sound in vsedit (vapoursynth editor) for all the tests

(2) Open tests/VTS_01_1-trim100-video-audio.ass 
then tests/VTS_01_1-trim100-video.vpy delivers video  as channel 0 
then tests/VTS_01_1-trim100-audio.vpy delivers audio  as channel 0 (separately in time)
>this works if you ensure plays does not goes outside boundary ie frame 101
>else you will be flooded by popups. Play and seeking work fine and did not stall just before the end as in vspreview
>there is just a minor problem with the horizonthal zoom for audio

(3) Open tests/VTS_01_1-trim100-applyrange.ass 
then tests/VTS_01_1-trim100-applyrange.vpy is used for video
>This will show we have a portion from 50 to 60 of VTS_01_1-trim100.ass using a mimick AVS method ApplyRange

(4) Open tests/VTS_01_1-trim100-frameval.ass
then tests/VTS_01_1-trim100-frameval.vpy is used for video
>This will show we have a portion from 50 to 60 of VTS_01_1-trim100.ass most similar of AVS Animate, you can
grab the current frame number in the filter that ApplyRange do no handle. 

(5) Open tests/VTS_01_1-trim100-range.ass
then tests/VTS_01_1-trim100-frameval.vpy is used for video
then tests/VTS_01_1-trim100-audio.vpy is used to restrore sound
>This will show how to add a green mask from 50 to 60 in ASS

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

## History

**1.2.0** - ApplyRange and FrameEval samples in tests/
**1.1.0** - Trim with video that has audio works in both aegisub and vspreview!
**1.0.0** - First release


## Contributing

Feel free to add other object and fixes.

## Development

### Compile .whl

```shell
$ ./package.sh
```

### Upload to PyPI

1. Create an API Token from the Web UI. (Edit your `~/.pypirc` with the generated token.)
2. Install Twine
```shell
$ python3 -m pip install --user --upgrade twine
```
3. Build the wheel bundle (.egg no more recognized) 
```shell
$ sudo rm -rf dist/&sudo rm -rf build&sudo python3 setup.py bdist_wheel
```
4. Upload the bundle
```shell
$ python3 -m twine upload dist/*
```

Note: The upload to PyPI is currently assured by GitHub Actions.


### Release

1. Increase the version number in `setup.py`.
2. Commit and push.
3. Create a new tag in GitHub to trigger the CI pipeline.

