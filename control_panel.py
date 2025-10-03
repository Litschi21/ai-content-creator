import asyncio
from create_vid import generate
import json
import os
import threading
import tkinter as tk
from tkinter import ttk
import traceback

state = {
    "current_status": "Ready",
    "subreddit": "AskReddit",
    "vid_format": "Shorts",
    "voice_gender": "Male",
    "voice_accent": "American",
    "post_amt": 1,
    "comment_amt": 0,
    "comment_to": 10,
    "post_to": 10
}


class ControlPanel(tk.Tk):
    def __init__(self):
        # Initialize Tkinter Window
        super().__init__()
        self.title("Control Panel")
        self.geometry("800x600")

        # Define Settings Tab vars
        self.settings_pady = (10, 0)

        self.short_subreddits = ["AskReddit", "dadjokes", "Jokes", "Showerthoughts"]
        self.long_subreddits = ["AmItheAsshole", "AmIOverreacting", "confession", "entitledparents", "EntitledPeople", "maliciouscompliance", "relationship_advice", "unpopularopinion"]
        self.subreddits = self.short_subreddits + self.long_subreddits
        self.default_sub = self.short_subreddits[0]

        self.video_formats = ["Shorts", "Long Form"]
        self.voice_genders = ["Male", "Female"]
        self.voice_accents = ["American", "British", "Canadian", "Irish", "Australian"]

        # Notebook Tabs
        self.tabControl = ttk.Notebook(self)
        self.g_tab = ttk.Frame(self.tabControl)
        self.settings_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.g_tab, text="Generation")
        self.tabControl.add(self.settings_tab, text="Settings")
        self.tabControl.pack(expand=1, fill="both")

        # Settings
        self.filename = "E:/Desk/Programming/portfolio-projects/ai-content-creator/data/settings.json"
        self.settings = self.load_settings()

        # Tkinter vars
        self.sub_opt = tk.StringVar(value=self.settings["Subreddit"])
        self.format_opt = tk.StringVar(value=self.settings["Video Format"])
        self.gender_opt = tk.StringVar(value=self.settings["Voice Gender"])
        self.accent_opt = tk.StringVar(value=self.settings["Voice Accent"])
        self.v1 = tk.DoubleVar(value=self.settings["Comment Amount"])
        self.v2 = tk.DoubleVar(value=self.settings["Post Amount"])
        self.v3 = tk.DoubleVar(value=self.settings["Video Count"])

        # Build tabs
        self.build_generation_tab()
        self.build_settings_tab()
    
    def build_generation_tab(self):
        self.g_btn = ttk.Button(self.g_tab, text="Generate and Upload", command=self.generate_vid)
        self.status = ttk.Label(self.g_tab, text=self.settings["Status"])

        self.g_btn.pack()
        self.status.pack()
    
    def build_settings_tab(self):
        sub_dropdown = tk.OptionMenu(self.settings_tab, self.sub_opt, *self.subreddits, command=self.get_sub)
        sub_label = ttk.Label(self.settings_tab, text="Subreddit")
        sub_label.pack(pady=self.settings_pady)
        sub_dropdown.pack()

        video_format = tk.OptionMenu(self.settings_tab, self.format_opt, *self.video_formats, command=self.get_vid_format)
        video_format.configure(state="disabled")
        vid_format_label = ttk.Label(self.settings_tab, text="Video Format")
        vid_format_label.pack(pady=self.settings_pady)
        video_format.pack()

        gender = tk.OptionMenu(self.settings_tab, self.gender_opt, *self.voice_genders, command=self.get_voice_gender)
        voice_gender_label = ttk.Label(self.settings_tab, text="Voice Gender")
        voice_gender_label.pack(pady=self.settings_pady)
        gender.pack()

        accent = tk.OptionMenu(self.settings_tab, self.accent_opt, *self.voice_accents, command=self.get_voice_accent)
        voice_accent_label = ttk.Label(self.settings_tab, text="Voice Accent")
        voice_accent_label.pack(pady=self.settings_pady)
        accent.pack()

        if self.format_opt.get() == "Shorts":
            comment_to = 10
            post_to = 10
        elif self.format_opt.get() == "Long Form":
            comment_to = 50
            post_to = 100

        self.comment_slider = tk.Scale(self.settings_tab, variable=self.v1, from_=0, to=comment_to, orient="horizontal", command=self.get_comment_amt)
        self.post_slider = tk.Scale(self.settings_tab, variable=self.v2, from_=1, to=post_to, orient="horizontal", command=self.get_post_amt)
        save_btn = tk.Button(self.settings_tab, text="Save Settings", command=self.save_settings)

        comment_label = ttk.Label(self.settings_tab, text="Comment Amount")
        comment_label.pack(pady=self.settings_pady)
        self.comment_slider.pack()

        post_label = ttk.Label(self.settings_tab, text="Post Amount")
        post_label.pack(pady=self.settings_pady)
        self.post_slider.pack()
        save_btn.pack()

    def load_settings(self):
        if not os.path.exists(self.filename):
            data = {
                "Status": "Ready",
                "Subreddit": self.short_subreddits[0],
                "Video Format": self.video_formats[0],
                "Voice Gender": self.voice_genders[0],
                "Voice Accent": self.voice_accents[0],
                "Comment Amount": 0,
                "Post Amount": 1,
                "Video Count": 0
            }
            with open(self.filename, 'w+') as f:
                json.dump(data, f, indent=4)
            return data
        else:
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except json.decoder.JSONDecodeError:
                print(traceback.format_exc())

    def save_settings(self):
        data = {
            "Status": self.status.cget("text"),
            "Subreddit": self.sub_opt.get(),
            "Video Format": self.format_opt.get(),
            "Voice Gender": self.gender_opt.get(),
            "Voice Accent": self.accent_opt.get(),
            "Comment Amount": int(self.v1.get()),
            "Post Amount": int(self.v2.get()),
            "Video Count": int(self.v3.get())
        }
        with open(self.filename, 'w+') as f:
            json.dump(data, f, indent=4)
        
        print(f"Settings saved.\n")
    
    def generate_vid(self):
        if self.status.cget("text") == "Ready" or self.status.cget("text") == "Generation complete.":
            def run_generation():
                try:
                    state.update({
                        "current_status": self.status,
                        "subreddit": self.sub_opt.get(),
                        "vid_format": self.format_opt.get(),
                        "voice_gender": self.gender_opt.get(),
                        "voice_accent": self.accent_opt.get(),
                        "comment_amt": int(self.v1.get()),
                        "post_amt": int(self.v2.get())
                    })

                    asyncio.run(generate(self.status))

                    self.status.after(0, lambda: self.status.config(text="Generation complete."))
                    self.after(3000, lambda: self.status.config(text="Ready"))
                except Exception as e:
                    self.status.after(0, lambda: self.status.config(text=f"Error: {str(e)}"))
                    print(traceback.format_exc())

            threading.Thread(target=run_generation, daemon=True).start()

    def get_status(self):
        state["current_status"] = self.status

    def get_sub(self, sub_name):
        if sub_name in self.short_subreddits:
            state["vid_format"] = "Shorts"
            state["comment_to"], state["post_to"] = 10, 10
        else:
            state["vid_format"] = "Long Form"
            state["comment_to"], state["post_to"] = 50, 100
        
        self.format_opt.set(state["vid_format"])
        self.comment_slider.config(to=state["comment_to"])
        self.post_slider.config(to=state["post_to"])
        state["subreddit"] = sub_name

    def get_vid_format(self, fmt):
        state["vid_format"] = fmt

    def get_voice_gender(self, gender):
        state["voice_gender"] = gender

    def get_voice_accent(self, accent):
        state["voice_accent"] = accent

    def get_comment_amt(self, amt):
        state["comment_amt"] = int(amt)

    def get_post_amt(self, amt):
        state["post_amt"] = int(amt)
    
    def get_vid_count(self, amt):
        state['vid_count'] = int(amt)
    
    def run(self):
        self.mainloop()

print(state)
