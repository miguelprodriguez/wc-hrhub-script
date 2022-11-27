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
    latestLog = '//span[@data-bind="if: InOutMode == 0"]'
    latestLogText = driver.find_element(By.XPATH, latestLog).get_attribute("innerText")
    return latestLogText == 'IN'

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