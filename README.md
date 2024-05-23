# Simpsons_Desktop
Package that can download images from Frinkiac with captions, set against the background of the SImpsons' family television set and set as your wallpaper.

Running "frinkiac_download_and_change.py" will prompt for how frequently (in seconds) you would like your desktop changed.
It will pop up the Chrome browser for use by Selenium, which you can subsequently minimize or hide. 
Clicks the random button, clicks the caption button, saves the file.
Once the file is saved, it crops the picture into the tv_set.jpeg file and saves it again.
The OS is checked and the proper method is used to change wallpaper to the new photo.
