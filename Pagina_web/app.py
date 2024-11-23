import streamlit as st
from utils import load_data, load_image
from config import *

# Pagina configuracion 
st.set_page_config(
    page_title="WNBAmarket",
    layout="wide"
)

def main():
    st.title("Estadísticas de Jugadoras de la WNBA (2016-2024)P")

    # Cargar datos
    data = load_data(DATA_URL)
    if data is None:
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
