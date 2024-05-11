import sys
import re
import subprocess
import platform
import os
import time
import html
import json

import httpx
import fzf
from bs4 import BeautifulSoup as bs

plt = platform.system()
username = os.getenv('username') if plt == 'Windows' else os.getlogin()
config_path = os.path.join(os.path.expanduser(f'~{username}'), '.config', 'yt-music', 'config.json')

if os.path.exists(config_path):
    with open(config_path) as f:
        config = json.load(f)
        use_rpc = config['RPC']
else:
    use_rpc = "false"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
}


if use_rpc == "true":
    from pypresence import Presence
    start = int(time.time())
    client_id = "1075791459409723472"
    RPC = Presence(client_id)
    RPC.connect()

client = httpx.Client(headers=headers, timeout=None)

base_url = "https://vid.puffyan.us"
pattern = r'<a.*?href="/watch\?v=(.*?)".*?><p.*?>(.*?)<\/p></a>'
channel_name_pattern = r'<span id="channel-name">(.*?)</span>'

MPV_EXECUTABLE = "mpv"

try:
    if len(sys.argv) == 1:
        query = input("Search: ")
        if query == "":
            print("ValueError: no query parameter provided")
            exit(1)
    else:
        query = " ".join(sys.argv[1:])
except KeyboardInterrupt:
    exit(0)

query = query.replace(' ', '+')
opts = []


def get_channel(video_id):
    resp = client.get(f"https://vid.puffyan.us/watch?v={video_id}")
    html_content = resp.text
    soup = bs(html_content, 'html.parser')
    channel_names = re.findall(channel_name_pattern, html_content)

    for name in channel_names:
        print(name.strip())
        get_channel.artist = name.strip()


def extract_video_id(video_title):
    match = re.search(r' - ([\w-]+)$', video_title)
    
    #match = re.search(pattern, video_title)
    
    if match:
        video_id = match.group(1)
        get_channel(video_id)
        return video_id
    else:
        print("no video id found")
        exit(1)

def determine_path() -> str:
    
    if plt == "Windows":
        return f"C:\\Users\\{os.getenv('username')}\\Downloads"
    
    elif (plt == "Linux"):
        return f"/home/{os.getlogin()}/Downloads"
    
    elif (plt == "Darwin"):
        return f"/Users/{os.getlogin()}/Downloads"

    else:
        print("[!] Make an issue for your OS.")
        exit(0)

def download(video_id, video_title):
    
    path: str = determine_path()
    video_title = video_title.replace(' ', '_')

    subprocess.call(f"yt-dlp -x \"https://music.youtube.com/watch?v={video_id}\" -o \"{path}/{video_title}\"", shell=True)



def play_loop(video_id, video_title):
   
    if use_rpc == "true":
        RPC.update(
            large_image = f"http://img.youtube.com/vi/{video_id}/0.jpg",
            large_text = "haha checkmate spotify plebs",
            small_image = "youtube_music_icon_svg",
            small_text = f"yt-music",
            start = start,
            details = f"{video_title} - loop",
            state = f"by {get_channel.artist}",
            buttons = [{"label": "Play on YouTube Music", "url": f"https://music.youtube.com/watch?v={video_id}"}],
        )

    args = [
        MPV_EXECUTABLE,
        f"https://music.youtube.com/watch?v={video_id}",
        f"--force-media-title={video_title}",
        "--no-video",
        "--loop",
    ]

    mpv_process = subprocess.Popen(args, stdout=subprocess.DEVNULL)
    mpv_process.wait()



def play(video_id, video_title):
   
    if use_rpc == "true":
        RPC.update(
            large_image = f"http://img.youtube.com/vi/{video_id}/0.jpg",
            large_text = "haha checkmate spotify plebs",
            small_image = "youtube_music_icon_svg",
            small_text = f"yt-music",
            start = start,
            details = f"{video_title}",
            state = f"by {get_channel.artist}",
            buttons = [{"label": "Play on YouTube Music", "url": f"https://music.youtube.com/watch?v={video_id}"}],
        )

    args = [
        MPV_EXECUTABLE,
        f"https://music.youtube.com/watch?v={video_id}",
        f"--force-media-title={video_title}",
        "--no-video",
    ]

    mpv_process = subprocess.Popen(args, stdout=subprocess.DEVNULL)
    mpv_process.wait()


def main():
    fetch = client.get(f"{base_url}/search?q={query}")
    matches = re.findall(pattern, fetch.text)
    for match in matches:
        video_id,  title = match
        title = html.unescape(title)
        opt = f"{title} - {video_id}"
        opts.append(opt)
    ch = fzf.fzf_prompt(opts)
    print(ch)
    idx = extract_video_id(ch)
    play_ch = fzf.fzf_prompt(["play", "loop", "download"])
    try:
        if play_ch == "play":
            play(idx, ch)
        elif play_ch == "loop":
            play_loop(idx, ch)
        elif play_ch == "download":
            download(idx, ch)
        else:
            print("[!] Nothing selected.")
            exit(1)
    except KeyboardInterrupt:
        exit(0)

main()
