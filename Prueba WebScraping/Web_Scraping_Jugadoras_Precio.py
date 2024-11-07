#Este es un codigo que toma los nombres y precio de contrato de las jugadoras de la pagina https://www.spotrac.com/wnba/rankings/player/_/year/2024/sort/contract_value
#Crea una serie de pandas con dichos datos y ademas los guarda en un csv

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

jugadoras = {'Nombre': [], 'Contrato' : []}
csv_file = 'contratos_jugadoras.csv'


r = requests.get('https://www.spotrac.com/wnba/rankings/player/_/year/2024/sort/contract_value') #Esto te da el codigo html de la pagina
soup = BeautifulSoup(r.text, 'html.parser')
links_nombres = soup.findAll('div', class_='link')
links_montos = soup.findAll('span', class_= 'medium')
def separar(link):
    link = str(link)
    start_tag = False
    for i in range(len(link)):
        if link[i] == '<' and not start_tag:
            start_tag = True
        elif link[i] == '>' and start_tag:
            index_start_information = i + 1
        elif link[i] == '<' and start_tag:
            index_stop_information = i
            start_tag = False
    return link[index_start_information:index_stop_information]

for link_nombre,link_monto in zip(links_nombres,links_montos):
    jugadoras['Nombre'].append(separar(link_nombre))
    jugadoras['Contrato'].append(separar(link_monto).strip()[1:])
   


#print(jugadoras)

df = pd.DataFrame(jugadoras)
df.to_csv('datos.csv', index=False)