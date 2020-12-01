import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import UnexpectedAlertPresentException
import pandas as pd
import os
from tqdm import tqdm

def download(company, path, finish_time, no_chrome):
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': path}
    options.add_experimental_option('prefs', prefs)
    if no_chrome == True:
        options.headless = True
    driver = webdriver.Chrome(executable_path="C:\\Users\\minnieljy\\chromedriver.exe", chrome_options=options)
    driver.implicitly_wait(finish_time)
    driver.delete_all_cookies()
    driver.get("https://www.capitaliq.com/CIQDotNet/Filings/FilingsAnnualReports.aspx")
    driver.find_element(By.ID, "password").send_keys("2022HKUcapiq6")
    driver.find_element(By.ID, "username").click()
    driver.find_element(By.ID, "username").send_keys("libser@hku.hk")
    driver.find_element(By.ID, "myLoginButton").click()
    driver.find_element(By.ID, "dspCustomView_Toggle_myCompanySearch_myInnerDS_myTickerBox").click()
    driver.find_element(By.ID, "dspCustomView_Toggle_myCompanySearch_myInnerDS_myTickerBox").send_keys(company)
    driver.find_element(By.ID, "dspCustomView_Toggle_ddlDateType").click()
    dropdown = driver.find_element(By.ID, "dspCustomView_Toggle_ddlDateType")
    dropdown.find_element(By.XPATH, "//option[. = 'Filing Date']").click()
    driver.find_element(By.ID, "dspCustomView_Toggle_ddlDateType").click()
    driver.find_element(By.ID, "dspCustomView_Toggle_myDateRange_myFromBox").click()
    driver.find_element(By.ID, "dspCustomView_Toggle_myDateRange_myFromBox").send_keys("01/10/2020")
    driver.find_element(By.ID, "dspCustomView_Toggle_myDateRange_myToBox").send_keys('11/10/2020')
    driver.find_element(By.ID, "dspCustomView_Toggle_myAO_ctl03_EC").click()
    dropdown = driver.find_element(By.ID, "dspCustomView_Toggle_myAO_Toggle_secFormTypes_optionsList")
    dropdown.find_element(By.XPATH, "//option[. = '10-Q']").click()
    dropdown.find_element(By.XPATH, "//option[. = '10-K']").click()
    driver.find_element(By.ID, "dspCustomView_Toggle_myAO_Toggle_secFormTypes_addBtn").click()

    dropdown = driver.find_element(By.ID, "dspCustomView_Toggle_myAO_Toggle_countries_optionsList")
    dropdown.find_element(By.XPATH, "//option[. = 'United States']").click()
    driver.find_element(By.ID, "dspCustomView_Toggle_myAO_Toggle_countries_addBtn").click()
    driver.find_element(By.ID, "dspCustomView_Toggle__saveCancel__saveBtn").click()
    element = driver.find_element(By.ID, "dspCustomView_Toggle__saveCancel__saveBtn")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    element = driver.find_element(By.CSS_SELECTOR, "body")
    driver.find_element(By.LINK_TEXT, "Form Type").click()
    driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .binderIcoSprite_doctype_word_img").click()
    driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) .binderIcoSprite_doctype_word_img").click()
    driver.find_element(By.CSS_SELECTOR, "tr:nth-child(4) .binderIcoSprite_doctype_word_img").click()
    driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > td > div > a > .binderIcoSprite_doctype_word_img").click()
    time.sleep(120)
    driver.quit()
    
def main(index_path, save_path, finish_time, show_chrome):
    df = pd.read_csv(index_path, header = 0)
    for i in df.columns[0:5]:
        if not os.path.exists(save_path + "\\" + i):
            os.makedirs(save_path + "\\" + i)
        print("Start the industry of ", i)
        try:
            with tqdm (range(0,df.shape[0]), desc = "download word files", ncols=80) as t:
                for j in t:
                    if pd.notnull(df[i][j]):
                        print("Start dwnloading", df[i][j])
                        times = 1
                        while times <= 3:
                            try:
                                if not os.path.exists(save_path + "\\" + i + "\\" + df[i][j].split(" ")[0]):
                                    os.makedirs(save_path + "\\" + i + "\\" + df[i][j].split(" ")[0])
                                download(df[i][j].split(" ")[0], save_path + "\\" + i + "\\" + df[i][j].split(" ")[0], finish_time, show_chrome)
                                break
                            except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException,UnexpectedAlertPresentException) as error:
                                times += 1
                                print("Cannot download", df[i][j])
                                print(f"Sleep for five seconds and try the {times} times!")
                                time.sleep(5)
        except KeyboardInterrupt:
            t.close()
            raise
        t.close()
        print("Finish the industry of ", i)

if __name__ == '__main__':
    main ("C:\\Users\\minnieljy\\Desktop\\bbg_price(1).csv", "C:\\Users\\minnieljy\\Desktop", 500, True) #index_path and save_path should be changed to local directory
