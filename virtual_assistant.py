import datetime
import pyttsx3
import speech_recognition as sr
import json

archivoDatos = './out_shellyht.json'
archivoStrings = './strings.json'
datosJson = {}
stringsJson = {}

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
    
def cargarJsons():
    
    global datosJson, stringsJson 

    try:
        with open(archivoDatos, 'r') as file:
            datosJson = json.load(file) 
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error al cargar {archivoDatos}: {str(e)}")
        datosJson = {} 

    try:
        with open(archivoStrings, 'r') as file:
            stringsJson = json.load(file) 
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error al cargar {archivoStrings}: {str(e)}")
        stringsJson = {}
    
def requests():
    saludo()
    cargarJsons()
    stop = False
    while not stop:
        try:
            request = audioATexto().lower()
            if 'qué temperatura hace' in request:
                decirDatosHoy(stringsJson.TODO)
            elif 'cuántos grados celsius hacen' in request:
                decirDatosHoy(stringsJson.CELSIUS)
            elif 'cuántos grados fahrenheit hacen' in request:
                decirDatosHoy(stringsJson.FAHRENHEIT)
            elif 'qué humedad hace' in request:
                decirDatosHoy(stringsJson.HUMEDAD)
            elif 'qué temperatura media hay' in request:
                decirMedias(stringsJson.TODO)
            elif 'cuántos grados celsius hay de media' in request:
                decirMedias(stringsJson.CELSIUS)
            elif 'cuántos grados fahrenheit hay de media' in request:
                decirMedias(stringsJson.FAHRENHEIT)
            elif 'cuánta humedad hay de media' in request:
                decirMedias(stringsJson.HUMEDAD)
            elif 'detener' in request or 'salir' in request:
                hablar("Adiós. Espero haber sido de ayuda.")
                stop = True
        except Exception as e:
            hablar("Ocurrió un error inesperado.")
            print(f"Algo ha ido mal: {str(e)}")
            
def obtenerFechaActual():
     fecha = datetime.datetime.now().strftime('%Y-%m-%d')
     return fecha
        
def decirDatosHoy(datos):
    try:

        fechaActual = obtenerFechaActual()
        temperaturaCelsius = None
        temperaturaFahrenheit = None
        humedad = None

        for linea in datosJson:
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

        if temperaturaCelsius is not None and datos == stringsJson.CELSIUS:
            hablar(f'La temperatura actual es de {temperaturaCelsius} grados Celsius.')
        elif temperaturaFahrenheit is not None and datos == stringsJson.FAHRENHEIT:
            hablar(f'La temperatura actual es de {temperaturaFahrenheit} grados Fahrenheit.')
        elif temperaturaCelsius is not None and temperaturaFahrenheit is not None and humedad is not None and datos == stringsJson.TODO :
            hablar(f'La temperatura actual es de {temperaturaCelsius} grados Celsius, {temperaturaFahrenheit} grados Fahrenheit y una humedad de {humedad}%')
        elif humedad is not None and datos == stringsJson.HUMEDAD:
            hablar(f'La humedad actual es de {humedad}%.')
        else:
            hablar("No se encontraron datos sobre hoy.")
        
    except FileNotFoundError:
        hablar("No pude encontrar el archivo de datos de temperatura.")
    except Exception as e:
        hablar("Ocurrió un error inesperado.")
        print(f"Algo ha ido mal: {str(e)}")

def calcularMedia(datos):
    num = 0
    for dato in datos:
        num == num + dato
    media = num / len(datos)
    
def obtenerFechasSemanaAnterior():
    fecha = obtenerFechaActual()
    print(fecha)
    lunesActual = fecha - datetime.timedelta(days=fecha.weekday())
    lunesAnterior = lunesActual - datetime.timedelta(weeks=1)
    fechasAnteriores = [(lunesAnterior + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    print("SEMANA ANTERIOR:"+fechasAnteriores)
    
    return fechasAnteriores
        
def decirMedias(datos):
    try:

        temperaturasCelsius = []
        temperaturasFahrenheit = []
        humedades = []
        
        for linea in datosJson:
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
                                temperaturasCelsius.push(json1['tC'])
                                temperaturasFahrenheit.push(json1['tF'])
                            elif 'payload' in json2 and 'tC' in json2['payload'] and 'tF':
                                temperaturasCelsius.push(json2['payload']['tC'])
                                temperaturasFahrenheit.push(json2['payload']['tF'])
                            elif 'rh' in json1:
                                humedades.push(json1['rh'])
                            elif 'payload' in json2 and 'rh' in json2['payload']:
                                humedades.push(json2['payload']['rh'])
                                    
            except json.JSONDecodeError:
                continue
        
        if len(temperaturasCelsius) > 0:
            mediaCelsius = calcularMedia(temperaturasCelsius)
        if len(temperaturasFahrenheit) > 0:
            mediaFahrenheit = calcularMedia(temperaturasFahrenheit)
        if len(humedades) > 0:
            mediaHumedad = calcularMedia(humedades)
        
        if datos == stringsJson.TODO and len(temperaturasCelsius) > 0 and len(temperaturasFahrenheit) > 0 and len(humedades) > 0:
            hablar(f'La temperatura media es de {mediaCelsius} grados Celsius y de {mediaFahrenheit} grados Fahrenheit.')
        elif datos == stringsJson.CELSIUS and len(mediaCelsius) > 0:
            hablar(f'La temperatura media es de {mediaCelsius} grados Celsius.')
        elif datos == stringsJson.FAHRENHEIT and len(mediaFahrenheit) > 0:
            hablar(f'La temperatura media es de {mediaFahrenheit} grados Faren.')
        elif datos == stringsJson.HUMEDAD and len(mediaHumedad) > 0:
            hablar(f'La humedad media es de {mediaHumedad}%.')
        else:
            hablar('No hay datos disponibles para calcular la media.')
        
    except FileNotFoundError:
        hablar("No pude encontrar el archivo de datos de temperatura.")
    except Exception as e:
        hablar("Ocurrió un error inesperado.")
        print(f"Algo ha ido mal: {str(e)}")