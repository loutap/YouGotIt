import yt_dlp

def my_hook(d):
    if d['status'] == 'downloading':
        print(d['_percent_str'])

try:
    url = "https://www.youtube.com/watch?v=aqz-KE-bpKQ"
    ydl_opts = {
        'progress_hooks': [my_hook],
        'format': 'best[height<=720]',
        'nocheckcertificate': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(f"Title: {info['title']}")
        # ydl.download([url]) # Commented out to save bandwidth/time for now
        print("Test successful")
except Exception as e:
    print(f"Error: {e}")
