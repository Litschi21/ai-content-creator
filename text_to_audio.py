import asyncio
import edge_tts
import json
from reddit_fetch import fetch_posts

settings_filename = "E:/Desk/Programming/portfolio-projects/ai-content-creator/data/settings.json"

def get_tts_info(status=None):
    voices = {
    "en-AU-NatashaNeural": "Female",
    "en-AU-WilliamMultilingualNeural": "Male",
    "en-CA-ClaraNeural": "Female",
    "en-CA-LiamNeural": "Male",
    "en-GB-MaisieNeural": "Female",
    "en-GB-RyanNeural": "Male",
    "en-IE-EmilyNeural": "Female",
    "en-IE-ConnorNeural": "Male",
    "en-US-JennyNeural": "Female",
    "en-US-RogerNeural": "Male"
    }

    final_voice = None
    for voice, gender in voices.items():
        if voice.startswith(accent_to_voice.get(accent)):
            if gender == voice_gender:
                final_voice = voice

    comments, descriptions, titles = fetch_posts(status)

    if not final_voice:
        final_voice = "en-US-RogerNeural"
        print(f"No voice found for {accent} {voice_gender}, using default: {final_voice}")

    post = None
    posts = []
    for i in range(max(len(comments), len(descriptions), len(titles))):
        if len(titles) > 1 and len(titles) > i:
            post = f"Post {i+1}\n" + titles[i]

        if len(descriptions) > i:
            if post:
                post += "\n" + descriptions[i]
            else:
                post = descriptions[i]

        if len(comments) > i:
            if post:
                post += f"Comment {i+1}\n" + comments[i]
            else:
                post = f"Comment {i+1}\n" + comments[i]
        posts.append(post)
        post = None

    text = titles[0] + "\n" + "\n\n\n".join(posts)
    print(text)
    print(f"Length: {len(text)}")

    split_text = text.split(" ")
    for i, word in enumerate(split_text):
        if word in abbreviations.keys():
            split_text[i] = abbreviations.get(word)

    text = " ".join(split_text)
    return text, final_voice

async def text_to_speech(text, voice, status=None):
    filename = "E:/Desk/Programming/portfolio-projects/ai-content-creator/data/audio.mp3"

    if status:
        status.config(text="Creating mp3 file")

    speech = edge_tts.Communicate(text, voice=voice)
    await speech.save(filename)

abbreviations = {
    "AITA": "Am I the Asshole",
    "TIL": "Today I learned",
    "AIO": "Am I Overreacting",
    "idk": "I don\"t know",
    "idc": "I don\"t care",
    "idgaf": "I don\"t give a fuck",
    "brb": "be right back",
    "btw": "by the way",
    "imo": "in my opinion",
    "imho": "in my humble opinion",
    "fyi": "for your information",
    "tbh": "to be honest",
    "omg": "oh my god",
    "np": "no problem",
    "nvm": "never mind",
    "wfh": "work from home",
    "wth": "what the hell",
    "afaik": "as far as I know",
    "asap": "as soon as possible",
    "atm": "at the moment",
    "dm": "direct message",
    "jk": "just kidding",
    "msg": "message",
    "yw": "you\"re welcome"
}

accent = "American"
voice_gender = "Male"

try:
    with open(settings_filename, "r") as f:
        data = json.load(f)

        voice_accent = data["Voice Accent"]
        voice_gender = data["Voice Gender"]
except FileNotFoundError:
    print("\nSettings not found. Open control panel and change settings if needed.\n")

accent_to_voice = {
    "American": "en-US",
    "Australian": "en-AU",
    "British": "en-GB",
    "Canadian": "en-CA",
    "Irish": "en-IE"
}

if __name__ == "__main__":
    text, voice = get_tts_info()
    asyncio.run(text_to_speech(text, voice))
