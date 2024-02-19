from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import undetected_chromedriver as uc
import pandas as pd
import time
import re

driver = webdriver.Chrome()
driver.maximize_window()
action = ActionChains(driver)
#driver.get('https://nowsecure.nl')
#time.sleep(4)
driver.get("http://c2896prd.cloudmv.com.br/sigss/login")
time.sleep(1)
t5 = WebDriverWait(driver, 5)
df = pd.read_excel('Autorizações.xlsx')

usuario = "04957832188"
senha = "36615886"

t5.until(EC.element_to_be_clickable((By.ID,'login.login'))).send_keys(usuario)
t5.until(EC.element_to_be_clickable((By.ID,'login.senha'))).send_keys(senha)
time.sleep(1)
t5.until(EC.element_to_be_clickable((By.ID,'entrar'))).click()
#time.sleep(3)
#t5.until(EC.element_to_be_clickable((By.CLASS_NAME,'menu-icon-nav sigss-icon'))).click()
time.sleep(1)
t5.until(EC.element_to_be_clickable((By.XPATH,'//button/span[text()="Atendimento"]'))).click()
time.sleep(1)
t5.until(EC.element_to_be_clickable((By.XPATH,'//button/span[text()="Faturamento"]'))).click()
time.sleep(1)
t5.until(EC.element_to_be_clickable((By.XPATH,'//a/span[text()="Autenticação"]'))).click()



for counter in range(len(df.index)):
  cod = df.iloc[counter,0]
  t5.until(EC.element_to_be_clickable((By.ID,'competencia_chzn'))).click()
  t5.until(EC.element_to_be_clickable((By.ID,'competencia_chzn_o_1'))).click()
  t5.until(EC.element_to_be_clickable((By.ID,'codBar'))).send_keys(cod)
  t5.until(EC.element_to_be_clickable((By.ID,'codBar'))).send_keys(Keys.ENTER)

time.sleep(1)