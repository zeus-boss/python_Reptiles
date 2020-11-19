from selenium import webdriver

driver = webdriver.Chrome(executable_path="D:\ProgramApp\chromedriver\chromedriver73.exe")

driver.get("https://www.baidu.com/")
driver.implicitly_wait(2)
driver.execute_script("window.open('https://www.douban.com/')")
driver.switch_to.window(driver.window_handles[1])

print(driver.page_source)