#importation des bibliothèques
import serial #sert pour la communiccation série
import sys #gère les fonctionnalitées du système
#PyQt5 gère les interfaces graphiques
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton
from PyQt5.QtCore import Qt
import json #permet de traiter les données JSON
from datetime import datetime, timedelta #datetime pour la manipulation sur les dates et time delta pour les opérations sur les dates

#Cette partie configure la communication série 
ser = serial.Serial(
    port='/dev/ttyS0', #Le nom du port de notre device
    baudrate=9600, #On règle le débit en bauds de notre device
    parity=serial.PARITY_NONE, #pas de parité
    stopbits=serial.STOPBITS_ONE, #un bit d'arrêt
    bytesize=serial.EIGHTBITS, #une taille en bit 
    timeout=1 #un délai d'attente
)

#La boucle est utilisée pour lire les données provenant de la communication série
#Les données sont lues à partir du port série, décryptées en tant que chaîne de caractères, puis nettoyées
while True:

    response = ser.readline().decode().strip()
    
    if response:  # Si des données sont reçues, elles sont extraites en tant que chaîne JSON valide à partir de la réponse.
        start_index = response.find('{')
        end_index = response.rfind('}')
        json_data = response[start_index:end_index + 1]
        #Ensuite, les données JSON sont chargées dans un dictionnaire data2 à l'aide de la fonction json.loads()
        data2 = json.loads(json_data) 
        print("Données météo :")
        print(json_data)
        #Enfin, les données météorologiques sont affichées et la boucle est interrompue
        break
    else:
        #Si aucune donnée n'est reçue, un message d'attente est affiché. 
        print('En attente de données...')

ser.close()#Enfin on ferme la connection série

#Cette fonction permet obtenir les dates des cinq prochains jours à partir de la date actuelle.
def get_next_5_days():
        days = []
        today = datetime.now().date() #on obtient la date actuelle
        #puis les cinq jours suivants sont calculés en ajoutant un délai de un jour à chaque itération de la boucle.
        for i in range(1, 6):
            day = today + timedelta(days=i)
            days.append(day.strftime('%Y-%m-%d'))#format : 'AAAA-MM-JJ' et puis et ajoutées à une liste days
        #la liste des dates est affichée et renvoyée.
        print(days)
        return days
    
class MainWindow(QMainWindow):
    def __init__(self, city): #le conctructeur initialise la fenêtre principale avec un titre, une géométrie et une ville spécifiée
        super().__init__()
        self.setWindowTitle('OpenWeatherMap') #titre
        self.setGeometry(100, 100, 800, 600)
        self.city = city #ville
        self.create_widgets() #permet de créer les widgets à afficher dans la fenêtre.
        
    def create_widgets(self):
        self.table = QTableWidget(0, 4, self)#création du tableau avec quatre colonnes représentant la date, l'heure, la température et la description
        self.table.setHorizontalHeaderLabels(['Date', 'Heure', 'Température (°C)', 'Description'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        #Un bouton "Mettre à jour" est ajouté ainsi que le tableau à un widget et à un layout pour les disposer correctement dans la fenêtre.
        widget = QWidget(self)
        layout = QVBoxLayout(widget)
        layout.addWidget(QPushButton('Mettre à jour', clicked=self.update_weather_data))
        layout.addWidget(self.table)
        
        self.setCentralWidget(widget)
    
    def update_weather_data(self): #cette méthode est définie pour mettre à jour les données météorologiques dans le tableau
        data = data2 #Les données récupérées précédemment sont stockées dans une variable data
        if data is not None:
            next_5_days = get_next_5_days() #Si des données existent, les cinq prochains jours sont obtenus à l'aide de la fonction get_next_5_days()
            row_count = len(next_5_days) * 8 #Le nombre de lignes du tableau est calculé en multipliant la longueur des jours par 8
            self.table.setRowCount(row_count) # fix 1
            row = 0
            #ensuite cette boucle parcourt chaque jour et chaque élément de la liste des données 
            for day in next_5_days:
                for item in data['list']: # fix 2
                    item_date = datetime.fromtimestamp(item['dt']) #La date de l'élément est convertie en objet datetime à l'aide de datetime.fromtimestamp()
                    #Si la date correspond au jour en cours, les données sont ajoutées aux cellules appropriées du tableau. L'indice de ligne est incrémenté à chaque itération
                    if item_date.date().strftime('%Y-%m-%d') == day:
                        date_item = QTableWidgetItem(item_date.date().strftime('%Y-%m-%d'))
                        date_item.setFlags(date_item.flags() ^ Qt.ItemIsEditable)
                        self.table.setItem(row, 0, date_item)
                        time_item = QTableWidgetItem(item_date.time().strftime('%H:%M:%S'))
                        time_item.setFlags(time_item.flags() ^ Qt.ItemIsEditable)
                        self.table.setItem(row, 1, time_item)
                        temp_item = QTableWidgetItem(str(item['main']['temp']))
                        temp_item.setFlags(temp_item.flags() ^ Qt.ItemIsEditable)
                        self.table.setItem(row, 2, temp_item)
                        desc_item = QTableWidgetItem(item['weather'][0]['description'])
                        desc_item.setFlags(desc_item.flags() ^ Qt.ItemIsEditable)
                        self.table.setItem(row, 3, desc_item)
                        row += 1


app = QApplication([])
window = MainWindow('Liège')
window.show() #on afiche la fenêtre
app.exec_() #on execute l'application 

