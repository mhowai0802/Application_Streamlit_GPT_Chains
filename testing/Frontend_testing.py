import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import collections
import time

question_list = ['商湯2023年毛利？']

options = Options()
driver = webdriver.Chrome(options=options)
driver.get('http://localhost:8501/SQL_chain_chi_to_eng')
time.sleep(5)
for question in question_list:
    element = driver.find_element(By.XPATH,'/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div/textarea')
    element.send_keys(question)
    button = driver.find_element(By.XPATH,'/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[3]/div/div/div/div/div/div/div/div/div[3]/button')
    button.click()