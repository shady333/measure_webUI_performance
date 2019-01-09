import contextlib
import time
import speedtest
import datetime
import os.path
import threading
import math

from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

lck = threading.Lock()

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
            print('%r  %2,2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def write_info_to_file(name, url, backend, frontend, connection_speed):
    global lck
    file_name = "results.csv"
    separator=","
    nextline="\r"
    lck.acquire()
    if(not os.path.isfile(file_name) or os.stat(file_name).st_size == 0):
        file = open(file_name, "w+")
        file.write("TIME" + separator + "NAME" + separator+ "URL" + separator + "BACKEND"
                   + separator + "FRONTEND" + separator + "CONNECTION" + nextline)
        file.close()

    file = open(file_name, "a+")
    file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+separator+name+separator+url+separator+str(backend)
               +separator+str(frontend)+separator+"\""+str(convert_size(connection_speed)).replace(".", ",")+"\""+nextline)
    file.close()
    lck.release()

def detectTimings(name, driver):
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backendPerformance = responseStart - navigationStart
    frontendPerformance = domComplete - responseStart
    '''speed_measure()'''
    try:
        download_speed = 0#speed_measure()
    except:
        download_speed = 0
    print(name)
    print("Back End: %s" % backendPerformance)
    print("Front End: %s" % frontendPerformance)
    print("Download Speed: %s" % download_speed)
    write_info_to_file(name, driver.current_url, backendPerformance, frontendPerformance, download_speed)
    return backendPerformance, frontendPerformance

@contextlib.contextmanager
def wait_for_page_load(self, timeout=200):
    self.log.debug("Waiting for page to load at {}.".format(self.driver.current_url))
    old_page = self.find_element_by_tag_name('html')
    yield
    WebDriverWait(self, timeout).until(staleness_of(old_page))


