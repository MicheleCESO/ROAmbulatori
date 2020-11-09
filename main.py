import sys										# Funzioni di sistema
import argparse
from time import sleep							# Per ritardare l'output
from IstGen import genIstanza					# Generatore di istanze
from os.path import isfile						# Controllo presenza file
from tkinter import *							# Per la grafica
from config import Config, NoGuiConfig
import SA
from euristica import *
from disegno import disegna

def main():
	# Configurazione
	conf = NoGuiConfig()
	
	# Menù contestuale

	titolo = """

	             ______                     _   _              _ _                
	             | ___ \                   | | | |            | (_)               
	             | |_/ / __ ___   __ _  ___| |_| |_ ___     __| |_                
	             |  __/ '__/ _ \ / _` |/ _ \ __| __/ _ \   / _` | |               
	             | |  | | | (_) | (_| |  __/ |_| || (_) | | (_| | |               
	             \_|  |_|  \___/ \__, |\___|\__|\__\___/   \__,_|_|               
	                              __/ |                                           
	                             |___/                                            
	______ _                          _____                      _   _            
	| ___ (_)                        |  _  |                    | | (_)           
	| |_/ /_  ___ ___ _ __ ___ __ _  | | | |_ __   ___ _ __ __ _| |_ ___   ____ _ 
	|    /| |/ __/ _ \ '__/ __/ _` | | | | | '_ \ / _ \ '__/ _` | __| \ \ / / _` |
	| |\ \| | (_|  __/ | | (_| (_| | \ \_/ / |_) |  __/ | | (_| | |_| |\ V / (_| |
	\_| \_|_|\___\___|_|  \___\__,_|  \___/| .__/ \___|_|  \__,_|\__|_| \_/ \__,_|
	                                       | |                                    
	                                       |_|                                    \n\n"""
	for char in titolo:
		sys.stdout.write(char)
		sys.stdout.flush()
		sleep(0.0001)
	sleep(1.5)

	scelta = {1:start, 2:conf.mostra, 3:conf.modifica, 4:sys.exit}
	
	while True:
		flag = False
		try:
			risposta = int(input("Selezionare un'opzione:\n\n1) Simulated Annealing\n2) Stampa configurazione\n3) Altera configurazione\n4) Esci\n\n"))
			print("")
			if risposta < 1 or risposta > 4:
				print("\nOpzione inesistente.\n\n")
			else:
				flag = True
		except ValueError:
			print("\nInput errato.\n\n")
		
		if flag:
			if risposta == 1:
				scelta[risposta](conf)
			else:
				scelta[risposta]()

def start(conf):
	ist = genIstanza(conf)
	ist = [[5], [5], [2, 4, 5, 1], [3], [5, 2], [4], [5, 2], [2, 3, 1, 5], [2], [1], [5, 3, 1], [5], [1, 4], [4], [1, 2, 3]]
	
	durata = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
	pazienti, jobs, ambulatori = euri(ist, durata)
	disegna(pazienti, durata)
	
	res = SA.sa(pazienti, jobs, ambulatori, conf)
	
	disegna(pazienti, durata)
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-g", "--grafica", action="store_true", help="utilizzo di interfaccia grafica")
	args = parser.parse_args() # Parsing degli argomenti
	if args.grafica: # Se al'opzione 'agrafica' è stata utilizzata, crea la GUI
		# Configurazione
		conf = Config()
		from grafica import MainWindow
		from PyQt5 import QtWidgets
		app = QtWidgets.QApplication(sys.argv)
		main = MainWindow(app, conf)
		main.show()
		sys.exit(app.exec_())
	else: # Proseguimento del programma sul terminale
		main()