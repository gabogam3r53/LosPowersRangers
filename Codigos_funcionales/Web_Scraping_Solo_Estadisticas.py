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

'''
2023 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2023&SeasonType=Regular%20Season',
                         2022 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2022&SeasonType=Regular%20Season',
                         2022 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2022&SeasonType=Regular%20Season',
                         2021 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2021&SeasonType=Regular%20Season',
                         2020 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2020&SeasonType=Regular%20Season',
                         2019 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2019&SeasonType=Regular%20Season',
                         2018 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2018&SeasonType=Regular%20Season',
                         2017 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2017&SeasonType=Regular%20Season',
                         2016 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2016&SeasonType=Regular%20Season'
                         

                        
                        2023 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2023&SeasonType=Regular%20Season',
                         2022 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2022&SeasonType=Regular%20Season',
                         2021 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2021&SeasonType=Regular%20Season',
                         2020 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2020&SeasonType=Regular%20Season',
                         2019 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2019&SeasonType=Regular%20Season',
                         2018 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2018&SeasonType=Regular%20Season',
                         2017 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2017&SeasonType=Regular%20Season',
                         2016 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2016&SeasonType=Regular%20Season',
                         2015 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2015&SeasonType=Regular%20Season',
                         2014 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2014&SeasonType=Regular%20Season',
                         2013 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2013&SeasonType=Regular%20Season',
                         2012 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2012&SeasonType=Regular%20Season',
                         2011 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2011&SeasonType=Regular%20Season',
                         2010 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2010&SeasonType=Regular%20Season',
                        '''

link_jugadoras_stats = { 2024 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2024&SeasonType=Regular%20Season',
                         2023 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2023&SeasonType=Regular%20Season',
                         2022 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2022&SeasonType=Regular%20Season',
                         2021 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2021&SeasonType=Regular%20Season',
                         2020 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2020&SeasonType=Regular%20Season',
                         2019 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2019&SeasonType=Regular%20Season',
                         2018 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2018&SeasonType=Regular%20Season',
                         2017 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2017&SeasonType=Regular%20Season',
                         2016 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2016&SeasonType=Regular%20Season',
                         2015 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2015&SeasonType=Regular%20Season',
                         2014 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2014&SeasonType=Regular%20Season',
                         2013 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2013&SeasonType=Regular%20Season',
                         2012 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2012&SeasonType=Regular%20Season',
                         2011 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2011&SeasonType=Regular%20Season',
                         2010 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2010&SeasonType=Regular%20Season',
                         2009 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2009&SeasonType=Regular%20Season',
                         2008 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2008&SeasonType=Regular%20Season',
                         2007 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2007&SeasonType=Regular%20Season',
                         2006 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2006&SeasonType=Regular%20Season',
                         2005 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2005&SeasonType=Regular%20Season',
                         2004 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2004&SeasonType=Regular%20Season',
                         2003 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2003&SeasonType=Regular%20Season',
                         2002 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2002&SeasonType=Regular%20Season',
                         2001 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2001&SeasonType=Regular%20Season',
                         2000 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2000&SeasonType=Regular%20Season'
                         }

def get_wnba_stats(link,año):
    logging.info(f"Iniciando funcion get_wnba_stats con link: {link}")
    anterior = 0
    suma = 0
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        logging.info("Inicializando navegador...")
        driver.get(link)
        time.sleep(15)

        columnas = {'RANK' : [], 'PLAYER' : [], 'TEAM': [], 'AGE': [], 'GP': [], 'W': [], 'L': [], 'MIN': [], 'PTS': [], 'FGM': [], 'FGA': [], 'FG%': [], '3PM': [], '3PA': [], '3P%': [], 
                  'FTM': [], 'FTA': [], 'FT%': [], 'OREB': [], 'DREB': [], 'REB': [], 'AST': [], 'TOV': [], 'STL': [], 'BLK': [], 'PF': [], 'FP': [], 'DD2': [],'TD3': [], '+/-': []}
        
        nuevo_dataset = {}

        for data in columnas.keys():
            if data == 'PLAYER':
                nombre = data
            else:
                nombre = '{} {}'.format(data, año)
            nuevo_dataset[nombre] = []
        
        logging.info("Obteniendo numero de paginas...")
        pages_elements = driver.find_elements(By.CLASS_NAME,"stats-table-pagination__info" )
        number_of_pages = int(pages_elements[0].text[:-2:-1])
        logging.info(f"Total de paginas: {number_of_pages}")

        for i in range(number_of_pages):
            if i != 0:
                logging.info(f"Cambiando a pagina {i+1} de {number_of_pages}")
                boton_cambiar = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.stats-table-pagination__next'))
                )
                boton_cambiar.click()
                time.sleep(5)

            player_elements = driver.find_elements(By.CSS_SELECTOR, "table tbody tr:not(.header)")
            logging.info(f"Encontradas {len(player_elements)} filas de jugadores en esta pagina")

            

            for row in player_elements:
                cells = row.find_elements(By.TAG_NAME, "td")
                for valor,tipo in zip(cells,nuevo_dataset.keys()):
                    dato_casilla = valor.text
                    if tipo != 'PLAYER' and tipo != 'RANK {}'.format(año):
                        nuevo_dataset[tipo].append(valor.text)
                    else:
                        if tipo == "RANK {}".format(año):
                            if anterior == valor.text:
                                suma = suma + 1
                                dato_casilla = str(int(valor.text) + suma)
                            else:
                                suma = 0
                        if dato_casilla not in nuevo_dataset[tipo]:
                            nuevo_dataset[tipo].append(dato_casilla)
                        if tipo == "RANK {}".format(año):
                            anterior = valor.text
        while len(nuevo_dataset['RANK {}'.format(año)]) > len(nuevo_dataset['PLAYER']):
            nuevo_dataset['RANK {}'.format(año)].pop()

        df = pd.DataFrame(nuevo_dataset)
        df.drop(['TEAM {}'.format(año)], axis = 1, inplace= True)
        return df
        # Crear DataFrame
        
    except Exception as e:
        logging.error(f"Error en get_wnba_stats: {str(e)}")
        if 'driver' in locals():
            driver.save_screenshot("error_detail.png")
        return None
        
    finally:
        if 'driver' in locals():
            logging.info("Cerrando el navegador...")
            driver.quit()
            logging.info("Funcion get_wnba_stats completada")

for fecha,link in link_jugadoras_stats.items():

    try:
        if fecha == 2024:
            data_jugadoras = get_wnba_stats(link,fecha)
        else:
            data_jugadoras = data_jugadoras.merge(get_wnba_stats(link,fecha), on='PLAYER', how='outer')
    except:
        print('error {}'.format(fecha))
data_jugadoras.to_csv('datos_solo_estadisticas_completo.csv', index=False, encoding='utf-8-sig')