# coding=utf8
from selenium import webdriver
from selenium.common import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

# chromedriver.exe
driver = webdriver.Chrome(
    executable_path=r'C:\Users\נטלי שוורצר\PycharmProjects\VIA\chromedriver_win32\chromedriver.exe')


class demoblaze:
    def __init__(self, username="NatalieS", password="n12345678"):
        self.username = username
        self.password = password

    def ui_section(self):

        driver.get("https://www.demoblaze.com/")  # Loading page
        driver.find_element(By.ID, "login2").click()  # Login to the system
        time.sleep(3)
        driver.find_element(By.ID, "loginusername").send_keys(self.username)
        driver.find_element(By.ID, "loginpassword").send_keys(self.password)
        driver.find_element(By.XPATH, "//button[text()='Log in']").click()
        time.sleep(3)
        driver.find_element(By.LINK_TEXT, "Nexus 6").click()  # Choose Nexus 6
        time.sleep(4)
        driver.find_element(By.LINK_TEXT, "Add to cart").click()  # Add to the cart Nexus 6 device
        # Accept the alert popup of product added
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                            "#sp_message_container_404503 iframe")))

            driver.find_element(By.CSS_SELECTOR,
                                '[class="message-component message-button no-children pg-accept-button"]').click()

        except UnexpectedAlertPresentException:

            print("Product was added successfully")

        time.sleep(3)
        driver.find_element(By.LINK_TEXT, "Cart").click()  # Move to Cart section

    def api_section(self):
        cart_data = requests.post('https://api.demoblaze.com/viewcart', json={
            'cookie': "TmF0YWxpZVMxNjY0Nzky",
            'flag': True
        })

        if cart_data.status_code != 200:
            raise Exception('Could make the request')

        items = cart_data.json()['Items']
        print(items)

        # Number of items verification
        if len(items) == 1:
            print("1 item was added to the cart")
        else:
            return False, print("Number of items is:", len(items), "and not as was expected")

        # Device id verification
        if items[0]['prod_id'] == 3:
            print("Device id is 3")
        else:
            return False, print("Wrong id number")

        # Get product info by ID
        product_info = requests.get('https://api.demoblaze.com/entries')
        product_info = product_info.json()['Items']

        # Expected product info
        device_model = 'Nexus 6'
        price = 650
        # Product info verification
        for device in product_info:
            if device['id'] == 3:
                if device['title'] == device_model and device['price'] == price:
                    print(f'Device model: {device_model}\nprice: {price}')
                else:
                    return False, print("Wrong device model/price")


ui = demoblaze()
ui.ui_section()
api = demoblaze()
api.api_section()
