# Asistente Onírico con API de OpenAI y Streamlit

Creando un asistente que lea las entradas de nuestro diario onírico y charle con nosotros sobre nuestros sueños.

El objetivo principal es probar como aplicar un asistente a esta tarea, usando unos pocos sueños de muestra, generados con IA, para evaluar la posibilidad a futuro de añadir una colección de sueños extensa en la que nuestro asistente pueda buscar nuestras señales oníricas y otros elementos, con la opción de incluir otras funcionalidades especializadas para profundizar en nuestro mundo onírico.

## Estructura del proyecto

- **Referencia** - La estructura principal de este proyecto está inspirada en la presentada en este repositorio: [Repo](https://github.com/pdichone/vincibits-study-buddy-knwoledge-retrieval). Aquí se crea un asistente que funciona como compañero de estudio. Recibe documentos a los que es capaz de acceder, leerlos y sacar ideas clave para responder a las preguntas del usuario sobre los temas tratados en ellos.

- **Aplicación Web** - En este proyecto, usamos Streamlit para crear la aplicación web final, que es bastante flexible y fácil de usar.

- **Entornos y marco de trabajo** - Para este proyecto, estaré usando un entorno de Conda, junto con VSCode.

- **Los scripts** - El proyecto consta de dos scripts principales:

- `app.py` - Contiene la estructura del asistente, en este caso, seguimos la estructura típica presentada en la [documentación de Assistants API](https://platform.openai.com/docs/assistants/overview?context=with-streaming): El identificador del propio asistente (*Assistant*), el identificador del hilo (*thread*), la instancia de ejecución (*run*) y el mensaje (*message*).
- `main.py` - Contiene las configuraciones para la App de *Streamlit*.

## Pasos para replicar este proyecto

### 1. Configuraciones y requisitos

1. **Repositorio** - Clonar el repositorio en nuestra máquina local.
2. **API OpenAI** - Generar una clave API de OpenAI, e incluirla en el fichero de variables de entorno o confugurarla para el proyecto actual como se indica en la documentación: ([Docs OpenAI](https://platform.openai.com/docs/quickstart?context=python)).
3. **Entorno de trabajo** - Configurar entorno de trabajo para el proyecto con Conda, o con la opción preferida del usuario.
4. **Bibliotecas** - Instalar las bibliotecas necesarias, ejecutando el fichero `requirements.txt` a través de la terminal:

```bash
pip instal -r requirements.txt
```

**Nota:** Asegurarse de que el entorno en el que queremos trabajar es el que está activo en el momento de ejecutar el fragmento anterior.

### 2. Creando la estructura del asistente (![app.py](app.py))

Esta es la estructura de nuestro asistente. Este script, lo queremos para interactuar con la API de asistentes de OpenAI, creando la estructura de asistentes básica.

Lo que hace el Script:

1. Inicializa la conexión con la API de OpenAI.
2. Crea un archivo en la API de OpenAI para ser utilizado por un asistente.
3. Crea un asistente y un hilo de chat (thread). El código para crear estos dos elementos luego lo comentamos, para no estar duplicándolo en cada ejecución. Luego incluimos a mano los IDs, tanto del hilo como del asistente manualmente en el código.
4. Envía un mensaje y ejecuta el asistente en el hilo de chat.
5. Ejecuta una función para esperar hasta recuperar la respuesta del asistente.
6. Por último, recupera los detalles de la ejecución del hilo.

#### Sobre las instrucciones del asistente

Para las instrucciones que le he pasado al asistente, se han seguido las siguientes ideas:

- Estructutar prompt con claridad.
- Especificar roles y expectativas de manera concisa.
- Dividir las instrucciones en segmentos diferenciables.

### 2. Creando la estructura de la APP de Streamlit (![main.py](main.py))

Este fichero corresponde a la estructura de la aplicación final de Streamlit, la cual proporciona una interfaz de usuario para:

- Subir archivos a OpenAI.
- Iniciar y gestionar un chat interactivo con un asistente de OpenAI.
- Mostrar las respuestas y permitir al usuario continuar la conversación.
- Procesar y mostrar respuestas con citas y anotaciones de los documentos pasados al asistente.

# Bibliografía y profundizar

- [Repositorio](https://github.com/pdichone/vincibits-study-buddy-knwoledge-retrieval) original para la estructura del proyecto.
- Tutorial en YouTube: [Curso de OpenAI Assistant API de freecodecamp.org](https://www.youtube.com/watch?v=qHPonmSX4Ms&ab_channel=freeCodeCamp.org)
- Documentación de Streamlit: [Docs](https://docs.streamlit.io/)
- [Documentación API OpenAI](https://platform.openai.com/docs/api-reference)
- Para más información sobre las sesiones de Streamlit: [Docs Session State Streamlit](https://docs.streamlit.io/library/api-reference/session-state)
