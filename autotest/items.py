from selenium.webdriver.common.by import By
from RandomWordGenerator import RandomWord
import random
from selenium.webdriver.support.select import Select


rw = RandomWord(max_word_size = 13,
                constant_word_size=True,
                include_digits=False,
                special_chars=r"@_!#$%^&*()<>?/\|}{~:",
                include_special_chars=False)

def items(driver, address):
    result_add = add(driver, address)
    if not result_add:
        return False
    
    return True


def add(driver, address):
    # try:
        place = ''
        for i in range(random.randint(1,5)):
            place += rw.generate()
        data = {
            'title':rw.generate(),
            'description': "test",
            'price': random.randint(1, 10000),
            'image': 'C:\elf.png'
        }
        driver.get(f"{address}/items/create")
        input_title = driver.find_element(By.ID, "title")
        input_description = driver.find_element(By.ID, "description")
        input_price = driver.find_element(By.ID, "price")
        input_image = driver.find_element(By.ID, "image")
        
        input_title.send_keys(data['title'])
        input_description.send_keys(data['description'])
        input_price.send_keys(data['price'])
        input_image.send_keys(r'C:\elf.png')
        
        driver.find_element(By.ID, "submit-btn").click()
        print(f"Информация о {data['title']} успешно добавлена")
        print(driver.find_element(By.XPATH, "/html/body/div/div").text)
        title = data['title']
        if f'Информация о "{title}" успешно добавлена' in driver.find_element(By.XPATH, "/html/body/div/div").text:
            return True, 
        else:
            return False
    # except:
    #     return False