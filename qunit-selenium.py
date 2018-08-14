#!/usr/bin/env python3
import time
import selenium
from base64 import b64encode
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml import etree
import sys
import re

def buildUrl(args):
    user = args[1]
    password = args[2]
    url = args[3]
    url = re.split("(http:\/\/|https:\/\/)", url)
    newurl = url[1] + user + ":" + password + "@" + url[2]
    return newurl

timetowait = sys.argv[4]
url = buildUrl(sys.argv);
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('chromedriver')
driver = webdriver.Chrome(chrome_options = options)  # Optional argument, if not specified will search path.
driver.get(url);
time.sleep(int(timetowait))
source = driver.page_source
driver.quit()
soup = bs(source, 'html.parser')
passedtests = soup.findAll("li", {"class":"pass"})
failedtests = soup.findAll("li", {"class":"fail"})
if(len(failedtests) > 0):
    top = Element("Errors")
    for test in failedtests:
        try:
            child = SubElement(top, 'Error')
            SubElement(child, 'module-name').text = test.findAll("span", {"class" : "module-name" })[0].getText()
            SubElement(child, 'test-name').text = test.findAll("span", {"class" : "test-name" })[0].getText()
            SubElement(child, 'test-message').text = test.findAll("span", {"class" : "test-message" })[0].getText()
            SubElement(child, 'test-expected').text = test.findAll("tr", {"class" : "test-expected" })[0].td.getText()
            SubElement(child, 'test-actual').text = test.findAll("tr", {"class" : "test-actual" })[0].td.getText()
            SubElement(child, 'test-diff').text = test.findAll("tr", {"class" : "test-diff" })[0].td.getText()
            SubElement(child, 'test-source').text = test.findAll("tr", {"class" : "test-source" })[0].td.getText()
        except:
            pass

    print(tostring(top))