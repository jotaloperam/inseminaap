import streamlit as st
import pandas as pd
import pandas_profiling as pp
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from streamlit_option_menu import option_menu
import datetime
import numpy as np

#CONFIGURACION DE LA PÁGINA
st.set_page_config(
     page_title = 'INSEMINAAP',
     page_icon = '8Insemiaap.png',
     layout = 'wide')

# Variable global para almacenar los datos cargados
data = None

# Función para cargar datos desde archivos
def cargar_datos(archivos):
    """
    Carga los datos desde archivos.

    Parámetros:
    - archivos (list): Lista de archivos a cargar.

    Retorna:
    - DataFrame: Datos cargados desde los archivos.
    """
    dataframes = []
    for archivo in archivos:
        if archivo.type == 'csv':
            df = pd.read_csv(archivo)
            dataframes.append(df)
        elif archivo.type == 'xlsx':
            df = pd.read_excel(archivo)
            dataframes.append(df)
    if dataframes:
        return pd.concat(dataframes, ignore_index=True)
    else:
        return None

# Función para mostrar el contenido del DataFrame
def mostrar_contenido():
    """
    Muestra el contenido de los datos cargados en forma de tabla.
    """
    global data
    if data is not None:
        st.subheader("Contenido de los archivos cargados")
        st.table(data)
    else:
        st.warning("No se han cargado archivos de datos.")

# Función para mostrar gráficas
def mostrar_graficas():
    """
    Muestra gráficas a partir de los datos cargados.
    """
    global data
    if data is not None:
        st.subheader("Gráficas de los datos")
        columns = data.columns
        selected_column = st.selectbox("Selecciona una columna", columns)
        if selected_column:
            fig, ax = plt.subplots()
            ax.plot(data[selected_column])
            ax.set_xlabel("Índice")
            ax.set_ylabel(selected_column)
            ax.set_title("Gráfico de línea")
            st.write(f"<h3>{selected_column}</h3>", unsafe_allow_html=True)
            st.pyplot(fig)
    else:
        st.warning("No se han cargado archivos de datos.")

# Función para mostrar el dashboard
def mostrar_dashboard():
    """
    Muestra un dashboard de los datos cargados.
    """
    global data
    if data is not None:
        st.subheader("Dashboard de datos")
        fig = px.scatter(data, x='x_column', y='y_column')
        st.plotly_chart(fig)

# Función para registrar un nuevo animal
def registrar_animal(especie, nombre, edad, peso):
    """
    Registra un nuevo animal en los datos.

    Parámetros:
    - especie (str): Especie del animal.
    - nombre (str): Nombre del animal.
    - edad (int): Edad del animal.
    - peso (float): Peso del animal.

    Retorna:
    - DataFrame: Datos actualizados con el nuevo animal.
    """
    global data
    nuevo_animal = pd.DataFrame({"Especie": especie, "Nombre": nombre, "Edad": edad, "Peso": peso}, index=[0])
    data = pd.concat([data, nuevo_animal], ignore_index=True)
    return data

# Función para realizar seguimiento de ciclos reproductivos
def realizar_seguimiento(animal_id, fecha):
    """
    Realiza el seguimiento de un animal en una fecha específica.

    Parámetros:
    - animal_id (str): ID del animal.
    - fecha (datetime.date): Fecha del seguimiento.
    """
    global data
    if data is None:
        st.warning("No se han cargado archivos de datos.")
        return
    index = data[data["Animal_ID"] == animal_id].index
    # Realiza el seguimiento del animal utilizando el índice obtenido

# Función para generar un informe de inseminaciones realizadas
def generar_informe():
    """
    Genera un informe de inseminaciones realizadas.

    Retorna:
    - DataFrame: Informe de inseminaciones realizadas.
    """
    global data
    if data is not None:
        columnas_informe = ["Especie", "Nombre", "Fecha_Seguimiento"]
        if all(col in data.columns for col in columnas_informe):
            informe = data[columnas_informe]
            return informe
        else:
            st.warning("El archivo de datos no contiene las columnas necesarias para generar el informe.")
    else:
        st.warning("No se han cargado archivos de datos.")

# Función para programar un recordatorio
def programar_recordatorio(animal_id, fecha):
    """
    Programa un recordatorio para un animal en una fecha específica.

    Parámetros:
    - animal_id (str): ID del animal.
    - fecha (datetime.date): Fecha del recordatorio.
    """
    # Lógica para programar un recordatorio para una fecha específica
    pass

# Estilos personalizados para el sidebar
sidebar_styles = {
    "background-color": "#fafafa",
    "padding": "0!important"
}

# Estilos personalizados para el botón de carga de archivos
button_styles = {
    "background-color": "#fafafa",
    "font-family": "Arial",
    "font-size": "14px"
}

# Interfaz de usuario
def main():
    global data
    # Configuración de la página

    st.image('5_trans_inseminapp_c.png')
    st.sidebar.image('Vacunautas_Logo.png')

    # Establecer los estilos personalizados para el sidebar
    st.sidebar.markdown(
        f"""
        <style>
            .sidebar .sidebar-content {{
                {"; ".join(f"{key}: {value}" for key, value in sidebar_styles.items())}
            }}
            .sidebar .fileinput-button {{
                {"; ".join(f"{key}: {value}" for key, value in button_styles.items())}
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Botón para cargar archivos CSV y Excel
    uploaded_files = st.sidebar.file_uploader("Cargar archivos", type=['csv', 'xlsx'], accept_multiple_files=True)
    if uploaded_files:
        data = cargar_datos(uploaded_files)
        st.sidebar.success("Archivos cargados exitosamente.")

    # Crear el menú utilizando option_menu de la biblioteca streamlit-option-menu en el subheader
    with st.subheader("Opciones"):
        menu_options = ["Plantilla de datos"]
        selected = st.selectbox("Seleccione una opción", menu_options)

    # Crear el menú utilizando option_menu de la biblioteca streamlit-option-menu
    with st.sidebar:
        menu_options = ["Mostrar contenido", "Gráficas", "Dashboard", "Registrar animal", "Seguimiento de ciclos", "Generar informe", "Programar recordatorio"]
        selected = option_menu("Seleccione una opción", menu_options, default_index=0)

    # Opción: Mostrar contenido
    if selected == "Mostrar contenido":
        mostrar_contenido()

    # Opción: Gráficas
    elif selected == "Gráficas":
        mostrar_graficas()

    # Opción: Dashboard
    elif selected == "Dashboard":
        mostrar_dashboard()

    # Opción: Registrar animal
    elif selected == "Registrar animal":
        st.subheader("Registrar nuevo animal")
        especie = st.text_input("Especie")
        nombre = st.text_input("Nombre")
        edad = st.number_input("Edad", min_value=0)
        peso = st.number_input("Peso", min_value=0.0)
        if st.button("Registrar"):
            data = registrar_animal(especie, nombre, edad, peso)
            st.success("Animal registrado exitosamente.")

    # Opción: Seguimiento de ciclos
    elif selected == "Seguimiento de ciclos":
        st.subheader("Realizar seguimiento de ciclos reproductivos")
        animal_id = st.text_input("ID del animal")
        fecha = st.date_input("Fecha de seguimiento", datetime.date.today())
        if st.button("Realizar seguimiento"):
            data = realizar_seguimiento(animal_id, fecha)
            st.success("Seguimiento realizado exitosamente.")

    # Opción: Generar informe
    elif selected == "Generar informe":
        st.subheader("Generar informe de inseminaciones realizadas")
        informe = generar_informe()
        if informe is not None:
            st.table(informe)
        else:
            st.warning("El archivo de datos no contiene las columnas necesarias para generar el informe.")

    # Opción: Programar recordatorio
    elif selected == "Programar recordatorio":
        st.subheader("Programar recordatorio")
        animal_id = st.text_input("ID del animal")
        fecha = st.date_input("Fecha del recordatorio")
        if st.button("Programar"):
            programar_recordatorio(animal_id, fecha)
            st.success("Recordatorio programado exitosamente.")

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
