from pytube import YouTube

try:
    # A generic, safe video (Big Buck Bunny or similar, or just a popular music video)
    url = "https://www.youtube.com/watch?v=aqz-KE-bpKQ" 
    yt = YouTube(url)
    print(f"Title: {yt.title}")
    stream = yt.streams.first()
    print("Stream found")
except Exception as e:
    print(f"Error: {e}")
