#!/usr/bin/env python3

from selenium import webdriver
from random import randrange, random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from time import sleep
import logging
import argparse
import enum
import os.path

def setup_logger(name, verbosity):
    logger = logging.getLogger(name)
    logger.setLevel(verbosity)
    handler = logging.StreamHandler()
    handler.setLevel(verbosity)
    handler.setFormatter(logging.Formatter("%(asctime)s "
                                           "%(levelname)-8s "
                                           "%(name)s: %(message)s",
                                           "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    return logger

class LogLevel(enum.IntEnum):
    debug = logging.DEBUG
    info = logging.INFO
    warn = logging.WARN
    error = logging.ERROR
    fatal = logging.FATAL
    crit = logging.CRITICAL

    def __str__(self):
        return self.name

class Command(enum.Enum):
    login = 1
    update = 2

    def __str__(self):
        return self.name

class BrowserType(enum.Enum):
    chrome = ChromeType.GOOGLE
    chromium = ChromeType.CHROMIUM

def update(browser, timeout):
    logger = logging.getLogger("UPDATE")
    browser.get("https://hh.ru/applicant/resumes")
    wait_page_to_load = WebDriverWait(browser, timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[@data-qa='resume-update-button']"))
    )
    update_buttons = browser.find_elements_by_xpath(
        "//button[@data-qa='resume-update-button']")
    logger.info("Located %d update buttons", len(update_buttons))
    for elem in update_buttons:
        elem.click()
        sleep(1 + 2 * random())
        logger.debug('click!')
    logger.info('Updated!')

def login(browser):
    logger = logging.getLogger("LOGIN")
    browser.get("https://hh.ru/account/login?backurl=%2Fapplicant%2Fresumes")
    wait_page_to_load = WebDriverWait(browser, 3600).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[@data-qa='resume-update-button']"))
    )
    logger.info('Successfully logged in!')

def parse_args():
    def check_loglevel(arg):
        try:
            return LogLevel[arg]
        except (IndexError, KeyError):
            raise argparse.ArgumentTypeError("%s is not valid loglevel" % (repr(arg),))

    def check_command(arg):
        try:
            return Command[arg]
        except (IndexError, KeyError):
            raise argparse.ArgumentTypeError("%s is not valid command" % (repr(arg),))

    def check_browser_type(arg):
        try:
            return BrowserType[arg]
        except (IndexError, KeyError):
            raise argparse.ArgumentTypeError("%s is not valid browser type" % (repr(arg),))

    def check_positive_float(arg):
        def fail():
            raise argparse.ArgumentTypeError("%s is not valid positive float" % (repr(arg),))
        try:
            fvalue = float(arg)
        except ValueError:
            fail()
        if fvalue <= 0:
            fail()
        return fvalue

    parser = argparse.ArgumentParser(
        description="Python script to update your CV",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--timeout",
                        help="webdriver wait timeout",
                        type=check_positive_float,
                        default=10.)
    parser.add_argument("-b", "--browser",
                        help="browser type",
                        type=check_browser_type,
                        choices=BrowserType,
                        default=BrowserType.chromium)
    parser.add_argument("-v", "--verbosity",
                        help="logging verbosity",
                        type=check_loglevel,
                        choices=LogLevel,
                        default=LogLevel.info)
    parser.add_argument("cmd", help="command",
                        type=check_command,
                        choices=Command)
    parser.add_argument("-d", "--data-dir",
                        default=os.path.join(os.path.expanduser("~"),
                                             '.config',
                                             'hhautomate',
                                             'datadir'),
                        help="datadir location",
                        metavar="FILE")
    return parser.parse_args()

def main():
    args = parse_args()
    mainlogger = setup_logger("MAIN", args.verbosity)
    setup_logger("UPDATE", args.verbosity)
    setup_logger("LOGIN", args.verbosity)

    chrome_options = Options()
    if args.cmd is Command.update:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('user-data-dir=' + args.data_dir)
    browser = webdriver.Chrome(
        ChromeDriverManager(chrome_type=args.browser).install(), options=chrome_options)

    try:
        if args.cmd is Command.login:
            login(browser)
        elif args.cmd is Command.update:
            update(browser, args.timeout)
    finally:
        browser.quit()

if __name__ == "__main__":
    main()
