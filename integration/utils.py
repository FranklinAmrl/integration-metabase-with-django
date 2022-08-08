import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

def get_iframe(url):
    options = Options()
    # activate the following two lines to run in headless mode.
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
    # /usr/bin/chromedriver is the path where I've installed chromedriver.
    driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=options)
    driver.get(url)
    # Wait till iframe loads
    sleep(5)
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML").encode('utf-8').strip()
    # Now you have the fully-loaded HTML, you may continue to use getElementByTagName or a different library like bs4 to extract the content of the iframe. 
    driver.close()
    return html