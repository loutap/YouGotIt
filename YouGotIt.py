import os
import customtkinter as ctk
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
import re

# Python app that lets you download a YourTube Video
# Developer: Lou Tapanes
# Date: 02/12/2024
Version = 'v1.5'

def sanitize_filename(filename):
    return re.sub(r'[\\\\/*?:\'"<>|]', '', filename)

# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Global variable to store the YouTube URL and selected directory
youtube_url = ""
selected_directory = ""
FileType = ".mp4"

# Create root window
root = ctk.CTk()
root.title('YouGotIt!')
root.geometry('720x650')

Titlelable = ctk.CTkLabel(root, text="YouGotIt!", font=("Helvetica", 44), text_color="#de626e" , fg_color="#2e2c2c")
Titlelable.pack(pady=5)
Titlelable2 = ctk.CTkLabel(root, text="Download any YouTube Video", font=("Verdana", 16), text_color="#afd5de" , fg_color="#2e2c2c")
Titlelable2.pack(pady=30)

dirlable = ctk.CTkLabel(root, text="", font=("Helvetica", 14))
dirlable.configure(text='Current download directory:')
dirlable.pack(pady=1)


# Create label to display selected directory path
dlPathLable = ctk.CTkLabel(root, text="", font=("Helvetica", 14))
dlPathLable.pack(pady=5)

selected_directory = "C:\\temp"
print(selected_directory)
dlPathLable.configure(text=selected_directory)

# Function to select directory
def select_directory():
    global selected_directory
    selected_directory = filedialog.askdirectory()  
    print(selected_directory)
    dlPathLable.configure(text=selected_directory)

# Create button to select directory
button = ctk.CTkButton(root, text="Change Download Directory", command=select_directory)
button.pack(pady=10)


# Create entry field for YouTube URL
YouTubeURL = ctk.CTkEntry(root, 
    placeholder_text="Paste in the YouTube URL",
    height=30,
    width=600,
    font=("Helvetica", 14),
    corner_radius=10,
    text_color='white'

) 
YouTubeURL.pack(pady=20)
 
# Chose Video or MP3
def toggle_state():
    global FileType
    if check_var.get() == 'on':
        FileType = ".mp3"
        resolutions_combobox['state'] = 'disabled'
        style.configure("TCombobox", fieldbackground= "gray", background= "black", foreground="gray")
        my_label.configure(root, text="Select Resolution",  text_color="#5e5c55")
    else:
        resolutions_combobox['state'] = 'readonly'
        FileType = ".mp4"
        
check_var = ctk.StringVar(value="off")
my_check =  ctk.CTkCheckBox(root, text="Download an MP3 instead of Video", variable=check_var, command=toggle_state, 
                            onvalue="on", 
                            offvalue="off",
                            checkbox_height=22,
                            checkbox_width=22,
                            corner_radius=50,
                            fg_color="red",
                            hover_color="gray",
                            font=("verdana", 14)
                            ).pack(pady=1)


my_label = ctk.CTkLabel(root, text="Select Resolution")
my_label.pack(pady=5)

# Create resolution combo box
resolutions = ["1080p", "720p", "360p"]
resolution_var = ctk.StringVar()
resolutions_combobox = ttk.Combobox(root, values=resolutions, textvariable=resolution_var)
style= ttk.Style()
style.theme_use('clam')
resolutions_combobox.pack(pady=("10p", "5p"))
resolutions_combobox.set("720px")

# Create progess bar and status
progress_lable = ctk.CTkLabel(root, text="0%")
progress_lable.pack(pady=10)

progress_bar = ctk.CTkProgressBar(root, width=400)
progress_bar.set(0.0)
progress_bar.pack(pady=(10, 5))

status_lable = ctk.CTkLabel(root, text="")
status_lable.pack(pady=(10, 5))

# DOWNLOAD
def download_video():
    url = YouTubeURL.get()
    resolution = resolution_var.get()
    progress_bar.pack(pady=(10, 5))
    progress_lable.pack(pady=(10, 5))
    status_lable.pack(pady=(10, 5))
    my_button['state'] = 'disabled'
    status_lable.configure(text="")
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        if FileType == '.mp4':
            stream = yt.streams.filter(res=resolution).first()
        else:
            stream = yt.streams.filter(only_audio=True).first()
        FileBase = sanitize_filename(yt.title)
        FileName = FileBase+ FileType
        
        print(stream)
        print(FileName)
        print(selected_directory)
        DLName = os.path.join(selected_directory, f"{FileName}")
        stream.download(output_path=selected_directory)
        print("DLName: " + DLName)
        base, ext = os.path.splitext(DLName)
        new_file = base + FileType
        print("new_file: " + new_file)
        print("base:" +base)
        if FileType == '.mp3':
            os.rename(selected_directory+"\\"+ FileBase +'.mp4', new_file)

        status_lable.configure(text=f'Downloaded!', text_color="white" , fg_color="green") 

    except Exception as e:
        status_lable.configure(text=f'Error {str(e)}', text_color="white" , fg_color="red")


def on_progress(stream, chunk, butes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - butes_remaining
    percentage_completed = bytes_downloaded / total_size * 100
    print(percentage_completed)
    progress_lable.configure(text = str(int(percentage_completed)) + "%")
    progress_lable.update()
    progress_bar.set(float(percentage_completed / 100))


# Create label to display messages
my_lable = ctk.CTkLabel(root, text="", font=("Helvetica", 24))
my_lable.pack(pady=10)

# Create button to start download
my_button = ctk.CTkButton(root, text='Download', command=download_video)
my_button.pack(pady=10)

# print(youtube_url)
# print(selected_directory)

verlable = ctk.CTkLabel(root, text=f'LMT {Version}', font=("Verdana", 8), text_color="#ffffff" )
verlable.place(relx = 1.0, 
               rely = 1.0, 
               anchor ='se')


root.mainloop()
