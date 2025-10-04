# ai-content-creator
Automatically generate videos by converting Reddit posts into AI-narrated videos with background gameplay.

## Description
- User-friendly GUI using tkinter
- Fetch Reddit Posts from chosen subreddit using API
- Generate mp3 file using edge-tts
- Transcribe using OpenAI's faster-whisper
- Burn subtitles into background footage with ffmpeg and moviepy

## Getting Started

### Dependencies
- Python 3.8+ (recommended).
- [FFmpeg](https://ffmpeg.org/download.html) must be installed and added to PATH.
- Python packages listed in requirements.txt: `pip install -r requirements.txt`
- Download bg footage at [this](https://drive.google.com/drive/folders/1r6vmfbwchYi-t-6i1qfPk_6XSZWY_u3X?usp=drive_link) Google Drive link.

Additionally, you need to create Reddit API credentials and enter it into the `Reddit Info` section in the settings tab.
This will require a client id, a client secret, and a user agent. A user agent can be any string, but it should follow some
basic formatting and should mention the name of what you're using as well as your Reddit account name (formatted as `r/userx`).
To get the client id and client secret you need to do as follows:
  1. Head to [this](https://www.reddit.com/prefs/apps) link and click "create an app" (or create another app if you already have one).
  2. Input the name of the application into the "name" field and mark the "script" box.
  3. Enter a short description of your app (not necessary, but recommended).
  4. For the redirect uri (not URL!) you should just enter `https://localhost` or use a website to contact you (twitter, own website, etc.)
  5. Complete the captcha and click "Create App"

For additional information, refer to [Reddit's API documentation](https://www.reddit.com/dev/api/).


### Installing
You can download my program by downloading all of the files and installing the dependencies as detailed above. You should enter
your own folder using the tkinter GUI or leave it empty if you would like this folder to be the current working directory.
You do not need to make any modifications to folders, but make sure the folders are mostly empty and/or do not contain any possibly
conflicting files such as "video.mp4" or "audio.mp3".
You can execute the program simply by running the `control_panel.py` file and entering your given settings (these will be saved in
`settings.json`) and then pressing the "Generate" button in the "Generation" tab.
If you need any help, please refer to this repo's discussion page.

### Settings
After installation, you can configure the following settings:
- Subreddit (AmItheAsshole, AmIOverreacting, confession, entitledparents, EntitledPeople, maliciouscompliance, relationship_advice, and unpopularopinion for longform and AskReddit, dadjokes, jokes, and Showerthoughts for shorts)
- Voice Gender (male/female)
- Voice Accent (American/British/Canadian/Irish/Australian)
- Amount of comments picked (0 - 25 for shorts, 0 - 100 for longform)
- Amount of posts picked (1 - 10 for shorts, 1 - 100 for longform)
- Output folder for video, audio files and `settings.json`
- Reddit API credentials

### License
This project is licensed under the [MIT] License - see the LICENSE.md file for details

### Acknowledgments
Thanks to ChatGPT/Claude for debugging help and YouTube/Google for needed tutorials on ffmpeg and moviepy.
