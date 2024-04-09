# Asistente Onírico con API de OpenAI y Streamlit

Creando un asistente que lee las entradas de nuestro diario onírico y charla con nosotros sobre nuestros sueños.

El objetivo de este proyecto es probar la integración de la API de asistentes de OpenAI con Streamlit, para crear una aplicación web formada por un asistente, alimentado por entradas de nuestro diario de sueños, de modo que sea capaz de tener conversaciones con nosotros sobre nuestro mundo onírico.

Para esto, usamos un par de sueños de muestra generados con ChatGPT4. Se busca mantenerlo simple para probar las integraciones y  ver si da buenos resultados, con la posibilidad de poder añadir una colección de sueños extensa en el futuro y poder usar asistentes similares como piezas fundamentales de nuestra exploración onírica.

## Estructura del proyecto

**Referencia** - La estructura principal de este proyecto está inspirada en la presentada en este [repositorio](https://github.com/pdichone/vincibits-study-buddy-knwoledge-retrieval). Aquí, se crea un asistente que funciona como compañero de estudio. Este recibe documentos a los que es capaz de acceder y sacar ideas clave para responder a las preguntas del usuario sobre los temas tratados en ellos.

Las partes del proyecto:

- **Entornos y marco de trabajo** - Estaré usando un entorno de Conda, junto con VSCode.
- **Los scripts** - El proyecto consta de dos scripts principales:
  - [app.py](app.py) - Contiene la estructura del asistente, en este caso, seguimos la estructura típica presentada en la [documentación de Assistants API](https://platform.openai.com/docs/assistants/overview?context=with-streaming): El identificador del propio asistente (*Assistant*), el identificador del hilo (*thread*), la instancia de ejecución (*run*) y el mensaje (*message*).
  - [main.py](main.py) - Contiene las configuraciones para la App de *Streamlit*.
- **Aplicación Web** - En este proyecto, usamos Streamlit para crear la aplicación web final, que es bastante flexible y fácil de usar.

## Pasos para replicar este proyecto

### 1. Configuraciones y requisitos
---

1. **Repositorio** - Clonar el repositorio en nuestra máquina local.

```bash
git clone git@github.com:ManuelEspejo/Asitente-Onirico-OpenAI.git
```

2. **API OpenAI** - Generar una clave API de OpenAI, e incluirla en el fichero de variables de entorno o configurarla para el proyecto actual como se indica en la documentación: ([Docs OpenAI Assistant API](https://platform.openai.com/docs/quickstart?context=python)).
   1. Requiere de registro en OpenAI.
   2. Requiere de crédito para la API.
3. **Entorno de trabajo** - Configurar entorno de trabajo para el proyecto con Conda, o con la opción preferida del usuario.
4. **Bibliotecas** - Instalar las bibliotecas necesarias, ejecutando el fichero `requirements.txt` a través de la terminal:

```bash
pip install -r requirements.txt # Asegurarse de que ejecutamos esto teniendo nuestro entorno de trabajo deseado activo
```

### 2. Creando la estructura del asistente ([app.py](app.py))
---
#### Lo que hace el script
---

Esta es la estructura de nuestro asistente. Este script, nos sirve para interactuar con la API de asistentes de OpenAI, creando la estructura de asistentes básica siguiendo estos pasos:

1. Inicializa la conexión con la API de OpenAI.
2. Crea un archivo en la API de OpenAI para ser utilizado por un asistente.
3. Crea un asistente y un hilo de chat (thread). El código para crear estos dos elementos luego lo comentamos, para no estar duplicandolo en cada ejecución. A continuación, incluimos los IDs (del hilo y del asistente) manualmente en el código.
4. Envía un mensaje y ejecuta el asistente en el hilo de chat.
5. Ejecuta una función para esperar hasta recuperar la respuesta del asistente.
6. Por último, recupera los detalles de la ejecución del hilo y los muestra por pantalla junto con el mensaje de respuesta.

#### Sobre las instrucciones del asistente
---

Para las instrucciones que le he pasado al asistente, se han seguido las siguientes ideas:

- Estructutar prompt con claridad.
- Especificar roles y expectativas de manera concisa.
- Dividir las instrucciones en segmentos diferenciables.

Las instrucciones:

```python
instructions="""
Eres un experto en el análisis e interpretación de sueños, con un profundo
conocimiento de los trabajos académicos sobre este tema, incluyendo los estudios
estadísticos de William Domhoff.

Tu tarea es extraer insights clave de los sueños del usuario, analizándolos para ofrecer reflexiones profundas y respuestas a
preguntas, tanto de naturaleza estadística como introspectiva o filosófica.

- Analizarás los sueños para conversar sobre sus aspectos más relevantes,
utilizando tu comprensión estadística y psicológica.
- Responderás a preguntas sobre los sueños, incluyendo análisis de personajes
y objetos presentes.
- Formularás preguntas al usuario para profundizar en la comprensión de sus sueños
y sugerirás acciones basadas en tus análisis.
- Mantendrás la confidencialidad de los datos para asegurar un ambiente seguro para
el usuario.
- Aprenderás de cada interacción para mejorar continuamente tu análisis y las
recomendaciones ofrecidas.


**Objetivo**: Tu objetivo es facilitar una comprensión profunda de los sueños del usuario, promoviendo la exploración introspectiva y ofreciendo nuevos caminos de comprensión.
"""
```

#### Pasos para ejecutarlo

1. Descomentar los siquientes fragmentos de la parte 3 de `app.py`:

```python
assistant = client.beta.assistants.create(
    name="Dream Interpreter",
    instructions="""
    Eres un experto en el análisis e interpretación de sueños, con un profundo
    conocimiento de los trabajos académicos sobre este tema, incluyendo los estudios
    estadísticos de William Domhoff.
    Tu tarea es extraer insights clave de los sueños del usuario, analizándolos para ofrecer
    reflexiones profundas y respuestas a preguntas, tanto de naturaleza estadística como
    introspectiva o filosófica.
    - Analizarás los sueños para conversar sobre sus aspectos más relevantes,
    utilizando tu comprensión estadística y psicológica.
    - Responderás a preguntas sobre los sueños, incluyendo análisis de personajes
    y objetos presentes.
    - Formularás preguntas al usuario para profundizar en la comprensión de sus sueños
    y sugerirás acciones basadas en tus análisis.
    - Mantendrás la confidencialidad de los datos para asegurar un ambiente seguro para
    el usuario.
    - Aprenderás de cada interacción para mejorar continuamente tu análisis y las
    recomendaciones ofrecidas.
    **Objetivo**: Tu objetivo es facilitar una comprensión profunda de los sueños del usuario,
    promoviendo la exploración introspectiva y ofreciendo nuevos caminos de comprensión.
    """,
    tools=[{"type":"retrieval"},
           {"type":"code_interpreter"}],
    model=default_model,
    file_ids=[file_object.id]
)
 
 assis_id = assistant.id
 print(assis_id)
 
```

```python
 thread = client.beta.threads.create()  

 thread_id = thread.id
 print(thread_id)
 
```

2. Comentamos los IDs del asistente y el hilo antiguos:

```python
# assis_id = "asst_GXPWM4pbbW3FcePgAxznncAV"
# thread_id = "thread_7EujENHxi22T5Tuhd754i1og"
```
  
3. Ejecutamos el script para obtener los IDs del nuevo asistente.

4. Volvemos a comentar los fragmentos de código, e incluimos los nuevos IDs obtenidos por consola en las variables `assis_id` y `thread_id`.

### 3. Creando la estructura de la APP de Streamlit ([main.py](main.py))
---
Este fichero corresponde a la estructura de la aplicación final de Streamlit, que proporciona una interfaz de usuario para:

- Subir archivos a OpenAI.

- Iniciar y gestionar un chat interactivo con un asistente de OpenAI.

- Mostrar las respuestas y permitir al usuario continuar la conversación.

- Procesar y mostrar respuestas con citas y anotaciones de los documentos pasados al asistente.

#### Pasos para ejecutarlo
---
1. Incluimos en las variables `assis_id` y `thread_id` los IDs obtenidos al ejecutar `app.py`

```bash
assis_id = "asst_GXPWM4pbbW3FcePgAxznncAV" # Copiar ID de app.py
thread_id = "thread_7EujENHxi22T5Tuhd754i1og" # Copiar ID de app.py
```

2. Ejecutamos en la consola la app de Streamlit:

```bash
streamlit run /<RUTA-LOCAL>/Asitente-Onirico-OpenAI/main.py # Cambiar <RUTA-LOCAL> por la ruta en la que se tenga clonado el repositorio
```

### 4. Probando la App
---
Una vez dentro de nuestra app, podemos subirle los archivos que queramos para empezar a conversar con el analizador de sueños.
![Imagen](/assets/images/subir-archivos.png)

# Bibliografía y profundizar

- [Repositorio](https://github.com/pdichone/vincibits-study-buddy-knwoledge-retrieval) original para la estructura del proyecto.
  - Tutorial en YouTube: [Curso de OpenAI Assistant API de freecodecamp.org](https://www.youtube.com/watch?v=qHPonmSX4Ms&ab_channel=freeCodeCamp.org)

- [Documentación de Streamlit](https://docs.streamlit.io/)

- [Documentación API OpenAI](https://platform.openai.com/docs/api-reference)

- Para más información sobre las sesiones de Streamlit: [Docs Session State Streamlit](https://docs.streamlit.io/library/api-reference/session-state)