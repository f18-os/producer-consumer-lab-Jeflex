# Phillip Hassoun's Threading Lab
### From Dr.Freudenthals OS class

[Contribution file for this project](./CONTRIBUTING.md)
#### This program will create 3 threads that will each have it's own task in processing a video. Extract, Convert to greyscale, and display, implemented with a Producer Consumer algorithm.
**Running the program**
> Run MultiThreadPC.py, ensure you run as sudo!
```
sudo python3 ./MultiThreadPC.py
```
Notice the output inside the shell. of each thread operating independently.

**Changing the Clip**
If you want to change the clip you're processing you'll need to change some variables.
>Open source file MultiThreadPC.py, here we use atom as our text editor.
```
atom MultiThreadPC.py
```
Change line 12
```
# filename of clip to load
filename = 'YOURCLIP.mp4'
```
Be mindful of clips to convert. Supported video formats are currently .mp4
