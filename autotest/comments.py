from selenium.webdriver.common.by import By
from RandomWordGenerator import RandomWord
import random
from selenium.webdriver.support.select import Select

rw = RandomWord(max_word_size = 13,
                constant_word_size=True,
                include_digits=False,
                special_chars=r"@_!#$%^&*()<>?/\|}{~:",
                include_special_chars=False)

def comments(driver, address):
    result_add = add(driver, address)
    if not result_add:
        return False
    
    return True


def add(driver, address):
    # try:
        data = {
            'text':rw.generate(),
            'rating': 0,
        }
        driver.get(f"{address}/comments/create/1")
        input_text = driver.find_element(By.ID, "text")
        input_rating = driver.find_element(By.ID, "rating")
        
        
        rating_select = Select(driver.find_element(By.ID, "rating"))
        rating_select.select_by_index(2)
        input_title = driver.find_element(By.ID, "text")
        
        input_text.send_keys(data['text'])
        input_rating.send_keys(data['rating'])
        
        
        driver.find_element(By.ID, "submit-btn").click()
        if "Отзыв добавлен" in driver.find_element(By.XPATH, "/html/body/div/div").text:
            return True
        else:
            return False
    # except:
    #     return False