import requests 
import serial
import json

# Configuration de la connexion série
ser = serial.Serial(
    port='/dev/ttyS0', # Utilisation du bon port
    baudrate=9600, # initialisation du bon baud rate
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# clé API
api_key = "bbcb2b6a701361f7dfc352d70ad3228d"

# Url de l'API qui nous permet d'aller chercher la météo
url = f'https://api.openweathermap.org/data/2.5/forecast?'

# Paramètres de la requête, on demande la ville, on utilise metric pour avoir les données en degré celsius
parameters = {
    'q': 'Liège',
    'units': 'metric',
    'appid': api_key
    }

# Faire la requête à l'API 
request = requests.get(url, parameters)

#on extrait les données json
data = request.json()

#On convertit la variable data en une chaine de caractère json
response= json.dumps(data)

#on envoie sur le port série
ser.write(response.encode())

#On affiche les données 
print( data)

# Fermer la connexion série
ser.close()

