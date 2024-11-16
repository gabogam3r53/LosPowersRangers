import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#leer el archivo donde estan las jugadoras
ruta_de_acceso = r"C:\Users\gabog\OneDrive\Documentos\Curso de samsumg\ProyectoPowerRangers\Datos\datos_todas_las_jugadoras_posibles.csv"
df = pd.read_csv(ruta_de_acceso) #Archivo 'datos_todas_las_jugadoras_posibles.csv'
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace('\t', ' ')
lista_de_todas_las_jugadoras = df['Nombre']  


años = [2024,2023,2022,2021,2020,2019,2018,2017,2016]

def filtrar_datos(df_data,año_contrato,año_estadisticas):   #Retorna df_correlacion
    df_nuevo = df_data.copy()
    df_correlacion = df_nuevo.loc[:,'Contrato {}'.format(año_contrato)]
    df_año_estadisticas = df_nuevo.filter(like= str(año_estadisticas))
    df_año_estadisticas.drop(columns = 'Contrato {}'.format(año_estadisticas), inplace = True)
    df_año_estadisticas.drop(columns = 'Equipo {}'.format(año_estadisticas), inplace = True)
    df_correlacion = pd.concat([df_correlacion, df_año_estadisticas],axis = 1)
    return df_correlacion

def Analisis_individual(jugadora): #Grafica jugadora de manera individual PTS Vs Contrato
  jugadora_a_consultar  = str(jugadora)
  df_jugadora_a_graficar = df.loc[df['Nombre'] == jugadora_a_consultar]
  df_jugadora_contratos = df_jugadora_a_graficar.filter(like= 'Contrato').drop(columns = 'Contrato 2016').stack().reset_index(drop=True)
  df_jugadora_pts = df_jugadora_a_graficar.filter(like= 'PTS').drop(columns = 'PTS 2024').stack().reset_index(drop=True)

  # Obtenemos la longitud del indice existente para df_jugadora_contratos
  index_len = len(df_jugadora_contratos.index)

  # Creamos una lista de años con la duración correcta
  años = list(range(2023, 2023 - index_len, -1)) #[2023, 2022, 2021, 2020]

  # Ahora asignamos el nuevo índice de forma correcta para evitar errores de dimensiones
  df_jugadora_contratos.index = años

  # Si df_jugadora_pts tiene una longitud diferente, ajuste en consecuencia
  if len(df_jugadora_pts.index) != index_len:
    # Ajuste la lista de años para df_jugadora_pts si es necesario
    pts_años = list(range(2023, 2023 - len(df_jugadora_pts.index), -1)) 
    df_jugadora_pts.index = pts_años
  else:
    df_jugadora_pts.index = años

  #print(df_jugadora_pts,df_jugadora_contratos)   #esto es para visualizar la informacion de los pts y los contratos

  #Graficar
  fig, ax1 = plt.subplots()  # Crea la figura y el primer eje
  ax1.plot(df_jugadora_pts, label='PTS')  # Grafica la primera curva en el primer eje
  ax1.set_xlabel('Año')  # Etiqueta del eje x
  ax1.set_ylabel('PTS', color='blue')  # Etiqueta del eje y primario (color azul)
  ax1.tick_params('y', labelcolor='blue') # Color de las etiqeutas del eje y primario

  ax2 = ax1.twinx()  # Crea un segundo eje (comparte el mismo eje)
  ax2.plot(df_jugadora_contratos, color='red', label='Contrato')  # Grafica la segunda curva en el segundo eje (color rojo)
  ax2.set_ylabel('Contrato', color='red')  # Etiqueta del eje y secundario (color rojo)
  ax2.tick_params('y', labelcolor='red')  # Color de las etiquetas del eje y secundario

  fig.tight_layout()  # Ajusta la gráfica
  plt.title(f'PTS vs. Contrato de {jugadora_a_consultar}') # Añade un título
  plt.legend() # Añade una leyenda
  plt.show()  # Muestra la gráfica

def graficar_individual_linea(datos_interes, df, player):    #Grafica jugadora de manera individual de datos de interes y los guarda en PNG
  fig, axes = plt.subplots(3, 3, figsize=(12, 8))
  df_player = df.loc[df['Nombre'] == player]
  y = df_player.filter(like= 'Contrato').drop(columns = 'Contrato 2016').stack().reset_index(drop=True)
  for i in range(len(datos_interes)):
    #x, y = seleccionar_todos_dispersion(datos_graficar[i], df_contratos_diferentes)
    x = df_player.filter(like= datos_interes[i]).drop(columns = '{} 2024'.format(datos_interes[i])).stack().reset_index(drop=True)
    #print(x)
    #print(y)
    # Ensure x and y have the same length
    min_len = min(len(x), len(y))
    x = x[:min_len]
    y = y[:min_len]
    if i < 3:
      axes[0,i].plot(x, y)
      axes[0,i].set_title('{} vs. contrato'.format(datos_graficar[i]))
    elif i >= 3 and i < 6:
      axes[1,i - 3].plot(x, y)
      axes[1,i - 3].set_title('{} vs. contrato'.format(datos_graficar[i]))
    else:
      axes[2,i - 6].plot(x, y)
      axes[2,i - 6].set_title('{} vs. contrato'.format(datos_graficar[i]))
  ruta_guardado = f"C:/Users/gabog/OneDrive/Documentos/Curso de samsumg/ProyectoPowerRangers/Analisis_Datos/GraficasIndividuales/{player.replace(' ', '_')}.png" 
  plt.savefig(ruta_guardado) # Guardar la gráfica en la ruta especificada
  plt.tight_layout()
  #plt.show()

#Se limpia los datos para solo tener los contratos que varian
datos_graficar = ['PTS', 'FGA', 'FGM', 'MIN','FP','TOV', 'RANK', 'AGE', '3P%']
nuevo_dataset = {'RANK' : [], 'AGE': [], 'GP': [], 'W': [], 'L': [], 'MIN': [], 'PTS': [], 'FGM': [], 'FGA': [], 'FG%': [], '3PM': [], '3PA': [], '3P%': [],
                  'FTM': [], 'FTA': [], 'FT%': [], 'OREB': [], 'DREB': [], 'REB': [], 'AST': [], 'TOV': [], 'STL': [], 'BLK': [], 'PF': [], 'FP': [], 'DD2': [],'TD3': [], '+/-': []}

df_contratos_diferentes = df.copy()
df_contratos = df.filter(like='Contrato')
df_contratos_colums = df_contratos.columns

for player in df['Nombre']:
    for i in range(len(años) - 2):
      if df.loc[df['Nombre'] == player, df_contratos_colums[i]].iloc[0] == df.loc[df['Nombre'] == player, df_contratos_colums[i + 1]].iloc[0]:
        df_contratos_diferentes.loc[df['Nombre'] == player, df_contratos_colums[i]] = np.nan
        for dato in nuevo_dataset.keys():
          df_contratos_diferentes.loc[df['Nombre'] == player, '{} {}'.format(dato,años[i+1])] = np.nan

df_contratos_diferentes.to_csv('datos_contratos_diferentes.csv')


#realizar la grafica individual de cada jugadora PTS vs Contrato
#for i in lista_de_todas_las_jugadoras:
#    Analisis_individual(i)

#realizar la grafica de cada jugadora de datos de interes y guardarlos en PNG
for i in lista_de_todas_las_jugadoras:
    print('jugadora:', i)
    graficar_individual_linea(datos_graficar,df_contratos_diferentes, i)