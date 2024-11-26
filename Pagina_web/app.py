import streamlit as st
from utils import load_data, load_image, load_data_csv
from config import *
import pandas as pd
import matplotlib.pyplot as plt

# Pagina configuracion 
st.set_page_config(
    page_title="WNBAmarket",
    layout="wide"
)
# URL de la imagen de fondo 
background_image_url = 'https://github.com/gabogam3r53/PowersRangers/blob/develop/Datos/Background_Paginaweb2.png?raw=true' 
# CSS para la imagen de fondo 
page_bg_img = f""" 
<style> 
.stApp {{
background-image: url({background_image_url});
background-size: contain; 
background-position: 100%;
background-repeat: no-repeat;  
background-attachment: fixed;
background-color: #000000;
}} 
.stApp::before {{
content: "";
background: rgba(0, 0, 0, 0.5); /* Color gris oscuro con transparencia */ 
}}
</style> 
"""
# Incorporar el CSS en Streamlit 
st.markdown(page_bg_img, unsafe_allow_html=True)


def main():
    
    st.markdown("# :blue[Estadísticas de Jugadoras de la WNBA (2016-2024)]")
    st.write("El presente proyecto se enfoca en el ámbito del baloncesto femenino de la WNBA, recopilando datos exhaustivos de las temporadas 2016-2024 directamente de las fuentes oficiales: Spotrac.com y Stats.wnba.com. Este conjunto de datos permitió realizar un análisis detallado de las jugadoras, sus estadísticas y tendencias a lo largo de los años.")
    st.divider()

    # Cargar datos
    data = load_data(DATA_URL)
    if data is None:
        st.error("Failed to load data. Please try again later.")
        return
    data_correlacion = load_data(DATA_CORRELACION_URL)
    if data_correlacion is None:
        st.error("Failed to load data. Please try again later.")
        return
    data_correlacion_csv = load_data_csv(DATA_CORRELACION_CSV_URL)
    if data_correlacion is None:
        st.error("Failed to load data. Please try again later.")
        return
    
    # Crea tres secciones principales usando columnas
    col1, col2 = st.columns([2, 1],gap="large")

    with col1:
        # Sección de tabla de datos
        with st.container():
            st.markdown("## :notebook_with_decorative_cover: :orange[Datos estadísticas y contratos]")
            st.dataframe(data, height=400)

        # Sección de estadísticas de contratos
        with st.container():
            st.markdown("## :mag: :orange[Gráfica: Contrato contra estadísticas interesantes]")
            contract_image = load_image(CONTRACT_GRAPH_URL)
            if contract_image:
                st.image(contract_image, use_column_width=True)
            st.markdown("""
                **Análisis de correlaciones entre estadísticas y valor de contrato en la WNBA.**
        
                En este análisis se explora la relación entre las estadísticas individuales de las jugadoras de la WNBA y el valor de sus contratos, utilizando datos de las temporadas 2016-2024. A través de gráficas de dispersión, se visualiza cómo variables como puntos por partido (PTS), intentos y aciertos de campo (FGA, FGM), minutos jugados (MIN), valoración (FP), pérdidas de balón (TOV) y rango (RANK) se relacionan con el valor de mercado de las jugadoras.
        
                **Principales hallazgos:**
        
                * **Correlación positiva:** Se observa una fuerte correlación positiva entre el valor de contrato y estadísticas como PTS, FGM, FGA, MIN, FP y TOV. Esto indica que, en general, las jugadoras con mayor producción ofensiva, mayor participación en el juego y mejor eficiencia tienden a tener contratos más altos.
                * **Correlación negativa:** Por otro lado, se encuentra una correlación negativa significativa entre el rango de la jugadora y el valor de su contrato. Este resultado es intuitivo, ya que las jugadoras con un rango más bajo (es decir, mejor clasificadas) suelen ser más valoradas en el mercado.
                * **Influencia de la edad:** El análisis de la variable edad revela un patrón interesante. Las jugadoras jóvenes suelen iniciar sus carreras con contratos más modestos, pero a medida que adquieren experiencia y reconocimiento, su valor de mercado tiende a aumentar hasta alcanzar un pico máximo entre los 30 y 33 años. Después de esta edad, el valor de mercado comienza a disminuir gradualmente.
                * **Efectividad en tiros de 3 puntos:** En contraste con las otras variables analizadas, el porcentaje de acierto en tiros de 3 puntos no muestra una correlación clara con el valor de contrato. Este hallazgo podría deberse a la históricamente baja efectividad de este tipo de tiro en la WNBA.
        
                **Conclusiones:**
        
                Los resultados de este análisis sugieren que las estadísticas tradicionales de producción ofensiva y participación en el juego son los principales determinantes del valor de mercado de las jugadoras de la WNBA. Sin embargo, factores como la edad y el rango también desempeñan un papel importante. Además, se destaca la necesidad de considerar el contexto histórico de la liga al interpretar los resultados, especialmente en el caso de estadísticas como el porcentaje de acierto en tiros de 3 puntos.
                """)
        with st.container():
            st.markdown("## :clock8: :orange[Tendencias Temporales en el Valor de Mercado]")
            st.dataframe(data_correlacion, height=400)

            # Limpiar el DataFrame para que tenga un formato adecuado
            data_correlacion_csv.set_index(data_correlacion_csv.columns[0], inplace=True)

            # Eliminar las filas de contratos (que no son métricas)
            data_correlacion_csv = data_correlacion_csv[~data_correlacion_csv.index.str.contains("Contrato")]


            # Seleccionar la métrica para visualizar
            metric = st.selectbox("Selecciona una métrica:", data_correlacion_csv.index)

            # Verificar si hay datos disponibles para la métrica seleccionada
            if metric in data_correlacion_csv.index:
                correlation_values = data_correlacion_csv.loc[metric].dropna().values  # Eliminar NaN para evitar errores

                years = data_correlacion_csv.columns[:][~data_correlacion_csv.loc[metric].isna()]  # Filtrar años correspondientes

                # Asegurarse de que las dimensiones coincidan

                years = years[::-1]
                correlation_values = correlation_values[::-1]

                if len(correlation_values) == len(years):
                    # Crear una gráfica
                    plt.figure(figsize=(10, 5))
                    plt.plot(years, correlation_values, marker='o')
                    plt.title(f'Correlación de {metric} a través de los años')
                    plt.xlabel('Años')
                    plt.ylabel('Correlación')
                    plt.xticks(rotation=45)
                    plt.grid()
                    plt.ylim(-1, 1)

                    # Mostrar la gráfica en Streamlit
                    st.pyplot(plt)
                else:
                    st.error("Error: Las dimensiones de los años y las correlaciones no coinciden.")
            else:
                st.error("No se encontraron datos para la métrica seleccionada.")
            
            st.markdown("""

                El análisis de las correlaciones en los contratos de jugadoras de la WNBA a través de los años revela cambios significativos en la importancia de ciertas métricas, especialmente en el contexto del aumento de los tiros de tres puntos.

                ##### 1. Triples encestados (3PM)
                - **Aumento en la Correlación**: La correlación de 3PM ha aumentado considerablemente en los últimos años. En 2017, la correlación era solo **0.0147**, mientras que en 2024 alcanzó **0.5511**. Esto indica un creciente énfasis en el juego exterior y la efectividad de los tiros de tres.
                - **Interpretación**: Este aumento sugiere que las estrategias de juego han evolucionado, priorizando más los tiros de tres puntos, lo que es consistente con la tendencia observada en el baloncesto profesional, donde se valora cada vez más la capacidad de anotar desde larga distancia.

                ##### 2. Puntos (PTS)
                - **Correlaciones Altas**: La correlación de PTS ha mostrado una tendencia a la baja desde un máximo de **0.7578** en 2020 a **0.5350** en 2024.  Aunque sigue siendo significativa, este descenso podría reflejar una diversificación en el enfoque ofensivo, donde no solo se depende del anotador principal.

                ##### 3. Asistencias (AST)
                - **Estabilidad Moderada**: Las asistencias han mantenido correlaciones relativamente estables, oscilando entre **0.5526** en 2017 y **0.2584** en 2024.sto puede indicar que, aunque hay un enfoque creciente en el tiro exterior, las jugadoras todavía están contribuyendo al juego colectivo a través de asistencias. 

                ##### 4. Porcentaje de Tiros de Tres (3P%)
                - **Correlación Variable**: La correlación del porcentaje de tiros de tres ha sido inconsistente, con un valor negativo significativo en 2023 (**-0.0069**). Esto sugiere que, aunque se están tomando más tiros de tres, la efectividad no ha seguido el mismo patrón.Dado que la WNBA es una liga en crecimiento, es posible que los equipos estén dispuestos a invertir en jugadoras que puedan aumentar su volumen de tiros, incluso si su efectividad no es alta en este momento. Esta estrategia podría ser parte de un enfoque a largo plazo para desarrollar un juego más dinámico y atractivo.

                
                """)


    with col2:

        # Sección leyenda de datos

        with st.container():
            abbrev = pd.DataFrame.from_dict(ABBREVS_WNBA, orient='index', columns=['Significado'])
    
            styled_df = abbrev.style.set_properties(**{
            'background-color': 'black',
            'color': 'white',
            'border': '1px solid #ddd',
            'padding': '8px'
            })
    
            st.dataframe(styled_df)
        
        # Sección de análisis de jugadores individuales
        with st.container():
            st.markdown("## :basketball: :orange[Gráfica: Jugadoras individuales]")
            player = st.selectbox(
                "Selección de jugadora:",
                options=data['Nombre'].unique()
            )
            
            # Mostrar Gráfica Individual de Jugadora Seleccionada
            st.write(f"### Gráfica Individual de {player}")
            player_graph_url = f"{INDIVIDUAL_GRAPHS_DIR}{player.replace(' ', '_')}.png"
            player_image = load_image(player_graph_url)
            if player_image:
                st.image(player_image, use_column_width=True)
            st.markdown("""
                **Análisis de gráfica de estadísticas y contratos Individual de las jugadoras de la WNBA**
        
                En este análisis se observa la relación entre las estadísticas individuales de las jugadoras de la WNBA y el valor de sus contratos.
                
                **Principales hallazgos:**
        
                * **Correlación Positiva:** PTS (Puntos), FGA (Intentos de Tiro de Campo), FGM (Tiros de Campo Anotados), MIN (Minutos Jugados), FP (Puntos de Fantasía), y 3P% (Porcentaje de Tiros de Tres Puntos) muestran una tendencia positiva con respecto a los valores de los contratos. Esto indica que, en general, a medida que las jugadoras tienen mejor desempeño en estas estadísticas, sus contratos tienden a ser más altos.
                Nota:Es importante destacar que en las gráficas individuales, estas correlaciones se visualizan claramente con tendencias ascendentes.
                * **Correlaciones Negativas:** RANK (Ranking de Jugadoras) y TOV (Pérdidas de Balón) presentan una correlación negativa con los valores de los contratos. Las jugadoras con mejor ranking (número más bajo) y las jugadoras con menos pérdidas de Balón tienden a recibir contratos más altos.
                * **Falta de Correlación Aparente en Algunas Estadísticas:** Algunas estadísticas como AGE (Edad) muestran una correlación positiva o negativa pero menos significativa, lo cual podría indicar que este factor no es tan determinante en la valoración de los contratos.
                                 
                **Conclusiones:**
                * **Factores de Rendimiento Individual:**  
                El rendimiento individual medido en puntos, intentos y tiros de campo anotados, minutos jugados, puntos de fantasía y porcentaje de tiros de tres puntos tiene una influencia significativa en la determinación del valor de los contratos de las jugadoras.
                
                * **Factores de Posicionamiento y Experiencia:**  
                El ranking de las jugadoras y la perdida de balones también son factores importantes, con una tendencia a que las jugadoras con menos perdidas de balones y mejor clasificadas reciban contratos más altos. Esto podría estar relacionado con el potencial de desarrollo y el valor de mercado de las jugadoras en esas categorías.
                
                * **Elementos No Considerados:**  
                A pesar de las correlaciones observadas, es probable que otros factores no representados en estas gráficas también influyan en el valor del contrato. Estos factores pueden incluir la reputación de la jugadora, su impacto en el marketing, su contribución al equipo más allá de las estadísticas individuales, y posibles negociaciones contractuales.
                
                * **Consistencia en los Datos:**  
                La mayoría de las gráficas muestran una consistencia en la relación entre las estadísticas y los valores de los contratos, lo que refuerza la validez de las conclusiones extraídas.

                 """)
        if player == 'NATASHA HOWARD':
            st.markdown("""
            * **Observacion:** Hay algunas jugadoras como por ejemplo "Natasha Howard", las cuales si se fijan en la grafica de puntos, tuvieron una mejora al pasar los años(primer contrato) y en consecuencia obtuvieron un mejor contrato debido a que las Fichó un nuevo equipo, ahora bien, este cambio hace que el numero de puntos que estaba teniendo anteriormente tienda a disminuir mientras se acostumbra a sus nuevas compañeras y logre adaptarse para tener las mismas posibilidades de hacer puntos en su nuevo equipo.
                Así mismo se puede analizar que cuando se generó el cambio de equipo los FGA (Intentos de Tiro de Campo) y  FGM (Tiros de Campo Anotados), tambien disminuyeron mientras Natasha Howard se adaptaba.
                
            * Estas graficas permiten estudiar el comportamiento de las jugadoras al pasar del tiempo antes y despues de un nuevo contrato.
             """)      
        # Sección de Estadísticas Anuales
        with st.container():
            st.markdown("## :chart: :orange[Gráfica: Media de estadísticas a traves de los años]")
            stat = st.selectbox(
                "Selección de estadística:",
                options=STATS_COLUMNS
            )
            
            st.write(f"### Gráfica de {stat} a través de los años")
            stat_graph_url = f"{YEARLY_GRAPHS_DIR}{stat.replace(' ', '_')}.png"
            stat_image = load_image(stat_graph_url)
            if stat_image:
                st.image(stat_image, use_column_width=True)

            if stat == 'GP':
                st.markdown("""
                            La temporada 2020 de la Women's National Basketball Association (WNBA) quedó marcada por un evento sin precedentes: la pandemia de COVID-19. 
                            Esta crisis sanitaria global obligó a la liga a implementar medidas sanitarias rigurosas y a ajustar su calendario de manera significativa. Una de las consecuencias 
                            más directas de estos cambios fue una notable disminución en el promedio de juegos jugados por jugadora.
                            """)
            if stat == 'PTS':
                st.markdown("""
                            Nota:  existe una tendencia al alza en PTS desde principios de la década de 2000 hasta mediados de la década de 2010. 
                            Esto sugiere un aumento en la ofensividad del juego durante este período.
                            """)
            if stat == 'FGM':
                st.markdown("""
                            Nota:  Desde principios de los años 2000 hasta mediados de la década de 2010, se observa un aumento gradual en el promedio de encestes de campo por partido. 
                            Observando que las jugadoras se volvieron más eficientes en anotar durante este período. Después del aumento inicial, el promedio se estabiliza y fluctúa dentro 
                            de un rango relativamente estrecho. Esta estabilidad podría indicar un equilibrio entre las estrategias ofensivas y defensivas.
                            """)
            if stat == '3PM':
                st.markdown("""
                            Nota: El promedio de triples anotados por partido en la WNBA revelan una tendencia clara e innegable: un aumento constante y significativo en el uso del tiro de tres puntos a lo largo de las últimas dos décadas. Esta evolución es un reflejo de cómo el juego femenino ha adoptado las tendencias globales del baloncesto moderno, donde el tiro de tres puntos se ha convertido en una herramienta ofensiva fundamental.
                            Es evidente que la WNBA ha experimentado una transición hacia un estilo de juego más rápido y dinámico, caracterizado por un mayor espaciamiento en la cancha y una mayor frecuencia de intentos de tres puntos. Esta tendencia se ha acelerado especialmente en los últimos diez años, lo que sugiere una adopción cada vez más rápida y generalizada de este tipo de tiro.
                            Varios factores pueden explicar este aumento en los triples anotados. En primer lugar, los cambios en las reglas del juego, como el espaciamiento de la cancha y los incentivos para tomar tiros de tres puntos, han fomentado este tipo de tiro. En segundo lugar, el desarrollo de las jugadoras, con una mayor especialización en el tiro de larga distancia y una mejor preparación física, ha contribuido a este incremento. Además, la influencia de la NBA, donde el tiro de tres puntos se ha convertido en una parte integral del juego, ha sido un factor determinante en la adopción de esta tendencia en la WNBA.
                            Las implicaciones de este aumento en los triples anotados son múltiples. Por un lado, ha hecho el juego más emocionante y atractivo para los espectadores, al generar un ritmo más rápido y una mayor cantidad de puntos. Por otro lado, ha obligado a los equipos a adaptar sus estrategias defensivas para hacer frente a la amenaza del tiro exterior. Sin embargo, una dependencia excesiva del tiro de tres puntos podría generar problemas ofensivos si las jugadoras no mantienen un alto porcentaje de acierto.
                            En conclusión, el análisis de los datos muestra una clara evolución hacia un baloncesto femenino más basado en el tiro de tres puntos. Esta tendencia, impulsada por diversos factores, ha transformado el juego y ha generado nuevas dinámicas tanto a nivel individual como colectivo. Para comprender mejor esta evolución, sería interesante realizar un análisis más profundo que incluya la comparación con otras ligas, el estudio del impacto de jugadoras individuales y la evaluación de las consecuencias a largo plazo de esta tendencia.
                            """)
            if stat == '3P%':
                st.markdown("""
                            Nota: Se observa una tendencia al alza en el porcentaje de triples a lo largo de los años analizados. Esto sugiere que las jugadoras de la WNBA están mejorando su habilidad para encestar desde la línea de tres puntos y que los equipos están adoptando estrategias que favorecen este tipo de tiro.
                            Si comparamos los datos de los últimos 10 años con los de las décadas anteriores, se aprecia un aumento más pronunciado en el porcentaje de triples, lo que indica una aceleración de esta tendencia en los últimos años.
                            """)
            if stat == 'DREB':
                st.markdown("""
                            Nota: A pesar de las fluctuaciones, se observa una tendencia general al alza en el DREB, especialmente a partir de mediados de la década de 2010. Esto indica que los equipos están poniendo un mayor énfasis en asegurar el rebote defensivo.
                            """)
            if stat == 'AST':
                st.markdown("""
                            Nota: El análisis del porcentaje de asistencias (AST) en la WNBA revela una tendencia al alza a lo largo de los años, lo que indica una evolución hacia un juego más colectivo y basado en la creación de oportunidades para las compañeras. Esta tendencia sugiere que el baloncesto femenino se ha vuelto más sofisticado tácticamente, con las jugadoras desarrollando una mayor habilidad para pasar el balón y reconocer las mejores opciones de anotación.

                            Varios factores pueden explicar este aumento en el porcentaje de asistencias. En primer lugar, el desarrollo de las bases ha sido fundamental. Las jugadoras en esta posición han mejorado significativamente sus habilidades de pase, visión de juego y capacidad para controlar el ritmo del partido. En segundo lugar, los cambios en los sistemas ofensivos de los equipos han favorecido un juego más fluido y basado en la circulación del balón. Los equipos modernos tienden a utilizar sistemas ofensivos más complejos que requieren una mayor colaboración entre las jugadoras y un mayor número de pases.

                            Además, el aumento del porcentaje de asistencias puede estar relacionado con otros factores, como la mejora en la calidad de la formación de las jugadoras, el énfasis en el juego en equipo en lugar del juego individual y la influencia de las tendencias generales del baloncesto a nivel mundial.

                            Al comparar el porcentaje de asistencias con otras estadísticas, como el porcentaje de triples, se observa una relación positiva. Esto sugiere que un aumento en el número de asistencias está asociado con un aumento en el número de triples anotados, lo que confirma la tendencia hacia un juego más basado en el movimiento del balón y la creación de tiros abiertos.

                            En conclusión, el análisis del porcentaje de asistencias en la WNBA muestra una clara evolución hacia un juego más colectivo y sofisticado. Esta tendencia es positiva y refleja el desarrollo del baloncesto femenino a nivel global. Sin embargo, es importante continuar analizando esta estadística en relación con otras variables para obtener una comprensión más completa de los factores que influyen en el éxito de los equipos y en la evolución del juego.
                            """)
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
