"""
Código del script original:
- https://github.com/pdichone/vincibits-study-buddy-knwoledge-retrieval/blob/main/app.py
"""

# Importando los paquetes necesarios

import logging
import time

import openai
from dotenv import load_dotenv

# 1. ---Conectamos con la API---

# Cargamos el entorno para la API
load_dotenv()

client = openai.OpenAI()

# Escogemos el modelo
default_model = "gpt-4" 

# 2. ---Archivo que usará el asistente---

# Ruta del archivo
filepath = 'Muestras-Sueños/2024-02-28.md'


# Objeto que corresponde al archivo
file_object = client.files.create(file=open(filepath, "rb"), purpose="assistants")

# 3. ---Creamos el asistente y el hilo---

# DESCOMENTAR SÓLO PARA LA PRIMERA EJECUCIÓN
# # Creando al asistente
# assistant = client.beta.assistants.create(
#     name="Dream Interpreter",
#     instructions="""
#     Eres un experto en el análisis e interpretación de sueños, con un profundo
#     conocimiento de los trabajos académicos sobre este tema, incluyendo los estudios
#     estadísticos de William Domhoff. Tu tarea es extraer insights clave de los sueños
#     de los usuarios, analizándolos para ofrecer reflexiones profundas y respuestas a
#     preguntas, tanto de naturaleza estadística como introspectiva o filosófica. 
    
#     - Analizarás los sueños para conversar sobre sus aspectos más relevantes,
#     utilizando tu comprensión estadística y psicológica.
#     - Responderás a preguntas sobre los sueños, incluyendo análisis de personajes 
#     y objetos presentes.
#     - Formularás preguntas al usuario para profundizar en la comprensión de sus sueños 
#     y sugerirás acciones basadas en tus análisis.
#     - Mantendrás la confidencialidad de los datos para asegurar un ambiente seguro para
#     el usuario.
#     - Aprenderás de cada interacción para mejorar continuamente tu análisis y las 
#     recomendaciones ofrecidas.
    
#     Tu objetivo es facilitar una comprensión profunda de los sueños del usuario, promoviendo
#     la exploración introspectiva y ofreciendo nuevos caminos de comprensión.""",
#     tools=[{"type":"retrieval"}],
#     model=default_model,
#     file_ids=[file_object.id] # Podemos pasar más de un archivo, por eso lo tenemos en formato lista
# )

# # Obtenemos el ID del asistente
# assis_id = assistant.id
# print(assis_id)

# Scripts codificados a mano una vez los hemos obtenido por la terminal
assis_id = "asst_GXPWM4pbbW3FcePgAxznncAV" # COMENTAR EN LA PRIMERA EJECUCIÓN
thread_id = "thread_7EujENHxi22T5Tuhd754i1og" # COMENTAR EN LA PRIMERA EJECUCIÓN

# DESCOMENTAR PARA LA PRIMERA EJECUCIÓN PARA EVITAR CREAR VARIOS THREADS
## Creamos el thread
# thread = client.beta.threads.create()

# # Obtenemos el id del thread
# thread_id = thread.id
# print(thread_id)

# 4. ---Creamos el mensaje y ejecutamos al asistente---

# Establecemos el mensaje
message = "Enumera los distintos elementos de mi sueño usando el enfoque de William Domhoff"

message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=message)

run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assis_id,
    instructions="Por favor, trata al usuario de Onironauta"
)

# 5. ---Esperamos a que se complete la ejecución---

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """
    Espera hasta que se complete la ejecución e imprime el tiempo transcurrido.

    Args:
    -----
    - client: El objeto cliente de OpenAI
    - thread_id: El ID del thread
    - run_id: El ID de la ejecución
    - sleep_interval: Tiempo en segundos a esperar entre comprobaciones.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                ) # Mostrando el tiempo transcurrido
                print(f"Ejecución completada en {formatted_elapsed_time}")
                logging.info(f"Ejecución completada en {formatted_elapsed_time}")
                # Obtenemos los mensajes una vez se ha completado la ejecución
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Respuesta del asistente: {response}")
                break
        except Exception as e:
            logging.error(f"Error ocurrido durante la ejecución: {e}")
            break
        logging.info("Esperando que la ejecución se complete...")
        time.sleep(sleep_interval)
        
        
# Lo ejecutamos
wait_for_run_completion(client=client,
                        thread_id=thread_id,
                        run_id=run.id)

# 6. ---Comprobando los registros de los pasos de la ejecución---

run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
print(f"Run Steps --> {run_steps.data[0]}")