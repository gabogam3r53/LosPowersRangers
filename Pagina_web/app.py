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

    # Leyenda
    abbrev = pd.DataFrame.from_dict(ABBREVS_WNBA, orient='index', columns=['Meaning'])

    # Apply CSS styles directly to the DataFrame
    st.markdown(f"""
    <style>
    #my_custom_table td {{
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }}
    #my_custom_table th {{
        background-color: #f2f2f2;
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }}
    </style>
    """)
    
    st.table(abbrev, table_id="my_custom_table")

    
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

    with col2:
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
