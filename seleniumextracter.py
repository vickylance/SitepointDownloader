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

path = "video_courses/"
savepath = "video_download/"

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def get_valid_foldername(s):
    return " ".join(str(s).replace('/', ' or ').replace('?', '').split('_'))

def makeDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def waitForLoad(inputXPath):
    '''Waits until the passed in xpath is loaded for the below mentioned PATIENCE_TIME in seconds
    '''
    PATIENCE_TIME = 10
    Wait = WebDriverWait(browser, PATIENCE_TIME)       
    Wait.until(EC.presence_of_all_elements_located((By.XPATH, inputXPath)))


def downloadfile(name,url):
    r = requests.get(url, stream = True)
    print "****Connected****"
    f=open(name,'wb');
    print "Downloading.....  " + name 
    # download started
    with open(name, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 1024*1024):
            if chunk:
                f.write(chunk)
        
    print "%s downloaded!\n"%name
    f.close()


# Load the chromium web driver
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
username.send_keys("vkkpp@hotmail.com")
password.send_keys("Rayquaza555!")
# Login to the website
browser.find_element_by_xpath("//input[@name='commit'][@value='Login']").click()
# Click on the courses button
waitForLoad("//a[@class='TypeFilter_Item u-Course']")
browser.find_element_by_xpath("//a[@class='TypeFilter_Item u-Course']").click()

# def page_has_loaded(driver):
#     page_state = driver.execute_script('return document.readyState;')
#     return page_state == 'complete'

# while True:
#     try:
#         if page_has_loaded(browser):
#             break
#     except:
#         pass


# def scrollDown(driver, value):
#     driver.execute_script("window.scrollBy(0,"+str(value)+")")

# # Scroll down the page
# def scrollDownAllTheWay(driver):
#     old_page = driver.page_source
#     while True:
#         print "Scrolling loop"
#         for i in range(2):
#             scrollDown(driver, 500)
#             time.sleep(2)
#         new_page = driver.page_source
#         if new_page != old_page:
#             old_page = new_page
#         else:
#             break
#     return True

# scrollDownAllTheWay(browser)

waitForLoad("//div[@class='LibraryContent_columns']")
waitForLoad("//a[@class=' LibraryCard u-course']")
time.sleep(5) # seconds

all_courses = browser.find_element_by_xpath("//div[@class='LibraryContent_columns']")
open('test.html', 'w').close()
with open("test.html", "a") as myfile:
    myfile.write(unicode(all_courses.get_attribute('innerHTML')).encode('utf8'))
soup = BeautifulSoup(all_courses.get_attribute('innerHTML'), 'html.parser')

all_courses = []

open('urls.txt', 'w').close()
for a in soup.find_all('a', href=True):
    course_name = a.find("div", class_="f-large f-bold").text
    all_courses.append([unicode(course_name).encode('utf-8'), unicode(a['href']).encode('utf-8')])
    with open("urls.txt", "a") as myfile:
        myfile.write(unicode(course_name).encode('utf-8') + " : " + unicode(a['href']).encode('utf-8') + '\n')

print all_courses
print len(all_courses)


makeDir("video_courses") # To save the text file with download links
makeDir("video_download") # To save the actual mp4 files in respective folders
for course in all_courses:
    browser.get(course[1])
    waitForLoad("//div[@id='stickyButton']/a")
    browser.find_element_by_xpath("//div[@id='stickyButton']/a").click()
    waitForLoad("//div[@class='Contents']")
    all_videos = browser.find_elements_by_xpath("//div[@class='Contents_row ']")
    video_titles = browser.find_elements_by_xpath("//span[@class='Contents_title']")
    SD_videos = browser.find_elements_by_xpath("//span[@class='Contents_actions']/a[1]")
    HD_videos = browser.find_elements_by_xpath("//span[@class='Contents_actions']/a[2]")
    open('video_courses/' + get_valid_filename(course[0]) + '.txt', 'w').close()
    video_list = []
    for idx, video in enumerate(all_videos):
        # try:
        video_title = video_titles[idx].get_attribute('innerHTML')
        SD_video = SD_videos[idx].get_attribute('href')
        HD_video = HD_videos[idx].get_attribute('href')
        video_list.append([video_title, HD_video])
    browser.execute_script("window.history.go(-1)")
    for idx, video in enumerate(video_list):
        downloadfile(savepath + get_valid_foldername(course[0]) + '/' + str(idx + 1).zfill(2) + '-' + get_valid_foldername(' '.join(unicode(video[0]).encode('utf-8').split()))+".mp4", video[1])
            # with open('video_courses/' + get_valid_filename(course[0]) + '.txt', "a") as myfile:
            #     myfile.write(' '.join(unicode(video_title).encode('utf-8').split()) + "||" + HD_video +'\n')
        # except:
        #     print "Most likely Quiz"
