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



#options = uc.ChromeOptions()
#options.add_argument("--password-store=basic")
#options.add_argument("--lang=en")
#options.add_experimental_option(
#    "prefs",
#    {
#        "credentials_enable_service": False,
#        "profile.password_manager_enabled": False,
#    },
#)




df = pd.read_excel('Autorizacao Sulamerica PSA 2023 2.xlsx')
print(df)
ds = pd.read_excel('Tabela Sulamerica.xlsx')
print(ds)


driver = webdriver.Chrome()
driver.maximize_window()
action = ActionChains(driver)
#driver.get('https://nowsecure.nl')
#time.sleep(4)
driver.get("https://saude.sulamericaseguros.com.br/prestador/login/")

time.sleep(1)

referenciado = "100000018677"
usuario = "MASTER"
senha = "lab@5886"

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,'sas-box-lgpd-info-accept-btn'))).click()

try:
    
    reffield = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME,'code')))
    reffield.click()
    reffield.clear()
    reffield.send_keys(referenciado)

    userfield = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME,'user')))
    userfield.click()
    userfield.clear()
    userfield.send_keys(usuario)

    passfield = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME,'senha')))
    passfield.click()
    passfield.clear()
    passfield.send_keys(senha)

    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="entrarLogin"]'))).click()

except:
    pass

time.sleep(3)
element = driver.find_element(By.XPATH,'//*[@id="nameCookie"]')
driver.execute_script('arguments[0].scrollIntoView(true);', element)

driver.get("https://saude.sulamericaseguros.com.br/prestador/servicos-medicos/contas-medicas/faturamento-tiss-3/faturamento/guia-de-sp-sadt/")



print('Tamanho da lista: ', len(df.index))
counter = 1
for counter in range(len(df.index)):
  carteirinha = df.iloc[counter,2]
  data = str(df.iloc[counter,4])
  solicitante = df.iloc[counter,6]
  conselho = df.iloc[counter,7]
  uf_conselho = df.iloc[counter,8]
  n_conselho = str(df.iloc[counter,9])
  cbos = str(df.iloc[counter,10])
  
  procedimentos = df.iloc[counter,5].split(';')
  precos = []
  for x in procedimentos:
    idx = ds[ds['CODIGO'] == int(x)].index[0]
    z  = ds.iloc[idx,2]
    precos.append(z)


  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'codigo-beneficiario-1'))).send_keys(carteirinha)
  #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'codigo-rne'))).send_keys(rg)
  #time.sleep(0.5)
  #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'uf-registro'))).click()
  #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'uf-registro'))).send_keys('GO')
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//button[contains(@class, "sas-form-submit")]'))).click()

  #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME,'guia-sadt.profissional-solicitante.tipo-documento-operadora.codigo'))).send_keys('CNPJ')
  #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'numero-profissional-operadora'))).send_keys('16867589000160')
  #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'nome-contratado-solicitante'))).send_keys('Analise Medicina Laboratorial')
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME,'guia-sadt.profissional-solicitante.nome'))).send_keys(solicitante)
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'conselho-profissional'))).send_keys(conselho)
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'uf-conselho-profissional'))).send_keys(uf_conselho)
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'numero-registro-conselho'))).send_keys(n_conselho)
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'cbo'))).send_keys(cbos)
  #time.sleep(1)
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ui-id-1"]/li'))).click()
  
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'carater-atendimento'))).send_keys('E')
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'data-solicitacao'))).send_keys(data)
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'flag-atendimento-rn'))).send_keys('N')
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'tipo-atendimento'))).send_keys('Exames')
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'indicador-acidente'))).send_keys('N')
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'tipo-consulta'))).send_keys('Primeira')
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'regime-atendimento'))).send_keys('Ambulatorial')

  #procedimentos = ['40302040','40301630','40302580','40301150','40302750','40316521','40316491','40302512','40302504','40302113','40302733']
  index = 0
  for proc in procedimentos:
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME,'per.data'))).send_keys(data)
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME,'per.codigo-procedimento'))).send_keys(proc)
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//a[contains(@class, "btn-busca-procedimento")]'))).click()
      time.sleep(0.3)
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME,'per.quantidade'))).send_keys('1')
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME,'per.valor-unitario'))).send_keys(str(precos[index]))
      WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.ID,'incluirPer'))).click()
      index += 1
      time.sleep(1)



  element = driver.find_element(By.XPATH,'//*[@id="observacao"]')
  driver.execute_script('arguments[0].scrollIntoView(true);', element)
  
  
  time.sleep(1)
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="confirmar-inclusao-sadt"]/span'))).click()
  print('Ficha ',carteirinha,' cadastrada!')
  time.sleep(3)
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="btnDialogVoltarEditar"]'))).click()
  time.sleep(1)
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/table[10]/tbody/tr/td[2]/table/tbody/tr[2]/td/form/div/div[2]/div/div[12]/div[3]/a'))).click()
  time.sleep(3)

driver.execute_script("alert('ROTINA FINALIZADA');")