import os
import threading
import re
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import yt_dlp
import datetime
import sys
import subprocess

# Python app that lets you download a YouTube Video
# Refactored and Optimized (using yt-dlp)
# Version 2.0 with Logging and File Opening
Version = 'v2.1'
LOG_FILE = "YouGotIt.log"

class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('YouGotIt! - YouTube Downloader')
        self.geometry('720x800')
        
        # Set appearance
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Variables
        self.download_directory = os.path.join(os.path.expanduser("~"), "Downloads")
        self.file_type_var = ctk.StringVar(value="video")
        self.resolution_var = ctk.StringVar(value="720p")
        self.last_downloaded_file = None
        self.is_cancelled = False
        
        self.create_widgets()
        
        # Update directory label
        self.dir_label_path.configure(text=self.download_directory)
        
        self.log_message(f"Application started. Version: {Version}")

    def log_message(self, message):
        """Appends a message to the log file with a timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        try:
            with open(LOG_FILE, "a") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Failed to write to log: {e}")

    def create_widgets(self):
        # Title
        self.title_label = ctk.CTkLabel(self, text="YouGotIt!", font=("Helvetica", 44), text_color="#de626e")
        self.title_label.pack(pady=5)
        
        self.subtitle_label = ctk.CTkLabel(self, text="Download any YouTube Video", font=("Verdana", 16), text_color="#afd5de")
        self.subtitle_label.pack(pady=(0, 30))

        # Directory Selection
        self.dir_info_label = ctk.CTkLabel(self, text="Current download directory:", font=("Helvetica", 14))
        self.dir_info_label.pack(pady=1)

        self.dir_label_path = ctk.CTkLabel(self, text="", font=("Helvetica", 14))
        self.dir_label_path.pack(pady=5)

        self.dir_button = ctk.CTkButton(self, text="Change Directory", command=self.select_directory)
        self.dir_button.pack(pady=10)

        # URL Entry
        self.url_entry = ctk.CTkEntry(self, 
            placeholder_text="Paste YouTube URL here",
            height=40,
            width=600,
            font=("Helvetica", 14),
            corner_radius=10
        )
        self.url_entry.pack(pady=20)

        # Options (Video vs Audio)
        self.checkbox = ctk.CTkCheckBox(self, text="Download Audio Only (MP3)", 
                                      variable=self.file_type_var, 
                                      onvalue="audio", offvalue="video",
                                      command=self.toggle_options,
                                      font=("Verdana", 14),
                                      fg_color="red", hover_color="gray")
        self.checkbox.pack(pady=10)

        # Resolution Selection
        self.res_label = ctk.CTkLabel(self, text="Select Quality")
        self.res_label.pack(pady=5)

        self.resolutions = ["Best Quality", "Lowest Quality"]
        self.res_option_menu = ctk.CTkOptionMenu(self, values=self.resolutions, variable=self.resolution_var)
        self.res_option_menu.pack(pady=10)
        self.resolution_var.set("Best Quality")

        # Progress Section
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.pack(pady=10)
        
        # Spinner (Hidden initially)
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.spinner_idx = 0
        self.spinner_label = ctk.CTkLabel(self.progress_frame, text="", font=("Courier New", 20))
        self.spinner_label.grid(row=0, column=0, padx=(0, 10))

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=400)
        self.progress_bar.set(0.0)
        self.progress_bar.grid(row=0, column=1)
        
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="0%", width=40)
        self.progress_label.grid(row=0, column=2, padx=(10, 0))

        self.status_label = ctk.CTkLabel(self, text="Ready", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        # Download Button
        self.download_button = ctk.CTkButton(self, text='Download', command=self.start_download_thread, height=40, font=("Helvetica", 16, "bold"))
        self.download_button.pack(pady=(20, 10))
        
        # Cancel Button
        self.cancel_button = ctk.CTkButton(self, text='Cancel', command=self.cancel_download, fg_color="red", hover_color="darkred")
        # cancel_button is packed dynamically
        
        # Open File Button (Initially Hidden)
        self.open_file_button = ctk.CTkButton(self, text="Open Downloaded File", command=self.open_last_file, height=30, fg_color="#2CC985", hover_color="#1e8a5b")

        # Version
        self.version_label = ctk.CTkLabel(self, text=f'LMT {Version}', font=("Verdana", 10), text_color="gray", cursor="hand2")
        self.version_label.place(relx=0.98, rely=0.98, anchor='se')
        
        # Bind click event to version label
        self.version_label.bind("<Button-1>", self.open_log_viewer)

    def toggle_options(self):
        if self.file_type_var.get() == "audio":
            self.res_option_menu.configure(state="disabled")
            self.res_label.configure(text_color="gray")
        else:
            self.res_option_menu.configure(state="normal")
            self.res_label.configure(text_color="white") # Assuming dark mode default text color

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.download_directory = directory
            self.dir_label_path.configure(text=self.download_directory)
            self.log_message(f"Download directory changed to: {self.download_directory}")

    def start_download_thread(self):
        url = self.url_entry.get()
        if not url:
            self.status_label.configure(text="Please enter a URL", text_color="red")
            return

        self.is_cancelled = False
        self.download_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")
        self.cancel_button.pack(pady=(0, 20)) # Show cancel button
        
        self.open_file_button.pack_forget() # Hide previous open button
        self.status_label.configure(text="Initializing...", text_color="white")
        
        # Start spinner animation
        self.progress_bar.set(0)
        self.progress_label.configure(text="0%")
        self.animate_spinner()

        self.log_message(f"Starting download for URL: {url}")

        # Run download in separate thread to prevent UI freezing
        thread = threading.Thread(target=self.download_video, args=(url,))
        thread.start()

    def animate_spinner(self):
        if self.download_button.cget("state") == "disabled" and not self.is_cancelled:
            char = self.spinner_chars[self.spinner_idx]
            self.spinner_label.configure(text=char)
            self.spinner_idx = (self.spinner_idx + 1) % len(self.spinner_chars)
            self.after(100, self.animate_spinner)
        else:
            self.spinner_label.configure(text="") # Clear spinner when done

    def cancel_download(self):
        self.is_cancelled = True
        self.status_label.configure(text="Cancelling...", text_color="orange")
        self.log_message("User requested application exit via Cancel.")
        self.destroy() # Exit the application immediately as requested

    def progress_hook(self, d):
        if self.is_cancelled:
            return
            
        if d['status'] == 'downloading':
            try:
                p_str = d.get('_percent_str', '').replace('%','')
                percentage = float(p_str) / 100
                
                # Update UI
                self.progress_label.configure(text=d.get('_percent_str', '0%'))
                self.progress_bar.set(percentage)
                
            except Exception:
                pass # safely ignore parsing errors during download
        # Removed setting "Processing..." here to prevent sticking

    def download_video(self, url):
        # Attempt 1: Requested Quality
        success = self._attempt_download(url, safe_mode=False)
        
        # Attempt 2: Safe Mode (Fallback if HLS/m3u8 fails)
        if not success and not self.is_cancelled:
            self.log_message("Primary download failed. Retrying with Safe Mode (Reliable HTTP format)...")
            self.status_label.configure(text="Retrying (Safe Mode)...", text_color="#FFD700") # Gold
            success = self._attempt_download(url, safe_mode=True)

    def _attempt_download(self, url, safe_mode=False):
        try:
            ydl_opts = {
                'progress_hooks': [self.progress_hook],
                'outtmpl': os.path.join(self.download_directory, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True, # Bypass SSL errors
                'overwrites': True, # Force overwrite if file exists
            }

            is_audio_only = self.file_type_var.get() == "audio"
            req_res = self.resolution_var.get()
            
            # Determine base format strings based on Quality Selection
            if req_res == "Lowest Quality":
                quality_video = 'worst'
                quality_audio = 'worstaudio'
            else: # Default to Best Quality
                quality_video = 'best'
                quality_audio = 'bestaudio'

            protocol_filter = '[protocol^=http]' if safe_mode else ''

            if is_audio_only:
                 # Audio format logic (e.g., 'bestaudio/best')
                 ydl_opts['format'] = f'{quality_audio}{protocol_filter}/{quality_video}{protocol_filter}'
            else:
                # Video format logic (e.g., 'best')
                # Without ffmpeg, 'best' usually gives a single pre-merged file (often 720p).
                ydl_opts['format'] = f'{quality_video}{protocol_filter}'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Check cancel
                if self.is_cancelled: return False
                
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'Video')
                
                if not safe_mode: # Only show fetching status on first try
                    self.status_label.configure(text=f"Fetching: {video_title[:30]}...")
                
                if self.is_cancelled: return False
                
                # Download
                ydl.download([url])

                if self.is_cancelled: return False

                # Get expected filename
                filename = ydl.prepare_filename(info)

                # Post-processing for simulated "MP3" if needed
                if is_audio_only:
                    try:
                        base, ext = os.path.splitext(filename)
                        if ext.lower() != '.mp3':
                            new_name = base + ".mp3"
                            if os.path.exists(new_name):
                                os.remove(new_name)
                            if os.path.exists(filename):
                                os.rename(filename, new_name)
                            filename = new_name 
                    except Exception as rename_err:
                        self.log_message(f"Rename warning: {rename_err}")
            
            # Success
            self.after(0, lambda: self.download_complete_callback(filename, video_title))
            return True
            
        except Exception as e:
            # Check for cancellation
            error_msg = str(e)
            if "CANCELLED" in error_msg:
                return False
            
            # If this was safe mode (last attempt), show error
            if safe_mode:
                self.after(0, lambda: self.download_error_callback(error_msg, url))
            
            return False

    def download_complete_callback(self, filename, video_title):
        self.last_downloaded_file = filename
        
        # Show Open Button
        self.status_label.configure(text="Download Complete!", text_color="#2CC985")
        
        display_name = os.path.basename(filename)
        if len(display_name) > 30:
            display_name = display_name[:27] + "..."
            
        self.open_file_button.configure(text=f"Open: {display_name}")
        # Add extra padding (approx 2 line breaks) before the green button
        self.open_file_button.pack(pady=(40, 5))
        
        self.log_message(f"Successfully downloaded: {video_title} to {filename}")
        self.reset_ui()

    def download_error_callback(self, error_msg, url):
        self.status_label.configure(text=f"Error: {error_msg[:100]}", text_color="red") # Limit error length
        self.log_message(f"Error downloading {url}: {error_msg}")
        print(f"Error details: {error_msg}")
        self.reset_ui()

    def reset_ui(self):
        self.download_button.configure(state="normal")
        self.cancel_button.pack_forget() # Hide cancel button
        self.spinner_label.configure(text="") # Clear spinner
    
    def open_last_file(self):
        """Opens the last downloaded file in the default OS application."""
        if self.last_downloaded_file and os.path.exists(self.last_downloaded_file):
            try:
                if sys.platform == "win32":
                    os.startfile(self.last_downloaded_file)
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, self.last_downloaded_file])
                self.log_message(f"Opened file: {self.last_downloaded_file}")
            except Exception as e:
                self.log_message(f"Failed to open file: {e}")
                self.status_label.configure(text="Could not open file", text_color="red")

    def open_log_viewer(self, event=None):
        """Opens a new window to display the log file content."""
        log_window = ctk.CTkToplevel(self)
        log_window.title("YouGotIt! - Logs")
        log_window.geometry("600x400")
        
        # Log Text Area
        log_textbox = ctk.CTkTextbox(log_window, width=580, height=380, corner_radius=10)
        log_textbox.pack(padx=10, pady=10)
        
        try:
            with open(LOG_FILE, "r") as f:
                log_content = f.read()
                log_textbox.insert("0.0", log_content)
        except FileNotFoundError:
            log_textbox.insert("0.0", "No log file found.")
        except Exception as e:
            log_textbox.insert("0.0", f"Error reading log file: {e}")
            
        log_textbox.configure(state="disabled") # Make read-only

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
