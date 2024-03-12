from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time, sys
from selenium.webdriver.common.by import By

from auth import auth
from comments import comments
from items import items

BASE_ADDRESS = 'http://192.168.50.68:8000'

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(driver_version="122.0.6261.95").install()), options=options)
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(driver_version="2.26").install()))

driver.maximize_window()
driver.implicitly_wait(60)
   
driver.get(BASE_ADDRESS)


result_auth  = auth(driver=driver, address=BASE_ADDRESS)
assert result_auth == True, "Ошибка при авторизации"

result_items  = items(driver=driver, address=BASE_ADDRESS)
assert result_items == True, "Ошибка при добавлении предмета"

result_comments  = comments(driver=driver, address=BASE_ADDRESS)
assert result_comments == True, "Ошибка при добавлении комментария"

driver.close()
driver.quit()
