import os
import signal
import sys
import time

from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

app = Flask(__name__)


def automate(anchor_email, anchor_password, anchor_title, anchor_description, anchor_file_path):
    # start browser & upload the downloaded video/audio file
    # -----------------------------------------------------------------

    print('[anchor_email]', anchor_email)
    print('[anchor_password]', anchor_password)
    print('[anchor_title]', anchor_title)
    print('[anchor_description]', anchor_description)
    print('[anchor_file_path]', anchor_file_path)

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

        file_upload_input.send_keys(anchor_file_path)

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

        title_input.send_keys(anchor_title)

        print('[browser]', 'find description text box')

        description_text_box = browser.find_element_by_css_selector('div[role=textbox]')

        print('[browser]', 'send description')

        description_text_box.send_keys(anchor_description)

        print('[browser]', 'find publish now button')

        publish_now_button = browser.find_element_by_xpath('//*[contains(text(), "Publish now")]')

        print('[browser]', 'click publish now button')

        webdriver.ActionChains(browser).move_to_element(publish_now_button).click().perform()

    except Exception as exception:
        return repr(exception), 400
    finally:
        print('[selenium] quit browser')
        browser.quit()
    return "published successfully as podcast", 200


@app.route("/", methods=['POST'])
def automator_trigger():
    anchor_email = request.form.get("email")
    anchor_password = request.form.get("password")
    anchor_title = request.form.get("title")
    anchor_description = request.form.get("description")
    anchor_file_path = os.path.abspath(request.files['file'].filename)
    return automate(anchor_email, anchor_password, anchor_title, anchor_description, anchor_file_path)


class TerminationSignalError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'Termination Signal Error'


def handle_termination_signal(signum, frame):
    print('[server] termination signal received')
    if __name__ == '__main__':
        raise TerminationSignalError()


signal.signal(signal.SIGTERM, handle_termination_signal)

if __name__ == '__main__':
    try:
        host = os.environ.get('HOST', '0.0.0.0')
        port = int(os.environ.get('PORT', 8080))
        app.run(host=host, port=port, debug=True)
    except TerminationSignalError as e:
        print('[server] is terminated')
