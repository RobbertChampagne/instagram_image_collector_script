import os
import time

#SELENIUM IMPORTS
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#WebDriverWait IMPORTS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#REPLACE FOLDER IMPORT
import shutil # to save it locally

#DOWNLOAD IMAGES
import requests

PATH = os.path.dirname(os.path.realpath(__file__)) + '\chromedriver.exe'    #Chrome version 88 ChromeDriver 88.0.4324.96
driver = webdriver.Chrome(PATH)

driver.set_window_position(-10000,0)   #hide browser window

driver.get('https://www.instagram.com/') #open browser and tab + visist link

try:
    #ACCEPT COOKIES
    accept_cookies = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='aOOlW  bIiDR  ']"))).click()

    #LOGIN
    username = WebDriverWait(driver, 10).until(          
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
    )
    password = WebDriverWait(driver, 10).until(          
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
    )

    username.clear()
    password.clear()
    username.send_keys("email")
    password.send_keys("password")

    log_in = WebDriverWait(driver, 10).until( #click on inlog button
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))).click()
    
    time.sleep(3) #wait until page is loaded (button classes are the same on both pages) 
        
    #SAVE LOGIN CREDENTIALS (not now)
    not_now_cookies = WebDriverWait(driver, 10).until( 
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='sqdOP yWX7d    y3zKF     ']"))).click()

    #SAVE NOTIFICATIONS (not now)
    not_now_noti = WebDriverWait(driver, 10).until( 
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='aOOlW   HoLwm ']"))).click()

    #SEARCHBOX SELECTEREN
    searchbox = WebDriverWait(driver, 10).until( 
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[class='XTCLo x3qfX ']")))

    #SEARCHBOX INVULLEN
    searchbox.clear() #empty input
    keyword = "#dog"
    searchbox.send_keys(keyword) #text in inputfield

    #CLICK THE FIRST LINK
    searchlink = WebDriverWait(driver, 10).until( 
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[class='-qQT3']"))).click()
    
    time.sleep(3) #wait until images are downloaded on the next page
    
    #GET IMAGES
    driver.execute_script("window.scrollTo(0,4000);") #start scrolling (4 times length of screen )
    images = driver.find_elements_by_tag_name('img') #get images tages
    images = [image for image in images if image.get_attribute('class') == "FFVAD"] #so you don't get the insta logo, etc..
    images = [image.get_attribute('src') for image in images] #turn the img tags into links   #data-src

    #CREATE FOLDER FOR IMAGES
    folder_path = os.path.dirname(os.path.realpath(__file__)) #current path
    folder_path = os.path.join(folder_path, keyword[1:]) # \cat


    if os.path.exists(folder_path): #if exists 
        shutil.rmtree(folder_path)  #replace
        os.makedirs(folder_path)    #create new

    else:
        os.makedirs(folder_path)        #else create


    #CREATE IMAGE SAVENAME
    counter = 0
    
    #SAVE IMAGES
    for image in images:
        name = os.path.join(folder_path, keyword[1:] + str(counter) + '.jpg') #savename
        link = image #src link

        with open(name, 'wb') as f: #create file
            im = requests.get(link)
            f.write(im.content) #response on the .get(), 'content' == bits ('wb') content

        counter += 1

except:
    print("Something went wrong. Please wait a few seconds and try again.")
    driver.quit()

finally:
    driver.quit()




