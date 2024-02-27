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
import openpyxl
from openpyxl import load_workbook
import time
import re

path = 'Autorizações.xlsx'
df = pd.read_excel(path)
result = []
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
            
def salva(resultado):
  wb = openpyxl.load_workbook(path)
  ws = wb.active
  ws.cell(row=counter+2, column=2).value = resultado
  wb.save(path)

def salvaResultado():
  wb = openpyxl.load_workbook(path)
  ws = wb.active
  for b in range(len(result)):
      temp = result[b]
      ws.cell(row=b+2, column=2).value = temp
  wb.save(path)

def lancarBiomedico():
  i = 1
  while i <= 6:
    try:
      time.sleep(0.6)
      rows[1].find_element(By.XPATH,"//td[7]/div/a").click()
      time.sleep(0.3)
      rows[1].find_element(By.XPATH,"//td[7]/div/div/div/input").click()
      time.sleep(0.1)
      rows[1].find_element(By.XPATH,"//td[7]/div/div/div/input").clear()
      time.sleep(0.1)
      rows[1].find_element(By.XPATH,"//td[7]/div/div/div/input").send_keys("glauceni")
      time.sleep(0.3)
      rows[1].find_element(By.XPATH,"//td[7]/div/div/div/input").send_keys(Keys.ENTER)
      time.sleep(0.3)
      rows[1].find_element(By.XPATH,"//td[7]/div/div/ul/table/tbody/tr[2]/td[2]/div").click()
      time.sleep(0.3)
      rows[1].find_element(By.XPATH,"//td[9]/div/a").click()
      time.sleep(0.3)
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
  exames = driver.find_elements(By.XPATH,"//table[@id='grid_info']/tbody/tr/td[3]")
  for i in range(len(cbos)):
    if cbos[i].text == "Selecione uma opção"  or cbos[i].text == "...":
      examesProblema.append(exames[i+1].text)
  s = ' e '.join(examesProblema)
  return s

def procTextTd(h,i):
  return driver.find_element(By.XPATH,f"//table[@id='grid_busca']/tbody/tr[{h}]/td[{i}]").text

def salvaTd(innerText,col):
  wb = openpyxl.load_workbook(path)
  ws = wb.active
  ws.cell(row=counter+2, column=col).value = innerText
  wb.save(path)

     
try:
  log = []
  driver = webdriver.Chrome()
  driver.maximize_window()
  action = ActionChains(driver)
  driver.get("http://c2896prd.cloudmv.com.br/sigss/login")
  time.sleep(1)
  t5 = WebDriverWait(driver, 5)

  usuario = "04957832188"
  senha = "36615886"

  t5.until(EC.element_to_be_clickable((By.ID,'login.login'))).send_keys(usuario)
  t5.until(EC.element_to_be_clickable((By.ID,'login.senha'))).send_keys(senha)
  time.sleep(1)
  t5.until(EC.element_to_be_clickable((By.ID,'entrar'))).click()
  t5.until(EC.element_to_be_clickable((By.XPATH,'//button/span[text()="Atendimento"]'))).click()
  t5.until(EC.element_to_be_clickable((By.XPATH,'//button/span[text()="Faturamento"]'))).click()
  t5.until(EC.element_to_be_clickable((By.XPATH,'//a/span[text()="Autenticação"]'))).click()

  sucesso = 0
  problemas = 0
  jaAutenticadas = 0
  pulei = 0
  print("Lista tem " + str(len(df.index)) + " guias")
  for counter in range(len(df.index)):
    cod = df.iloc[counter,0]
    result = df.iloc[counter,1]
    if result == "Guia autenticada com sucesso" or result == "Guia já autenticada!" or "Erro" in str(result):
      pulei += 1
      print(cod + " - Pulei " + str(pulei))
      continue
    for i in range(2):
      k = i + 2
      time.sleep(1)
      WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.ID,'competencia_chzn'))).click()
      time.sleep(0.5)
      t5.until(EC.element_to_be_clickable((By.ID,f'competencia_chzn_o_{k}'))).click()
      time.sleep(0.5)
      t5.until(EC.element_to_be_clickable((By.ID,'codBar'))).clear()
      t5.until(EC.element_to_be_clickable((By.ID,'codBar'))).send_keys(cod)
      time.sleep(0.5)
      t5.until(EC.element_to_be_clickable((By.ID,'codBar'))).send_keys(Keys.ENTER)
      time.sleep(1)

      WebDriverWait(driver, 10).until( AnyEc(
      EC.element_to_be_clickable(
          (By.XPATH,'//button/span[contains(.,"OK")]')),
      EC.element_to_be_clickable(
          (By.XPATH,'//button/span[contains(.,"Gravar")]')) ))
      try:
        classMsgSistema = driver.find_element(By.XPATH, "//div[./div/span[contains(text(),'Mensagem do sistema')]]").get_attribute('class')
        msgSistema = driver.find_element(By.XPATH, "//div[./div/span[contains(text(),'Mensagem do sistema')]]").get_attribute('innerText')
        if "display-block" in classMsgSistema and "já foi autenticado" in msgSistema:
          jaAutenticadas += 1
          print(cod + " - Guia já autenticada!")
          salva("Guia já autenticada!")
          t5.until(EC.element_to_be_clickable((By.XPATH,'//button/span[contains(., "OK")]'))).click()
          break
        if "display-block" in classMsgSistema and "fora da faixa" in msgSistema:
          t5.until(EC.element_to_be_clickable((By.XPATH,'//button/span[contains(., "OK")]'))).click()
          if i == 2:
            print(cod + " - Guia fora da data de autenticação!")
            salva("Guia está fora da faixa permitida para a competência")
          continue
      except: pass
      
      el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "load_grid_info")))
      WebDriverWait(driver, 10).until(lambda d: 'display: block' not in el.get_attribute('style'))

      styleGrid = driver.find_element(By.XPATH, "//div[./div/span[contains(text(),'Informações Obrigatórias')]]").get_attribute('style')
      if "display: block" in styleGrid:
        try:
          rows = driver.find_elements(By.XPATH,"//table[@id='grid_info']/tbody/tr")
          if not rows[1].find_element(By.XPATH,"//td[7]/select").get_attribute("disabled"):
            lancarBiomedico()
            confere = confereCbos()
            if confere:
              driver.find_element(By.XPATH, "//div[9]/div[3]/div/button[2]").click()
              problemas += 1
              print(cod +" - "+ confere)
              salva("Erros no(s) exame(s): " + confere)
              break
               
          time.sleep(1.3)
          driver.find_element(By.XPATH, "//button/span[contains(.,'Gravar')]").click()
          try:
            classMsgSistema = driver.find_element(By.XPATH, "//div[./div/span[contains(text(),'Mensagem do sistema')]]").get_attribute('class')
            msgSistema = driver.find_element(By.XPATH, "//div[./div/span[contains(text(),'Mensagem do sistema')]]").get_attribute('innerText')
            if "display-block" in classMsgSistema and "CBO não informado!" in msgSistema:
              t5.until(EC.element_to_be_clickable((By.XPATH,'//button/span[contains(., "OK")]'))).click()
              problemas += 1
              print(cod + " - Não foi possível autenticar a guia!")
              salva("Não foi possível autenticar a guia!")
              driver.find_element(By.XPATH, "//div[9]/div[3]/div/button[2]").click()
              time.sleep(0.5)
              break
          except: pass
          try:
            el = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//div[./div/span[contains(text(),'Informações Obrigatórias')]]")))
            WebDriverWait(driver, 10).until(lambda d: 'display: block' not in el.get_attribute('style'))
            sucesso += 1
            print(cod + " - Guia autenticada com sucesso")
            salva("Guia autenticada com sucesso")
            time.sleep(0.5)
            grid = driver.find_elements(By.XPATH,"//table[@id='grid_busca']/tbody/tr")
            tamanhoGrid = len(grid)
            for i in range(2, 9):
              salvaTd(procTextTd(tamanhoGrid,i),i+1)
            salvaTd(time.asctime(),10)
            break
          except:
            problemas += 1
            print(cod + " - Não foi possível autenticar a guia!")
            salva("Não foi possível autenticar a guia!")
            driver.find_element(By.XPATH, "//div[9]/div[3]/div/button[2]").click()
            time.sleep(0.5)
            break
        except :
          problemas += 1
          time.sleep(1)
          print(cod + " - Não foi possível autenticar a guia!")
          salva("Não foi possível autenticar a guia!")
          driver.find_element(By.XPATH, "//div[9]/div[3]/div/button[2]").click()
          el = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//div[./div/span[contains(text(),'Informações Obrigatórias')]]")))
          WebDriverWait(driver, 10).until(lambda d: 'display: block' not in el.get_attribute('style'))
          break
      el = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//div[./div/span[contains(text(),'Informações Obrigatórias')]]")))
      WebDriverWait(driver, 10).until(lambda d: 'display: block' not in el.get_attribute('style'))

  finalID = driver.find_elements(By.XPATH,"//table[@id='grid_busca']/tbody/tr/td[2]")
  finalNome = driver.find_elements(By.XPATH,"//table[@id='grid_busca']/tbody/tr/td[4]")
  finalData = driver.find_elements(By.XPATH,"//table[@id='grid_busca']/tbody/tr/td[5]")
  finalLocal = driver.find_elements(By.XPATH,"//table[@id='grid_busca']/tbody/tr/td[6]")
  finalQtdAut = driver.find_elements(By.XPATH,"//table[@id='grid_busca']/tbody/tr/td[7]")
  finalQtdReal = driver.find_elements(By.XPATH,"//table[@id='grid_busca']/tbody/tr/td[8]")
  gridfinal = [finalID,finalNome,finalData,finalLocal,finalQtdAut,finalQtdReal]
  guia = 0
  dadosGuia=[]
  wb = openpyxl.load_workbook(path)
  ws = wb["Planilha2"]
  linha = len(ws['A'])

  for guia in range(len(finalNome)):
    if guia == 0:
      continue
    dadosGuia=[]
    for i in range(6):
      if i == 0:
        ws.cell(row=linha+guia, column=i+1).value = gridfinal[i][guia].get_attribute("title")
        dadosGuia.append("EXAM-"+gridfinal[i][guia].text)
      ws.cell(row=linha+guia, column=i+1).value = gridfinal[i][guia].text
      dadosGuia.append(gridfinal[i][guia].text)
    ws.cell(row=linha+guia, column=7).value = time.asctime(time.localtime())
    k =" ".join(dadosGuia)
  wb.save(path)
      
  print(str(counter+1) + " autorizações trabalhadas!")
  print(str(sucesso) + " autorizações autenticadas com sucesso!")
  print(str(problemas) + " autorizações com erros!")
  print(str(jaAutenticadas) + " autorizações novas que tentei autenticar, mas já estavam autenticadas!")
  print(str(pulei) + " autorizações estavam na lista mas foram passadas em outra rotina anterior")
except RuntimeError as error:
  print(error)