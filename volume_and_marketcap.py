import numpy as np
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import gspread
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_authorized_user_file("token.json", SCOPES)
SHEET_ID = "1__zJY2xcap5jWF7xKkfN6qkUvDetCODgHGichjRPTfQ"
SHEET_NAME = "Dados"
gc = gspread.service_account('credentials3.json')
spreadsheet = gc.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet(SHEET_NAME)

url = 'https://www.coingecko.com/pt'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find('table')
table_rows = table.find_all('tr')
fortune = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [i.get_text(strip=True).replace("$","") for i in td]
    row.append(time.asctime())
    fortune.append(row)





fortune = pd.DataFrame(fortune)
fortuneA = fortune.loc[2:, [1,2,4,9,10,14]]
fortuneA = fortuneA.replace('$','', regex=True)
worksheet.append_rows(fortuneA.values.tolist(),value_input_option="USER_ENTERED")
print(fortuneA.to_string())
