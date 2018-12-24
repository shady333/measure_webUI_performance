# measure_webUI_performance

## Prerequirements

Install required packages
pip install selenium

### How to use

Write a simple selenium based scenario

And insert method detectTimings(NAME, DRIVER) to get page load timings from your web page

### Example
Code
```
driver.get('http://gmail.com')
wait_for_page_load(wait_timeout)
detectTimings("Gmail load", driver)
```

Output
```
Gmail load
Back End: 522
Front End: 1804
```
