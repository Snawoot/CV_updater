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

def locate_buttons(browser):
    return list(elem for elem in browser.find_elements_by_xpath(
        "//button[@data-qa='resume-update-button']")
        if "bloko-link" not in elem.get_attribute("class").split()
        )

def buttons_disabled(browser):
    return all(elem.get_attribute("disabled") is not None
               for elem in locate_buttons(browser))

def update(browser, timeout):
    logger = logging.getLogger("UPDATE")
    browser.get("https://hh.ru/applicant/resumes")
    wait_page_to_load = WebDriverWait(browser, timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[@data-qa='resume-update-button']"))
    )
    update_buttons = locate_buttons(browser)
    logger.info("Located %d update buttons", len(update_buttons))
    for elem in update_buttons:
        sleep(1 + 2 * random())
        elem.click()
        logger.debug('click!')
    WebDriverWait(browser, timeout).until(buttons_disabled)
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
                                             'hhautomate'),
                        help="application datadir location",
                        metavar="FILE")
    return parser.parse_args()

class BrowserFactory:
    def __init__(self, profile_dir, browser_type, headless=True):
        chrome_options = Options()
        # option below causes webdriver process remaining in memory
        # chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('user-data-dir=' + profile_dir)
        if headless:
            chrome_options.add_argument('--headless')
        self._options = chrome_options
        self._type = browser_type

    def new(self):
        return webdriver.Chrome(
            ChromeDriverManager(chrome_type=self._type).install(),
            options=self._options)


def do_login(browser_factory):
    browser = browser_factory.new()
    try:
        login(browser)
    finally:
        browser.quit()

def do_update(browser_factory, timeout):
    browser = browser_factory.new()
    try:
        update(browser, timeout)
    finally:
        browser.quit()

def main():
    args = parse_args()
    mainlogger = setup_logger("MAIN", args.verbosity)
    setup_logger("UPDATE", args.verbosity)
    setup_logger("LOGIN", args.verbosity)

    profile_dir = os.path.join(args.data_dir, 'profile')
    browser_factory = BrowserFactory(profile_dir,
                                     args.browser.value,
                                     args.cmd is Command.update)

    if args.cmd is Command.login:
        mainlogger.info("Login mode. Please enter your credentials in opened "
                        "browser window.")
        do_login(browser_factory)
    elif args.cmd is Command.update:
        mainlogger.info("Update mode. Running headless browser.")
        db_path = os.path.join(args.data_dir, 'hhautomate.db')
        do_update(browser_factory, args.timeout)

if __name__ == "__main__":
    main()
