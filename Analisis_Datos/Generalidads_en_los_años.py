import pandas as pd
import matplotlib.pyplot as plt

años = [2024]
def grafica_generalidades_una(df, dato_jugadora, dato_estadistico, años):
    df_dato = df.filter(like=dato_jugadora)
    df_per_year = df_dato.describe().loc[dato_estadistico]
    df_per_year.index = pd.RangeIndex(start=2024, stop=2000, step=-1)

    # Create the plot with customizations
    plt.figure(figsize=(10, 6))  # Set figure size
    plt.plot(df_per_year.index, df_per_year.values, marker='o', linestyle='-', color='blue', linewidth=2)

    # Add title and labels
    plt.title(f'{dato_estadistico} de {dato_jugadora} a través del tiempo', fontsize=16)
    plt.xlabel('Año', fontsize=12)
    plt.ylabel(dato_estadistico, fontsize=12)

    # Customize grid and ticks
    plt.grid(True, linestyle='--', alpha=0.7)  # Add a grid
    plt.xticks(df_per_year.index, rotation=45, ha='right')  # Rotate x-axis labels

    # Add a legend (optional)
    # plt.legend([dato_estadistico], loc='upper right')

    plt.tight_layout()  # Adjust layout for better spacing
    ruta_guardado = f"C:\\Users\\Persona\\Documents\\Curso IA Samsung\\Proyecto_Data\\PowersRangers\\Analisis_Datos\\Graficas\\Graficas_datos_liga_por_año\\{dato_jugadora.replace(' ', '_')}.png" 
    plt.savefig(ruta_guardado) # Guardar la gráfica en la ruta especificada
    plt.show()

nuevo_dataset = {'RANK' : [], 'AGE': [], 'GP': [], 'MIN': [], 'PTS': [], 'FGM': [], 'FGA': [], 'FG%': [], '3PM': [], '3PA': [], '3P%': [],
                  'FTM': [], 'FTA': [], 'FT%': [], 'OREB': [], 'DREB': [], 'AST': [], 'TOV': [], 'STL': [], 'BLK': [], 'PF': [], 'FP': [], 'DD2': [],'TD3': [], "+/-": []}
ruta_de_acceso = r'C:\Users\Persona\Documents\Curso IA Samsung\Proyecto_Data\PowersRangers\Datos\datos_solo_estadisticas_completo.csv'
df = pd.read_csv(ruta_de_acceso)
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace('\t', ' ')

for dato in nuevo_dataset.keys():
  grafica_generalidades_una(df,dato,'mean', años)