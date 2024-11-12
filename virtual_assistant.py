import datetime
import pyttsx3
import speech_recognition as sr
import json

archivoDatos = './out_shellyht.json'

def audioATexto():
    
    r = sr.Recognizer()
    
    with sr.Microphone() as origin:
        r.pause_threshold = 0.8
        
        print('Puedes comenzar a hablar')
        
        audio = r.listen(origin)
        
        try:
            text = r.recognize_google(audio, language='es-es')
            return text
        except sr.UnknownValueError:
            print('Ups, no te entendí')
            return 'Esperando'
        except sr.RequestError:
            print('Ups, sin servicio')
            return 'Esperando'
        except:
            print('Ups, algo ha salido mal')
            return 'Esperando'
        
def hablar(msg):
    newVoiceRate = 180
    engine = pyttsx3.init()
    engine.setProperty('voice', 'com.apple.eloquence.es-ES.Monica')
    engine.setProperty('rate', newVoiceRate)
    engine.say(msg)
    engine.runAndWait()
    
def obtenerVoces():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for i, voice in enumerate(voices):
        print(f"Voz {i}")
        print(f"Id {voice.id}")
        print(f"Nombre {voice.name}")
        print(f"Idioma {voice.languages}")
        print(f"Género {voice.gender}")
        print(f"Género {voice.age}")
        print(f"---------------------------")
        
def decirDia():
    day = datetime.date.today()
    weekday = {
        0: 'Lunes',
        1: 'Martes',
        2: 'Miércoles',
        3: 'Jueves',
        4: 'Viernes',
        5: 'Sábado',
        6: 'Domingo'
    }
    hablar(f'Hoy es {weekday[day.weekday()]}')
    
def decirHora():
    hora = datetime.datetime.now()
    hablar(f'En este momento son las {hora.hour} horas y {hora.minute} minutos')
    
def saludo():
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches.'
    elif 6 <= hora.hour < 13:
        momento = 'Buenos días.'
    else:
        momento = 'Buenas tardes.'
    hablar(f'{momento} Soy Lía, tu asistente personal. Por favor, dime en qué puedo ayudarte.')
    
def requests():
    saludo()
    stop = False
    while not stop:
        request = audioATexto().lower()
    
        if 'qué temperatura hace' in request:
            decirDatosHoy('temperaturaCompleta')
        elif 'cuántos grados celsius hacen' in request:
           decirDatosHoy('celsius')
        elif 'cuántos grados fahrenheit hacen' in request:
            decirDatosHoy('fahrenheit')
        elif 'qué humedad hace' in request:
            decirDatosHoy('humedad')
        
        
def decirDatosHoy(datos):
    try:
        with open(archivoDatos, 'r') as file:
            lineas = file.readlines()

        fechaActual = datetime.datetime.now().strftime('%Y-%m-%d')
        temperaturaCelsius = None
        temperaturaFahrenheit = None
        humedad = None

        for linea in lineas:
            fecha = linea[:10]
            if fechaActual == fecha:
                try:
                    partes = linea.split(' ', 2)
                    if len(partes) >= 3:
                        jsonStrings = partes[2].split('} {')
                        json1 = json.loads(jsonStrings[0] + '}')
                        json2 = json.loads('{' + jsonStrings[1])

                        if 'tC' in json1:
                            temperaturaCelsius = json1['tC']
                            temperaturaFahrenheit = json1['tF']
                        elif 'payload' in json2 and 'tC' in json2['payload'] and 'tF':
                            temperaturaCelsius = json2['payload']['tC']
                            temperaturaFahrenheit = json2['payload']['tF']
                        elif 'rh' in json1:
                            humedad = json1['rh']
                        elif 'payload' in json2 and 'rh' in json2['payload']:
                            humedad = json2['payload']['rh']
                            
                except json.JSONDecodeError:
                    continue

        if temperaturaCelsius is not None and datos == 'celsius':
            hablar(f'La temperatura actual es de {temperaturaCelsius} grados Celsius.')
        elif temperaturaFahrenheit is not None and datos == 'fahrenheit':
            hablar(f'La temperatura actual es de {temperaturaFahrenheit} grados Fahrenheit.')
        elif temperaturaCelsius is not None and temperaturaFahrenheit is not None and datos == 'temperaturaCompleta' :
            hablar(f'La temperatura actual es de {temperaturaCelsius} grados Celsius y {temperaturaFahrenheit} grados Fahrenheit.')
        elif humedad is not None and datos == 'humedad':
            hablar(f'La humedad actual es de {humedad}%.')
        else:
            hablar("No se encontraron datos sobre hoy.")
        
    except FileNotFoundError:
        hablar("No pude encontrar el archivo de datos de temperatura.")
    except Exception as e:
        hablar("Ocurrió un error inesperado.")
        print(f"Algo ha ido mal: {str(e)}")