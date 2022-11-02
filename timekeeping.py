from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import os 
from dotenv import load_dotenv
load_dotenv()

driver = webdriver.Chrome("chromedriver")
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
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, clockClassname)))
    driver.find_element(By.CLASS_NAME, clockClassname).click()

    isLoggedIn = checkIsLoggedIn()
    if isLoggedIn: 
        driver.find_element(By.XPATH, '//li[@data-bind="click: webBundyLogOut"]').click()
    else: 
        driver.find_element(By.XPATH, '//li[@data-bind="click: webBundyLogIn"]').click()

def confirmPopUp():   
    successButtonXPath = "//button[@data-bb-handler='success']"
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, successButtonXPath)))
    driver.find_element(By.XPATH, successButtonXPath).click()

def closeConfirmationPopUp():
    okButtonXPath = "//button[@data-bb-handler='ok']"
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, okButtonXPath)))
    driver.find_element(By.XPATH, okButtonXPath).click()

def reloadPage(): 
    driver.refresh()

def closeAndQuitBrowser(): 
    # 5 seconds to check if login/logout is logged on dashboard
    time.sleep(5)
    driver.close()
    driver.quit()

try: 
    login()
    timeinOrTimeout()
    confirmPopUp()
    closeConfirmationPopUp()
    reloadPage()
    closeAndQuitBrowser()
except: 
    print("Something went wrong")
