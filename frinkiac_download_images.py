#Provides options to download Simpsons screencaps from Frinkiac
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

def create_wallpaper(img, new_title):
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
    default_image.save('wallpaper_' + new_title + '.png')

if __name__ == '__main__':
    count = int(input("How many images would you like to download? "))
    television = input("Would you like them placed in the television image? (y/n) ")
    #Set up driver
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    url = 'https://frinkiac.com/caption/S14E19/828494'
    driver.get(url)
    #Variable for file names
    wallpaper_name = 0
    for x in range(count):
        click_random_button()
        sleep(1)
        click_meme_button()
        sleep(1)
        print(f"Downloading number {x} : {driver.title}.")
        download_image(return_image(), driver.title)
        sleep(1)
        if television.lower() == "y":
            create_wallpaper(driver.title + ".jpg", driver.title)
