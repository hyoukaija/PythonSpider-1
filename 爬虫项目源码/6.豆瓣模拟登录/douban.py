from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.PhantomJS()
driver.get('http://www.douban.com')

# 输入账号密码
driver.find_element_by_name('form_email').send_keys('xx@xx.com')
driver.find_element_by_name('form_password').send_keys('xxxxx')

# 模拟点击登录
driver.find_element_by_class_name('bn-submit').click()

# 等待3秒
time.sleep(3)

# 登录后截图
driver.save_screenshot('douban.png')

driver.quit()