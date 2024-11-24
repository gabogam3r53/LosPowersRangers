import streamlit as st
from utils import load_data, load_image
from config import *
import pandas as pd

# Pagina configuracion 
st.set_page_config(
    page_title="WNBAmarket",
    layout="wide"
)

def main():
    st.title("Estadísticas de Jugadoras de la WNBA (2016-2024)")
    st.write("El presente proyecto se enfoca en el ámbito del baloncesto femenino de la WNBA, recopilando datos exhaustivos de las temporadas 2016-2024 directamente de las fuentes oficiales: Spotrac.com y Stats.wnba.com. Este conjunto de datos permitió realizar un análisis detallado de las jugadoras, sus estadísticas y tendencias a lo largo de los años.")

    # Cargar datos
    data = load_data(DATA_URL)
    if data is None:
        st.error("Failed to load data. Please try again later.")
        return
    data_correlacion = load_data(DATA_CORRELACION_URL)
    if data_correlacion is None:
        st.error("Failed to load data. Please try again later.")
        return
    # Crea tres secciones principales usando columnas
    col1, col2 = st.columns([2, 1])

    with col1:
        # Sección de tabla de datos
        with st.container():
            st.subheader("Estadísticas de jugadoras")
            st.dataframe(data, height=400)

        # Sección de estadísticas de contratos
        with st.container():
            st.subheader("Gráfica: Contrato contra Estadísticas Interesantes")
            contract_image = load_image(CONTRACT_GRAPH_URL)
            if contract_image:
                st.image(contract_image, use_column_width=True)
            st.markdown("""
                **Análisis de correlaciones entre estadísticas y valor de contrato en la WNBA**
        
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
            st.subheader("Tendencias Temporales en el Valor de Mercado")
            st.dataframe(data_correlacion, height=400)

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
            st.subheader("Gráfica: Jugadoras individuales")
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
                 * **Observacion:** Hay algunas jugadoras como por ejemplo "Natasha Howard", las cuales si se fijan en la grafica de puntos, tuvieron una mejora al pasar los años(primer contrato) y en consecuencia obtuvieron un mejor contrato debido a que las Fichó un nuevo equipo, ahora bien, este cambio hace que el numero de puntos que estaba teniendo anteriormente tienda a disminuir mientras se acostumbra a sus nuevas compañeras 
                y logre adaptarse para tener las mismas posibilidades de hacer puntos en su nuevo equipo.
                                    
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

        # Sección de Estadísticas Anuales
        with st.container():
            st.subheader("Gráfica: Media de estadísticas a traves de los años")
            stat = st.selectbox(
                "Selección de estadística:",
                options=STATS_COLUMNS
            )
            
            st.write(f"### Gráfica de {stat} a través de los años")
            stat_graph_url = f"{YEARLY_GRAPHS_DIR}{stat.replace(' ', '_')}.png"
            stat_image = load_image(stat_graph_url)
            if stat_image:
                st.image(stat_image, use_column_width=True)

if __name__ == "__main__":
    main()
