from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

'''
Data sources on Google Data Studio can be saved in the cache for a faster vizualization but the dataset can only be refreshed automatically once a day at best
The following script use Selenium to execute this refresh, by opening the data source (from its url) and pressing the 'Save and extract' button
It is therefore possible to refresh the dataset at a desired frequency while keeping a fast visualization.
The script requires the user to login to their Google account. It will not work if the 2 factor authentication is activated.
'''


def refresh_data(url):
	driver = webdriver.Chrome('./chromedriver')
	driver.get("https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin")

	mail_address = ''
	password = ''

	# Find login field
	login_field = WebDriverWait(driver, 10).until(
	    EC.presence_of_element_located((By.ID, 'identifierId')))
	login_field.send_keys(mail_address)

	# Click next button
	driver.find_element_by_id('identifierNext').click()

	# Find password field
	password_field = WebDriverWait(driver, 10).until(
	    EC.presence_of_element_located((By.ID, 'password')))
	password_field = password_field.find_element_by_tag_name('input')
	password_field.send_keys(password)

	# Click next button
	driver.find_element_by_id('passwordNext').click()

	time.sleep(2)
	
	driver.get(url)
	driver.find_element_by_xpath('//*[@id="body"]/div/div/shade/div/div[3]/div/div/detail/div/div[1]/detail-navigation/div/div[1]/button[1]/div[2]').click()
	driver.find_element_by_xpath('//*[@id="connector-container"]/div/div/snapshot-config/dataview-editor/div/div/dataview-editor-summary/div/div[2]/button').click()
	







