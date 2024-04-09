"""
Código del script original:
https://github.com/pdichone/vincibits-study-buddy-knwoledge-retrieval/blob/main/main.py
"""

# Importando los paquetes necesarios
import time

import openai
import streamlit as st
from dotenv import load_dotenv

# 1. ---Conectamos con la API e incluimos los IDs---

# Cargamos el entorno para la API
load_dotenv()

client = openai.OpenAI()

# Escogemos el modelo
default_model = "gpt-4-turbo-preview" 

# IDs del asistente y del thread
# IDs incluidos a mano una vez hemos ejecutado por primera vez el script (app.py)
assis_id = "asst_UnPj5l8tNbyFxaQ4gvLjJ7rw"
thread_id = "thread_uGmHPd5c1R8CXAft2af59Jfv"


# 2. ---Comprobamos si los valores se encuentran en la sesión---

# Primero comprobamos el/los archivo(s)
if "file_id_list" not in st.session_state: # Podemos subir más de un archivo
    st.session_state.file_id_list = []

# Comprobamos el valor booleano "start_chat"
if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

# Comprobamos el id del thread
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
    
# 2. ---Estableciendo las configuraciones del front end---

# Título e icono
st.set_page_config(
    page_title="Dreams Analyzer - Explore your Dreams", # Título de nuestra página
    page_icon=":waxing_crescent_moon:") # Shortcodes iconos: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

# 3. ---Funcionalidades y botones---

# Función para subir archivos a OpenAI
def upload_to_openai(filepath):
    """
    Sube los archivos de la ruta especificada a OpenAI, para que el asistente
    los use posteriormente.
    
    args:
    -----
    filepath: Ruta del archivo a subir
    
    return:
    -------
    ID del archivo subido
    """
    with open(filepath, "rb") as file:
        response = client.files.create(file=file.read(), purpose="assistants")
    return response.id

# Barra lateral para subir archivos
file_uploaded = st.sidebar.file_uploader(
    "Se sube un archivo que será transformado en embeddings.", key="file_upload"
)

# Botón para subir el archivo al pulsarlo
if st.sidebar.button("Subir Archivo"):
    if file_uploaded:
        with open(f"{file_uploaded.name}", "wb") as f:
            f.write(file_uploaded.getbuffer())
        another_file_id = upload_to_openai(f"{file_uploaded.name}")
        st.session_state.file_id_list.append(another_file_id)
        st.sidebar.write(f"File ID:: {another_file_id}")
        
        
# Mostramos los ids de los archivos
if st.session_state.file_id_list:
    st.sidebar.write("IDs de los archivos:")
    for file_id in st.session_state.file_id_list:
        st.sidebar.write(file_id)
        try:
            # Intentamos asociar cada id de archivo con el asistente
            assistant_file = client.beta.assistants.files.create(
                assistant_id=assis_id, file_id=file_id
            )
        except Exception as e:
            print(f"Error al asociar el archivo con ID {file_id} al asistente: {e}")


        
# Botón para inicializar la sesión de chat
if st.sidebar.button("Empezar a chatear..."):
    if st.session_state.file_id_list:
        st.session_state.start_chat = True

        # Creamos nuevo thread para cada sesión de chat
        chat_thread = client.beta.threads.create()
        st.session_state.thread_id = chat_thread.id
        st.write("Thread ID:", chat_thread.id)
    else:
        st.sidebar.warning(
            "No se encontraron archivos, por favor, subir uno al menos para empezar"
        )
        
        
# Función para procesar mensajes con citas
def process_message_with_citations(message):
    """
    Extraer contenido y anotaciones del mensaje y formatear las citas
    como notas de pie de página.
    
    args
    ----
    message: El mensaje completo sin formatear
    
    return:
    -------
    full_response: El mensaje formateado con citas y anotaciones
    """
    message_content = message.content[0].text
    annotations = (
        message_content.annotations if hasattr(message_content, "annotations") else []
    )
    citations = []

    # Iteramos sobre las anotaciones y añadimos notas
    for index, annotation in enumerate(annotations):
        # Reemplazamos el texto con una nota
        message_content.value = message_content.value.replace(
            annotation.text, f" [{index + 1}]"
        )

        # Recopilamos citas basadas en los atributos de las anotaciones
        if file_citation := getattr(annotation, "file_citation", None):
            # Recuperamos los detalles de los archivos citados
            cited_file = {
                "filename": "Dreams_Statistical_Analysis.pdf"
            }  # TODO: Esto debe reemplazarse con el recuperador de archivos cuando se pueda
            citations.append(
                f'[{index + 1}] {file_citation.quote} from {cited_file["filename"]}'
            )
        elif file_path := getattr(annotation, "file_path", None):
            # Marcador de posicion para la citación del documento
            cited_file = {
                "filename": "Dreams_Statistical_Analysis.pdf"
            }  # TODO: Esto debe reemplazarse con el recuperador de archivos cuando se pueda
            citations.append(
                f'[{index + 1}] Click [here](#) to download {cited_file["filename"]}'
            )  # El enlace de descarga debe reemplazarse con la ruta de descarga

    # Añadimos la nota al final del contenido del mentaje
    full_response = message_content.value + "\n\n" + "\n".join(citations)
    return full_response


# La interfaz principal
st.title("Dreams Analyzer ")
st.write("Aprende en profundidad sobre tus sueños")


# Comprobamos la sesión
if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4"
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostramos los mensajes existentes si los hay
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input del chat para el usuario
    if prompt := st.chat_input("Empezar a escribir..."):
        # Añadimos el mensaje del usuario al estado y lo mostramos en la pantalla
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Añadimos el mensaje del usuario al thread existente
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id, role="user", content=prompt
        )

        # Creamos una ejecución con instrucciones adicionales
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assis_id,
            instructions="""Por favor, responde con el conocimiento adquirido a través de los
            archivos proporcionados. Cuando se añada información adicional, asegurate de distinguirla
            con negrita o subrayando el texto.
            """,
        )

        # Se ve un spinner mientras el asistente piensa
        with st.spinner("Espera... Generando respuesta..."):
            while run.status != "completed":
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id, run_id=run.id
                )
            # Recuperamos los mensajes añadidos por el asistente
            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            )
            # Procesamos y mostramos por pantalla los mensajes
            assistant_messages_for_run = [
                message
                for message in messages
                if message.run_id == run.id and message.role == "assistant"
            ]

            for message in assistant_messages_for_run:
                full_response = process_message_with_citations(message=message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
                with st.chat_message("assistant"):
                    st.markdown(full_response, unsafe_allow_html=True)

    else:
        # Instrucciones para el usuario para comenzar la conversación
        st.write(
            "Por favor, sube por lo menos un archivo para empezar, clickando en el botón 'Start Chat'"
        )
        
# Ejecutar `streamlit run main.py` en la consola para iniciar el script
