
from selenium import webdriver
import time

driver = webdriver.Chrome(executable_path="E:\chromedriver\chromedriver73.exe")

driver.get("https://www.baidu.com")

time.sleep(4)

driver.quit()