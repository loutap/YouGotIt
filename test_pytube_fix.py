from pytube import YouTube
import pytube.innertube

# Monkeypatching pytube to fix HTTP 400 Error
# Force usage of WEB client
original_init = pytube.innertube.InnerTube.__init__

def new_init(self, client='ANDROID_MUSIC', use_oauth=False, allow_cache=True):
   client = 'MWEB' 
   original_init(self, client=client, use_oauth=use_oauth, allow_cache=allow_cache)

pytube.innertube.InnerTube.__init__ = new_init

try:
    # A generic, safe video (Big Buck Bunny or similar, or just a popular music video)
    url = "https://www.youtube.com/watch?v=aqz-KE-bpKQ" 
    yt = YouTube(url)
    print(f"Title: {yt.title}")
    stream = yt.streams.first()
    print("Stream found")
except Exception as e:
    print(f"Error: {e}")
