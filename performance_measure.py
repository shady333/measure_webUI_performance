import contextlib
import time
import speedtest
import datetime
import os.path

from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

def speed_measure():
    st = speedtest.Speedtest()
    st.get_best_server()
    return st.download()

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed

def write_info_to_file(url, backend, frontend, connection_speed):
    file_name = "results.csv"
    separator=","
    nextline="\r"
    if(not os.path.isfile(file_name) or os.stat(file_name).st_size == 0):
        file = open(file_name, "w+")
        file.write("TIME" + separator + "URL" + separator + "BACKEND"
                   + separator + "FRONTEND" + separator + "CONNECTION" + nextline)
        file.close()

    file = open(file_name, "a+")
    file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+separator+url+separator+str(backend)
               +separator+str(frontend)+separator+str(connection_speed)+nextline)
    file.close()

def detectTimings(name, driver):
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backendPerformance = responseStart - navigationStart
    frontendPerformance = domComplete - responseStart
    '''speed_measure()'''
    download_speed = ""
    print(name)
    print("Back End: %s" % backendPerformance)
    print("Front End: %s" % frontendPerformance)
    print("Download Speed: %s" % download_speed)
    write_info_to_file(driver.current_url, backendPerformance, frontendPerformance, download_speed)
    return backendPerformance, frontendPerformance

@contextlib.contextmanager
def wait_for_page_load(self, timeout=200):
    self.log.debug("Waiting for page to load at {}.".format(self.driver.current_url))
    old_page = self.find_element_by_tag_name('html')
    yield
    WebDriverWait(self, timeout).until(staleness_of(old_page))


