import sys										# Funzioni di sistema
from time import sleep							# Per ritardare l'output
from IstGen import genIstanza					# Generatore di istanze
import config									# Gestisce la configurazione del programma
from os.path import isfile						# Controllo presenza file
from itertools import permutations as perm 		# Per gestire le permutazioni
from tkinter import *							# Per la grafica

pi = [1,2,3,4,5]

def permuta(lista):
	return list(perm(lista))

def risolvi(ist):
	# Riordino istanza per cardinalità decrescente
	ist.sort(key=len)
	ist.reverse()
	print(">>>>>>>>",ist)
	startP = [0] * len(ist) # Start pazienti
	startJ = [{} for _ in range(len(ist))] # Ogni dizionario contiene gli start|stop dei jobs di un paziente
	statoStanze = [0,0,0]

	listaPazienti = [] # Pazienti presenti nei laboratori
	gestionePazienti = {} # Dizionario che collega gli indici degli ambulatori agli indici dei pazienti
	storicoPazienti = {} # Dizionario che tiene traccia degli abbinamenti tra pazienti e ambulatori

	indiciUtilizzabili = [i for i in range(len(ist))] # Indici per capire quali pazienti scegliere

	for _ in ist:#range(len(ist)): # Per ogni paziente
		minimo = statoStanze.index(min(statoStanze))
		print("**** ",minimo)
		cancellaPazienti(listaPazienti,statoStanze,minimo,gestionePazienti)

		# Inizializzazione delle variabili
		index = 0
		minimoConflitto = 999
		flag = True

		# Ciclo che sceglie il paziente tra quelli disponibili che genera meno conflitti
		while flag and index < len(ist):
			print(flag,index)
			if index in indiciUtilizzabili:
				conflitto, soluzione = confronto(ist,startJ,listaPazienti,index,statoStanze[minimo]) # Confrontiamo paziente scelto attuale con quelli precedentemente scelti
			
				# Se trovo un paziente che genera meno conflitto, lo tengo da parte
				if conflitto < minimoConflitto:
					minimoConflitto = conflitto
					indexSol = index
					sol = soluzione
					if conflitto == 0: # Se non c'è conflitto, non posso trovare elemento migliore, quindi esco dal ciclo
						flag = False
						print("falso")
					else:
						index += 1
				else:
					index += 1
			else:
				index += 1

		# Inserimento in ambulatorio
		listaPazienti.append(indexSol)
		#print(indexSol,sol,indexSol-1,"\n",ist)
		ist[indexSol] = sol # Nuovo arrangiamento degli esami del paziente
		gestionePazienti[minimo] = indexSol
		storicoPazienti[indexSol] = minimo
		indiciUtilizzabili.remove(indexSol) # Cancello elemento già estratto

		# Aggiornamento ambulatorio
		statoStanze[minimo] += conflitto
		for elm in ist[indexSol]:
			statoStanze[minimo] += pi[elm-1]
	return startJ,storicoPazienti

# Cancella i pazienti che escono dagli ambulatori
def cancellaPazienti(listaPazienti,ambulatori,indexAmb,collegamento):
	if ambulatori[indexAmb] > 0:
		print("\n**** {} **** {}\n".format(listaPazienti,collegamento))
		listaPazienti.remove(collegamento[indexAmb])

# Gestisce il confronto tra i pazienti già inseriti e uno nuovo
def confronto(istanza, startJobs, pazientiInAmbulatorio, nuovoPaziente, startNuovo):

	global pi

	if len(pazientiInAmbulatorio) == 0:
		
		# Genero gli start momentanei del nuovo paziente
		startScorr = startNuovo
		for elm in istanza[nuovoPaziente]:
			startJobs[nuovoPaziente][elm] = startScorr
			startScorr += pi[elm-1]
		
		# Ritorno direttamente la parte dell'istanza relativa al paziente, siccome non ci sono altri pazienti negli ambulatori.
		return 0,istanza[nuovoPaziente]

	# Permutazioni possibili del nuovo paziente	
	lista3 = permuta(istanza[nuovoPaziente])

	if len(pazientiInAmbulatorio) == 1:
		lista2 = None
		start2 = None
	else:
		lista2 = istanza[pazientiInAmbulatorio[1]]
		start2 = startJobs[pazientiInAmbulatorio[1]]
		#print("++++++",istanza,"\n",startJobs,"\n",pazientiInAmbulatorio[1])
	costo = 9999
	for p3 in lista3:
		startAttuali = {} # Resetto gli start del nuovo paziente
		
		# Genero gli start momentanei del nuovo paziente
		startScorr = startNuovo
		for elm in p3:
			startAttuali[elm] = startScorr
			startScorr += pi[elm-1] # Aggiorno lo start

		#print("1---->",p3,startAttuali)
		livelloConflitto1 = verifica(istanza[pazientiInAmbulatorio[0]],startJobs[pazientiInAmbulatorio[0]],p3,startAttuali)
		#print("2---->",start2,p3,startAttuali)
		livelloConflitto2 = verifica(lista2,start2,p3,startAttuali)
		#print("3---->",p3,startAttuali)
		totaleConflitto = livelloConflitto1 + livelloConflitto2
		#print("--->",totaleConflitto)
		if totaleConflitto < costo:
			costo = totaleConflitto
			sol = p3
			startJobs[nuovoPaziente] = startAttuali
		if totaleConflitto == 0:
			break

	return costo, list(sol)

def verifica(jobsVecchi,start,jobsNuovi,startNuovo):
	global pi
	conflittoTotale = 0

	if jobsVecchi == None:
		return conflittoTotale
	for el in jobsNuovi:
		if el in jobsVecchi: # Se ci sono due esami dello stesso tipo
			#print("//////////////",el,start,startNuovo,jobsVecchi,jobsNuovi)
			diff = start[el] - startNuovo[el]
			if abs(diff) < pi[el-1]: # Conflitto
				conflitto = diff + pi[el-1]
				
				conflittoTotale += conflitto

				# Aggiornamento degli start in base al conflitto estratto
				for i in range(jobsNuovi.index(el),len(jobsNuovi)):
					startNuovo[jobsNuovi[i]] += conflitto
	return conflittoTotale

def disegna(dati,indiciAmbulatori):
	global pi
	
	colori = {1:"red",2:"blue",3:"yellow",4:"orange",5:"pink"} # Colori dei diversi jobs

	scala = 30
	offset = 10
	altezza = 50
	i = 0

	# Inizializzazione finestra grafica
	root = Tk()
	root.geometry("1500x220")
	canvas = Canvas(root,width=1500,height=220)
	scrollbar = Scrollbar(root,orient=HORIZONTAL)
	scrollbar.pack(side = BOTTOM,fill = X)
	scrollbar.config(command=canvas.xview)
	canvas.config(xscrollcommand=scrollbar.set)
	canvas.pack()
	print("indici:",indiciAmbulatori)
	# Generazione rettangoli colorati con etichette e valori di riferimento
	for paziente in dati:
		for chiave, valore in paziente.items():
			x1 = valore * scala + offset
			y1 = (2 - indiciAmbulatori[i]) * altezza + offset
			x2 = (valore + pi[chiave-1]) * scala + offset
			y2 = y1 + altezza
			canvas.create_rectangle(x1,y1,x2,y2,fill=colori[chiave])
			canvas.create_text((x1+x2)/2,(y1+y2)/2,text=str(chiave)+" P"+str(i))
			canvas.create_line(x2,160,x2,180)
			canvas.create_text(x2,200,text=str(valore+pi[chiave-1]))
		i += 1
	# Piano cartesiano
	canvas.create_line(10,10,10,160,width=3)
	canvas.create_line(10,160,1500,160,width=3)
	canvas.create_line(10,160,10,180)
	canvas.create_text(10,200,text="0")
	mainloop()

def greedy(ist):
	starts,temp = risolvi(ist)
	print(starts,"----",temp)
	disegna(starts,temp)
	input()

def testo():
	print("\n 3 ambulatori.\n")

if __name__ == "__main__":

	# Gestione della configurazione
	global ist,conf
	if (not isfile("config.ini")):
		conf = config.genConfig()
	else:
		conf = config.loadConfig()
	
	print(conf)

	# Menù contestuale

	test = """

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
	for char in test:
		sys.stdout.write(char)
		sys.stdout.flush()
		sleep(0.0004)
	sleep(1.5)

	scelta = {1:greedy,3:config.showConfig,4:config.changeConfig,5:sys.exit}
	
	while True:
		flag = False
		try:
			risposta = int(input("\nSelezionare un'opzione:\n\n1) Algoritmo Greedy\n2) Simulated Annealing\n3) Stampa configurazione\n4) Altera configurazione\n5) Esci\n\n"))
			print("")
			if risposta < 1 or risposta > 6:
				print("\nOpzione inesistente.\n\n")
			else:
				flag = True
		except ValueError:
			print("\nInput errato.\n\n")
		
		if flag:
			if risposta in [5]:
				scelta[risposta]()
			elif risposta in [1,2]:
				#ist = [[1], [2, 5], [1], [4], [1, 3, 2], [4, 5], [2, 3, 5], [1], [4, 3, 1], [4, 3], [4, 2], [3, 1], [5, 2], [1, 4, 5]] #Crea errore
				ist = genIstanza(conf["Istanze"])
				scelta[risposta](ist)
			else:
				scelta[risposta](conf)

	#paziente = MCP(ist)
	#ist = [[2, 4], [4, 2, 3], [5, 4]]
	# Generazione istanza casuale
	#ist = [[4, 1], [5], [2, 5], [3]]
	#ist = [[4, 1], [2, 5, 4, 3], [4], [1, 4, 5], [3, 4, 5], [3, 5, 2], [3, 2], [1, 3, 5], [3, 4, 5], [5, 3, 2]]
	#ist = genIstanza()
	#print(ist)
	#pprint(ist)
	#paziente = MCP(ist)
	#print(paziente)