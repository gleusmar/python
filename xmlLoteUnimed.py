import xml.etree.ElementTree as ET
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import gspread

### If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

### The ID and range of a sample spreadsheet.
#SAMPLE_SPREADSHEET_ID = "1BZrcaBDi2bbz58iF5DUxlth_z4cZfQkQKHgVshhMO7o"
#SAMPLE_RANGE_NAME = "Página1!A:H"

creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#try:
#    service = build("sheets", "v4", credentials=creds)
#except: pass

SHEET_ID = "1SvqutLLXAaygiihpNuBkXRr_tUNlVRtgmdcsE7Z4rOI"
SHEET_NAME = "Página9"
gc = gspread.service_account('credentials3.json')
spreadsheet = gc.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet(SHEET_NAME)

files = ['protocolo678487127.xml','protocolo678633264.xml','protocolo678635573.xml','protocolo678730036.xml','protocolo678735911.xml','protocolo678986623.xml','protocolo679008631.xml','protocolo679172760.xml','protocolo679267120.xml','protocolo679273801.xml']

for file in files:
    tree = ET.parse(file)
    root = tree.getroot()
    ans="{http://www.ans.gov.br/padroes/tiss/schemas}"
    array=[]

    lote = int(root.find('.//'+ans+'numeroLote').text)
    dtEnvio = root.find('.//'+ans+'dataEnvioLote').text
    for paciente in root.findall('.//'+ans+'dadosGuias'):
        dtExecucacao = paciente.find('.//'+ans+'dataRealizacao').text
        nGuia = int(paciente.find('.//'+ans+'numeroGuiaPrestador').text)
        valorTotal = float(paciente.find('.//'+ans+'valorLiberado').text)
        carteira = int(paciente.find('.//'+ans+'numeroCarteira').text)
        nome = paciente.find('.//'+ans+'nomeBeneficiario').text
        for exame in paciente.findall('.//'+ans+'procedimentoRealizado'):
            procCod = int(exame.find('.//'+ans+'codigoProcedimento').text)
            procNome = exame.find('.//'+ans+'descricaoProcedimento').text
            procQtd = float(exame.find('.//'+ans+'quantidadeExecutada').text)
            procValor = float(exame.find('.//'+ans+'valorUnitario').text)
            procTotal = float(exame.find('.//'+ans+'valorTotal').text)
            #print(dtExecucacao,nGuia,valorTotal,carteira,nome,procCod,procNome,procQtd,procValor,procTotal)
            array.append([lote,dtEnvio,dtExecucacao,nGuia,valorTotal,carteira,nome,procCod,procNome,procQtd,procValor,procTotal])
    #print(array)
    worksheet.append_rows(array)