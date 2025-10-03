import faster_whisper
import ffmpeg
import json
import math
from moviepy.editor import *
from mutagen.mp3 import MP3
import os
import random
from text_to_audio import get_tts_info, text_to_speech
import time

settings_filename = "E:/Desk/Programming/portfolio-projects/ai-content-creator/data/settings.json"
shorts_folder = "E:/Desk/Programming/portfolio-projects/ai-content-creator/data/bg-footage/Shorts/"
long_form_folder = "E:/Desk/Programming/portfolio-projects/ai-content-creator/data/bg-footage/Long-Form/"

audio_file = "E:/Desk/Programming/portfolio-projects/ai-content-creator/data/audio.mp3"
vid_file = "E:/Desk/Programming/portfolio-projects/ai-content-creator/data/vid.mp4"
final_vid = "E:/Desk/Programming/portfolio-projects/ai-content-creator/data/video.mp4"
vid_name = "vid"

sub_file = f"portfolio-projects/ai-content-creator/data/sub-{vid_name}.en.srt"

def get_bg_footage(status=None):
    if status:
        status.config(text="Getting Background Footage")

    with open(settings_filename, "r") as f:
        data = json.load(f)

        vid_fmt = data["Video Format"]

    if vid_fmt == "Shorts":
        bg_vid = shorts_folder + random.choice(os.listdir(shorts_folder))
    else:
        bg_vid = long_form_folder + random.choice(os.listdir(long_form_folder))

    mp3_len = MP3("E:/Desk/Programming/portfolio-projects/ai-content-creator/data/audio.mp3")
    mp3_len = float(mp3_len.info.length)

    mp4_len = float(get_mp4_len(bg_vid))

    # Get Clip from Background Footage
    start = round(random.uniform(0, mp4_len - mp3_len), 2)
    end = round(start+mp3_len, 2)
    bgclip = VideoFileClip(bg_vid).subclipped(start, end)
    audioclip = AudioFileClip(audio_file)
    time.sleep(1)

    if status:
        status.config(text="Creating video from Background Footage")
    
    new_audioclip = CompositeAudioClip([audioclip])
    bgclip.audio = new_audioclip
    bgclip.write_videofile(vid_file, threads=8, preset="ultrafast")

async def generate(status):
    text, voice = get_tts_info(status)
    await (text_to_speech(text, voice, status))

    get_bg_footage(status)
    get_subs(status)

def get_mp4_len(filename):
    clip = VideoFileClip(filename)
    duration = clip.duration
    return duration

def get_subs(status):
    segments = transcribe(audio_file, status)
    sub_file = generate_subtitle_file(segments)
    add_subtitle_to_vid(sub_file, status)

def transcribe(audio, status=None):
    if status:
        status.config(text="Transcribing mp3 file")
    
    model = faster_whisper.WhisperModel("small", device="cpu", cpu_threads=8, compute_type="int8")
    segments, info = model.transcribe(audio, beam_size=1)

    return list(segments)

def format_time(secs):
    hours = math.floor(secs / 3600)
    secs %= 3600

    minutes = math.floor(secs / 60)
    secs %= 60

    milliseconds = round((secs - math.floor(secs)) * 1000)
    secs = math.floor(secs)

    formatted_time = f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
    return formatted_time

def generate_subtitle_file(segments):
    subtitle_file = sub_file
    text = ""

    for index, segment in enumerate(segments):
        segment_start = format_time(segment.start)
        segment_end = format_time(segment.end)

        text += f"{str(index+1)}\n"
        text += f"{segment_start} --> {segment_end}\n"
        text += f"{segment.text}\n"
        text += "\n"
    
    with open(subtitle_file, "w") as f:
        f.write(text)

    return subtitle_file

def add_subtitle_to_vid(subtitle_file, status):
    if status:
        status.config(text="Adding subtitles to video")
    
    print(f"Subtitle file path: {subtitle_file}")
    print(f"File exists: {os.path.exists(subtitle_file)}")

    vid_stream = ffmpeg.input(vid_file)
    output_vid = final_vid

    stream = ffmpeg.output(vid_stream, output_vid,
                           vf=f"subtitles={subtitle_file}")
    ffmpeg.run(stream, overwrite_output=True)

if __name__ == "__main__":
    if os.path.exists(vid_file):
        os.remove(vid_file)

    if os.path.exists(sub_file):
        os.remove(sub_file)
