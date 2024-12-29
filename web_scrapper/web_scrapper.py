from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import json


driver= webdriver.Chrome()
url = "https://find-and-update.company-information.service.gov.uk/"
driver.get(url)
driver.maximize_window()
time.sleep(5)


global company_name_list

# Open and read the JSON file
with open('config.json', 'r') as file:
    company_name_list = json.load(file)


def search(company_name):
    search_bar = driver.find_element(By.XPATH,"//input[@id='site-search-text']")
    search_bar.click()
    search_bar.send_keys(company_name)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(3)
    xpath = f"//a[normalize-space()='{company_name}']"
    first_result = driver.find_element(By.XPATH, xpath)
    first_result.click()
    time.sleep(3)


def fetch_results(company_name):
    creation_date_element = driver.find_element(By.XPATH, "//dd[@id='company-creation-date']")
    creation_date = creation_date_element.text
    print("creation_date:", creation_date)

    people_tab = driver.find_element(By.XPATH, "//a[@id='people-tab']")
    people_tab.click()
    time.sleep(2)

    pscs_link = driver.find_element(By.XPATH, "//a[@id='pscs-link']")
    pscs_link.click()
    time.sleep(2)

    person_name_element = driver.find_element(By.CSS_SELECTOR, "span[id='psc-name-1'] span b")
    person_name = person_name_element.text
    print("Person Name:", person_name)

    data = {'company_name':[company_name],
    'Incorporated on': [creation_date],
            'Person Name': [person_name]}

    # Create DataFrame
    df = pd.DataFrame(data)

    df.to_csv("company data", index= False)




search(company_name_list["company_name"][0])
fetch_results(company_name_list["company_name"][0])
driver.quit()
