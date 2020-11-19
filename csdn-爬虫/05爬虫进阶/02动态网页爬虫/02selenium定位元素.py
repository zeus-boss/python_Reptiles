from selenium import webdriver

driver = webdriver.Chrome(executable_path="D:\ProgramApp\chromedriver\chromedriver73.exe")
driver.get("https://www.baidu.com")

# inputTag = driver.find_element_by_id("kw")
# inputTags = driver.find_elements_by_class_name("s_ipt")[0]
# print(inputTags)
# inputTag = driver.find_element_by_name("wd")
# inputTag = driver.find_element_by_tag_name("input")
# inputTag = driver.find_element_by_xpath("//input[@id='kw']")
inputTag = driver.find_element_by_css_selector("#form #kw")
inputTag.send_keys("python")