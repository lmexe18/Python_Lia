# Asistente de Voz Lía

## Descripción del Proyecto

**Lía** es un asistente de voz inteligente diseñado para proporcionar información en tiempo real sobre la temperatura y la humedad de una sala. Utiliza un archivo JSON para obtener y procesar los datos, y es capaz de responder mediante voz a diversas solicitudes, además de enviar mensajes con la información por WhatsApp usando `pywhatkit`.

---

## Funcionalidades Principales

1. **Interacción por Voz**:
   - Lía se presenta al iniciar la aplicación y queda en espera de comandos de voz.
   - Escucha y reconoce comandos como:
     - "¿Cuál es la temperatura actual?"
     - "¿Cuáles son los grados celsius actuales?"
     - "¿Cuáles son los grados fahrenheit actuales?"
     - "¿Cuál es la humedad actual?"
     - "¿Cuál es la temperatura media?"
     - "¿Cuáles son los grados celsius de media?"
     - "¿Cuáles son los grados fahrenheit de media?"
     - "¿Cuál es la humedad de media?"
     - "Detener" o "Salir"
   - Responde con la información correspondiente de manera clara y precisa.

2. **Procesamiento de Datos**:
   - **Datos Actuales**: Lía accede a un archivo JSON para obtener la temperatura y humedad del día.
   - **Medias Semanales**: Calcula los promedios de la temperatura y la humedad basándose en los registros de los últimos 7 días.

3. **Envío de Información por WhatsApp**:
   - Lía puede enviar automáticamente la información solicitada a un número de WhatsApp predefinido.

4. **Respuestas por Voz**:
   - Utiliza la librería `pyttsx3` para convertir texto en voz, ofreciendo una experiencia interactiva y fluida.

---

## Instalación y Configuración

### Requisitos Previos
- Tener Python 3.x instalado en tu sistema.
- Librerías de Python necesarias:
  - `pyttsx3`
  - `speech_recognition`
  - `pywhatkit`
  - `json`
  - `datetime`

### Pasos de Instalación
1. **Descarga el Proyecto**:
   - Descarga y descomprime el archivo de la release en tu directorio de trabajo.

2. **Configuración del Entorno Virtual**:
   - Abre una terminal o cmd y ejecuta los siguientes comandos:
     ```bash
     cd [ruta_del_directorio]
     python -m venv rec_voz_venv
     ```
   - **Activar el entorno virtual**:
     - En **Windows**: 
       ```bash
       .\rec_voz_venv\Scripts\activate
       ```
     - En **Linux**:
       ```bash
       source rec_voz_venv/bin/activate
       ```
   - **Instalar las dependencias**:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configuración de Archivos JSON**:
   - Crea un archivo `enviarDatos.json` con la estructura adecuada, basada en `enviarDatos-schema.json`.

---

## Ejecución del Asistente

1. **Iniciar el Asistente**:
   - Con el entorno virtual activado, ejecuta:
     ```bash
     python main.py
     ```
   - Lía se presentará y quedará a la espera de comandos de voz.

2. **Uso de Comandos de Voz**:
   - Realiza tu solicitud, y Lía responderá con la información correspondiente.
   - También enviará la información por WhatsApp si está configurado.

---

## Estructura del Proyecto

- **`out_shellyht.json`**: Contiene los registros de temperatura y humedad.
- **`strings.json`**: Define los mensajes y comandos reconocidos por el asistente.
- **`enviarDatos.json`**: Configura el número de teléfono para el envío de mensajes por WhatsApp.

---

## Tecnologías Utilizadas

- **Python 3.x**
- **Librerías**:
  - `pyttsx3`: Conversión de texto a voz.
  - `speech_recognition`: Reconocimiento de voz para captar los comandos del usuario.
  - `pywhatkit`: Envío de mensajes por WhatsApp.
  - `json` y `datetime`: Manipulación de datos y fechas.


---

**Lía**: tu asistente personal para monitorear la temperatura y humedad de manera fácil y cómoda, usando solo tu voz.
