import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
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

creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#try:
#    service = build("sheets", "v4", credentials=creds)
#except: pass

SHEET_ID = "1BZrcaBDi2bbz58iF5DUxlth_z4cZfQkQKHgVshhMO7o"
SHEET_NAME = "Página1"
gc = gspread.service_account('credentials3.json')
spreadsheet = gc.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet(SHEET_NAME)

def getAutorizacoes():
    return worksheet.get_all_records()


def atualizaCelula(x,y,value):
    worksheet.update_cell(x,y,value)

def atualizaCelulas(x,value):
    worksheet.update_cell(x,5,"Guia autenticada com sucesso!")
    worksheet.update(f"E{x}:L{x}",value)
    worksheet.update_cell(x,13,time.asctime())