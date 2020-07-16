import os
import sys
import time

import youtube_dl
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

# check environmental variables
# -----------------------------------------------------------------------------------

video_url = os.environ.get('VIDEO_URL')

if not video_url:
    print('VIDEO_URL environment variable is not set')
    sys.exit(0)

print('[video_url]', video_url)

anchor_email = os.environ.get('ANCHOR_EMAIL')

if not anchor_email:
    print('ANCHOR_EMAIL environment variable is not set')
    sys.exit(0)

print('[anchor_email]', anchor_email)

anchor_password = os.environ.get('ANCHOR_PASSWORD')

if not anchor_password:
    print('ANCHOR_PASSWORD environment variable is not set')
    sys.exit(0)

print('[anchor_password]', anchor_password)

# download YouTube video/audio & extract required information
# -----------------------------------------------------------------------------------

ydl_opts = {'format': 'bestaudio/best', 'outtmpl': '%(id)s.%(ext)s'}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(video_url)
    video_id = info_dict.get('id', None)
    video_title = info_dict.get('title', None)
    video_description = info_dict.get('description', None)

print('[video_id]', video_id)
print('[video_title]', video_title)
print('[video_description]', video_description)

# find & get absolute path of the downloaded video/audio file
# -----------------------------------------------------------------------------------

for entry in os.scandir('.'):
    if entry.is_file() and entry.name.startswith(video_id):
        video_path = os.path.abspath(entry)
        break

print('[video_path]', video_path)

# start browser & upload the downloaded video/audio file
# -----------------------------------------------------------------

chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument("window-size=1920,1080")

browser = webdriver.Chrome(chrome_options=chrome_options)

short_wait = WebDriverWait(browser, 8)
long_wait = WebDriverWait(browser, 64)
very_long_wait = WebDriverWait(browser, 512)

try:
    print('[browser]', 'go to login page')

    browser.get("https://anchor.fm/login")

    print('[browser]', 'find login form')

    login_form = browser.find_element_by_id('LoginForm')

    print('[browser]', 'find email input')

    email_input = login_form.find_element_by_id('email')

    print('[browser]', 'send email')

    email_input.send_keys(anchor_email)

    print('[browser]', 'find password input')

    password_input = login_form.find_element_by_id('password')

    print('[browser]', 'send password')

    password_input.send_keys(anchor_password)

    print('[browser]', 'find login button')

    login_button = login_form.find_element_by_css_selector('button[type=submit]')

    print('[browser]', 'click login button')

    login_button.click()

    print('[browser]', 'wait until new episode text is visible')

    long_wait.until(expected_conditions.visibility_of_element_located((By.LINK_TEXT, 'New Episode')))

    print('[browser]', 'go to new episode page')

    browser.get("https://anchor.fm/dashboard/episode/new")

    print('[browser]', 'wait 5 seconds for page to be ready')

    time.sleep(5)

    print('[browser]', 'wait until save button is visible')

    short_wait.until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'button[class*=saveButton]')))

    print('[browser]', 'find file upload input element')

    file_upload_input = browser.find_element_by_css_selector('input[type=file]')

    print('[browser]', 'send video path to file upload input element')

    file_upload_input.send_keys(video_path)

    print('[browser]', 'wait until save button is not clickable')

    very_long_wait.until_not(
        expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, 'button[class*=saveButton]')))

    print('[browser]', 'find save button')

    save_episode_button = browser.find_element_by_css_selector('button[class*=saveButton]')

    print('[browser]', 'find status info text')

    status_info = browser.find_element_by_css_selector('div[data-cy=audioSegmentSubtitle]')

    print('[browser]', status_info.text, end='')

    while not save_episode_button.is_enabled():

        time.sleep(1)

        if os.name == 'posix':
            print('\n' + '[browser] ' + status_info.text, end='', flush=True)
        else:
            print('\r' + '[browser] ' + status_info.text, end='', flush=True)

        if status_info.text == 'UPLOAD FAILED':
            print('[browser]', 'upload failed')
            sys.exit(0)

    print()

    print('[browser]', 'wait until save button is clickable')

    very_long_wait.until(
        expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, 'button[class*=saveButton]')))

    print('[browser]', 'click save button')

    save_episode_button.click()

    print('[browser]', 'wait until element with id title is visible')

    short_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'title')))

    print('[browser]', 'find title input')

    title_input = browser.find_element_by_id('title')

    print('[browser]', 'send title')

    title_input.send_keys(video_title)

    print('[browser]', 'find description text box')

    description_text_box = browser.find_element_by_css_selector('div[role=textbox]')

    print('[browser]', 'send description')

    description_text_box.send_keys(video_description)

    print('[browser]', 'find publish now button')

    publish_now_button = browser.find_element_by_xpath('//*[contains(text(), "Publish now")]')

    print('[browser]', 'click publish now button')

    webdriver.ActionChains(browser).move_to_element(publish_now_button).click().perform()

finally:
    print('[selenium] quit browser')
    browser.quit()
