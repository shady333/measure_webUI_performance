import time
from selenium import webdriver
from performance_measure import detectTimings, wait_for_page_load
from configparser import ConfigParser
from selenium.webdriver.chrome.options import Options

main_counter = 0
driver = None
timeout_between_sessions = 60

def reinit_driver():
    global driver
    config = ConfigParser()
    config.read('ConfigFile.properties')
    driver_path = config.get('BrowserExecutables', 'chrome.driver')
    if (driver != None):
        driver.quit()
    options = Options()
    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    driver.minimize_window()

def start_performance_runner(web_url, message_log='Page load'):
    wait_timeout = 300
    reinit_driver()
    try:
        driver.get(web_url)
        wait_for_page_load(wait_timeout)
        detectTimings(message_log, driver)
    except:
        print("Something bad happened inside. Continue...")
    driver.quit()

while True:
    try:
        for x in range(10):
            main_counter += 1
            print("Iteration: ", main_counter)
            start_performance_runner("http://gmail.com", "Gmail")

    except:
        print("Something bad happened. Continue...")
    print("Wait for some time (sec)", timeout_between_sessions)
    time.sleep(timeout_between_sessions)