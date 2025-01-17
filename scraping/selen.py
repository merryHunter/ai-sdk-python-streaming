from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import urllib

url = r'https://www.autonation.com/cars-for-sale'
opts = webdriver.ChromeOptions()
opts.headless = True
driver = webdriver.Chrome(opts)
driver.get(url)
time.sleep(4)
WebDriverWait(driver, 10).until(EC.alert_is_present())
driver.switch_to.alert.accept()
try:
    driver.find_element(by=By.XPATH, value='/html/body/div[14]/div[2]/div/div[1]/div/div[2]/div/button[2]').click()
except Exception as e:
    print(e)

time.sleep(10)
cars = driver.find_elements(by=By.CLASS_NAME, value='tile-container')
car_list = []
for i, car in enumerate(cars):
    name = car.find_element(by=By.XPATH, value=f'.//*[@id="srp-tile-vehiclename-{i}"]').text
    price = car.find_element(by=By.XPATH, value=f'.//*[@id="srp-tile-lockedprice-{i}"]').text
    condition = car.find_element(by=By.XPATH, value=f'.//*[@id="srp-tile-stocktype-{i}"]').text
    distance = car.find_element(by=By.XPATH, value=f'.//*[@id="srp-tile-distance-{i}"]').text
    link = car.find_elements(by=By.TAG_NAME, value="a")[0].get_attribute('href')

    car_item = {
        'name': name,
        'price': price,
        "distance": distance,
        "condition": condition,
        'link': link
    }
    car_list.append(car_item)

df = pd.DataFrame(car_list)
timestamp = time.strftime("%Y-%m-%d")
df.to_csv(f'data/cars_{timestamp}.csv', index=False)

driver.quit()
