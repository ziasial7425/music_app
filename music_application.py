import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Music Player")

        # Initialize pygame mixer
        pygame.init()
        pygame.mixer.init()

        # Initialize variables
        self.music_files = []
        self.folder_path = ""
        self.current_index = -1
        self.paused = False

        # Button to load folder
        tk.Button(root, text="Load Music Folder", command=self.load_folder).pack(pady=5)

        # Listbox to display songs
        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(pady=5)

        # Control buttons (Play, Pause, Next, Previous)
        controls = tk.Frame(root)
        controls.pack(pady=5)

        tk.Button(controls, text="Previous", command=self.previous_song, width=10).grid(row=0, column=0, padx=5)
        tk.Button(controls, text="Play", command=self.play_selected, width=10).grid(row=0, column=1, padx=5)
        tk.Button(controls, text="Pause/Resume", command=self.pause_resume, width=12).grid(row=0, column=2, padx=5)
        tk.Button(controls, text="Next", command=self.next_song, width=10).grid(row=0, column=3, padx=5)

        # Label to show status (e.g., Playing, Paused)
        self.status = tk.Label(root, text="", fg="blue")
        self.status.pack()

    def load_folder(self):
        # Open dialog to select folder and load .mp3/.wav files
        folder = filedialog.askdirectory()
        if folder:
            self.music_files = [f for f in os.listdir(folder) if f.endswith((".mp3", ".wav"))]
            self.folder_path = folder
            self.listbox.delete(0, tk.END)
            for file in self.music_files:
                self.listbox.insert(tk.END, file)
            self.current_index = 0
            self.status.config(text="Folder loaded successfully.")

    def play_selected(self):
        # Play song selected in listbox
        selected = self.listbox.curselection()
        if selected:
            self.current_index = selected[0]
            self.play_song()
        else:
            messagebox.showinfo("Info", "Please select a song to play.")

    def play_song(self):
        # Play current song from list
        song = self.music_files[self.current_index]
        path = os.path.join(self.folder_path, song)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        self.listbox.select_clear(0, tk.END)
        self.listbox.select_set(self.current_index)
        self.status.config(text=f"Playing: {song}")
        self.paused = False

    def pause_resume(self):
        # Pause or resume current song
        if pygame.mixer.music.get_busy():
            if self.paused:
                pygame.mixer.music.unpause()
                self.status.config(text=f"Resumed: {self.music_files[self.current_index]}")
            else:
                pygame.mixer.music.pause()
                self.status.config(text="Paused")
            self.paused = not self.paused
        else:
            messagebox.showinfo("Info", "No song is currently playing.")

    def next_song(self):
        # Play next song if available
        if self.current_index < len(self.music_files) - 1:
            self.current_index += 1
            self.play_song()
        else:
            self.status.config(text="No next song.")

    def previous_song(self):
        # Play previous song if available
        if self.current_index > 0:
            self.current_index -= 1
            self.play_song()
        else:
            self.status.config(text="No previous song.")

# Run the app
root = tk.Tk()
app = MusicPlayer(root)
root.mainloop()
