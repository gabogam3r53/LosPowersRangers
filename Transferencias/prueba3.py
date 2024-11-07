from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Configurar el controlador de Selenium utilizando WebDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Función para buscar y extraer la información de la jugadora
def buscar_jugadora(nombre_jugadora):
    #Pagina a navegar
    url = 'https://www.365scores.com/es'
    driver.get(url)
    
    # Esperar a que el botón de búsqueda esté presente y hacer clic en él
    try:
        boton_buscar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.site-header_search_button__3pJPq'))
        )
        boton_buscar.click()
        print("Botón de búsqueda clickeado.")
    except Exception as e:
        print("No se pudo hacer clic en el botón de búsqueda:", e)
        return
    
    # Esperar a que el campo de búsqueda esté presente, hacer clic y añade el nombre de la jugadora
    try:
        campo_busqueda = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.new-search-widget_input__aoNqC'))  
        )
        campo_busqueda.click()
        campo_busqueda.send_keys(nombre_jugadora)
        time.sleep(2) #Se espera un poco para que cargue la jugadora a buscar
        campo_busqueda.send_keys(Keys.RETURN)  # Simular la tecla Enter
        print(f"Nombre de jugadora '{nombre_jugadora}' ingresado y búsqueda iniciada.")
    except Exception as e:
        print("No se pudo ingresar el nombre de la jugadora:", e)
        return
    try:   
        link_elemento = WebDriverWait(driver, 10).until(  #Le da click a la jugadora
            EC.presence_of_element_located((By.CLASS_NAME, 'new-search-widget_entity_item_intersection__L-eHP'))
        )
        link_elemento.click()
    except Exception as e:
        print(f"No se pudo obtener el enlace o navegar al enlace de la jugadora '{nombre_jugadora}':", e) 
        return
    
    #Se toma el contenedor que nos interesa y se guarda el html de este
    list_container = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "list_container__AMVNC"))
    )

    html_content = list_container.get_attribute('innerHTML')
    
    # Se pasa el html a la libreria beautifulsoap para analizarlo
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extraer la información de los elementos especificados
    nombres = soup.find_all('div', class_='ellipsis_container__ciMmU')
    fechas = soup.find_all('div', class_='athlete-widget_transfer_date__quLhJ')

    
    # Extraer el texto de cada elemento
    nombres_texto = [nombre.get_text(strip=True) for nombre in nombres]
    fechas_texto = [fecha.get_text(strip=True) for fecha in fechas]
    
    # Crear un DataFrame con la información extraída
    data = {
        'Nombre': nombres_texto,
        'Fecha': fechas_texto
    }
    
    df = pd.DataFrame(data)
    
    # Imprimir el DataFrame
    print("DataFrame con la información extraída:")
    return(df)

# Nombre de la jugadora que deseas buscar
nombre_jugadora = "Alyssa Thomas"

# Llamar a la función para buscar y extraer la información
print(buscar_jugadora(nombre_jugadora))


# Cerrar el navegador
driver.quit()
