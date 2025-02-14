# %%
#SE COMENTAN LOS Fig show
#SE DETERMINA RANGO DE FECHAS CORTO
import pandas as pd
import re

import regex
import demoji

import numpy as np
from collections import Counter

import plotly
import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS

import streamlit as st


st.markdown(
    """
    <link 
        rel="stylesheet" 
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" 
        integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" 
        crossorigin="anonymous"
    >
    """,
    
    unsafe_allow_html=True,
)





col1, col2, col3 = st.columns([1, 1, 1])  # Crea 3 columnas, la central es el doble de ancha

with col1:
    st.markdown(
        """
        <p style="text-align: center; align-items: center;">❤️🖤</p>
        """,
    
        unsafe_allow_html=True,
    )

with col2:  # Inserta la imagen en la columna central
    st.image("Recursos/Iconos/myl.png", width=100,use_container_width=True )

with col3:
    st.markdown(
        """
        <p style="text-align: center; align-items: center;">🖤❤️</p>
        """,

        unsafe_allow_html=True,
    )  





st.markdown(
    """


<style>
.fade-in1 {
  opacity: 0; /* Inicialmente oculto */
  animation: fadeIn 5s ease-in-out forwards; /* Animación al cargar */
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>

<div class="fade-in1">
  <h1 style="align-items: center; text-align: center;">Mi bombón sabor 🍓</h1>
</div>
    """,
    
    unsafe_allow_html=True,
)

st.markdown(
    """


<style>
.fade-in2 {
  opacity: 0; /* Inicialmente oculto */
  animation: fadeIn 10s ease-in-out forwards; /* Animación al cargar */
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>

<div class="fade-in2">
  <p style="align-items: center; text-align: center;">En cualquier parte que estés, si te sientes feliz, emocionada, triste o si sólo quieres recordar nuestra hermosa relación, te regalo este espacio virtual que creé exclusivamente para ti <strong>Mi Bombón</strong></p>
</div>
    """,
    
    unsafe_allow_html=True,
)


col1, col2, col3 = st.columns([1, 1, 1])  # Crea 3 columnas, la central es el doble de ancha

with col1:
    st.write()

with col2:  # Inserta la imagen en la columna central
    st.image("Recursos/Pic/3.png", width=500,use_container_width=True )

with col3:
    st.write()


st.markdown(
    """


<style>
.fade-in2 {
  opacity: 0; /* Inicialmente oculto */
  animation: fadeIn 10s ease-in-out forwards; /* Animación al cargar */
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>

<div class="fade-in2">
  <p> 🐢Cada cimiento de esta plataforma la construí con mucha dedicación y amor, esto sólo es el principio de muchas cosas interesantes que quiero mostrarte a través de este espacio y mostrarte algunas habilidades que recientemente he aprendido relacionada con la analítica de datos.🐢</p>
</div>
    """,
    
    unsafe_allow_html=True,
)


if st.button("Mostrar dedicatoria",type="primary", use_container_width=True):
    st.write("Para mí, el utilizar los conocimientos sobre la analítica de datos para mostrar datos interesantes sobre muchos aspectos de la vida que pueden ser útiles para mejorar, la asimilo como una herramienta fundamental para mi y los grandes proyectos que quiero lograr. Crear fue espacio es terapéutico para mí porque, al mismo tiempo que pongo en práctica algunas cosas nuevas que voy aprendiendo, me sirve como relajación y un reto mental demandante.")

st.header("Análisis de nuestro Chat de Whatsapp 💬")

st.write("Te quiero presentar la primera sección de esta plataforma 🤩 (La cual iré actualizando con el tiempo), esta sección consiste en un proyecto que programé para analizar los datos de TODO nuestro chat de WhatsApp, desde el primer mensaje que te envié, hasta el último. Es algo totalmente nuevo para mí y por eso espero me falta mejorar, pero por el momento espero te guste")




# %%
#DEFINICIÓN FORMATOS

# Patron regex para identificar el comienzo de cada línea del txt con la fecha y la hora
def IniciaConFechaYHora(s):
    # Ejemplo: '9/16/23, 5:59 PM - ...'
    
    patron = '^([1-9]|1[0-9]|2[0-9]|3[0-1])(\/)([1-9]|1[0-2])(\/)(2[0-9]), ([0-9]+):([0-9][0-9])\s?([AP][M]) -'
    
    resultado = re.match(patron, s)  # Verificar si cada línea del txt hace match con el patrón de fecha y hora
    if resultado:
        return True
    return False

# Patrón para encontrar a los miembros del grupo dentro del txt
def EncontrarMiembro(s):
    patrones = ['Leonel Rivas:', 'Mi Bombon 🖤:']

    patron = '^' + '|'.join(patrones)
    resultado = re.match(patron, s)  # Verificar si cada línea del txt hace match con el patrón de miembro
    if resultado:
        return True
    return False

# Separar las partes de cada línea del txt: Fecha, Hora, Miembro y Mensaje
def ObtenerPartes(linea):
    
    splitLinea = linea.split(' - ')
    FechaHora = splitLinea[0]                    
    splitFechaHora = FechaHora.split(', ')
    Fecha = splitFechaHora[0]                    
    Hora = ' '.join(splitFechaHora[1:])          
    Mensaje = ' '.join(splitLinea[1:])             
    if EncontrarMiembro(Mensaje):
        splitMensaje = Mensaje.split(': ')
        Miembro = splitMensaje[0]               
        Mensaje = ' '.join(splitMensaje[1:])    
    else:
        Miembro = None       
    return Fecha, Hora, Miembro, Mensaje

# %%
#LECTURA DE ARCHIVO Y MUESTREO DE TABLA COMPLETA

# Leer el archivo txt descargado del chat de WhatsApp
RutaChat = 'Data/Chat mi bombon.txt'

# Lista para almacenar los datos (Fecha, Hora, Miembro, Mensaje) de cada línea del txt
DatosLista = []
with open(RutaChat, encoding="utf-8") as fp:
    fp.readline() # Eliminar primera fila relacionada al cifrado de extremo a extremo
    Fecha, Hora, Miembro = None, None, None
    while True:
        linea = fp.readline()
        if not linea:
            break
        linea = linea.strip()
        if IniciaConFechaYHora(linea): # Si cada línea del txt coincide con el patrón fecha y hora
            Fecha, Hora, Miembro, Mensaje = ObtenerPartes(linea) # Obtener datos de cada línea del txt
            DatosLista.append([Fecha, Hora, Miembro, Mensaje])

# Convertir la lista con los datos a dataframe
df = pd.DataFrame(DatosLista, columns=['Fecha', 'Hora', 'Miembro', 'Mensaje'])

# Cambiar la columna Fecha a formato datetime
df['Fecha'] = pd.to_datetime(df['Fecha'], format="%d/%m/%y")

# Eliminar los posibles campos vacíos del dataframe
# y lo que no son mensajes como cambiar el asunto del grupo o agregar a alguien
df = df.dropna()

# Resetear el índice
df.reset_index(drop=True, inplace=True)
#df

# %%
#DEFINICIÓN DE RANGO DE FECHAS DE ANALISIS

#Fecha inicio - Fin (Año, Mes, Día)
#start_date = '2023-10-15'
#end_date = '2024-12-28'

start_date = '2023-9-16'
end_date = '2025-2-13'



df = df[(df['Fecha'] >= start_date) & (df['Fecha'] <= end_date)]
st.write("RANGO DE ANALISIS")
st.markdown(
    """

<div class="fade-in2">
  <p style="align-items: center; text-align: center;"><strong>Inicio</strong></p>
</div>
    """,
    
    unsafe_allow_html=True,
)
st.write(df.head(1))
st.markdown(
    """

<div class="fade-in2">
  <p style="align-items: center; text-align: center;"><strong>Fin</strong></p>
</div>
    """,
    
    unsafe_allow_html=True,
)
st.write(df.tail(1))

start_color, end_color = st.select_slider(
    "Rango de fechas de analisis",
    options=[
        "Septiembre 2023",
        "Octubre 2023",
        "Noviembre 2023",
        "Diciembre 2023",
        "Enero 2024",
        "Febrero 2024",
        "Marzo 2024",
        "Abril 2024",
        "Mayo 2024",
        "Junio 2024",
        "Julio 2024",
        "Agosto 2024",
        "Septiembre 2024",
        "Octubre 2024",
        "Noviembre 2024",
        "Diciembre 2024",
        "Enero 2025",
        "Febrero 2025",
    ],
    value=("Septiembre 2023", "Febrero 2025"),
)
st.write("Selección de fechas de ", start_color, "a", end_color, " (Próximamente bb) 😁 ")


# %%
#CONTEO

def ObtenerEmojis(Mensaje):
    emoji_lista = []
    data = regex.findall(r'\X', Mensaje)  # Obtener lista de caracteres de cada mensaje
    for caracter in data:
        if demoji.replace(caracter) != caracter:
            emoji_lista.append(caracter)
    return emoji_lista

# Obtener la cantidad total de mensajes
total_mensajes = df.shape[0]

# Obtener la cantidad de archivos multimedia enviados
multimedia_mensajes = df[df['Mensaje'] == '<Multimedia omitido>'].shape[0]

# Obtener la cantidad de emojis enviados
df['Emojis'] = df['Mensaje'].apply(ObtenerEmojis) # Se agrega columna 'Emojis'
emojis = sum(df['Emojis'].str.len())

# Obtener la cantidad de links enviados
url_patron = r'(https?://\S+)'
df['URLs'] = df.Mensaje.apply(lambda x: len(re.findall(url_patron, x))) # Se agrega columna 'URLs'
links = sum(df['URLs'])

#Obtener la cantidad de veces que le he pedido uber:
url_patron_ubereats = r'(\bte está llegando un regalo\b)'
df['PedidosUber'] = df.Mensaje.apply(lambda y: len(re.findall(url_patron_ubereats, y))) # Se agrega columna 'URLs'
ubereats = sum(df['PedidosUber'])


#Obtener la cantidad de veces que le he dicho te amo:
amo_patron = r'(\bamo\b)'
df['TeAmos'] = df.Mensaje.apply(lambda y: len(re.findall(amo_patron, y))) # Se agrega columna 'URLs'
teAmos = sum(df['TeAmos'])

#Obtener la cantidad de veces que me gusta d ti
encanta_patron = r'(\bAlgo que me\b)'
df['Rutina'] = df.Mensaje.apply(lambda y: len(re.findall(encanta_patron, y))) # Se agrega columna 'URLs'
encanta = sum(df['Rutina'])

#Obtener la cantidad de veces que me gusta d ti
noches_patron = r'(\bBuenas noches\b)'
df['BuenasNoches'] = df.Mensaje.apply(lambda y: len(re.findall(noches_patron, y))) # Se agrega columna 'URLs'
noches = sum(df['BuenasNoches'])



# Todos los datos pasarlo a diccionario
estadistica_dict = {'Tipo': ['Mensajes', 'Multimedia', 'Emojis', 'Links','Ubereats','Teamos','Rutina','Noches'],
        'Cantidad': [total_mensajes, multimedia_mensajes, emojis, links, ubereats,teAmos,encanta,noches ]
        }

#Convertir diccionario a dataframe
estadistica_df = pd.DataFrame(estadistica_dict, columns = ['Tipo', 'Cantidad'])

# Establecer la columna Tipo como índice
estadistica_df = estadistica_df.set_index('Tipo')



st.subheader("🐢 - Conteo de cosas importantes para nosotros")

col1, col2 = st.columns([2, 1])  # Crea 3 columnas, la central es el doble de ancha

with col1:
    st.write("Veces que nos hemos dicho Te amo:")
    st.write(teAmos, " Te amo's ❤️")

with col2:  # Inserta la imagen en la columna central
    st.image("Recursos/Iconos/myl2.png", width=200,use_container_width=True )


col1, col2 = st.columns([2, 1])  # Crea 3 columnas, la central es el doble de ancha

with col1:
    st.write("Veces que nos hemos hemos deseado Buenas noches 🌕")
    st.write(noches, " Buenas noches (Puede variar por las mayúsculas)",)

with col2:  # Inserta la imagen en la columna central
    st.image("Recursos/Iconos/luna.png", width=200,use_container_width=True )


col1, col2 = st.columns([2, 1])  # Crea 3 columnas, la central es el doble de ancha

with col1:
    st.write("Veces que te he consentido pidiendote Uber Eats 😋")
    st.write(ubereats, " Pedidos con dedicatoria especial",)

with col2:  # Inserta la imagen en la columna central
    st.image("Recursos/Iconos/ubereats.png", width=200,use_container_width=True )


col1, col2 = st.columns([2, 1])  # Crea 3 columnas, la central es el doble de ancha

with col1:
    st.write("Veces que nos hemos dicho lo que nos encanta de nosotros ❤️")
    st.write(ubereats, " Veces que nos hemos dicho lo que nos gusta el uno del otro",)

with col2:  # Inserta la imagen en la columna central
    st.image("Recursos/Pic/2.png", width=200,use_container_width=True )







# %%
#LISTA DE EMOJIS MÁS USADOS

# Obtener emojis más usados y las cantidades en el chat del grupo del dataframe
emojis_lista = list([a for b in df.Emojis for a in b])
emoji_diccionario = dict(Counter(emojis_lista))
emoji_diccionario = sorted(emoji_diccionario.items(), key=lambda x: x[1], reverse=True)

# Convertir el diccionario a dataframe
emoji_df = pd.DataFrame(emoji_diccionario, columns=['Emoji', 'Cantidad'])

# Establecer la columna Emoji como índice
emoji_df = emoji_df.set_index('Emoji').head(10)

st.subheader("🐢 - Emojis y contador")

col1, col2 = st.columns([2, 1])  # Crea 3 columnas, la central es el doble de ancha

with col1:
    st.write(estadistica_df)

with col2:  # Inserta la imagen en la columna central
    st.write(emoji_df)


