import contextlib
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

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