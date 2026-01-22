import yt_dlp
import os

url = "https://www.youtube.com/shorts/5GqfmmAQhQw"
download_directory = "."

ydl_opts = {
    'outtmpl': os.path.join(download_directory, '%(title)s.%(ext)s'),
    # 'quiet': True,
    # 'no_warnings': True,
    'nocheckcertificate': True,
    'format': 'best',
}

print("Attempting download...")
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Download finished.")
except Exception as e:
    print(f"Error: {e}")
