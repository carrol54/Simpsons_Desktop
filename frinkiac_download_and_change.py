#Provides options to download Simpsons screencaps from Frinkiac, add to a television screen image and then set as a wallpaper.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import requests
from PIL import Image
import os
import ctypes, subprocess, platform

def get_buttons():
    buttons = []
    for d in driver.find_elements('tag name', 'button'):
        buttons.append({"Name" : d.text, "Element" : d})
    return buttons

def click_meme_button():
    buttons = get_buttons()
    for button in buttons:
        if button["Name"] == "MAKE MEME":
            button['Element'].click()

def click_random_button():
    buttons = get_buttons()
    for button in buttons:
        if button["Name"] == "RANDOM":
            button['Element'].click()

def return_image():
    image = driver.find_elements(By.XPATH, """//*[@id="app"]/div/div/div/section/div/div[1]/div/a/img""")
    return(image[0].get_attribute("src"))

def download_image(img_url, img_name):
    response = requests.get(img_url)
    if response.status_code == 200:
        with open(img_name + ".jpg", "wb") as f:
            f.write(response.content)
            print(f"Successfully saved {f}")
    else:
        print("Could not download image...")

def create_wallpaper(img, new_name):
    default_image = Image.open("tv_set.jpeg")
    image_to_paste = Image.open(img)

    # Dimensions of the white-out area in the template
    whiteout_width = 495
    whiteout_height = 305

    # Desired placement coordinates within the white-out area
    desired_x = 100
    desired_y = 50

    # Adjust the placement coordinates for pasting based on the white-out area dimensions
    adjusted_x = desired_x - (whiteout_width // 2)  # Adjust horizontally by half of the width
    adjusted_y = desired_y - (whiteout_height // 2)  # Adjust vertically by half of the height

    #Resize the image to paste, paste it onto the tv set
    image_to_paste = image_to_paste.resize((whiteout_width, whiteout_height), Image.ANTIALIAS)
    default_image.paste(image_to_paste, (130, 75))

    #Save as wallpaper file
    default_image.save(new_name + '.png')

def windows_change_wallpaper(file_path):
    wallpaper_path = os.path.abspath(file_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 3)
    print("Wallpaper changed!")

def apple_change_wallpaper(file_path):
    wallpaper_path = os.path.abspath(file_path)
    script = f'tell application "Finder" to set desktop picture to POSIX file "{wallpaper_path}"'
    subprocess.run(['osascript', '-e', script])
    print("Wallpaper changed!")

if __name__ == '__main__':
    time = int(input("How frequently (in seconds) would you like the desktop to change? "))
    #Set up driver
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    url = 'https://frinkiac.com/caption/S14E19/828494'
    driver.get(url)
    #Variable for file names
    wallpaper_name = 0
    #OS Check
    os_name = platform.system()
    if os_name == "Darwin":
        #Mac
        while True:
            click_random_button()
            sleep(int(time/3))
            click_meme_button()
            sleep(int(time/3))
            print(f"Downloading {driver.title}.")
            download_image(return_image(), driver.title)
            sleep(int(time/3))
            create_wallpaper(driver.title + ".jpg", str(wallpaper_name))
            apple_change_wallpaper(str(wallpaper_name) + ".png")
            wallpaper_name += 1


    elif os_name == "Windows":
        #Winders
        while True:
            click_random_button()
            sleep(1)
            click_meme_button()
            sleep(1)
            print(f"Downloading {driver.title}.")
            download_image(return_image(), driver.title)
            sleep(time)
            create_wallpaper(driver.title + ".jpg", str(wallpaper_name))
            windows_change_wallpaper(str(wallpaper_name) + ".png")
            
    else:
        print("Failed")