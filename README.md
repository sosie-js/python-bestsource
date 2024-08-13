# <img src="https://github.com/sosie-js/python-bssource/blob/1.0.0/icons/python-bssource.png?raw=true" alt="logo" width="32"> python-bssource

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

The choice for authors of vspreview not wanting to fix broken old versions for reason of time
and efficiency, claiming fixes has been done with recent versions is understable. 
>However, this means forcing everybody to upgrade python to the latest release to make it work 
>this requirement exludes normal ubuntu end users stalled with python 3.10. 
>Python support does not follow such a rule and let two precedent version open. 

In addition refusing contributions and considering everyone is working in a developper 
destop env is another thing 
>Normally, this does not allow arrogance as a group of developpers a place to insult 
>others and trigger ban first to show their superiority and then dicussion.

For now what we can expect is from this: player stalling and sound goes outside boundaries when you insists
on resuming play. It may have bee fixed in latest release of vspreview.
>It is not quite clear that it comes from vspreview as the trim part is still experimental and
>when I trimed to the length of video making normally the video untouched, the audio problems arise.

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

