# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 12:01:09 2018

Objetivo: Contar la cantidad de nombres distintos existentes en el data-set. 
Supuesto: Los nombres compuestos son tomados en cuanta por separado. Por ejemplo,
Maria Ines, cuenta para Maria y para Ines pero no como Maria Ines. 
No se resolvio el problema de errores en los nombres. 

@author: Agus velazquez
"""

import pandas as pd
import numpy as np

# Frente a un data-set muy grande, utilizamos la opcion chunk para crear un 
# objeto iterable y particionarlo.
chunk_iter = pd.read_csv('historico-nombres.csv', chunksize = 1000000)

unicos = pd.DataFrame({0: []}) # unicos es el data-set con la respuesta final, se crea vacio.
#%% Iteracion en cada chunk
for chunk in chunk_iter:    
    chunk = chunk.replace(['^\s+$'], np.nan, regex = True) #elimino celdas enteramente vacias para que funcione el str.split
    nombres = chunk['nombre'].str.split(expand = True) #separo los nombres compuestos de cada persona
    prima_list = nombres[0].unique() #primer lista formada con la primer columna
    prima_list = pd.DataFrame(prima_list)
    n_columns = len(nombres.columns)
    for column in range(0,n_columns):
        a = nombres[column]
        a = a.to_frame(name = 'Name')
        a = a[~a['Name'].isin(prima_list[0])]  #Comparacion
        a = a['Name'].unique() #Dejo solo los unicos
        a = pd.DataFrame(a)
        prima_list = pd.concat([prima_list, a], axis = 0)
        del a; del column
    unicos = unicos.append(prima_list, ignore_index = True) #apendizo cada lista de unicos
    del nombres
#%% Ultima limpieza de valores repetidos en la lista final
unicos = pd.unique(unicos[0])
unicos = pd.DataFrame(unicos, columns=['Nombres unicos'])

print(unicos.nunique()) #Respuesta: Cantidad de nombres unicos
