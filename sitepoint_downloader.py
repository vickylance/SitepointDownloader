from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import os
import re
import requests
import shutil

video_links = "video_courses/"
video_download = "video_download/"

def makeDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def get_valid_foldername(s):
    return " ".join(str(s).replace('/', ' or ').replace('?', '').split('_'))

def waitForLoad(inputXPath):
    '''Waits until the passed in xpath is loaded for the below mentioned PATIENCE_TIME in seconds
    '''
    PATIENCE_TIME = 10
    Wait = WebDriverWait(browser, PATIENCE_TIME)       
    Wait.until(EC.presence_of_all_elements_located((By.XPATH, inputXPath)))

def downloadfile(name,url):
    r = requests.get(url, stream = True)
    print("****Connected****")
    f=open(name,'wb')
    print("Downloading.....  " + name )
    # download started
    with open(name, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 1024*1024):
            if chunk:
                f.write(chunk)
        
    print("%s downloaded!\n"%name)
    f.close()

# Load the chromium web drivers
chromedriver = 'C:\\Projects\\ai-projects\\SitepointDownloader\\chromedriver.exe'
browser = webdriver.Chrome(chromedriver)
# Open Sitepoint website
browser.get("https://www.sitepoint.com/premium/sign-in")
# Fill in Username and Password
username = browser.find_element_by_id("user_login")
password = browser.find_element_by_id("user_password")
# Clear the input field before entering data
username.clear()
password.clear()
# Enter the username and password
username.send_keys("Username")
password.send_keys("Password")
# Login to the website
browser.find_element_by_xpath("//input[@name='commit'][@value='Login']").click()
waitForLoad("//a[@class='TypeFilter_Item u-Course']")

url_lst = []
with open('./urls.txt') as f:
    url_lst = [str(line).rstrip().split('||') for line in f]

if os.path.exists(video_links):
    shutil.rmtree(video_links)
if os.path.exists(video_download):
    shutil.rmtree(video_download)

makeDir("video_courses") # To save the text file with download links
makeDir("video_download") # To save the actual mp4 files in respective folders
for url in url_lst:
    download_dir = video_download + get_valid_foldername(get_valid_filename(url[0]))
    makeDir(download_dir)
    browser.get(url[1])
    browser.find_element_by_xpath("//div[@id='stickyButton']/a").click()
    waitForLoad("//div[@class='Contents']")

    HD_videos = browser.find_elements_by_xpath("//span[@class='Contents_actions']/a[2]")
    video_titles = browser.find_elements_by_xpath("//span[@class='Contents_actions']/a[2]/../../span[@class='Contents_title']")
    open(video_links + get_valid_filename(url[0]) + '.txt', 'w').close()
    video_list = []

    for idx, video in enumerate(HD_videos):
        video_title = ' '.join(unicode(video_titles[idx].get_attribute('innerHTML')).encode('utf-8').split())
        HD_video = unicode(HD_videos[idx].get_attribute('href')).encode('utf-8')
        video_list.append([video_title, HD_video])
        with open(video_links + get_valid_filename(url[0]) + '.txt', "a") as myfile:
            myfile.write(video_title + "||" + HD_video +'\n')
        
    print(video_list)
    browser.execute_script("window.history.go(-1)")
    for idx, video in enumerate(video_list):
        downloadfile(download_dir + '/' + str(idx + 1).zfill(2) + '-' + get_valid_foldername(get_valid_filename(video[0]))+".mp4", video[1])
    
