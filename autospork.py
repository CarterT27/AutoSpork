import os
import time
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

try:
  username = os.getenv('USERNAME')
  password = os.getenv('PASSWORD')
except:
  print('Please create a .env file with your username and password stored as USERNAME and PASSWORD on their own lines')

driver = webdriver.Chrome(options=chrome_options)

def login(url,usernameName, username, passwordName, password, submit_buttonSelector):
   driver.get(url)
   driver.find_element_by_name(usernameName).send_keys(username)
   time.sleep(1)
   driver.find_element_by_name(passwordName).send_keys(password)
   time.sleep(1)
   driver.find_element_by_css_selector(submit_buttonSelector).click()
   time.sleep(1)

def sporkLogin():
  try:
    login("https://app.spork.school/", "username", username, "password", password, ".ui.grey.button")
    print('Login successful')
    time.sleep(1)
    driver.find_element_by_css_selector('a.item.schedule').click()
    time.sleep(1)
  except Exception as e:
    print(e)

def isLoggedIn():
  try:
    driver.find_element_by_css_selector('a.active.item.schedule').click()
    return True
  except:
    return False

def joinClass():
  if isLoggedIn():
    print('Logging into class')
    try:
      # Find green button
      driver.find_element_by_css_selector('button.ui.green.compact.button').click()
      print('Successfully joined class')
    except:
      print('Class has not started yet')
      print('Trying again in 10 seconds')
      time.sleep(10)
      joinClass()
  else:
    sporkLogin()

classStartTimes = ['14:30', '15:25', '16:20', '17:15', '18:10', '19:05', '20:00', '21:55', '22:50'] #All converted to UTC
classStartTimes.remove('18:10') #Lunch Period UTC

#Scheduling
for startTime in classStartTimes:
  schedule.every().day.at(startTime).do(joinClass)

#Run
sporkLogin()
time.sleep(1)
while(True):
  schedule.run_pending()
  time.sleep(1)