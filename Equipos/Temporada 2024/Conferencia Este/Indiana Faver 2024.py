from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def get_wnba_stats():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        url = "https://stats.wnba.com/team/1611661325/players-traditional/"
        driver.get(url)
        time.sleep(15)
        
        headers = ['PLAYERS', 'GP', 'MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 
                  'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'PF', '+/-']
        
        rows = []
        player_elements = driver.find_elements(By.CSS_SELECTOR, "table tbody tr:not(.header)")
        
        for row in player_elements:
            cells = row.find_elements(By.TAG_NAME, "td")
            player_data = []
            for cell in cells:
                player_data.append(cell.text)
            if player_data:
                rows.append(player_data)
        
        # Crear DataFrame
        df = pd.DataFrame(rows, columns=headers)
        
        # Filtrar filas que contienen solo None
        df = df.dropna(how='all')
        
        # Filtrar filas que no son jugadoras (como RECORD:, EASTERN CONF:, etc.)
        df = df[~df['PLAYERS'].str.contains('RECORD:|EASTERN|PPG:|RPG:|APG:|OPG:|2024', regex=True, na=False)]
        
        # Eliminar duplicados
        df = df.drop_duplicates(subset=['PLAYERS'])
        
        # Resetear los índices
        df = df.reset_index(drop=True)
        
        # Guardar en CSV
        csv_path = "indiana_fever_stats.csv"
        df.to_csv(csv_path, index=False)
        print(f"Datos guardados en: {csv_path}")
        
        return df
        
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
stats = get_wnba_stats()

if stats is not None and not stats.empty:
    print("\nEstadísticas obtenidas:")
    print(stats)
    print(f"\nNúmero total de jugadoras: {len(stats)}")
else:
    print("No se pudieron obtener los datos o el DataFrame está vacío")