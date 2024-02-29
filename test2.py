import numpy as np
import pandas as pd
array = ([[3, 5, 2, 4],
       [7, 6, 8, 8],
       [1, 6, 7, 7]])

array2 = pd.DataFrame([[["nan","nan","nan","nan","nan","nan","nan"],
  ['380506-1','EXAME','INDIARA PEREIRA RAMOS','28/02/2024','UNIDADE DE PRONTO ATENDIMENTO - UPA 24 HORAS',2.0,2.0]]])
print (array2)

print(array2.iloc[:,-1:])