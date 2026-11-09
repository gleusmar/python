import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import time
from datetime import datetime
import re
from io import StringIO
from sheetsApi import getAutorizacoes
from sheetsApi import atualizaCelula
from sheetsApi import atualizaCelulas

log = []
options = ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Configuração para GitHub Actions (usa Chrome do sistema)
if os.environ.get('GITHUB_ACTIONS'):
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.binary_location = "/usr/bin/chromium-browser"
    service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
else:
    # Configuração local (usa webdriver-manager)
    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

driver.maximize_window()
action = ActionChains(driver)
driver.get("http://2896prd.cloudmv.com.br/sigss")
tempo = WebDriverWait(driver, 10)
usuario = os.environ.get('USUARIO', '04957832188')
senha = os.environ.get('SENHA', 'XLGPG@x@UQ9JTQv')


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
  print("URL após driver.get: " + str(driver.current_url))
  print("Título: " + str(driver.title))
  try:
    user_el = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID,'username')))
  except Exception:
    try:
      print("URL no timeout: " + str(driver.current_url))
      print("Título no timeout: " + str(driver.title))
      driver.save_screenshot("login_timeout.png")
      with open("login_timeout.html","w",encoding="utf-8") as f:
        f.write(driver.page_source)
      print("Debug salvo em login_timeout.png / login_timeout.html")
    except Exception:
      pass
    raise
  pass_el = tempo.until(EC.visibility_of_element_located((By.ID,'password')))
  try:
    user_el.clear()
  except Exception:
    pass
  user_el.send_keys(usuario)
  try:
    pass_el.clear()
  except Exception:
    pass
  pass_el.send_keys(senha)
  login_el = tempo.until(EC.presence_of_element_located((By.NAME,'submit')))
  try:
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_el)
  except Exception:
    pass
  try:
    tempo.until(EC.element_to_be_clickable((By.NAME,'submit')))
    login_el.click()
  except Exception:
    try:
      driver.execute_script("arguments[0].click();", login_el)
    except Exception:
      pass_el.send_keys(Keys.ENTER)
  try:
    WebDriverWait(driver, 15).until(lambda d: d.execute_script("return document.readyState") == "complete")
  except Exception:
    pass
  try:
    driver.switch_to.default_content()
  except Exception:
    pass
  for label, ancestor in [("Atendimento","button"),("Faturamento","button")]:
    el = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, f'//span[normalize-space()="{label}"]')))
    try:
      container = el.find_element(By.XPATH, f'ancestor::{ancestor}[1]')
    except Exception:
      container = el
    try:
      driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
    except Exception:
      pass
    try:
      container.click()
    except Exception:
      driver.execute_script("arguments[0].click();", container)
  el = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//span[normalize-space()="Autenticação"]')))
  try:
    container = el.find_element(By.XPATH, 'ancestor::a[1]')
  except Exception:
    container = el
  try:
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
  except Exception:
    pass
  try:
    container.click()
  except Exception:
    driver.execute_script("arguments[0].click();", container)
  print("Logado")            
def lancarBiomedico():
  i = 1
  while i <= 6:
    try:
      # Primeiro, tenta com os XPaths absolutos informados pelo usuário
      prof_click_abs = "/html/body/div[9]/div[2]/form/div/div/div[3]/div[3]/div/table/tbody/tr[2]/td[7]/div"
      prof_input_abs = "/html/body/div[9]/div[2]/form/div/div/div[3]/div[3]/div/table/tbody/tr[2]/td[7]/div/div/div/input[1]"
      prof_option_abs = "/html/body/div[9]/div[2]/form/div/div/div[3]/div[3]/div/table/tbody/tr[2]/td[7]/div/div/ul/table/tbody/tr[2]/td[2]/div"

      WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, prof_click_abs))
      ).click()

      try:
        prof_input = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.XPATH, prof_input_abs))
        )
      except Exception:
        prof_input = WebDriverWait(driver, 10).until(
          EC.visibility_of_element_located((By.XPATH, prof_input_abs))
        )

      prof_input.click()
      # limpar de maneira robusta
      try:
        prof_input.clear()
      except Exception:
        prof_input.send_keys(Keys.CONTROL, 'a')
        prof_input.send_keys(Keys.DELETE)
      try:
        prof_input.send_keys("glauceni")
      except Exception:
        # fallback para o elemento ativo, caso o input real esteja focado
        driver.switch_to.active_element.send_keys("glauceni")
      prof_input.send_keys(Keys.ENTER)

      WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, prof_option_abs))
      ).click()

      # CBO (td[9]) pelos XPaths absolutos correspondentes
      cbo_click_abs = "/html/body/div[9]/div[2]/form/div/div/div[3]/div[3]/div/table/tbody/tr[2]/td[9]/div"
      cbo_input_abs = "/html/body/div[9]/div[2]/form/div/div/div[3]/div[3]/div/table/tbody/tr[2]/td[9]/div/div/div/input[1]"

      WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, cbo_click_abs))
      ).click()

      try:
        cbo_input = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.XPATH, cbo_input_abs))
        )
      except Exception:
        cbo_input = WebDriverWait(driver, 10).until(
          EC.visibility_of_element_located((By.XPATH, cbo_input_abs))
        )

      cbo_input.click()
      try:
        cbo_input.clear()
      except Exception:
        cbo_input.send_keys(Keys.CONTROL, 'a')
        cbo_input.send_keys(Keys.DELETE)
      try:
        cbo_input.send_keys("221205")
      except Exception:
        driver.switch_to.active_element.send_keys("221205")
      cbo_input.send_keys(Keys.ENTER)
      
      time.sleep(0.2)
      break
    except Exception:
      # Fallback: âncora no container visível "Informações Obrigatórias"
      try:
        container_xpath = "//div[./div/span[contains(text(),'Informações Obrigatórias')]]"
        prof_click_xpath = container_xpath + "//table/tbody/tr[2]/td[7]/div"
        prof_input_xpath = container_xpath + "//table/tbody/tr[2]/td[7]/div/div/div/input[1]"
        prof_option_xpath = container_xpath + "//table/tbody/tr[2]/td[7]/div/div/ul/table/tbody/tr[2]/td[2]/div"

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, prof_click_xpath))).click()
        prof_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, prof_input_xpath)))
        prof_input.click()
        prof_input.send_keys(Keys.CONTROL, 'a')
        prof_input.send_keys(Keys.DELETE)
        prof_input.send_keys("glauceni")
        prof_input.send_keys(Keys.ENTER)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, prof_option_xpath))).click()

        cbo_click_xpath = container_xpath + "//table/tbody/tr[2]/td[9]/div"
        cbo_input_xpath = container_xpath + "//table/tbody/tr[2]/td[9]/div/div/div/input[1]"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, cbo_click_xpath))).click()
        cbo_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, cbo_input_xpath)))
        cbo_input.click()
        cbo_input.send_keys(Keys.CONTROL, 'a')
        cbo_input.send_keys(Keys.DELETE)
        cbo_input.send_keys("221205")
        cbo_input.send_keys(Keys.ENTER)
        time.sleep(0.2)
        break
      except Exception:
        pass
      i += 1
      time.sleep(0.2)
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

def click_dialog_button(label: str, dialog_title: str = 'Informações Obrigatórias'):
  dialog_xpath = f"//div[contains(@class,'ui-dialog') and contains(@style,'display: block') and .//span[contains(@class,'ui-dialog-title') and normalize-space()='{dialog_title}']]"
  btn_xpath = f"{dialog_xpath}//div[contains(@class,'ui-dialog-buttonpane')]//button[.//span[normalize-space()='{label}']]"
  btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, btn_xpath)))
  try:
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
  except Exception:
    pass
  try:
    btn.click()
  except Exception:
    driver.execute_script("arguments[0].click();", btn)
  return btn

def reset_context_between_competencia():
  # Fecha mensagem do sistema se aberta
  try:
    classMsgSistema = driver.find_element(By.XPATH, "//div[./div/span[contains(text(),'Mensagem do sistema')]]").get_attribute('class')
    if "display-block" in classMsgSistema:
      tempo.until(EC.element_to_be_clickable((By.XPATH,'//button/span[contains(., "OK")]'))).click()
  except: pass
  # Fecha 'Informações Obrigatórias' se aberta
  try:
    el = driver.find_element(By.XPATH, "//div[./div/span[contains(text(),'Informações Obrigatórias')]]")
    if 'display: block' in el.get_attribute('style'):
      # tenta por botão com texto
      try:
        btn = el.find_element(By.XPATH, ".//button[.//span[normalize-space()='Cancelar' or normalize-space()='Fechar' or normalize-space()='Fechar Sem Gravar']]")
        btn.click()
      except Exception:
        # fallback ao caminho antigo
        try:
          click_dialog_button('Voltar')
        except Exception:
          driver.find_element(By.XPATH, "//div[9]/div[3]/div/button[2]").click()
      WebDriverWait(driver, 10).until(lambda d: 'display: block' not in el.get_attribute('style'))
  except: pass
  # Fecha dropdowns Chosen ativos com ESC
  try:
    active_chosen = driver.find_elements(By.XPATH, "//div[contains(@class,'chzn-container') and contains(@class,'chzn-container-active')]")
    if active_chosen:
      ActionChains(driver).send_keys(Keys.ESCAPE).perform()
      time.sleep(0.05)
  except: pass
  # Fecha dropdowns/focus com ESC e clica no body
  try:
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(0.05)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    driver.find_element(By.TAG_NAME, 'body').click()
  except: pass
  # Aguarda overlay de modal sumir e, se necessário, remove via JS
  try:
    WebDriverWait(driver, 3).until(EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class,'ui-widget-overlay') and contains(@style,'display: block')]")))
  except Exception:
    try:
      driver.execute_script("document.querySelectorAll('.ui-widget-overlay').forEach(e=>e.style.display='none')")
    except Exception:
      pass
  # Aguarda loader sumir se presente
  try:
    el = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "load_grid_info")))
    WebDriverWait(driver, 10).until(lambda d: 'display: block' not in el.get_attribute('style'))
  except: pass

def set_competencia_by_index(idx: int) -> bool:
  # Primeiro tenta via Chosen (#competencia_chzn)
  try:
    container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'competencia_chzn')))
    anchor = container.find_element(By.CSS_SELECTOR, 'a.chzn-single')
    # Abre o dropdown se não estiver aberto
    if 'chzn-container-active' not in container.get_attribute('class'):
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#competencia_chzn a.chzn-single'))).click()
    # Aguarda a caixa de busca do Chosen (dropdown aberto)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'competencia_chzn_search')))

    # Seleciona a opção pelo id competencia_chzn_o_{idx}
    opt = None
    try:
      opt = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, f'competencia_chzn_o_{idx}')))
    except Exception:
      # Fallback: pega a (idx)-ésima opção ativa ignorando o placeholder (id *_o_0)
      try:
        options = container.find_elements(By.CSS_SELECTOR, 'ul.chzn-results > li.active-result')
        # garante que temos opções suficientes
        if options and len(options) > idx:
          opt = options[idx]
      except Exception:
        opt = None
    if opt is None:
      raise Exception('Não encontrou opção de competência pelo índice informado')
    try:
      driver.execute_script("arguments[0].scrollIntoView({block:'nearest'});", opt)
    except Exception:
      pass
    try:
      WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='competencia_chzn_o_{idx}']|."))).click()
    except Exception:
      try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable(opt)).click()
      except Exception:
        driver.execute_script("arguments[0].click();", opt)

    # Verifica se o texto exibido mudou para o título/label da opção
    try:
      chosen_text = opt.get_attribute('title') or opt.text
      WebDriverWait(driver, 5).until(lambda d: d.find_element(By.CSS_SELECTOR, '#competencia_chzn a.chzn-single span').text.strip() == (chosen_text or '').strip())
    except Exception:
      pass
    # Garante que o dropdown fechou
    try:
      WebDriverWait(driver, 5).until(lambda d: 'chzn-single-with-drop' not in d.find_element(By.CSS_SELECTOR, '#competencia_chzn a.chzn-single').get_attribute('class'))
    except Exception:
      try:
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
      except Exception:
        pass
    return True
  except Exception:
    # Fallback: tenta selecionar via <select id="competencia">
    try:
      select_el = driver.find_element(By.ID, 'competencia')
      Select(select_el).select_by_index(idx)
      try:
        driver.execute_script("arguments[0].dispatchEvent(new Event('change', {bubbles:true}))", select_el)
      except Exception:
        pass
      return True
    except Exception:
      return False

def ensure_codbar_ready():
  el = tempo.until(EC.element_to_be_clickable((By.ID,'codBar')))
  try:
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
  except Exception:
    pass
  # Garante que nenhum dropdown/overlay está ativo
  try:
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(0.05)
  except Exception:
    pass
  try:
    driver.execute_script("if(document.activeElement) document.activeElement.blur();")
  except Exception:
    pass
  try:
    el.click()
    driver.execute_script("arguments[0].focus();", el)
  except Exception:
    pass
  return el

def set_competencia_current() -> bool:
  """Abre o Chosen #competencia_chzn e seleciona a opção cujo texto representa o mês/ano corrente."""
  now = datetime.now()
  tgt_month = now.month
  tgt_year = now.year
  try:
    container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'competencia_chzn')))
    # abre dropdown se necessário
    if 'chzn-container-active' not in container.get_attribute('class'):
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#competencia_chzn a.chzn-single'))).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'competencia_chzn_search')))
    # aguarda as opções carregarem no dropdown
    try:
      WebDriverWait(driver, 10).until(lambda d: len(container.find_elements(By.CSS_SELECTOR, 'ul.chzn-results > li')) > 1)
      WebDriverWait(driver, 10).until(lambda d: len(container.find_elements(By.CSS_SELECTOR, 'ul.chzn-results > li.active-result')) > 0)
    except Exception:
      pass
    time.sleep(0.2)

    # procura opção por texto (ex.: "10 — 2025"). Tolerante a diferentes traços.
    options = container.find_elements(By.CSS_SELECTOR, 'ul.chzn-results > li.active-result')
    target = None
    for li in options:
      txt = (li.get_attribute('title') or li.text or '').strip()
      # normaliza travessões: -, – (U+2013), — (U+2014)
      txt_norm = re.sub(r"[\-\u2013\u2014]", '-', txt)
      m = re.search(r"^(\d{1,2})\s*-\s*(\d{4})$", txt_norm)
      if not m:
        continue
      m_int, y_int = int(m.group(1)), int(m.group(2))
      if m_int == tgt_month and y_int == tgt_year:
        target = li
        break
    if target is None:
      return False
    try:
      driver.execute_script("arguments[0].scrollIntoView({block:'nearest'});", target)
    except Exception:
      pass
    try:
      WebDriverWait(driver, 5).until(EC.element_to_be_clickable(target)).click()
    except Exception:
      driver.execute_script("arguments[0].click();", target)

    # garante fechamento do dropdown
    try:
      WebDriverWait(driver, 5).until(lambda d: 'chzn-single-with-drop' not in d.find_element(By.CSS_SELECTOR, '#competencia_chzn a.chzn-single').get_attribute('class'))
    except Exception:
      try:
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
      except Exception:
        pass
    return True
  except Exception:
    return False

df = pd.DataFrame(getAutorizacoes())
sucesso = 0
problemas = 0
jaAutenticadas = 0
pulei = 0
colE = df.iloc[:,4] if df.shape[1] > 4 else pd.Series([np.nan] * len(df))
mask_para_aut = colE.isna() | (colE.astype(str).str.strip() == '')
total_para_aut = int(mask_para_aut.sum())
print("Lista tem " + str(len(df.index)) + " guias")
print("Há " + str(total_para_aut) + " guias para autenticar!")
logaAcessa()

ordem_nao_autenticadas = 0
for counter in range(len(df.index)):
  cod = df.iloc[counter,0]
  result = df.iloc[counter,4]
  skip_keys = ["Guia autenticada com sucesso!",
               "Guia já autenticada!",
               "Erro",
               "O agendamento de exame da guia",
               "Cliente",
               "não é válida",
               "ão autenticada",
               "excluído",
               "á autenticada",
               "Não foi possível autenticar"]
  if any(key in str(result) for key in skip_keys):
    pulei += 1
    continue
  if bool(mask_para_aut.iloc[counter]):
    ordem_nao_autenticadas += 1
    print(str(counter+2) + " " + str(ordem_nao_autenticadas) + "/" + str(total_para_aut))
  else:
    print(counter+2)
  h = 1
  while h <= 4:
    try:
      for i in range(3):
        k = i + 2
        # Na 2ª e 3ª tentativa, reseta o contexto para evitar bloqueio de digitação
        if i > 0:
          reset_context_between_competencia()
          time.sleep(0.1)
        time.sleep(1)
        set_competencia_current()
        cb = ensure_codbar_ready()
        cb.clear()
        cb.send_keys(cod)
        cb.send_keys(Keys.ENTER)
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
          if "display-block" in classMsgSistema and ("O agendamento" in msgSistema or "O Agendamento" in msgSistema):
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
            if not rows[1].find_element(By.XPATH,".//td[7]/select").get_attribute("disabled"):
              lancarBiomedico()
            confere, listaExames = confereCbos()
            atualizaCelula(counter+2,15,listaExames)
            if confere:
              try:
                click_dialog_button('Voltar')
              except Exception:
                driver.find_element(By.XPATH, "//button/span[contains(.,'Voltar')]").click()
              problemas += 1
              print(cod +" - "+ confere)
              atualizaCelula(counter+2,5,"Erros no(s) exame(s): " + confere)
              break      
            time.sleep(1.3)
            click_dialog_button('Gravar')

            try:
              classMsgSistema = driver.find_element(By.XPATH, "//div[./div/span[contains(text(),'Mensagem do sistema')]]").get_attribute('class')
              msgSistema = driver.find_element(By.XPATH, "//div[./div/span[contains(text(),'Mensagem do sistema')]]").get_attribute('innerText')
              if "display-block" in classMsgSistema and "CBO não informado!" in msgSistema:
                tempo.until(EC.element_to_be_clickable((By.XPATH,'//button/span[contains(., "OK")]'))).click()
                problemas += 1
                print(cod + " - Não foi possível autenticar a guia!1")
                atualizaCelula(counter+2,5,"Não foi possível autenticar a guia!")
                try:
                  click_dialog_button('Voltar')
                except Exception:
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
              try:
                click_dialog_button('Voltar')
              except Exception:
                driver.find_element(By.XPATH, "//div[9]/div[3]/div/button[2]").click()
              time.sleep(0.5)
              break
          except :
            problemas += 1
            time.sleep(1)
            print(cod + " - Não foi possível autenticar a guia!3")
            atualizaCelula(counter+2,5,"Não foi possível autenticar a guia!")
            try:
              click_dialog_button('Voltar')
            except Exception:
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
