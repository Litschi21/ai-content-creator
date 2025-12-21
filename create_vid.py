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

def get_bg_footage(settings_filename, shorts_folder, long_form_folder, audio_file, vid_file, filename, status=None):
    if status:
        status.config(text="Getting Background Footage")

    with open(settings_filename, "r") as f:
        data = json.load(f)

        vid_fmt = data["Video Format"]

    if vid_fmt == "Shorts":
        bg_vid = shorts_folder + random.choice(os.listdir(shorts_folder))
    else:
        bg_vid = long_form_folder + random.choice(os.listdir(long_form_folder))

    mp3_len = MP3(filename + "audio.mp3")
    mp3_len = float(mp3_len.info.length)

    mp4_len = float(get_mp4_len(bg_vid))

    # Get Clip from Background Footage
    start = round(random.uniform(0, mp4_len - mp3_len), 2)
    end = round(start+mp3_len, 2)
    bgclip = VideoFileClip(bg_vid).subclip(start, end)
    audioclip = AudioFileClip(audio_file)
    time.sleep(1)

    if status:
        status.config(text="Creating video from Background Footage")
    
    new_audioclip = CompositeAudioClip([audioclip])
    bgclip.audio = new_audioclip
    bgclip.write_videofile(vid_file, threads=8, preset="ultrafast")

async def generate(status, client_id, client_secret, user_agent, filename):
    settings_filename = filename + "settings.json"
    shorts_folder = filename + "bg-footage/Shorts/"

    long_form_folder = filename + "bg-footage/Long-Form/"

    audio_file = filename + "audio.mp3"
    vid_file = "vid.mp4"
    final_vid = "video.mp4"
    vid_name = "vid"

    sub_file = f"sub-{vid_name}.en.srt"

    text, voice = get_tts_info(client_id, client_secret, user_agent, status)
    if text and voice:
        await (text_to_speech(text, voice, status))

        get_bg_footage(settings_filename, shorts_folder, long_form_folder, audio_file, vid_file, filename, status)
        get_subs(status, audio_file, sub_file, final_vid, vid_file)
    else:
        return

def get_mp4_len(filename):
    clip = VideoFileClip(filename)
    duration = clip.duration
    return duration

def get_subs(status, audio_file, sub_file, final_vid, vid_file):
    segments = transcribe(audio_file, status)
    sub_file = generate_subtitle_file(segments, sub_file)
    add_subtitle_to_vid(sub_file, status, final_vid, vid_file)

def transcribe(audio, status=None):
    if status:
        status.config(text="Transcribing mp3 file")
    
    model = faster_whisper.WhisperModel("small", device="cpu", cpu_threads=8, compute_type="int8")
    segments, _ = model.transcribe(audio, beam_size=1)

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

def generate_subtitle_file(segments, sub_file):
    text = ""

    for index, segment in enumerate(segments):
        segment_start = format_time(segment.start)
        segment_end = format_time(segment.end)

        text += f"{str(index+1)}\n"
        text += f"{segment_start} --> {segment_end}\n"
        text += f"{segment.text}\n"
        text += "\n"
    
    with open(sub_file, "w") as f:
        f.write(text)

    return sub_file

def add_subtitle_to_vid(subtitle_file, status, final_vid, vid_file):
    if status:
        status.config(text="Adding subtitles to video")
    
    print(f"Subtitle file path: {subtitle_file}")
    print(f"File exists: {os.path.exists(subtitle_file)}")

    vid_stream = ffmpeg.input(vid_file)
    output_vid = final_vid

    stream = ffmpeg.output(vid_stream, output_vid,
                           vf=f"subtitles={subtitle_file}")
    ffmpeg.run(stream, overwrite_output=True)
