import streamlit as st
import pandas as pd
import datetime
import openpyxl
from streamlit_option_menu import option_menu
import plotly.express as px
import altair as alt
import matplotlib.pyplot as plt
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
from io import StringIO

# Obtener la fecha actual en español
meses = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]

dias_semana = [
    "lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"
]

now = datetime.now()
current_date = f"{dias_semana[now.weekday()]}, {now.day} de {meses[now.month - 1]} de {now.year}"

# Mostrar la fecha en la barra lateral
st.sidebar.title(f'📅 Fecha:')
st.sidebar.markdown(
    f'<h2 style="color: #333;">{current_date}</h2>',
    unsafe_allow_html=True
)

# Cambiar el fondo de color del sidebar
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Separar con línea horizontal
st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# Configuración del menú principal en la barra lateral
with st.sidebar:
    selected = option_menu(
        menu_title='Menu Principal',
        options=['Principal', 'Estado de Camas', 'Visualizar Camas', 'Ingresar Cama', 'Ingresar Atencion', 'Medicos'],
        menu_icon='gear',
        icons=['', '', '', '', '', ''],
        default_index=0,
        orientation='vertical',
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "red", "font-size": "16px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "lightblue"},
        }
    )
    
#####################################################################################################    
# Se crean funciones para leer archivos .xlsx

# Función para cargar el archivo ATB.xlsx
def cargar_ATB():
    try:
        df = pd.read_excel('data\ATB.xlsx')
        return df
    except FileNotFoundError:
        df_ATB = pd.DataFrame(columns=['CAMA', 'DNI', 'FECHA', 'ATB','FINALIZA'])
        return df_ATB

# Función para cargar el archivo Cama.xlsx
def cargar_Cama():
    try:
        df = pd.read_excel(r'data\Cama.xlsx')
        return df
    except Exception as e:
        print(f"No se pudo cargar Cama.xlsx: {e}")
        return None

# Función para cargar el archivo Cultivo.xlsx
def cargar_Cultivo():
    try:
        df = pd.read_excel('data\Cultivo.xlsx')
        return df
    except FileNotFoundError:
        df_Cultivo = pd.DataFrame(columns=['CAMA', 'DNI', 'FECHA', 'METODO','RESULTADO'])
        return df_Cultivo

# Función para cargar el archivo Diagnostico.xlsx
def cargar_Diagnostico():
    try:
        df = pd.read_excel('data\Diagnostico.xlsx')
        return df
    except FileNotFoundError:
        df_Diagnostico = pd.DataFrame(columns=['CAMA', 'DNI', 'FECHA', 'DIAGNOSTICO'])
        return df_Diagnostico

# Función para cargar el archivo Examen Complementario.xlsx
def cargar_ExamenComplementario():
    try:
        df = pd.read_excel('data\Examen Complementario.xlsx')
        return df
    except FileNotFoundError:
        df_ExamenComplementario = pd.DataFrame(columns=['CAMA', 'DNI', 'FECHA', 'EX. COMPLEMENTARIO'])
        return df_ExamenComplementario

# Función para cargar el archivo Funciones Fisiologicas.xlsx
def cargar_FuncionesFisiologicas():
    try:
        df = pd.read_excel('data\Funciones Fisiologicas.xlsx')
        return df
    except FileNotFoundError:
        df_FuncionesFisiologicas = pd.DataFrame(columns=['CAMA', 'DNI', 'FECHA', 'ALIMENTACION', 'DIURESIS', 'CATARSIS'])
        return df_FuncionesFisiologicas

# Función para cargar el archivo Laboratorio.xlsx
def cargar_Laboratorio():
    try:
        df = pd.read_excel('data\Laboratorio.xlsx')
        return df
    except FileNotFoundError:
        df_Laboratorio = pd.DataFrame(columns=['CAMA', 'DNI', 'FECHA', 'LABORATORIOS'])
        return df_Laboratorio

# Función para cargar el archivo Paciente.xlsx
def cargar_Paciente():
    try:
        df = pd.read_excel('data\Paciente.xlsx')
        return df
    except FileNotFoundError:
        df_Paciente = pd.DataFrame(columns=['DNI', 'NOMBRE', 'APELLIDO', 'EDAD','CAMA', 'FECHA NAC', 'FECHA ING', 'ANTECEDENTES', 'DIAGNOSTICO', 'MEDICO', 'FECHA REGISTRO', 'HORA REGISTRO'])
        return df_Paciente

# Función para cargar el archivo Procedimiento.xlsx
def cargar_Procedimiento():
    try:
        df = pd.read_excel('data\Procedimiento.xlsx')
        return df
    except FileNotFoundError:
        df_Procedimiento = pd.DataFrame(columns=['CAMA', 'DNI', 'FECHA', 'METODO'])
        return df_Procedimiento

# Función para cargar el archivo Medico.xlsx
def cargar_Medico():
    try:
        df = pd.read_excel('data/Medico.xlsx')
        return df
    except FileNotFoundError:
        df_Medico = pd.DataFrame(columns=['DNI', 'NOMBRE', 'APELLIDO', 'TELEFONO','EMAIL'])
        return df_Medico
    

# Asignar los DataFrame a cada variable:
df_ATB = cargar_ATB()
df_Cama = cargar_Cama()
df_Cultivo = cargar_Cultivo()
df_Diagnostico = cargar_Diagnostico()
df_ExamenComplementario = cargar_ExamenComplementario()
df_FuncionesFisiologicas = cargar_FuncionesFisiologicas()
df_Laboratorio = cargar_Laboratorio()
df_Paciente = cargar_Paciente()
df_Procedimiento = cargar_Procedimiento()
df_Medico = cargar_Medico()


# Funciones para guardar cada DataFrame en un archivo Excel
def guardar_ATB(df):
    try:
        df.to_excel('data\ATB.xlsx', index=False)
        print("DataFrame ATB guardado exitosamente en ATB.xlsx")
    except Exception as e:
        print(f"No se pudo guardar ATB.xlsx: {e}")

def guardar_Cama(df):
    try:
        df.to_excel('data\Cama.xlsx', index=False)
        print("DataFrame Cama guardado exitosamente en Cama.xlsx")
    except Exception as e:
        print(f"No se pudo guardar Cama.xlsx: {e}")

def guardar_Cultivo(df):
    try:
        df.to_excel('data\Cultivo.xlsx', index=False)
        print("DataFrame Cultivo guardado exitosamente en Cultivo.xlsx")
    except Exception as e:
        print(f"No se pudo guardar Cultivo.xlsx: {e}")

def guardar_Diagnostico(df):
    try:
        df.to_excel('data\Diagnostico.xlsx', index=False)
        print("DataFrame Diagnostico guardado exitosamente en Diagnostico.xlsx")
    except Exception as e:
        print(f"No se pudo guardar Diagnostico.xlsx: {e}")

def guardar_ExamenComplementario(df):
    try:
        df.to_excel('data\Examen Complementario.xlsx', index=False)
        print("DataFrame Examen Complementario guardado exitosamente en Examen Complementario.xlsx")
    except Exception as e:
        print(f"No se pudo guardar Examen Complementario.xlsx: {e}")

def guardar_FuncionesFisiologicas(df):
    try:
        df.to_excel('data\Funciones Fisiologicas.xlsx', index=False)
        print("DataFrame Funciones Fisiologicas guardado exitosamente en Funciones Fisiologicas.xlsx")
    except Exception as e:
        print(f"No se pudo guardar Funciones Fisiologicas.xlsx: {e}")

def guardar_Laboratorio(df):
    try:
        df.to_excel('data\Laboratorio.xlsx', index=False)
        print("DataFrame Laboratorio guardado exitosamente en Laboratorio.xlsx")
    except Exception as e:
        print(f"No se pudo guardar Laboratorio.xlsx: {e}")

def guardar_Paciente(df):
    try:
        df.to_excel('data\Paciente.xlsx', index=False)
        print("DataFrame Paciente guardado exitosamente en Paciente.xlsx")
    except Exception as e:
        print(f"No se pudo guardar Paciente.xlsx: {e}")

def guardar_Procedimiento(df):
    try:
        df.to_excel('data\Procedimiento.xlsx', index=False)
        print("DataFrame Procedimiento guardado exitosamente en Procedimiento.xlsx")
    except Exception as e:
        print(f"No se pudo guardar Procedimiento.xlsx: {e}")
        
def guardar_Medico(df):
    try:
        df.to_excel('data/Medico.xlsx', index=False)
        print("DataFrame Medico guardado exitosamente en Medico.xlsx")
    except Exception as e:
        print(f"No se pudo guardar Medico.xlsx: {e}")
        
        
# #############################################################################################################

if selected == 'Principal':
    # Título de la aplicación
    st.image('imagen/banner.jpg')
    st.write('*************')  
    
    # Descripción de la aplicación
    st.markdown("""
    ## Bienvenida a la Aplicación de Gestión Hospitalaria

    Esta aplicación está diseñada para facilitar la administración y el seguimiento de la ocupación y disponibilidad de camas en un hospital, así como la gestión de atención médica y la información de los médicos. La interfaz intuitiva y el menú lateral desplegable permiten un acceso rápido y eficiente a todas las funcionalidades esenciales. A continuación, se presenta una descripción detallada de cada una de las opciones del menú.

    ### Opciones del Menú Lateral

    1. **Principal**
       - **Descripción**: Esta es la página principal de la aplicación. Aquí puedes obtener una visión general del estado actual de las operaciones y acceder a información relevante y actualizada. Es el punto de partida para navegar por las demás secciones.

    2. **Estado de Camas**
       - **Descripción**: En esta sección, puedes visualizar el estado actual de todas las camas en el hospital. Esto incluye información sobre cuáles camas están ocupadas y cuáles están disponibles. También permite cambiar el estado de una cama de ocupada a libre cuando corresponda.

    3. **Visualización de Camas**
       - **Descripción**: Esta opción proporciona una vista detallada y organizada de todas las camas del hospital. Es útil para obtener una comprensión completa de la distribución y ocupación de las camas en tiempo real.

    4. **Ingresar Camas**
       - **Descripción**: Esta sección permite al personal administrativo agregar nuevas camas al sistema. Es esencial para mantener actualizada la base de datos de camas disponibles y asegurar una gestión eficiente del espacio hospitalario.

    5. **Ingresar Atención**
       - **Descripción**: Aquí se registran los datos de atención de los pacientes. Esta funcionalidad es crucial para llevar un seguimiento detallado de los tratamientos y atenciones recibidas por cada paciente, asegurando así una gestión integral de la salud de los mismos.

    6. **Médicos**
       - **Descripción**: En esta sección, se puede gestionar la información de los médicos del hospital. Incluye la capacidad de añadir nuevos médicos, actualizar la información existente y asegurar que los datos de contacto y especialidades de los médicos estén siempre actualizados.


    """)
    
    st.write('*************')
 
        
# #############################################################################################################

if selected == 'Estado de Camas':
    # Título de la aplicación
    st.image('imagen/banner.jpg')    
    st.title("Estado de Camas 🛏️:")

    st.write('*************')        
    
    # Visualizar las camas 
    st.markdown("**<p style='font-size:20px;'>Visualizar el estado de las Camas:</p>**", unsafe_allow_html=True)    
    st.dataframe(df_Cama)
    st.write('*************')
    
    st.markdown("**<p style='font-size:20px;'>Elija la Cama que desea Modificar. Seleccione una opcion:</p>**", unsafe_allow_html=True)
    # Selector para el número de cama
    numero_cama = st.selectbox("**Numero de Cama**", df_Cama['CAMA'], index=0, placeholder="Elija una opcion")
    
    # Filtrar la fila correspondiente al número de cama seleccionado
    fila_seleccionada = df_Cama[df_Cama['CAMA'] == numero_cama]
    
    if not fila_seleccionada.empty:
        # Mostrar el estado actual
        estado_actual = fila_seleccionada['OCUPACION'].values[0]
        st.info(f"El estado actual de la cama {numero_cama} es: {estado_actual}")

        if estado_actual == 'OCUPADA':
            # Botón para confirmar el cambio a 'LIBRE'
            if st.button("Cambiar a LIBRE"):
                # Actualizar el DataFrame
                df_Cama.loc[df_Cama['CAMA'] == numero_cama, 'OCUPACION'] = 'LIBRE'
                guardar_Cama(df_Cama)
                
                st.success(f"El estado de la cama {numero_cama} ha sido cambiado a LIBRE.")
                
                # Mostrar el DataFrame actualizado
                st.write('*************')
                st.markdown("**<p style='font-size:20px;'>Estado Actualizado de las Camas:</p>**", unsafe_allow_html=True)
                st.dataframe(df_Cama)
        else:
            st.error("Debe seleccionar la opción de ingresar cama en el menú y cargar los datos.")

        
# #############################################################################################################

if selected == 'Visualizar Camas':
    # Título de la aplicación
    st.image('imagen/banner.jpg')
    st.title("Visualizacion de Camas 🛏️:")
    st.write('*************')
    
    st.markdown("**<p style='font-size:20px;'>Elija la Cama que desea controlar. Seleccione una opcion:</p>**", unsafe_allow_html=True)
    # Selector para el número de cama
    numero_cama = st.selectbox("**Numero de Cama**", df_Cama['CAMA'], index=0, placeholder="Elija una opcion")
    
    # Filtrar la fila correspondiente al número de cama seleccionado
    fila_seleccionada = df_Cama[df_Cama['CAMA'] == numero_cama]
    
    # Verificar el estado de ocupación de la cama seleccionada
    if fila_seleccionada['OCUPACION'].values[0] == 'OCUPADA':
        st.warning('La cama está Ocupada.')

        # Filtrar las filas correspondientes al número de cama seleccionado en df_Paciente
        pacientes_cama_seleccionada = df_Paciente[df_Paciente['CAMA'] == numero_cama]
        
        # Ordenar por la columna de fecha de ingreso en orden descendente y seleccionar la primera fila
        paciente_reciente = pacientes_cama_seleccionada.sort_values(by='FECHA ING', ascending=False).iloc[0]
        
        # Extraer el DNI del paciente reciente
        dni = paciente_reciente["DNI"]
        st.write('*************')
        st.error(f'**Diagnostico:** {paciente_reciente["DIAGNOSTICO"]}')
        

        col1, col2 = st.columns(2)
        
        with col1:
            st.write('\n')
            st.markdown(f'**Cama:** {int(paciente_reciente["CAMA"])}')
            st.markdown(f'**Nombre:** {paciente_reciente["NOMBRE"]}')
            st.markdown(f'**Apellido:** {paciente_reciente["APELLIDO"]}')
            st.markdown(f'**Dni:** {int(paciente_reciente["DNI"])}')
            st.markdown(f'**Edad:** {int(paciente_reciente["EDAD"])}')
            fecha_nac_formateada = pd.to_datetime(paciente_reciente["FECHA NAC"]).strftime('%d/%m/%Y')
            st.markdown(f'**Fecha Nacimiento:** {fecha_nac_formateada}')

            
            
        with col2:
            st.write('\n')
            st.markdown(f'**Fecha Ingreso:** {paciente_reciente["FECHA ING"]}')
            st.markdown(f'**Hora Registro:** {paciente_reciente["HORA REGISTRO"]}')
            st.markdown(f'**Medico:** {paciente_reciente["MEDICO"]}')
            st.markdown(f'**Antecedentes:** {paciente_reciente["ANTECEDENTES"]}') 
        
 
        # Filtrar cada DataFrame por el DNI del paciente reciente
        df_FuncionesFisiologicas_filtrado = df_FuncionesFisiologicas[df_FuncionesFisiologicas["DNI"] == dni]
        df_Diagnostico_filtrado = df_Diagnostico[df_Diagnostico["DNI"] == dni]
        df_Cultivo_filtrado = df_Cultivo[df_Cultivo["DNI"] == dni]
        df_Laboratorio_filtrado = df_Laboratorio[df_Laboratorio["DNI"] == dni]
        df_ExamenComplementario_filtrado = df_ExamenComplementario[df_ExamenComplementario["DNI"] == dni]
        df_Procedimiento_filtrado = df_Procedimiento[df_Procedimiento["DNI"] == dni]
        df_ATB_filtrado = df_ATB[df_ATB["DNI"] == dni]
        st.write('*************')



        st.info('**Funciones Fisiologicas:**')
        st.write(df_FuncionesFisiologicas_filtrado[['FECHA', 'ALIMENTACION', 'DIURESIS', 'CATARSIS']])

        st.write('*************')
        st.info('**Diagnostico:**')
        st.write(df_Diagnostico_filtrado[['FECHA', 'DIAGNOSTICO']])

        st.write('*************')
        st.info('**Cultivos:**')
        st.write(df_Cultivo_filtrado[['FECHA','METODO', 'RESULTADO']])

        st.write('*************')
        st.info('**Laboratorios:**')
        st.write(df_Laboratorio_filtrado[['FECHA', 'LABORATORIOS']])

        st.write('*************')
        st.info('**Examen Complementario:**')
        st.write(df_ExamenComplementario_filtrado[['FECHA', 'EX. COMPLEMENTARIO']])

        st.write('*************')
        st.info('**Procedimientos:**')
        st.write(df_Procedimiento_filtrado[['FECHA', 'METODO']])

        st.write('*************')
        st.info('**ATB:**')
        st.write(df_ATB_filtrado[['FECHA','ATB', 'FINALIZA']])

        
        
        # Función para convertir DataFrame a texto
        def df_to_text(df, title):
            if df.empty:
                return ''
            text = f'{title}\n'
            text += df.to_string(index=False)
            text += '\n\n'
            return text

        # Combinando toda la información en un solo string
        info_text = f'Cama: {int(paciente_reciente["CAMA"])}\n'
        info_text += f'Nombre: {paciente_reciente["NOMBRE"]}\n'
        info_text += f'Apellido: {paciente_reciente["APELLIDO"]}\n'
        info_text += f'Dni: {int(paciente_reciente["DNI"])}\n'
        info_text += f'Edad: {int(paciente_reciente["EDAD"])}\n'
        info_text += f'Fecha Nacimiento: {paciente_reciente["FECHA NAC"]}\n'
        info_text += f'Fecha Ingreso: {paciente_reciente["FECHA ING"]}\n'
        info_text += f'Hora Registro: {paciente_reciente["HORA REGISTRO"]}\n'
        info_text += f'Medico: {paciente_reciente["MEDICO"]}\n'
        info_text += f'Antecedentes: {paciente_reciente["ANTECEDENTES"]}\n'
        info_text += f'Diagnostico: {paciente_reciente["DIAGNOSTICO"]}\n'
        info_text += '\n*************\n\n'

        info_text += df_to_text(df_FuncionesFisiologicas[['FECHA', 'ALIMENTACION', 'DIURESIS', 'CATARSIS']], 'Funciones Fisiologicas:')
        info_text += df_to_text(df_Diagnostico[['FECHA', 'DIAGNOSTICO']], 'Diagnostico:')
        info_text += df_to_text(df_Cultivo[['FECHA', 'METODO', 'RESULTADO']], 'Cultivos:')
        info_text += df_to_text(df_Laboratorio[['FECHA', 'LABORATORIOS']], 'Laboratorios:')
        info_text += df_to_text(df_ExamenComplementario[['FECHA', 'EX. COMPLEMENTARIO']], 'Examen Complementario:')
        info_text += df_to_text(df_Procedimiento[['FECHA', 'METODO']], 'Procedimientos:')
        info_text += df_to_text(df_ATB[['FECHA', 'ATB', 'FINALIZA']], 'ATB:')
        info_text += '*************\n'
        

        # Convertir el texto a un archivo descargable
        downloadable_text = StringIO(info_text)
        
        st.write('*************')
        st.subheader('**Descarga la Informacion de la Cama Seleccionada:**')
        
        nombre_archivo = f"Cama_{paciente_reciente['CAMA']}_{paciente_reciente['NOMBRE'].replace(' ', '_')}_{paciente_reciente['APELLIDO'].replace(' ', '_')}.txt"
        
        # Botón para descargar el texto
        st.download_button(label='Descargar Información', data=downloadable_text.getvalue(),file_name=nombre_archivo,
                           mime='text/plain')
        
    
    
    else:
        st.error('La cama está Libre. Si ha sido ocupada, recuerde ingresar el cambio en el sistema.')
    

    

    st.write('*************')
    # Visualizar las camas 
    st.markdown("**<p style='font-size:20px;'>Visualizar el estado de las Camas:</p>**", unsafe_allow_html=True)    
    st.dataframe(df_Cama)      
        
# #############################################################################################################

if selected == 'Ingresar Cama':
    # Título de la aplicación
    st.image('imagen/banner.jpg')
    st.title("Gestión de Camas - 🛏️:")
    st.write('*************')
    
    st.markdown("**<p style='font-size:20px;'>Para agregar un Nuevo Ingreso de Cama, Seleccione una opcion:</p>**", unsafe_allow_html=True)
    
    # Crear una columna temporal con nombre y apellido combinados
    df_Medico['NOMBRE_COMPLETO'] = df_Medico['NOMBRE'] + ' ' + df_Medico['APELLIDO']
    
    # Selector para el número de cama
    numero_cama = st.selectbox("**Numero de Cama**", df_Cama['CAMA'], index=0, placeholder="Elija una opcion")
    
    # Filtrar la fila correspondiente al número de cama seleccionado
    fila_seleccionada = df_Cama[df_Cama['CAMA'] == numero_cama]
    
    # Verificar el estado de ocupación de la cama seleccionada
    if fila_seleccionada['OCUPACION'].values[0] == 'LIBRE':
        st.write('La cama está Libre')
        
        # Formulario para ingresar datos del paciente
        with st.form(key="form_ingresar_cama", clear_on_submit=True):
            dni = st.text_input("DNI", autocomplete=None).upper()
            nombre = st.text_input("NOMBRE", autocomplete=None).upper()
            apellido = st.text_input("APELLIDO").upper()
            edad = st.number_input("EDAD", min_value=0, value=None, step=1, format="%d", placeholder="Escribe un número")
                        
            # Campo de entrada de texto para la fecha de nacimiento
            fecha_texto = st.text_input("INGRESE FECHA DE NACIMIENTO (DD/MM/YYYY)")
            
            # Convertir la cadena de texto en objeto de fecha
            try:
                fecha_nac = datetime.strptime(fecha_texto, "%d/%m/%Y").date()
                st.success(f"Fecha de nacimiento seleccionada: {fecha_nac}")
            except ValueError:
                st.error("Por favor, ingrese la fecha en formato DD/MM/YYYY")
                fecha_nac = None  # Si hay un error, asignar None a fecha_nac
            

            
            fecha_ing = st.date_input("Fecha de Ingreso")
            
            antecedentes = st.text_input("ANTECEDENTES", autocomplete=None).upper()
            diagnostico = st.text_input("DIAGNOSTICO", autocomplete=None).upper()
            medico = st.selectbox("MEDICO", df_Medico["NOMBRE_COMPLETO"], index=None, placeholder="Elija una opcion")
            fecha_hoy = st.date_input("FECHA REGISTRO", value=datetime.now().date(), format="DD/MM/YYYY", disabled=True)
            hora_registro = datetime.now().strftime("%H:%M:%S")
            
            # Botón para enviar el formulario
            submit = st.form_submit_button("Guardar")

            # Guardar los datos en el DataFrame si se ha enviado el formulario
            if submit:
                if not all([dni, nombre, apellido, edad, fecha_nac, fecha_ing, antecedentes, diagnostico, medico, fecha_hoy]):
                    st.warning("Todos los campos son obligatorios. Por favor, llene todos los campos.")
                else:
                    # Crear nueva fila con los datos ingresados
                    nueva_fila = {
                        'DNI': dni,
                        'NOMBRE': nombre,
                        'APELLIDO': apellido,
                        'EDAD': edad,
                        'CAMA': numero_cama,
                        'FECHA NAC': fecha_nac.strftime('%d/%m/%Y'),
                        'FECHA ING': fecha_ing.strftime('%d/%m/%Y'),
                        'DIAGNOSTICO' : diagnostico,
                        'ANTECEDENTES': antecedentes,
                        'MEDICO' : medico,
                        'FECHA REGISTRO' : fecha_hoy.strftime('%d/%m/%Y'),
                        'HORA REGISTRO' : hora_registro
                    }

                    # Convertir la lista de diccionarios en un DataFrame
                    df_nueva_fila = pd.DataFrame([nueva_fila])

                    # Concatenar el DataFrame original con el nuevo DataFrame
                    df_Paciente = pd.concat([df_Paciente, df_nueva_fila], ignore_index=True)

                    # Guardar el DataFrame actualizado
                    guardar_Paciente(df_Paciente)
                    st.success("Nuevo Paciente agregado.")

                    # Actualizar el estado de ocupación de la cama a 'OCUPADA'
                    df_Cama.loc[df_Cama['CAMA'] == numero_cama, 'OCUPACION'] = 'OCUPADA'
                    guardar_Cama(df_Cama)  # Guardar los cambios en el archivo de camas

                    # Mostrar los datos del nuevo paciente agregado
                    st.write(df_nueva_fila)

    else:
        st.error('La cama está Ocupada por un Paciente. Si ha sido desocupada, recuerde ingresar el cambio en el sistema.')
    
    st.write('*************')
    
    # Visualizar las camas 
    st.markdown("**<p style='font-size:20px;'>Visualizar el estado de las Camas:</p>**", unsafe_allow_html=True)
    
    st.dataframe(df_Cama)    



#####################################################################################################

if selected == 'Ingresar Atencion':
    # Título de la aplicación
    st.image('imagen/banner.jpg')
    st.title("Gestión de Atención 🩺:")
    st.write('*************')
    
    st.markdown("**<p style='font-size:20px;'>Para agregar una Nueva Atención de Cama, Seleccione una opción:</p>**", unsafe_allow_html=True)
    
    # Selector para el número de cama
    numero_cama = st.selectbox("**Número de Cama**", df_Cama['CAMA'], index=0, placeholder="Elija una opción")
    
    # Filtrar la fila correspondiente al número de cama seleccionado
    fila_seleccionada = df_Cama[df_Cama['CAMA'] == numero_cama]
    
    # Verificar el estado de ocupación de la cama seleccionada
    if fila_seleccionada['OCUPACION'].values[0] == 'OCUPADA':
        st.warning('La cama está Ocupada, Ingrese una Nueva Atención.')

        # Filtrar las filas correspondientes al número de cama seleccionado en df_Paciente
        pacientes_cama_seleccionada = df_Paciente[df_Paciente['CAMA'] == numero_cama]
        
        # Ordenar por la columna de fecha de ingreso en orden descendente y seleccionar la primera fila
        paciente_reciente = pacientes_cama_seleccionada.sort_values(by='FECHA ING', ascending=False).iloc[0]
        
        # Extraer el DNI del paciente reciente
        dni = paciente_reciente["DNI"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write('\n')
            st.info(f'**Cama:** {paciente_reciente["CAMA"]}')
            st.info(f'**Nombre:** {paciente_reciente["NOMBRE"]}')
            st.info(f'**Edad:** {paciente_reciente["EDAD"]}')
            st.info(f'**Fecha Ingreso:** {paciente_reciente["FECHA ING"]}')
            st.info(f'**Fecha Registro:** {paciente_reciente["FECHA REGISTRO"]}')
            
        with col2:
            st.write('\n')
            st.info(f'**DNI:** {paciente_reciente["DNI"]}')
            st.info(f'**Apellido:** {paciente_reciente["APELLIDO"]}')
            fecha_nac_formateada = pd.to_datetime(paciente_reciente["FECHA NAC"]).strftime('%d/%m/%Y')
            st.info(f'**Fecha Nacimiento:** {fecha_nac_formateada}')
            st.info(f'**Medico:** {paciente_reciente["MEDICO"]}')
            st.info(f'**Hora Registro:** {paciente_reciente["HORA REGISTRO"]}')
            
        st.info(f'**Antecedentes:** {paciente_reciente["ANTECEDENTES"]}')
        
        # Formulario para ingresar datos de atención
        with st.form(key="form_ingresar_atencion", clear_on_submit=True):
            st.warning('Funciones Fisiológicas.')
            alimentacion = st.text_input("Alimentación", autocomplete=None).upper()
            diuresis = st.text_input("Diuresis", autocomplete=None).upper()
            catarsis = st.text_input("Catarsis", autocomplete=None).upper()
            fecha_ff = st.date_input("Fecha Funciones Fisiológicas", value=datetime.today())
            st.write('*************')
            st.warning('Cultivos.')
            metodo = st.text_input("Método", autocomplete=None).upper()
            resultado = st.text_input("Resultado", autocomplete=None).upper()
            fecha_cultivo = st.date_input("Fecha Cultivo", value=datetime.today())
            st.write('*************')
            st.warning('Laboratorios.')
            laboratorio = st.text_input("Laboratorio").upper()
            fecha_laboratorio = st.date_input("Fecha Laboratorio", value=datetime.today())
            st.write('*************')
            st.warning('Examen Complementario.')
            ex_complementario = st.text_input("Examen Complementario").upper()
            fecha_excomplementario = st.date_input("Fecha Examen Complementario", value=datetime.today())
            st.write('*************')
            st.warning('Procedimientos.')
            procedimiento = st.text_input("Método Procedimiento").upper()
            fecha_procedimiento = st.date_input("Fecha Procedimiento", value=datetime.today())
            st.write('*************')
            st.warning('ATB.')
            atb = st.text_input("ATB").upper()
            fecha_atb = st.date_input("Fecha Antibiótico", value=datetime.today())
            fecha_finaliza = st.date_input("Fecha Finaliza", value=datetime.today())
            st.write('*************')
            st.warning('Medico.')
            medico = st.selectbox("Médico", df_Medico["NOMBRE"], index=None, placeholder="Elija una opción")
            fecha_hoy = st.date_input("Fecha Registro", value=datetime.now().date(), format="DD/MM/YYYY", disabled=False)
            hora_registro = datetime.now().strftime("%H:%M:%S")
            
            # Botón para enviar el formulario
            submit = st.form_submit_button("Guardar")

            # Guardar los datos en el DataFrame si se ha enviado el formulario
            if submit:
                if any([alimentacion, diuresis, catarsis, metodo, resultado, laboratorio, ex_complementario, procedimiento, atb]):
                    if alimentacion or diuresis or catarsis:
                        nueva_ff = {
                            'CAMA': numero_cama,
                            'DNI': dni,
                            'FECHA': fecha_ff.strftime('%d/%m/%Y'),
                            'ALIMENTACION': alimentacion,
                            'DIURESIS': diuresis,
                            'CATARSIS': catarsis                    
                        }
                        df_nueva_ff = pd.DataFrame([nueva_ff])
                        df_FuncionesFisiologicas = pd.concat([df_FuncionesFisiologicas, df_nueva_ff], ignore_index=True)
                        guardar_FuncionesFisiologicas(df_FuncionesFisiologicas)
                        st.success("Nuevo Funciones Fisiológicas agregado.")
                        st.write(df_nueva_ff)

                    if metodo or resultado:
                        nueva_cultivo = {
                            'CAMA': numero_cama,
                            'DNI': dni,
                            'FECHA': fecha_cultivo.strftime('%d/%m/%Y'),
                            'METODO': metodo,
                            'RESULTADO': resultado   
                        }
                        df_nueva_cultivo = pd.DataFrame([nueva_cultivo])
                        df_Cultivo = pd.concat([df_Cultivo, df_nueva_cultivo], ignore_index=True)
                        guardar_Cultivo(df_Cultivo)
                        st.success("Nuevo Cultivo agregado.")
                        st.write(df_nueva_cultivo)

                    if laboratorio:
                        nueva_laboratorio = {
                            'CAMA': numero_cama,
                            'DNI': dni,
                            'FECHA': fecha_laboratorio.strftime('%d/%m/%Y'),
                            'LABORATORIO': laboratorio   
                        }
                        df_nueva_laboratorio = pd.DataFrame([nueva_laboratorio])
                        df_Laboratorio = pd.concat([df_Laboratorio, df_nueva_laboratorio], ignore_index=True)
                        guardar_Laboratorio(df_Laboratorio)
                        st.success("Nuevo Laboratorio agregado.")
                        st.write(df_nueva_laboratorio)

                    if ex_complementario:
                        nueva_excomplementario = {
                            'CAMA': numero_cama,
                            'DNI': dni,
                            'FECHA': fecha_excomplementario.strftime('%d/%m/%Y'),
                            'EX. COMPLEMENTARIO': ex_complementario               
                        }
                        df_nueva_excomplementario = pd.DataFrame([nueva_excomplementario])
                        df_ExamenComplementario = pd.concat([df_ExamenComplementario, df_nueva_excomplementario], ignore_index=True)
                        guardar_ExamenComplementario(df_ExamenComplementario)
                        st.success("Nuevo Examen Complementario agregado.")
                        st.write(df_nueva_excomplementario)

                    if procedimiento:
                        nueva_procedimiento = {
                            'CAMA': numero_cama,
                            'DNI': dni,
                            'FECHA': fecha_procedimiento.strftime('%d/%m/%Y'),
                            'METODO': procedimiento                  
                        }
                        df_nueva_procedimiento = pd.DataFrame([nueva_procedimiento])
                        df_Procedimiento = pd.concat([df_Procedimiento, df_nueva_procedimiento], ignore_index=True)
                        guardar_Procedimiento(df_Procedimiento)
                        st.success("Nuevo Procedimiento agregado.")
                        st.write(df_nueva_procedimiento)

                    if atb:
                        nueva_atb = {
                            'CAMA': numero_cama,
                            'DNI': dni,
                            'FECHA': fecha_atb.strftime('%d/%m/%Y'),
                            'ATB': atb,
                            'FINALIZA': fecha_finaliza.strftime('%d/%m/%Y')
                        }
                        df_nueva_atb = pd.DataFrame([nueva_atb])
                        df_ATB = pd.concat([df_ATB, df_nueva_atb], ignore_index=True)
                        guardar_ATB(df_ATB)
                        st.success("Nuevo ATB agregado.")
                        st.write(df_nueva_atb)
                else:
                    st.warning("Debe ingresar al menos un dato en alguna de las secciones.")
            
    else:
        st.error('La cama está Libre. Si ha sido ocupada, recuerde ingresar el cambio en el sistema.')   
    

#####################################################################################################

if selected == 'Medicos':
    # Título de la aplicación
    st.image('imagen/banner.jpg')
    st.title("Gestión de Medicos")
    # st.image('abogados.jpg')
    st.write('\n')
    st.subheader('Selecciona una Opcion', help=None)


    opcion = st.radio(
        "Selecciona una Opcion",
        ["Medicos", "Crear Medicos"],
        key="Tabla Medicos", horizontal=True, label_visibility="collapsed"
    )

    if opcion == "Medicos":
        st.subheader('', divider='gray')
        st.title("Medicos")
        st.write("Aquí puedes ver la lista de Medicos.")
        df_Medico[['APELLIDO', 'NOMBRE', 'DNI', 'TELEFONO', 'EMAIL']]
        


        # Función para descargar el DataFrame filtrado como archivo XLSX
        def download_excel(df, file_name='data.xlsx'):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
            excel_data = output.getvalue()
            return excel_data

        # Convertir el DataFrame filtrado a XLSX
        excel_data = download_excel(df_Medico)

        # Botón de descarga para el DataFrame filtrado
        st.download_button(
            label="DESCARGAR LISTA",
            data=excel_data,
            file_name="Medicos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        st.write("***************")



    elif opcion == "Crear Medicos":
        st.subheader('', divider='gray')
        st.title("Crear Medicos")
        st.write("Complete el formulario para agregar un nuevo Medico.")

        with st.form(key="form_crear_Medicos", clear_on_submit=True):
            nombre_completo = st.text_input("NOMBRE", autocomplete=None).upper()
            apellido = st.text_input("APELLIDO").upper()
            documento = st.number_input("DNI", min_value=None, value=None, step=1, format="%d", placeholder="Escribe un número")
            telefono = st.text_input("TELEFONO").upper()
            email = st.text_input("EMAIL", placeholder="ejemplo@xmail.com")

            # Se crea el botón para guardar
            submit_button = st.form_submit_button("Guardar")

            if submit_button:
                if not all([nombre_completo, apellido, telefono, email]):
                    st.warning("Todos los campos son obligatorios. Por favor, llene todos los campos.")
                elif documento in df_Medico["DNI"].values:
                    st.warning(f"El N° Expediente '{documento}' ya existe. Intente con otro número.")
                else:
                    nueva_fila = {
                        'DNI' : documento,
                        'NOMBRE': nombre_completo,
                        'APELLIDO': apellido,
                        'TELEFONO': telefono,
                        'EMAIL': email
                    }
                    # Convertir el diccionario en una lista de diccionarios
                    lista_nuevas_filas = [nueva_fila]

                    # Convertir la lista de diccionarios en un DataFrame
                    df_nuevas_filas = pd.DataFrame(lista_nuevas_filas)

                    # Concatenar el DataFrame original con el nuevo DataFrame
                    df_Medico = pd.concat([df_Medico, df_nuevas_filas], ignore_index=True)

                    # Guardar el DataFrame actualizado
                    guardar_Medico(df_Medico)
                    st.success(f"Se agregó un nuevo Medico")
                    st.write(df_nuevas_filas)
    
#########################################################################################################
