import sys										# Funzioni di sistema
from time import sleep							# Per ritardare l'output
import os										# Per gestire l'uscita dal programma
from config import Config
from threading import Thread
from menù import Menù
from grafica import MainWindow
from PyQt5 import QtWidgets						# Interfaccia grafica

'''
Nota importante: le appplicazioni PyQt devono funzionare sul main thread, da qui la scelta di utilizzare la console come thread demone.
'''
def main():
	# Configurazione
	config = Config()
	
	# Creazione della grafica
	app = QtWidgets.QApplication(sys.argv)
	mainW = MainWindow(config)
	mainW.show()
	
	# Creazione del thread per gestire la console
	menù = Menù(config, mainW)
	t=Thread(name="console", target=menù.start, daemon=True)
	t.start()

	sys.exit(app.exec_()) # Avvio dell'applicazione grafica
	
if __name__ == "__main__":
	main()