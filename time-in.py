from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "small-image")))
    driver.find_element(By.CLASS_NAME, "small-image").click()

    isLoggedIn = checkIsLoggedIn()
    if isLoggedIn: 
        driver.find_element(By.XPATH, '//li[@data-bind="click: webBundyLogOut"]').click()
    else: 
        driver.find_element(By.XPATH, '//li[@data-bind="click: webBundyLogIn"]').click()

# def confirmPopup():   
#     WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-bb-handler='danger']")))
#     driver.find_element(By.XPATH, "//button[@data-bb-handler='success']").click()

try: 
    login()
    timeinOrTimeout()
    # confirmPopup()
    print("Logged in successfully")
except: 
    print("Something went wrong")

