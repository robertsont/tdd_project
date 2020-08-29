from selenium import webdriver
from .base import FunctionalTest

def quit_if_possible(browser):
    try: browser.quit()
    except: pass