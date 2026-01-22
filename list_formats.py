import yt_dlp
import os

url = "https://www.youtube.com/shorts/5GqfmmAQhQw"

ydl_opts = {
    'nocheckcertificate': True,
    'listformats': True,
}

print("Listing formats...")
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.extract_info(url, download=False)
