from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

driver = webdriver.Chrome(executable_path="D:\ProgramApp\chromedriver\chromedriver73.exe")

# driver.get(r"D:\VIPCourse\视频\CSDN爬虫课程\代码\05爬虫进阶\02动态网页爬虫\abc.html")

# div = driver.find_element_by_id("mydiv")
# print(div.get_property("id"))
# print(div.get_property("data-name"))
# print(div.get_attribute("id"))
# print(div.get_attribute("data-name"))

driver.get("https://www.baidu.com/")
# driver.save_screenshot("baidu.png")
btn = driver.find_element_by_id("su")
print(type(btn))