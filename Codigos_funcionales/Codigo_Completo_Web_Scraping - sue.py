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

#Constantes
#csv_file = 'data.csv'
link_jugadoras_precio = { 2024 : 'https://www.spotrac.com/wnba/rankings/player/_/year/2024/sort/contract_value',
                         2023 : 'https://www.spotrac.com/wnba/rankings/player/_/year/2023/sort/contract_value',
                         2022 :'https://www.spotrac.com/wnba/rankings/player/_/year/2022/sort/contract_value',
                         2021 : 'https://www.spotrac.com/wnba/rankings/player/_/year/2021/sort/contract_value',
                         2020 : 'https://www.spotrac.com/wnba/rankings/player/_/year/2020/sort/contract_value',
                         2019 : 'https://www.spotrac.com/wnba/rankings/player/_/year/2019/sort/contract_value', 
                         2018 : 'https://www.spotrac.com/wnba/rankings/player/_/year/2018/sort/contract_value',
                         2017 : 'https://www.spotrac.com/wnba/rankings/player/_/year/2017/sort/contract_value',
                         2016 : 'https://www.spotrac.com/wnba/rankings/player/_/year/2017/sort/contract_value',
                        }

link_jugadoras_stats = { 2024 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2024&SeasonType=Regular%20Season',
                         2023 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2023&SeasonType=Regular%20Season',
                         2022 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2022&SeasonType=Regular%20Season',
                         2021 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2021&SeasonType=Regular%20Season',
                         2020 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2020&SeasonType=Regular%20Season',
                         2019 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2019&SeasonType=Regular%20Season',
                         2018 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2018&SeasonType=Regular%20Season',
                         2017 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2017&SeasonType=Regular%20Season',
                         2016 : 'https://stats.wnba.com/players/traditional/?sort=PTS&dir=-1&Season=2016&SeasonType=Regular%20Season'
                         }

#Procedimientos iniciales
# Configurar el controlador de Selenium utilizando WebDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


logging.basicConfig(filename='Proceso', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
data_jugadoras = None


#Funciones

def obtener_nombre_jugadoras(link):
    logging.info("Iniciando obtencion de nombres de jugadoras")
    jugadoras = {'Nombre': []}
    max_retries = 3
    for attempt in range(max_retries):
        try:
            r = requests.get(link) #Esto te da el codigo html de la pagina
            soup = BeautifulSoup(r.text, 'html.parser')
            links_nombres = soup.findAll('div', class_='link')
            for link_nombre in links_nombres:
                jugadoras['Nombre'].append(separar(link_nombre).upper())
            logging.info("Nombres de jugadoras obtenidos exitosamente")
            df = pd.DataFrame(jugadoras)
            return df
        except Exception as e:
            logging.error(f"Error en obtener_nombre_jugadoras: {e}")
            if attempt == max_retries - 1:
                logging.warning("No se pudo obtener los nombres de las jugadoras.")
                return None
            logging.info(f"Intento {attempt + 1} de conexion fallido. Intentando nuevamente...")
            time.sleep(5)

    return None


def obtener_precio_jugadoras(link,jugadoras, numero_contrato):
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

def obtener_equipo_fecha_fichaje(nombre_jugadora):
    #Pagina a navegar
    url = 'https://www.365scores.com/es'
    driver.get(url)
    
    #Esperar a que el botón de búsqueda esté presente y hacer clic en él
    try:
        boton_buscar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.site-header_search_button__3pJPq'))
        )
        boton_buscar.click()
        logging.info("Boton de búsqueda clickeado.")
    except Exception as e:
        logging.error(f"No se pudo hacer clic en el botón de busqueda: {e}")
        return None
    
    #Esperar a que el campo de búsqueda esté presente, hacer clic y añade el nombre de la jugadora
    try:
        
        
        campo_busqueda = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.new-search-widget_input__aoNqC'))
        )
        
        campo_busqueda.click()
        campo_busqueda.send_keys(nombre_jugadora)
        time.sleep(2) #Se espera un poco para que cargue la jugadora a buscar
        campo_busqueda.send_keys(Keys.RETURN)  # Simular la tecla Enter
        logging.info(f"Nombre de jugadora '{nombre_jugadora}' ingresado y búsqueda iniciada.")
    except Exception as e:
        logging.error(f"No se pudo ingresar el nombre de la jugadora: {e}")
        return None
    try:   
        container = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "new-search-widget_entity_item_intersection__L-eHP"))) 
        '''
        link_elemento = WebDriverWait(driver, 10).until(  #Le da click a la jugadora
            container.presence_of_element_located((By.CLASS_NAME, 'new-search-widget_entity_item_intersection__L-eHP'))
        )
        '''
        nombre_jugador_normalizado = nombre_jugadora.lower().replace(" ", "-")
        link = driver.find_element(By.XPATH, f".//a[contains(@class, 'new-search-widget_entity_item_intersection__L-eHP') and contains(@href, '{nombre_jugador_normalizado}')]")
        #container = driver.find_element(By.XPATH, ".//a[contains(@class, 'new-search-widget_entity_item_intersection__L-eHP') and contains(@href, '{nombre_jugadora}')]")
        #container = driver.find_element(By.CLASS_NAME, "new-search-widget_entity_item__Tthzc")
        #link_elemento = container.find_element(By.CLASS_NAME, 'new-search-widget_entity_item_intersection__L-eHP')
        #link_elemento.click()
        link.click()
        logging.info(f"Navegando a la pagina del jugador {nombre_jugadora}")
    except Exception as e:
        logging.error(f"No se pudo obtener el enlace o navegar al enlace de la jugadora '{nombre_jugadora}': {e}")
        data = {
        'Nombre': [np.nan],
        'Fecha': [np.nan]
        }
    
        df = pd.DataFrame(data)
        return df
    
    #Se toma el contenedor que nos interesa y se guarda el html de este
    try:
        list_container = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "list_container__AMVNC"))
        )

        html_content = list_container.get_attribute('innerHTML')
        
        #Se pasa el html a la libreria beautifulsoap para analizarlo
        soup = BeautifulSoup(html_content, 'html.parser')
        
        #Extraer la información de los elementos especificados
        nombres = soup.find_all('div', class_='ellipsis_container__ciMmU')
        fechas = soup.find_all('div', class_='athlete-widget_transfer_date__quLhJ')

        
        #Extraer el texto de cada elemento
        nombres_texto = [nombre.get_text(strip=True) for nombre in nombres]
        fechas_texto = [fecha.get_text(strip=True) for fecha in fechas]
        
        #Crear un DataFrame con la información extraída
        data = {
            'Nombre': nombres_texto,
            'Fecha': fechas_texto
        }
        
        df = pd.DataFrame(data)
        
        #Imprimir el DataFrame
        logging.info("DataFrame con la información extraida:")
        return(df)
    except:
        logging.error(f"Error con'{nombre_jugadora}': {e}")
        data = {
        'Nombre': [np.nan],
        'Fecha': [np.nan]
        }
    
        df = pd.DataFrame(data)
        return df
    
    
def añadir_equipo_fecha_fichaje(df):
    logging.info(f"Iniciando funcion añadir_equipo_fecha_fichaje con DataFrame de {len(df)} jugadoras")
    columna = {'Equipo': [], 'Fecha fichaje': []}
    for index, jugadora in df.iterrows():
        logging.debug(f"Procesando jugadora: {jugadora['Nombre']}")
        informacion = obtener_equipo_fecha_fichaje(jugadora['Nombre'])
        if isinstance(informacion, pd.DataFrame) and not informacion.empty:
            equipo = informacion['Nombre'][0] if len(informacion) > 0 else np.nan
            fecha_fichaje = informacion['Fecha'][0] if len(informacion) > 0 else np.nan
            columna['Equipo'].append(equipo)
            columna['Fecha fichaje'].append(fecha_fichaje)
            logging.info(f"Informacion obtenida para {jugadora['Nombre']}: Equipo={equipo}, Fecha fichaje={fecha_fichaje}")
        else:
            logging.warning(f"No se obtuvieron datos válidos para {jugadora['Nombre']}")
    
    nuevo_df = pd.DataFrame(columna)
    df_juntos = pd.concat([df, nuevo_df], axis=1)
    logging.info("Funcion añadir_equipo_fecha_fichaje completada. DataFrame actualizado con nuevas columnas.")
    return df_juntos

def arreglar_dataframe(data_jugadoras):
    
    #Cambiar columnas de nombres por los nuevos nombres con los acentos para que coincidan con la pagina de las estadisticas
    nombresjugadorasfix = data_jugadoras['Nombre']
    lista_nombres = nombresjugadorasfix.tolist()
    #print("\nLista de nombres:", lista_nombres)
    lista_nombres[7] = 'CHEYENNE PARKER-TYUS'
    lista_nombres[31] = 'BETNIJAH LANEY-HAMILTON'
    lista_nombres[75] = 'LOU LOPEZ SÉNÉCHAL'
    lista_nombres[86] = 'DORKA JUHÁSZL'
    lista_nombres[114] = 'ASTOU NDOUR-FALL'
    lista_nombres[135] = 'IVANA DOJKIĆ'
    #lista_nombres[143] = 'OLIVIA ÉPOUPA'
    return lista_nombres    #returnamos los nuevos nombres
    

def get_wnba_stats(link,data_original,año):
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

        nuevo_dataset = {'RANK' : [], 'PLAYER' : [], 'TEAM': [], 'AGE': [], 'GP': [], 'W': [], 'L': [], 'MIN': [], 'PTS': [], 'FGM': [], 'FGA': [], 'FG%': [], '3PM': [], '3PA': [], '3P%': [], 
                  'FTM': [], 'FTA': [], 'FT%': [], 'OREB': [], 'DREB': [], 'REB': [], 'AST': [], 'TOV': [], 'STL': [], 'BLK': [], 'PF': [], 'FP': [], 'DD2': [],'TD3': [], '+/-': []}
        
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
                    if tipo != 'PLAYER' and tipo != 'RANK':
                        nuevo_dataset[tipo].append(valor.text)
                    else:
                        if tipo == "RANK":
                            if anterior == valor.text:
                                suma = suma + 1
                                dato_casilla = str(int(valor.text) + suma)
                            else:
                                suma = 0
                        if dato_casilla not in nuevo_dataset[tipo]:
                            nuevo_dataset[tipo].append(dato_casilla)
                        if tipo == "RANK":
                            anterior = valor.text
                            
        # Crear DataFrame
        logging.info("Creando DataFrame con las nuevas columnas...")
        nuevas_columnas = {}

        for data in nuevo_dataset.keys():
            if data != 'PLAYER' and data != 'TEAM':
                nombre = '{} {}'.format(data, año)
                nuevas_columnas[nombre] = []
            
        resta = 0
        for player in data_original['Nombre']:
            for data in nuevo_dataset.keys():
                if data != 'PLAYER' and data != 'TEAM':
                    if player in nuevo_dataset['PLAYER']:
                        nombre = '{} {}'.format(data, año)
                        nuevas_columnas[nombre].append(nuevo_dataset[data][nuevo_dataset['PLAYER'].index(player)])

                    else:
                        resta = resta + 1
                        nombre = '{} {}'.format(data, año)
                        nuevas_columnas[nombre].append(np.nan)
        #print('Se encontraron {} jugadoras', data_original.shape[0] - resta/len(nuevo_dataset.keys()))
        logging.info(f"Se encontraron {data_original.shape[0] - resta/len(nuevo_dataset.keys())} jugadoras")
        df = pd.DataFrame(nuevas_columnas)
        logging.info("Funcion get_wnba_stats completada exitosamente.")
        return df
        
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

sue = { 'Nombre': ['Sue Bird']}
sue = pd.DataFrame(sue)

data_jugadoras = obtener_nombre_jugadoras(link_jugadoras_precio[2023])
for fecha,link in link_jugadoras_precio.items():
    data_jugadoras = obtener_precio_jugadoras(link,sue,fecha)


data_jugadoras['Nombre'] = arreglar_dataframe(data_jugadoras) #sustituimos la nueva lista en el dataframe

for fecha,link in link_jugadoras_stats.items():
    data_jugadoras = pd.concat([data_jugadoras,get_wnba_stats(link,data_jugadoras,fecha)], axis=1)

print(data_jugadoras)
data_jugadoras.to_csv('datos_completos_fd.csv', index=False, encoding='utf-8-sig')

#data_jugadoras.info()
'''
data_jugadoras_prueba = data_jugadoras.iloc[0:4]


data_jugadoras_completo = añadir_equipo_fecha_fichaje(data_jugadoras_prueba)
data_jugadoras_completo.to_csv('datos.csv', index=False, encoding='utf-8-sig')
data_jugadoras_completo.info(verbose=True)
'''

def check_data_update():
    global data_jugadoras
    current_time = datetime.datetime.now()
    logging.info(f"Iniciando verificación de actualización de datos a las {current_time.strftime('%H:%M')}")
    
    if current_time.hour == 0 and current_time.minute == 0:
        logging.info("Hora de actualizacion. Proceso comenzando...")
        data_jugadoras = obtener_nombre_jugadoras(link_jugadoras_precio[2023])
        for fecha, link in link_jugadoras_precio.items():
            logging.info(f"Actualizando datos para fecha: {fecha}")
            data_jugadoras = obtener_precio_jugadoras(link, data_jugadoras, fecha)
        
        for fecha, link in link_jugadoras_stats.items():
            logging.info(f"Actualizando estadisticas para fecha: {fecha}")
            data_jugadoras = pd.concat([data_jugadoras, get_wnba_stats(link, data_jugadoras, fecha)], axis=1)
        
        logging.info("Actualizacion completa. Datos actualizados.")
    else:
        logging.info("No es hora de actualizar los datos.")

def scrape_data():
    global data_jugadoras
    try:
        check_data_update()
        logging.info("Scraping completo")
    except Exception as e:
        logging.error(f"Error durante el scraping: {e}")

schedule.every().day.at("00:00").do(scrape_data)
schedule.every().day.at("12:00").do(scrape_data)


def main():
    global data_jugadoras

    if data_jugadoras is None:
        logging.info("Inicializando datos de jugadoras por primera vez")
        data_jugadoras = obtener_nombre_jugadoras(link_jugadoras_precio[2023])
        for fecha, link in link_jugadoras_precio.items():
            logging.info(f"Actualizando datos para fecha: {fecha}")
            data_jugadoras = obtener_precio_jugadoras(link, data_jugadoras, fecha)
        
        for fecha, link in link_jugadoras_stats.items():
            logging.info(f"Actualizando estadisticas para fecha: {fecha}")
            data_jugadoras = pd.concat([data_jugadoras, get_wnba_stats(link, data_jugadoras, fecha)], axis=1)
    
    logging.info("Inicializacion de datos completada")

    while True:
        schedule.run_pending()
        time.sleep(60)
    logging.info("Proceso terminado")
if __name__ == "__main__":
    main()

#salir del driver
driver.quit