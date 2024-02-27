import openpyxl
import pandas as pd
import time

path = 'Autorizações.xlsx'
wb = openpyxl.load_workbook(path)
ws = wb["Planilha2"]
#ws.cell(row=10, column=7).value = time.localtime()
ws.cell(row=10, column=8).value = time.asctime(time.localtime())

wb.save(path)