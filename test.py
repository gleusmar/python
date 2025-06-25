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
#import undetected_chromedriver as uc
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import time
from io import StringIO
from sheetsApi import getAutorizacoes
from sheetsApi import atualizaCelula
from sheetsApi import atualizaCelulas

log = []
driver = webdriver.Chrome()
driver.maximize_window()
action = ActionChains(driver)
driver.get("http://2896prd.cloudmv.com.br/sigss")
tempo = WebDriverWait(driver, 5)
usuario = "04957832188"
senha = "XLGPG@x@UQ9JTQv"


class AnyEc:
    def __init__(self, *args):
        self.ecs = args
    def __call__(self, driver):
        for fn in self.ecs:
            try:
                res = fn(driver)
                if res:
                    return True
            except:
                pass
def logaAcessa():
  tempo.until(EC.element_to_be_clickable((By.ID,'username'))).send_keys(usuario)
  tempo.until(EC.element_to_be_clickable((By.ID,'password'))).send_keys(senha)
  tempo.until(EC.element_to_be_clickable((By.NAME,'submit'))).click()
  tempo.until(EC.element_to_be_clickable((By.XPATH,'//button/span[text()="Atendimento"]'))).click()
  tempo.until(EC.element_to_be_clickable((By.XPATH,'//button/span[text()="Faturamento"]'))).click()
  tempo.until(EC.element_to_be_clickable((By.XPATH,'//a/span[text()="Autenticação"]'))).click()
  print("logado")            
def lancarBiomedico():
  i = 1
  while i <= 6:
    try:
      time.sleep(0.2)
      rows[1].find_element(By.XPATH,"//td[7]/div/a").click()
      time.sleep(0.2)
      rows[1].find_element(By.XPATH,"//td[7]/div/div/div/input").click()
      time.sleep(0.2)
      rows[1].find_element(By.XPATH,"//td[7]/div/div/div/input").clear()
      time.sleep(0.2)
      rows[1].find_element(By.XPATH,"//td[7]/div/div/div/input").send_keys("glauceni")
      time.sleep(0.2)
      rows[1].find_element(By.XPATH,"//td[7]/div/div/div/input").send_keys(Keys.ENTER)
      time.sleep(0.2)
      rows[1].find_element(By.XPATH,"//td[7]/div/div/ul/table/tbody/tr[2]/td[2]/div").click()
      time.sleep(0.2)
      rows[1].find_element(By.XPATH,"//td[9]/div/a").click()
      time.sleep(0.2)
      rows[1].find_element(By.XPATH,"//td[9]/div/div/div/input").click()
      time.sleep(0.1)
      rows[1].find_element(By.XPATH,"//td[9]/div/div/div/input").clear()
      time.sleep(0.1)
      rows[1].find_element(By.XPATH,"//td[9]/div/div/div/input").send_keys("221205")
      time.sleep(0.3)
      rows[1].find_element(By.XPATH,"//td[9]/div/div/div/input").send_keys(Keys.ENTER)
      time.sleep(0.3)
      break
    except:
      i += 1
      print(cod + " - Tentativa " + str(i))

def confereCbos():
  examesProblema = []
  cbos = driver.find_elements(By.XPATH,"//table[@id='grid_info']/tbody/tr/td[9]/div/a")
  profissionais = driver.find_elements(By.XPATH,"//table[@id='grid_info']/tbody/tr/td[7]/div/a")
  exames = driver.find_elements(By.XPATH,"//table[@id='grid_info']/tbody/tr/td[3]")
  examesTodos = []
  for i in range(len(cbos)):
    examesTodos.extend([exames[i+1].text, profissionais[i].text, cbos[i].text])
    if "GLAUCENI" not in str(profissionais[i].text) or cbos[i].text == "Selecione uma opção"  or cbos[i].text == "...":
      examesProblema.append(exames[i+1].text)
  if (examesProblema):
    examesProblema.insert(0, "Guia autorizada para: " + profissionais[0].text)
  s = ' e '.join(examesProblema)
  t = ';'.join(examesTodos)
  return s, t

def ultimaLinhaAutenticados():
  table = driver.find_element(By.ID,"grid_busca")
  rows = table.find_elements(By.TAG_NAME,"tr")
  lastrow = rows[len(rows)-1]
  tds = lastrow.find_elements(By.TAG_NAME,"td")
  array=[]
  for td in tds:
    array.append(td.text)
  return [array]

def esperaGridEsconder():
  el = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//div[./div/span[contains(text(),'Informações Obrigatórias')]]")))
  WebDriverWait(driver, 30).until(lambda d: 'display: block' not in el.get_attribute('style'))

df = pd.DataFrame(getAutorizacoes())
sucesso = 0
problemas = 0
jaAutenticadas = 0
pulei = 0
print("Lista tem " + str(len(df.index)) + " guias")
logaAcessa()

for counter in range(len(df.index)):
  cod = df.iloc[counter,0]
  result = df.iloc[counter,4]
  if result == "Guia autenticada com sucesso!" or result == "Guia já autenticada!" or "Erro" in str(result) or "O agendamento de exame da guia" in str(result): 
    pulei += 1
    continue
  print(counter)
  h = 1
  while h <= 4:
    try:
      for i in range(3):
        k = i + 1
        time.sleep(1)
        WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.ID,'competencia_chzn'))).click()
        tempo.until(EC.element_to_be_clickable((By.ID,f'competencia_chzn_o_{k}'))).click()
        tempo.until(EC.element_to_be_clickable((By.ID,'codBar'))).clear()
        tempo.until(EC.element_to_be_clickable((By.ID,'codBar'))).send_keys(cod)
        tempo.until(EC.element_to_be_clickable((By.ID,'codBar'))).send_keys(Keys.ENTER)
        WebDriverWait(driver, 10).until( AnyEc(EC.element_to_be_clickable((By.XPATH,'//button/span[contains(.,"OK")]')),EC.element_to_be_clickable((By.XPATH,'//button/span[contains(.,"Gravar")]')) ))
        try:
          classMsgSistema = driver.find_element(By.XPATH, "//div[./div/span[contains(text(),'Mensagem do sistema')]]").get_attribute('class')
          msgSistema = driver.find_element(By.XPATH, "//div[./div/span[contains(text(),'Mensagem do sistema')]]").get_attribute('innerText')
          if "display-block" in classMsgSistema and "já foi autenticado" in msgSistema:
            jaAutenticadas += 1
            print(cod + " - Guia já autenticada!")
            atualizaCelula(counter+2,5,"Guia já autenticada!")
            tempo.until(EC.element_to_be_clickable((By.XPATH,'//button/span[contains(., "OK")]'))).click()
            break
          if "display-block" in classMsgSistema and "fora da faixa" in msgSistema:
            tempo.until(EC.element_to_be_clickable((By.XPATH,'//button/span[contains(., "OK")]'))).click()
            continue
          if "display-block" in classMsgSistema and ("O agendamento" in msgSistema or "O Agendamento" in msgSistema or "Cliente" in msgSistema):
            problemas += 1
            print(cod + " - " + msgSistema)
            atualizaCelula(counter+2,5,msgSistema)
            tempo.until(EC.element_to_be_clickable((By.XPATH,'//button/span[contains(., "OK")]'))).click()
            break
        except: pass
        
        el = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "load_grid_info")))
        WebDriverWait(driver, 30).until(lambda d: 'display: block' not in el.get_attribute('style'))

        styleGrid = driver.find_element(By.XPATH, "//div[./div/span[contains(text(),'Informações Obrigatórias')]]").get_attribute('style')
        if "display: block" in styleGrid:
          try:
            rows = driver.find_elements(By.XPATH,"//table[@id='grid_info']/tbody/tr")
            if not rows[1].find_element(By.XPATH,"//td[7]/select").get_attribute("disabled"):
              lancarBiomedico()
            confere, listaExames = confereCbos()
            atualizaCelula(counter+2,15,listaExames)
            if confere:
              driver.find_element(By.XPATH, "//div[9]/div[3]/div/button[2]").click()
              problemas += 1
              print(cod +" - "+ confere)
              atualizaCelula(counter+2,5,"Erros no(s) exame(s): " + confere)
              break      
            time.sleep(1.3)
            driver.find_element(By.XPATH, "//button/span[contains(.,'Gravar')]").click()

            try:
              classMsgSistema = driver.find_element(By.XPATH, "//div[./div/span[contains(text(),'Mensagem do sistema')]]").get_attribute('class')
              msgSistema = driver.find_element(By.XPATH, "//div[./div/span[contains(text(),'Mensagem do sistema')]]").get_attribute('innerText')
              if "display-block" in classMsgSistema and "CBO não informado!" in msgSistema:
                tempo.until(EC.element_to_be_clickable((By.XPATH,'//button/span[contains(., "OK")]'))).click()
                problemas += 1
                print(cod + " - Não foi possível autenticar a guia!1")
                atualizaCelula(counter+2,5,"Não foi possível autenticar a guia!")
                driver.find_element(By.XPATH, "//div[9]/div[3]/div/button[2]").click()
                time.sleep(0.5)
                break
            except: pass
            try:
              esperaGridEsconder()
              sucesso += 1
              print(cod + " - Guia autenticada com sucesso!")
              atualizaCelulas(counter+2,ultimaLinhaAutenticados())
              time.sleep(0.5)
              break
            except:
              problemas += 1
              print(cod + " - Não foi possível autenticar a guia!2")
              atualizaCelula(counter+2,5,"Não foi possível autenticar a guia!")
              driver.find_element(By.XPATH, "//div[9]/div[3]/div/button[2]").click()
              time.sleep(0.5)
              break
          except :
            problemas += 1
            time.sleep(1)
            print(cod + " - Não foi possível autenticar a guia!3")
            atualizaCelula(counter+2,5,"Não foi possível autenticar a guia!")
            driver.find_element(By.XPATH, "//div[9]/div[3]/div/button[2]").click()
            el = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//div[./div/span[contains(text(),'Informações Obrigatórias')]]")))
            WebDriverWait(driver, 10).until(lambda d: 'display: block' not in el.get_attribute('style'))
            break
        esperaGridEsconder()
      break
    except:
      driver.refresh()
      h += 1
      print("Falha " + str(h))
          
print(str(counter+1) + " autorizações trabalhadas!")
print(str(sucesso) + " autorizações autenticadas com sucesso!")
print(str(problemas) + " autorizações com erros!")
print(str(jaAutenticadas) + " autorizações novas que tentei autenticar, mas já estavam autenticadas!")
print(str(pulei) + " autorizações estavam na lista mas foram passadas em outra rotina anterior")
