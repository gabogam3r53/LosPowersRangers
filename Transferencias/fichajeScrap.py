import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


transferencia = {'Nombre': [], 'Fecha' : []}
csv_file = 'fichajes_jugadoras.csv'

url = 'https://www.365scores.com/es/basketball/player/natasha-howard-95187'
respuesta = requests.get(url)

soup = BeautifulSoup(respuesta.text, 'html.parser')

links_nombres = soup.findAll('div', class_="ellipsis_container__ciMmU")
links_montos = soup.findAll('div', class_= "athlete-widget_transfer_date__quLhJ")
print(links_montos, links_nombres)

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

#for link_nombre,link_monto in zip(links_nombres,links_montos):
#    transferencia['Nombre'].append(separar(link_nombre))
#    transferencia['Fecha'].append(separar(link_monto).strip()[1:])

#df = pd.DataFrame(transferencia)
#df.to_csv('datosTransferencias.csv', index=False)

#prueba1