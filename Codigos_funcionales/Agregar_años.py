import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
import schedule
import datetime
import logging

link_jugadoras_stats = { 2019 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2024&SeasonType=Regular%20Season',
                         2018 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2023&SeasonType=Regular%20Season',
                         2017 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2022&SeasonType=Regular%20Season',
                        }


logging.basicConfig(filename='Proceso', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
data_jugadoras = None

def agregar_precio_jugadoras(link,jugadoras, numero_contrato):

    logging.info(f"Iniciando obtencion de precios de jugadoras desde {link}")
    nueva_columna_contrato = 'Contrato {}'.format(numero_contrato)
    nueva_columna_equioi = 'Equipo {}'.format(numero_contrato)
    df = {'Nombre' : [] , 'Contrato' : [],'Fecha' :[]}
    max_retries = 3
    for attempt in range(max_retries):
        try:
            r = requests.get(link) #Esto te da el codigo html de la pagina
            soup = BeautifulSoup(r.text, 'html.parser')
            links_nombres = soup.findAll('div', class_='link')
            links_montos = soup.findAll('span', class_= 'medium')
            links_fechas = soup.findAll('small',class_= 'mt-0 d-block')
            for link_nombre,link_monto,link_fecha in zip(links_nombres,links_montos,links_fechas):
                #if separar(link_nombre) != "A'ja Wilson" and separar(link_nombre) != 'Azurá Stevens' and separar(link_nombre) != 'Stephanie Soares':
                df['Nombre'].append(separar(link_nombre).upper())
                df['Contrato'].append(int((separar(link_monto).strip()[1:]).replace(",","")))
                df['Fecha'].append(link_fecha.string.strip().split(',')[0])
    
            if len(df['Contrato']) < len(jugadoras['Nombre']):
                while len(df['Contrato']) != len(jugadoras['Nombre']):
                    df['Contrato'].append(np.nan)
                    df['Nombre'].append(np.nan)
   
            for nombre, valor,fecha in zip(df['Nombre'],df['Contrato'],df['Fecha']):
                if nombre in jugadoras['Nombre'].values:
                    jugadoras.loc[jugadoras['Nombre'] == nombre, nueva_columna_contrato] = valor
                    jugadoras.loc[jugadoras['Nombre'] == nombre, nueva_columna_equioi] = fecha
            return jugadoras
        
        except Exception as e:
            logging.error(f"Error en obtener_precio_jugadoras: {e}")
            if attempt == max_retries - 1:
                logging.warning("No se pudo obtener los precios de las jugadoras.")
                return None
            logging.info(f"Intento {attempt + 1} de conexion fallido. Intentando nuevamente...")
            time.sleep(5)    
    logging.info(f"Precios de jugadoras obtenidos exitosamente.")
    return None

def separar(link):
    logging.debug(f"Separando texto: {link}")
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
    logging.debug(f"Texto separado: {link[index_start_information:index_stop_information]}")
    return link[index_start_information:index_stop_information]
