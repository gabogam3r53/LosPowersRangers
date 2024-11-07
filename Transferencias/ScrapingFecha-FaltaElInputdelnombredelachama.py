from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def get_wnba_stats(nombre_jugadora):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        url = "https://www.365scores.com/es/basketball/player/natasha-howard-95187"
        driver.get(url)
        
        # Esperar hasta que el botón "Ver más" esté presente y hacer clic en él 
        #boton_buscar = WebDriverWait(driver, 10).until(
        #    EC.element_to_be_clickable((By.CSS_SELECTOR, '.site-header_search_button__3pJPq site-header_active__xhd5z')) # Ajusta el selector según sea necesario 
        #     ) 
        #boton_buscar.click()
        
        #campo_busqueda = WebDriverWait(driver, 10).until(
        #    EC.presence_of_element_located((By.CSS_SELECTOR, '.campo-busqueda-selector'))
        #)
        #campo_busqueda.click() 
        #campo_busqueda.send_keys(nombre_jugadora) 
        #campo_busqueda.send_keys(Keys.RETURN)
        #print(f"Nombre de jugadora '{nombre_jugadora}' ingresado y búsqueda iniciada.")
        
        boton_ver_mas = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.expandable-footer_show_more_button_container__fchpn')) # Ajusta el selector según sea necesario 
             ) 
        boton_ver_mas.click() 
        #print("Botón 'Ver más' clickeado.")    
        time.sleep(15)
        
        headers = ['Historial de transferencias', 'Equipos']
        fichaje = {'Nombre': [], 'Fecha' : []}
        csv_file = 'fichaje_jugadoras.csv'
        
        rows = []
        equipos = driver.find_elements(By.CSS_SELECTOR, '.athlete-widget_transfer_competitor_name__gFCCV')
        fechas = driver.find_elements(By.CSS_SELECTOR, '.athlete-widget_transfer_date__quLhJ')
        
        for equipo,fecha in zip(equipos,fechas):
            fichaje['Nombre'].append(equipo.text)
            fichaje['Fecha'].append(fecha.text)
        
        df = pd.DataFrame(fichaje)
        print(df)

    except Exception as e:
        print(f"Error detallado: {e}")
        if 'driver' in locals():
            driver.save_screenshot("error_detail.png")
        return None
        
    finally:
        if 'driver' in locals():
            driver.quit()

# Ejecutar el scraping
print("Iniciando web scraping...")


nombre_jugadora = "Natasha Howard"
stats = get_wnba_stats(nombre_jugadora)
