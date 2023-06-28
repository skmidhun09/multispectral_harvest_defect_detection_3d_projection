import os
from moviepy.editor import *

def convert_mp4_to_gif(mp4_file, gif_file):
    video = VideoFileClip(mp4_file)
    video.write_gif(gif_file, fps=4)

def convert_all_mp4_to_gif(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".mp4"):
            mp4_file = os.path.join(folder_path, file)
            gif_file = os.path.join(folder_path, file[:-4] + ".gif")
            convert_mp4_to_gif(mp4_file, gif_file)
            print(f"Converted {mp4_file} to {gif_file}")

# Provide the path to the folder containing the MP4 files
folder_path = "C:/Users/skmid/OneDrive/Desktop/New folder/New folder (5)/"
convert_all_mp4_to_gif(folder_path)