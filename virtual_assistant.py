# @author Laura María Pedraza Gómez
import datetime
import pyttsx3
import speech_recognition as sr
import json
import pywhatkit as kit

archivoDatos = './out_shellyht.json'
archivoStrings = './strings.json'
archivoEnviarDatos = './enviarDatos.json'

stringsJson = {}
enviarJson = {}

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
    hablar(f'{momento} Soy Lía, tu asistente personal de temperatura. Por favor, dime en qué puedo ayudarte.')
    
# Solamente cargamos el json de los strings y de los datos a enviar para evitar el error del jsonDecoder en el out_shellyht.json
def cargarJsonStrings():
    global stringsJson 
    global enviarJson
    try:
        with open(archivoStrings, 'r') as file:
            stringsJson = json.load(file)
        with open(archivoEnviarDatos, 'r') as file:
            enviarJson = json.load(file)
            
    except Exception as e:
        hablar("Ocurrió un error inesperado.")
        print(f"Algo ha ido mal: {str(e)}")
            
    
def requests():
    saludo()
    cargarJsonStrings()
    stop = False
    while not stop:
        request = audioATexto().lower()
        if 'cuál es la temperatura actual' in request:
            decirDatosHoy(stringsJson["TODO"])
        elif 'cuáles son los grados celsius actuales' in request:
            decirDatosHoy(stringsJson["CEL"])
        elif 'cuáles son los grados fahrenheit actuales' in request:
            decirDatosHoy(stringsJson["FAH"])
        elif 'cuál es la humedad actual' in request:
            decirDatosHoy(stringsJson["HUM"])
        elif 'cuál es la temperatura media' in request:
            decirMedias(stringsJson["TODO"])
        elif 'cuáles son los grados celsius de media' in request:
            decirMedias(stringsJson["CEL"])
        elif 'cuáles son los grados fahrenheit de media' in request:
            decirMedias(stringsJson["FAH"])
        elif 'cuál es la humedad de media' in request:
            decirMedias(stringsJson["HUM"])
        elif 'detener' in request or 'salir' in request:
            hablar("Adiós. Espero haber sido de ayuda.")
            stop = True
        
def obtenerFechaActual():
     fecha = datetime.datetime.now().strftime('%Y-%m-%d')
     return fecha

def enviarMensaje(mensaje):
    numTelf = enviarJson["TEL"]
    hora = datetime.datetime.now().hour
    minuto = datetime.datetime.now().minute + 1 
    kit.sendwhatmsg(numTelf, mensaje, hora, minuto)
    
def decirDatosHoy(datos):
    try:
        with open(archivoDatos, 'r') as file:
            lineas = file.readlines()
            
        fechaActual = obtenerFechaActual()
        temperaturaCelsius = None
        temperaturaFahrenheit = None
        humedad = None
        
        mensaje = ''
        
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

        if temperaturaCelsius is not None and datos == stringsJson["CEL"]:
            mensaje = 'La temperatura actual es de ' + str(temperaturaCelsius) + ' grados Celsius.'
            hablar(mensaje)
        elif temperaturaFahrenheit is not None and datos == stringsJson["FAH"]:
            mensaje = 'La temperatura actual es de ' + str(temperaturaFahrenheit) + ' grados Fahrenheit.'
            hablar(mensaje)
        elif temperaturaCelsius is not None and temperaturaFahrenheit is not None and humedad is not None and datos == stringsJson["TODO"]:
            mensaje = 'La temperatura actual es de ' + str(temperaturaCelsius) + ' grados Celsius, ' + str(temperaturaFahrenheit) + ' grados Fahrenheit y una humedad de ' + str(humedad) + '%'
            hablar(mensaje)
        elif humedad is not None and datos == stringsJson["HUM"]:
            mensaje = 'La humedad actual es de ' + str(humedad) + '%.'
            hablar(mensaje)
        else:
            mensaje = 'No se encontraron datos sobre hoy.'
            hablar(mensaje)
            
        enviarMensaje(mensaje)
        
    except FileNotFoundError:
        hablar("No pude encontrar el archivo de datos de temperatura.")
    except Exception as e:
        hablar("Ocurrió un error inesperado.")
        print(f"Algo ha ido mal al cargar la temperatura: {str(e)}")
    
def obtenerFechasSemanaAnterior():
    fecha = datetime.datetime.strptime(obtenerFechaActual(), '%Y-%m-%d')
    lunesActual = fecha - datetime.timedelta(days=fecha.weekday())
    lunesAnterior = lunesActual - datetime.timedelta(weeks=1)
    fechasAnteriores = [
        (lunesAnterior + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)
    ]
    return fechasAnteriores

def calcularMedia(datos):
    num = 0
    
    for dato in datos:
        num = num + dato
        
    media = num / len(datos)
    return media
        
def decirMedias(datos):
    try:
        with open(archivoDatos, 'r') as file:
            lineas = file.readlines()
            
        temperaturasCelsius = []
        temperaturasFahrenheit = []
        humedades = []
        
        mensaje = ''
            
        for linea in lineas:
            try:
                fecha = linea[:10]
                fechasValidas = obtenerFechasSemanaAnterior()
                for dias in fechasValidas:
                    if fecha == dias:
                        partes = linea.split(' ', 2)
                        if len(partes) >= 3:
                            jsonStrings = partes[2].split('} {')
                            json1 = json.loads(jsonStrings[0] + '}')
                            json2 = json.loads('{' + jsonStrings[1])

                            if 'tC' in json1:
                                temperaturasCelsius.append(json1['tC'])
                                temperaturasFahrenheit.append(json1['tF'])
                            elif 'payload' in json2 and 'tC' in json2['payload'] and 'tF':
                                temperaturasCelsius.append(json2['payload']['tC'])
                                temperaturasFahrenheit.append(json2['payload']['tF'])
                            elif 'rh' in json1:
                                humedades.append(json1['rh'])
                            elif 'payload' in json2 and 'rh' in json2['payload']:
                                humedades.append(json2['payload']['rh'])
                                    
            except json.JSONDecodeError:
                continue
        
        if len(temperaturasCelsius) > 0:
            mediaCelsius = calcularMedia(temperaturasCelsius)
        if len(temperaturasFahrenheit) > 0:
            mediaFahrenheit = calcularMedia(temperaturasFahrenheit)
        if len(humedades) > 0:
            mediaHumedad = calcularMedia(humedades)
        
        if datos == stringsJson["TODO"] and len(temperaturasCelsius) > 0 and len(temperaturasFahrenheit) > 0 and len(humedades) > 0:
            mensaje = 'La temperatura media es de ' + str(mediaCelsius) + ' grados Celsius, ' + str(mediaFahrenheit) + ' grados Fahrenheit y la humedad media es de ' + str(mediaHumedad) + '%'
            hablar(mensaje)
        elif datos == stringsJson["CEL"] and len(mediaCelsius) > 0:
            mensaje = 'La temperatura media es de ' + str(mediaCelsius) + ' grados Celsius.'
            hablar(mensaje)
        elif datos == stringsJson["FAH"] and len(mediaFahrenheit) > 0:
            mensaje = 'La temperatura media es de ' + str(mediaFahrenheit) + ' grados Fahrenheit.'
            hablar(mensaje)
        elif datos == stringsJson["HUM"] and len(mediaHumedad) > 0:
            mensaje = 'La humedad media es de ' + str(mediaHumedad) + '%.'
            hablar(mensaje)
        else:
            mensaje = 'No hay datos disponibles para calcular la media.'
            hablar(mensaje)

        enviarMensaje(mensaje)
        
    except FileNotFoundError:
        hablar("No pude encontrar el archivo de datos de temperatura.")
    except Exception as e:
        hablar("Ocurrió un error inesperado.")
        print(f"Algo ha ido mal al cargar la media: {str(e)}")