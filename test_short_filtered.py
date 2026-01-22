import yt_dlp
import os

url = "https://www.youtube.com/shorts/5GqfmmAQhQw"
download_directory = "."

ydl_opts = {
    'outtmpl': os.path.join(download_directory, '%(title)s.%(ext)s'),
    'quiet': False, # Show output to see which format is picked
    'no_warnings': True,
    'nocheckcertificate': True,
    # Try to avoid m3u8 to see if it falls back to 18 or similar reliable format
    'format': 'best[protocol^=http]', 
}

print("Attempting download with protocol filter...")
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Download finished.")
except Exception as e:
    print(f"Error: {e}")
