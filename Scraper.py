from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time

origin = "SJC"
destination = "MSN"

# keep browser window open after completion
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options = chrome_options)

def button(by, query, idx):
    element = driver.find_elements(by, query, idx)
    element.click()
    return element

def button(by, query):
    return button(by, query, 0)

def run():
    driver.get("https://www.google.com/travel/flights")
    driver.maximize_window()
    driver.implicitly_wait(3)

    time.sleep(1)

    orgn1 = driver.find_element(By.XPATH, "//*[@aria-label='Where from?']")
    orgn1.click()
    driver.implicitly_wait(3)
    
    multi = driver.find_element(By.XPATH, "//button[@aria-label='Origin, Select multiple airports']")
    multi.click()
    driver.implicitly_wait(3)

    remove = driver.find_elements(By.XPATH, "//div[@aria-label='Remove']")[0]
    remove.click()

    orgn2 = driver.find_element(By.XPATH, "//*[@aria-label='Where from? ']")
    orgn2.send_keys(origin)
    orgn2.send_keys(Keys.ENTER)
    driver.implicitly_wait(3)

    done = driver.find_elements(By.XPATH, "//button[@aria-label='Done']")[1]
    done.click()
    driver.implicitly_wait(3)

    dest1 = driver.find_element(By.XPATH, "//input[@aria-label='Where to? ']")
    dest1.click()
    driver.implicitly_wait(3)

    multi = driver.find_element(By.XPATH, "//button[@aria-label='Destination, Select multiple airports']")
    multi.click()
    driver.implicitly_wait(3)

    dest2 = driver.find_elements(By.XPATH, "//*[@aria-label='Where to? ']")[1]
    dest2.send_keys(destination)
    dest2.send_keys(Keys.ENTER)
    driver.implicitly_wait(3)

    done = driver.find_elements(By.XPATH, "//button[@aria-label='Done']")[1]
    done.click()
    driver.implicitly_wait(3)

    type = driver.find_element(By.XPATH, "//*[@aria-labelledby='i6 i7']")
    type.click()
    driver.implicitly_wait(3)

    one_way = driver.find_element(By.XPATH, "//li[@data-value='2']")
    one_way.click()
    
    # dest = driver.find_elements(By.XPATH, "//input[@aria-label='Where to? ']")[0]
    # dest.click()
    # dest.send_keys(destination)
    # driver.implicitly_wait(3)

    # dest = driver.find_element(By.XPATH, "//li[@data-code='"+destination+"']")
    # dest.click()
    # driver.implicitly_wait(3)

    # departure = driver.find_element(By.XPATH, "//input[@aria-label='Departure']")
    # departure.click()
    # time.sleep(1)
    # departure.send_keys("11/12/2024")
    # driver.implicitly_wait(3)
    
if __name__ == "__main__":
    run()
