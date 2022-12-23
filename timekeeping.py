from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

import time

import os 
from dotenv import load_dotenv
load_dotenv()

TIMEOUT_LIMIT = 20

chrome_driver_service=Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=chrome_driver_service)
driver.get("https://whitecloak.hrhub.ph/Login.aspx")

def main():
    successButtonXPath = "//button[@data-bb-handler='success']"
    okButtonXpath = "//button[@data-bb-handler='ok']"

    login()
    toggle_timein_or_timeout()
    confirm_popup_by_xpath(successButtonXPath)
    confirm_popup_by_xpath(okButtonXpath)
    reload_page()
    close_and_quit_browser()

def login(): 
    driver.find_element(By.ID, "txtUsername").send_keys(os.getenv('USERNAME'))
    driver.find_element(By.ID, "txtPassword").send_keys(os.getenv('PASSWORD'))
    driver.find_element(By.NAME, "btnLogIn").click()

def toggle_timein_or_timeout():
    clock_classname = "clock-icon"
    clock_element = WebDriverWait(driver, TIMEOUT_LIMIT).until(EC.element_to_be_clickable((By.CLASS_NAME, clock_classname)))
    clock_element.click()

    is_logged_in = check_is_logged_in()
    if is_logged_in: 
        driver.find_element(By.XPATH, '//li[@data-bind="click: webBundyLogOut"]').click()
    else: 
        driver.find_element(By.XPATH, '//li[@data-bind="click: webBundyLogIn"]').click()

def check_is_logged_in(): 
    latest_log = '//span[@data-bind="if: InOutMode == 0"]'
    latest_log_text = driver.find_element(By.XPATH, latest_log).get_attribute("innerText")
    return latest_log_text == 'IN'

def confirm_popup_by_xpath(xpath):   
    xpath_element = WebDriverWait(driver, TIMEOUT_LIMIT).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    xpath_element.click()

def reload_page(): 
    driver.refresh()

def close_and_quit_browser(): 
    review_logs_buffer = 5
    time.sleep(review_logs_buffer)
    driver.close()
    driver.quit()

try: 
    main()
except: 
    print("Something went wrong")