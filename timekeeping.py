from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

import time

import os 
from dotenv import load_dotenv
load_dotenv()

TIMEOUTLIMIT = 20

chromeDriverService=Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=chromeDriverService)
driver.get("https://whitecloak.hrhub.ph/Login.aspx")

def login(): 
    driver.find_element(By.ID, "txtUsername").send_keys(os.getenv('USERNAME'))
    driver.find_element(By.ID, "txtPassword").send_keys(os.getenv('PASSWORD'))
    driver.find_element(By.NAME, "btnLogIn").click()

def checkIsLoggedIn(): 
    firstRowSelector = "#dashboard-container-fluid > div.col-md-12 > div > div.col-md-8 > div > div.col-md-6.widget.clearfix > div > div.widget-wrapper > div.widget-content > div.widget-body > div:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(2) > span:nth-child(1)"
    firstRowText = driver.find_element(By.CSS_SELECTOR, firstRowSelector).get_attribute("innerText")
    return firstRowText == 'IN'

def timeinOrTimeout():
    clockClassname = "small-image"
    element = WebDriverWait(driver, TIMEOUTLIMIT).until(EC.element_to_be_clickable((By.CLASS_NAME, clockClassname)))
    element.click()

    isLoggedIn = checkIsLoggedIn()
    if isLoggedIn: 
        driver.find_element(By.XPATH, '//li[@data-bind="click: webBundyLogOut"]').click()
    else: 
        driver.find_element(By.XPATH, '//li[@data-bind="click: webBundyLogIn"]').click()

def confirmPopUpByXPath(xpath):   
    element = WebDriverWait(driver, TIMEOUTLIMIT).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()

def reloadPage(): 
    driver.refresh()

def closeAndQuitBrowser(): 
    logsBufferTime = 5
    time.sleep(logsBufferTime)
    driver.close()
    driver.quit()

def runAll():
    successButtonXPath = "//button[@data-bb-handler='success']"
    okButtonXpath = "//button[@data-bb-handler='ok']"

    login()
    timeinOrTimeout()
    confirmPopUpByXPath(successButtonXPath)
    confirmPopUpByXPath(okButtonXpath)
    reloadPage()
    closeAndQuitBrowser()

try: 
    runAll()
except: 
    print("Something went wrong")