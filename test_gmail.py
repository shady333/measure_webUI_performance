from selenium import webdriver
from performance_measure import detectTimings, wait_for_page_load, timeit
from configparser import ConfigParser
from selenium.webdriver.chrome.options import Options

wait_timeout = 200

config = ConfigParser()
config.read('ConfigFileLocal.properties')

driver_path = config.get('BrowserExecutables', 'chrome.driver')

options = Options()
# options.set_headless(headless=True)
driver = webdriver.Chrome(options=options, executable_path=driver_path)

@timeit
def open_gmail():
    driver.get('http://gmail.com')
    wait_for_page_load(wait_timeout)

open_gmail()
detectTimings("Gmail load", driver)

driver.quit()

