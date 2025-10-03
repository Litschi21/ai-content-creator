# ai-content-creator
This project's use is generating video content, in both short- and longform videos, using Reddit posts from a variety of subreddits.

## Description
This AI content creator uses tkinter for a user-friendly interface, then fetches Reddit posts from a picked subreddits (with many
more options as well), then generates an mp3 file using that text, then it transcribes that mp3 file to create the subtitles with
ffmpeg and moviepy. Finally, it combines Minecraft background footage with the subtitles to create a finalized mp4 file. It's use
is mostly to help with quick content generation, making use of Reddit's API and various other tools.

## Getting Started
### Dependencies
The dependencies are all written out in the requirements.txt file and can be imported easily using `pip install requirements.txt`.
You should have Python 3.x and above. OS does not matter, although this was designed on Windows 10/11, so it might not work on
other OS systems.

### Installing
You can download my program by downloading all of the files and installing the dependencies as detailed above. You should enter
your own folder using the tkinter GUI or leave it empty if you would like this folder to be the current working directory.
You do not need to make any modifications to folders, but make sure the folders are mostly empty and/or do not contain any possibly
conflicting files such as "video.mp4" or "audio.mp3".
You can execute the program simply by running the `control_panel.py` file and entering your given settings (these will be saved in
`settings.json`) and then pressing the "Generate" button in the "Generation" tab.
If you need any help, please refer to this repo's discussion page.

### Authors
Project Manager: Litschi
Team Lead: Litschi
Computer Programmer: Litschi
Tester: Litschi

### License
This project is licensed under the [MIT] License - see the LICENSE.md file for details

### Acknowledgments
Thanks to ChatGPT for debugging help and YouTube/Google for needed tutorials on ffmpeg and moviepy.
