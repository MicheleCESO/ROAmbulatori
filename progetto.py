from IstGen import genIstanza
from itertools import permutations as perm
from tkinter import *

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

	for _ in range(len(ist)):
		index = 0
		minimoConflitto = 999
		minimo = minStato(statoStanze)

		cancellaPazienti(listaPazienti,statoStanze,minimo,gestionePazienti)

		flag = True

		while flag and index < len(ist):
			if index in indiciUtilizzabili:
				conflitto, sol = confronto(ist,startJ,listaPazienti,index,statoStanze[minimo[0]]) # Confrontiamo paziente scelto attuale con quelli precedentemente scelti
			
				if conflitto < minimoConflitto:
					minimoConflitto = conflitto
					indexSol = index
				if conflitto == 0:
					flag = False
			index += 1

		# Inserimento in ambulatorio
		listaPazienti.append(indexSol)
		ist[indexSol] = sol
		gestionePazienti[minimo[0]] = indexSol
		storicoPazienti[indexSol] = minimo[0]
		#print("***",gestionePazienti,minimo[0],sol)
		print("***",gestionePazienti,indiciUtilizzabili,indexSol)
		indiciUtilizzabili.remove(indexSol) # Cancello elemento già estratto
		listaPazienti.append(indexSol)

		# Aggiornamento ambulatorio
		statoStanze[minimo[0]] += conflitto
		for elm in ist[index-1]:
			statoStanze[minimo[0]] += pi[elm-1]
	return startJ,storicoPazienti

# Cancella i pazienti che escono dagli ambulatori
def cancellaPazienti(listaPazienti,ambulatori,minimo,collegamento):
	for elm in minimo[::-1]:
		if ambulatori[elm] > 0:
			print("*_*",listaPazienti,collegamento[elm])
			listaPazienti.remove(collegamento[elm])

# Ritorna gli indici con i valori minimi della lista
def minStato(lista):
	index = []
	minimo = 9999
	for i in range(3):
		if minimo > lista[i]:
			minimo = lista[i]
			index = [i]
		elif minimo == lista[i]:
			index.append(i)
	return index

# Gestisce il confronto tra i pazienti già inseriti e uno nuovo
def confronto(istanza, startJobs, pazientiInAmbulatorio, nuovoPaziente, startNuovo):

	global pi

	# Permutazioni possibili del nuovo paziente	
	lista3 = permuta(istanza[nuovoPaziente])
	if len(pazientiInAmbulatorio) == 0:
		
		# Genero gli start momentanei del nuovo paziente
		startScorr = startNuovo
		for elm in istanza[nuovoPaziente]:
			startJobs[nuovoPaziente][elm] = startScorr
			startScorr += pi[elm-1] # Aggiorno lo start

		return 0,istanza[nuovoPaziente]
	
	elif len(pazientiInAmbulatorio) == 1:
		lista2 = None
		start2 = None
	else:
		lista2 = istanza[pazientiInAmbulatorio[1]]
		start2 = startJobs[pazientiInAmbulatorio[1]]

	costo = 9999
	for p3 in lista3:
		startAttuali = {} # Resetto gli start del nuovo paziente
		
		# Genero gli start momentanei del nuovo paziente
		startScorr = startNuovo
		for elm in p3:
			startAttuali[elm] = startScorr
			startScorr += pi[elm-1] # Aggiorno lo start
		print("---->",p3,startAttuali)
		livelloConflitto1 = verifica(istanza[pazientiInAmbulatorio[0]],startJobs[pazientiInAmbulatorio[0]],p3,startAttuali)
		livelloConflitto2 = verifica(lista2,start2,p3,startAttuali)
		
		totaleConflitto = livelloConflitto1 + livelloConflitto2
		print("--->",totaleConflitto)
		if totaleConflitto < costo:
			costo = totaleConflitto
			sol = p3
			startJobs[nuovoPaziente] = startAttuali
		if totaleConflitto == 0:
			break

	return costo, sol

def verifica(jobsVecchi,start,jobsNuovi,startNuovo):
	global pi
	conflittoTotale = 0

	if jobsVecchi == None:
		return conflittoTotale
	for el in jobsNuovi:
		if el in jobsVecchi: # Se ci sono due esami dello stesso tipo
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



if __name__ == "__main__":
	#paziente = MCP(ist)
	ist = [[2, 4], [4, 2, 3], [5, 4]]
	# Generazione istanza casuale
	#ist = [[4, 1], [5], [2, 5], [3]]
	#ist = [[4, 1], [2, 5, 4, 3], [4], [1, 4, 5], [3, 4, 5], [3, 5, 2], [3, 2], [1, 3, 5], [3, 4, 5], [5, 3, 2]]
	#ist = genIstanza()
	print(ist)
	#pprint(ist)
	#paziente = MCP(ist)
	#print(paziente)
	starts,temp = risolvi(ist)
	print(starts)
	disegna(starts,temp)
	input()