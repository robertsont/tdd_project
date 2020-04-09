from selenium import webdriver

browser = webdriver.Firefox(executable_path='E:\\Dropbox\\Documents\\self_learning\\tdd_project_folder\\geckodriver.exe')
browser.get('http://localhost:8000')

assert 'Django' in browser.title