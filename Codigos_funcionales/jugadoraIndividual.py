import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Cargar los datos desde un archivo CSV
df = pd.read_csv('datos_completos_2023_2016.csv')

jugadoras_filtrado = ['DEWANNA BONNER','ALYSSA THOMAS','ARIKE OGUNBOWALE', 'MARINA MABREY', 'CHEYENNE PARKER-TYUS', 'AERIAL POWERS', 'BETNIJAH LANEY', 'KAYLA MCBRIDE', 'BRITTNEY SYKES']
df_filtrado_total = pd.DataFrame()

# Filtrar las jugadoras guardadas
def filtrar_jugadoras(jugadoras_filtrado, df):
    df_filtrado_total = pd.DataFrame()
    for jugadora in jugadoras_filtrado:
        df_filtrado = df.loc[df['Nombre'] == jugadora]
        df_filtrado_total = pd.concat([df_filtrado_total, df_filtrado], ignore_index=True)
    return df_filtrado_total

# Asumiendo que tu DataFrame original se llama 'df'
x = filtrar_jugadoras(jugadoras_filtrado, df)
print(x)

# Filtrar las columnas
columnas_filtradas = ['Nombre', 'Contrato 2024', 'Contrato 2023', 'Contrato 2022', 'Contrato 2021', 'Contrato 2020','Contrato 2019','Contrato 2018','Contrato 2017','Contrato 2016', 'RANK 2023', 'RANK 2022', 'RANK 2021', 'RANK 2020','RANK 2019','RANK 2018','RANK 2017','RANK 2016']
df_filtrado2 = x[columnas_filtradas]
print(df_filtrado2)

# Filtrar fila según jugadora
df_filtrado = df_filtrado2.loc[df_filtrado2['Nombre'] == 'BRITTNEY SYKES']
print("\nDataFrame filtrado por la jugadora 'DEWANNA BONNER':\n", df_filtrado)

años = [2024,2023,2022,2021,2020,2019,2018,2017,2016]

nuevo_dataset = {'RANK' : [], 'AGE': [], 'GP': [], 'W': [], 'L': [], 'MIN': [], 'PTS': [], 'FGM': [], 'FGA': [], 'FG%': [], '3PM': [], '3PA': [], '3P%': [], 
                  'FTM': [], 'FTA': [], 'FT%': [], 'OREB': [], 'DREB': [], 'REB': [], 'AST': [], 'TOV': [], 'STL': [], 'BLK': [], 'PF': [], 'FP': [], 'DD2': [],'TD3': [], '+/-': []}
df = df_filtrado
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

df_contrato = pd.read_csv('datos_contratos_diferentes.csv')
df_contrato