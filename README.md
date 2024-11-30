POWER RANGERS

WNBAmarket: Análisis de las estadísticas que tienen mayor correlación con el valor de mercado de
las jugadoras de baloncesto en Estados Unidos.

El presente proyecto se enfoca en el ámbito del baloncesto femenino de la WNBA, recopilando
datos exhaustivos de las temporadas 2016-2024 directamente de las fuentes oficiales: Spotrac.com y Stats.wnba.com. Este conjunto de datos 
permitió realizar un análisis detallado de las jugadoras, sus estadísticas y tendencias a lo largo de los años.

--TABLA DE CONTENIDO--  
1. Nombre del equipo y nombre del proyecto     
2. Descripción  
3. Arquitectura   
4. Proceso  
5. Funcionalidades  
6. Estado del proyecto  
7. Agradecimientos  

[Arquitectura]

—Librerías de Scrapping:
BeautifulSoup ,  Selenium  ,  Webdriver_manager.chrome  ,   Schedule  ,   Logging  ,  CSV  ,   Datetime. 


—Liberías de visualizacion de datos:
Matplotlib (pyplot)  ,  Seaborn  ,  Numpy

—Librerías Generales: 
Streamlit  ,  Pandas  ,  Requests  ,  io (BytesIO)  ,  PIL (Image)

[Proceso]  
—Recopilación de información: Extracción de datos de las jugadoras desde el 2016 hasta el 2024 usando codigos y librerias de web scrapping para automatizar el proceso, incluyendo sus contratos y estadisticas para saber como ha actuado la liga a traves de casi 10 años

—Procesamiento de datos: Filtracion de información para obtener lo que es mas importante en la valoracion de una jugadora, como son:
Edad, Ranking del equipo al que pertenecen, Minutos en cancha, promedio de puntos por partido, asistencias por partido, porcentaje de tiros de campo, porcentaje de intentos en puntos de 3, porcentaje de tiros libres intentados, Robos por partido, tapones por partido, Rebotes, perdidas de balon, faltas cometidas, Dobles Dobles, Triples Dobles y +/- (Puntos que obtiene el equipo cuando la jugadora esta en cancha).

—Creacion de codigo CSV para guardar la información con los datos de las jugadoras. 

—Creacion de codigos de correlacion a traves del codigo CSV para poder detectar que estadisticas se toman mas en cuenta para el precio de mercado/valor de contrato

—Creacion de graficas de los equipos para reflejar visualmente que tipo de jugadoras buscan los equipos de la WNBA para adquirir sus servicios

—Creacion de una pagina web para visualizar los datos y leer las concluisones que se han llegado al observar la correlacion entre los contratos y las estadisticas de forma publica (https://powerrangers-wnbamarket.streamlit.app/)


[Funcionalidades]  
—Realización de análisis comparativo de correlaciones entre estadísticas y valor de contrato en la WNBA.  
—Visualizacion gráfica de la relación entre las estadísticas individuales de las jugadoras de la WNBA y el valor de sus contratos.  
—Análisis de las correlaciones en los contratos de jugadoras de la WNBA a través de los años.  
—Descubrir regularidades en la forma en que se valoran a las jugadoras.  




[Estado del Proyecto]  
FINALIZADO

[Agradecimientos]  
Expresamos nuestro agradecimiento a los profesores, Jenny Remolina y Álvaro Arauz, por su dedicación en la revisión y corrección de nuestros trabajos. Su ayuda nos ha permitido 
mejorar significativamente nuestros conocimientos en Python. Agradecemos también a nuestros compañeros por el intercambio de ideas y experiencias.
