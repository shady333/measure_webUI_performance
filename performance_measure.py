import contextlib
import time

from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

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

def detectTimings(name, driver):
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backendPerformance = responseStart - navigationStart
    frontendPerformance = domComplete - responseStart
    print(name)
    print("Back End: %s" % backendPerformance)
    print("Front End: %s" % frontendPerformance)
    return backendPerformance, frontendPerformance

@contextlib.contextmanager
def wait_for_page_load(self, timeout=200):
    self.log.debug("Waiting for page to load at {}.".format(self.driver.current_url))
    old_page = self.find_element_by_tag_name('html')
    yield
    WebDriverWait(self, timeout).until(staleness_of(old_page))


