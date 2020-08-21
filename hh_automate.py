#!/usr/bin/env python3

from selenium import webdriver
from random import randint
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import email, password, timeout
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from time import sleep

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("window-size=1400,2100")
chrome_options.add_argument('--disable-gpu')


def main():
    while True:
        try:
            browser = webdriver.Chrome(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=chrome_options)
            browser.get("https://hh.ru/account/login?backurl=%2Fapplicant%2Fresumes")
            wait_page_to_load = WebDriverWait(browser, timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@data-qa='login-input-username']"))
            )
            find_email_input = browser.find_element_by_xpath(
                "//input[@data-qa='login-input-username']")
            find_email_input.send_keys(email)
            find_password_input = browser.find_element_by_xpath(
                "//input[@data-qa='login-input-password']")
            find_password_input.send_keys(password)

            find_submit = browser.find_element_by_xpath(
                "//input[@data-qa='account-login-submit']")
            find_submit.submit()
            find_cv = WebDriverWait(browser, timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[5]/div[2]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div/a[2]/span/span[1]"))
            )
            find_cv.click()
            update_cv = WebDriverWait(browser, timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[6]/div/div/div[3]/div/div/div/div[1]/div[3]/div/div[5]/div/div/div/div[1]/span/button"))
            )
            update_cv.click()

            print('updated')
        #except TimeoutException as exc:
        #    print('Timed out')
        finally:
            pass
        update_period = 60 * 60 * 4 + 60 * randint(1, 20)
        sleep(float(update_period))


if __name__ == "__main__":
    main()
