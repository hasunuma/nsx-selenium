from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time
import yaml
import threading
import argparse

drivers = []
height=0
width=0
pos_height=0
pos_width=0
MAX_ACCESS=15
SELENIUM_IPADDR=""
NSX_IPADDR=""

def access_nsx(arg):
  i = 0
  driver = arg[0]
  name = arg[1]
  passwd = arg[2]
  wait = WebDriverWait(driver, 10)
  print("loop init")
  while(1):
    t = int(time.time())
    if t % 10 == 0:
      if driver.current_url == 'https://'+NSX_IPADDR+'/nsx/#/app/home/overview':
        try:
          driver.find_element(By.CLASS_NAME, 'nav-user').click()
          driver.find_element(By.LINK_TEXT, 'ログアウト').click()
          wait.until(expected_conditions.visibility_of_element_located((By.ID, "username")))
          driver.find_element(By.ID, 'username').send_keys(name)
          driver.find_element(By.ID, 'password').send_keys(passwd)
        except Exception as e:
          print(e)
      elif driver.current_url == 'https://'+NSX_IPADDR+'/nsx/index.html':
        driver.refresh()
      else:
        try:
          driver.find_element(By.NAME, 'submit-btn').click()
        except Exception as e:
          print(e)
          continue
      driver.execute_script('window.scrollTo(document.body.scrollWidth,0);')
      i+=1
      print(t)
    if i >= MAX_ACCESS:
      break
    time.sleep(0.01)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--selenium',required=True)
  parser.add_argument('--nsx',required=True)
  args = parser.parse_args()
  SELENIUM_IPADDR = args.selenium
  NSX_IPADDR = args.nsx
  with open('user.yaml','r') as yml:
    user = yaml.safe_load(yml)
  try:
    th = []
    for i,name in enumerate(user):
      print(name)
      print(user[name]['pass'])
    
      options = Options()
      options.add_argument("--profile-directory=Profile"+str(i))
      options.add_argument("--disable-features=Translate")
      options.set_capability('acceptInsecureCerts',True)
      driver = webdriver.Remote(
         command_executor='http://'+SELENIUM_IPADDR+':4444/wd/hub',
         options=options)
      wait = WebDriverWait(driver, 60)
      if i == 0:
        driver.maximize_window()
        height = driver.get_window_size()['height']
        width = driver.get_window_size()['width']/len(user)
      driver.set_window_size(width, height)
      driver.set_window_position(pos_width,pos_height)
      pos_width+=width
      drivers.append({"driver": driver, "username": name})
      
      driver.get('https://'+NSX_IPADDR+'/')
      driver.find_element(By.ID, 'username').send_keys(name)
      driver.find_element(By.ID, 'password').send_keys(user[name]['pass'])
      driver.find_element(By.NAME, 'submit-btn').click()
      time.sleep(5)
      driver.execute_script('window.scrollTo(document.body.scrollWidth,0);')
      th.append(threading.Thread(target=access_nsx, args=([driver, name, user[name]['pass']],)))
      driver.execute_script('window.scrollTo(document.body.scrollWidth,0);')
    for t in th:
      print(t)
      t.start()
    for t in th:
      t.join()
  finally:
    for d in drivers:
      d["driver"].quit()

