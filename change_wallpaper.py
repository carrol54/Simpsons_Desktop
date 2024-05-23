#Changes wallpaper
import os
import ctypes, subprocess, platform
from time import sleep
import random


def windows_change_wallpaper(file_path):
    wallpaper_path = os.path.abspath(file_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 3)
    print("Wallpaper changed!")

def apple_change_wallpaper(file_path):
    wallpaper_path = os.path.abspath(file_path)
    script = f'tell application "Finder" to set desktop picture to POSIX file "{wallpaper_path}"'
    subprocess.run(['osascript', '-e', script])
    print("Wallpaper changed!")

if __name__ == "__main__":
    print("This will randomly change your desktop to a file in a specified path at a specified interval.")
    file_path = input("What's the path you'd like to use? If the current directory, enter '.' ")
    which_files = input("All files (a) or all files that begin with a particular string? If so, enter string (ex. wallpaper_) ")
    nap_time = int(input("How frequently, in seconds, would you like the desktop to change? "))
    try:
        all_files = os.listdir(file_path)
        if which_files != "a":
            new_files = []
            for file in all_files:
                if file.lower().startswith(which_files):
                    new_files.append(file)
        else:
            new_files = all_files
    except FileNotFoundError:
        print(f"{file_path} is not a valid path. Please try again...")

    #OS Check
    os_name = platform.system()
    if os_name == "Darwin":
        #Mac
        while True:
            apple_change_wallpaper(random.choice(new_files))
            sleep(nap_time)

    elif os_name == "Windows":
        #Winders
        while True:
            windows_change_wallpaper(random.choice(new_files))
            sleep(nap_time)
            
    else:
        print("Failed")
