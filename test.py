import openpyxl
import pandas as pd
from openpyxl import load_workbook

path = 'Autorizações.xlsx'
df = pd.read_excel(path)
#result = ["Guia já autenticada!"]

'''wb = openpyxl.load_workbook(path)
ws = wb.active
for b in range(len(result)):
    temp = result[b]
    ws.cell(row=b+2, column=2).value = temp
wb.save(path)'''
def salva(resultado):
  wb = openpyxl.load_workbook(path)
  ws = wb.active
  ws.cell(row=2, column=2).value = resultado
  wb.save(path)

salva("Guia autenticada com sucesso")