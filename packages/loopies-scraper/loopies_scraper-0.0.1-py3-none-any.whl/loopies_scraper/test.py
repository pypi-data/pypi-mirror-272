#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import lxml.html
import time, calendar
from datetime import datetime
import os, re, json, logging

from scraper import Scraper

def main():
    logging.getLogger().disabled = False
    log_format = "%(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)

    scraper = Scraper(driver_name='firefox', proxy='default')
    scraper.driver.get('https://www.basketball-reference.com/leagues/')
    

if __name__ == "__main__":
    main()