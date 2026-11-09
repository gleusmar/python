import os.path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import time

import gspread

### If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

### The ID and range of a sample spreadsheet.
#SAMPLE_SPREADSHEET_ID = "1BZrcaBDi2bbz58iF5DUxlth_z4cZfQkQKHgVshhMO7o"
#SAMPLE_RANGE_NAME = "Página1!A:H"

# Autenticação via service account (credentials3.json / CREDENTIALS_FILE)

SHEET_ID = "1LRkvR3BPMpEfPw0v_r3Pv74pdkWjq20FViijFfIwZzc"
SHEET_NAME = "Página1"

# Usa variável de ambiente para o arquivo de credenciais, com fallback para local
credentials_file = os.environ.get('CREDENTIALS_FILE', 'credentials3.json')
gc = gspread.service_account(credentials_file)
spreadsheet = gc.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet(SHEET_NAME)

def getAutorizacoes():
    return worksheet.get_all_records()


def atualizaCelula(x,y,value):
    worksheet.update_cell(x,y,value)

def atualizaCelulas(x,value):
    worksheet.update_cell(x,5,"Guia autenticada com sucesso!")
    worksheet.update(f"F{x}:M{x}",value)
    worksheet.update_cell(x,14,time.asctime())