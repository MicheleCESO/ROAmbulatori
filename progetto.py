import sys										# Funzioni di sistema
import getopt
from time import sleep							# Per ritardare l'output
from IstGen import genIstanza					# Generatore di istanze
import config									# Gestisce la configurazione del programma
from os.path import isfile						# Controllo presenza file
from tkinter import *							# Per la grafica
from config import Config, NoGuiConfig

pi = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}

def main(argv):
	for arg in argv:
		print(arg)
	optlist, args = getopt.getopt(argv, "hn", ["nogui"])
	print(optlist)

def test():
	global ist,conf
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

	scelta = {2:conf.mostra,3:conf.modifica,4:sys.exit}
	
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
			if risposta in [5]:
				scelta[risposta]()
			elif risposta == 1:
				#ist = [[1], [2, 5], [1], [4], [1, 3, 2], [4, 5], [2, 3, 5], [1], [4, 3, 1], [4, 3], [4, 2], [3, 1], [5, 2], [1, 4, 5]] #Crea errore
				ist = genIstanza(conf["Istanze"])
				scelta[risposta](ist)
			else:
				scelta[risposta]()

if __name__ == "__main__":
	test()
	#main(sys.argv[1:])
