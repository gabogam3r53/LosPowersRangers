import pandas as pd

años = [2024,2023,2022,2021,2020]

def filtrar_datos(df,año_contrato,año_estadisticas):
    df_correlacion = df['Contrato {}'.format(año_contrato)]
    df_año_estadisticas = df.filter(like= str(año_estadisticas))
    df_año_estadisticas.drop('Contrato {}'.format(año_estadisticas), axis=1, inplace = True)
    df_año_estadisticas.drop('Equipo {}'.format(año_estadisticas), axis=1, inplace = True)
    df_correlacion = pd.concat([df_correlacion, df_año_estadisticas],axis = 1)
    return df_correlacion

#Importar datos
df = pd.read_csv('\ProyectoPowerRangers\Datos\datos_completos_2023.csv')
#df.columns = df.columns.str.strip()
#df.columns = df.columns.str.replace('\t', ' ')
#correlacion = df[['Contrato 2024', 'RANK 2023', 'AGE 2023', 'GP 2023', 'W 2023', 'L 2023', 'MIN 2023', 'PTS 2023', 'FGM 2023', 'FGA 2023', 'FG% 2023', '3PM 2023', '3PA 2023', '3P% 2023', 'FTM 2023', 'FTA 2023', 'FT% 2023', 'OREB 2023', 'DREB 2023', 'REB 2023', 'AST 2023', 'TOV 2023', 'STL 2023', 'BLK 2023', 'PF 2023', 'FP 2023', 'DD2 2023', 'TD3 2023', '+/- 2023']].corr()
#correlacion.to_csv('Correlacion.csv')

df.info(verbose=False)

for i in range(len(años) - 1):
    df_correlacion = filtrar_datos(df,años[i],años[i + 1])
    correlacion = df_correlacion.corr()
    i_correlacion = correlacion.iloc[0].sort_values(ascending=False)
    i_correlacion.index = i_correlacion.index.str.replace(str(años[i + 1]), '')
    if i == 0:
        contrato_correlacion = i_correlacion
    else:
        contrato_correlacion = pd.concat([contrato_correlacion,i_correlacion],axis = 1)
contrato_correlacion.to_csv('Correlacion_contrato.csv')
#print(contrato_correlacion)
